# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "beautifulsoup4>=4.12.0",
#     "lxml>=5.0.0",
#     "tqdm>=4.66.0",
# ]
# ///
#!/usr/bin/env python3
"""Planalto Brazilian Legislation High-Throughput Scraper & Indexer.

Crawls and downloads federal legislation from planalto.gov.br/ccivil_03/
Extracts categorical metadata (doc_type, number, date, scraped_at, ementa),
creates structured catalog indexes (docs/index.csv & docs/index.json),
and recursively sweeps the body text of every document to discover and fetch unmapped laws.
Supports multithreaded downloads with automatic fallback to synchronous execution.
"""

import argparse
import concurrent.futures
import csv
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# --- Configuration & Hub Endpoints ---

BASE_URL = "https://www.planalto.gov.br/ccivil_03/"

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "corpus"
WORKERS = 50

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 LEX-Scraper/1.0"

MONTHS_PT = {
    "janeiro": "01", "fevereiro": "02", "março": "03", "marco": "03",
    "abril": "04", "maio": "05", "junho": "06", "julho": "07",
    "agosto": "08", "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
}

HUB_ENDPOINTS: Dict[str, List[str]] = {
    "constituicao": [
        "https://www.planalto.gov.br/ccivil_03/Constituicao/Constituicao.htm",
        "https://www.planalto.gov.br/ccivil_03/Constituicao/ConstituicaoCompilado.htm",
        "https://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc/quadro_emc.htm",
        "https://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emc_p/quadro_emc_p.htm",
        "https://www.planalto.gov.br/ccivil_03/Constituicao/Emendas/Emr/quadro_emr.htm",
    ],
    "codigos": [
        "https://www.planalto.gov.br/ccivil_03/Codigos/quadro_cod.htm",
    ],
    "leis_ordinarias": [
        "https://www.planalto.gov.br/ccivil_03/LEIS/_Lei-Ordinaria.htm",
    ],
    "leis_complementares": [
        "https://www.planalto.gov.br/ccivil_03/LEIS/LCP/Quadro_Lcp.htm",
        "https://www.planalto.gov.br/ccivil_03/LEIS/LCP/_quadro-lcp.htm",
    ],
    "leis_delegadas": [
        "https://www.planalto.gov.br/ccivil_03/LEIS/Ldl/Quadro_LDL.htm",
    ],
    "leis_imperio": [
        "https://www.planalto.gov.br/ccivil_03/LEIS/LIM/_Quadro-LIM.htm",
    ],
    "decretos_leis": [
        "https://www.planalto.gov.br/ccivil_03/Decreto-Lei/principal_ano.htm",
    ],
    "decretos": [
        "https://www.planalto.gov.br/ccivil_03/decreto/_Dec_ano.htm",
    ],
    "decretos_nao_numerados": [
        "https://www.planalto.gov.br/ccivil_03/DNN/quadro/_Dnn_ano.htm",
    ],
    "medidas_provisorias": [
        "https://www.planalto.gov.br/ccivil_03/MPV/Principal.htm",
    ],
    "decretos_legislativos": [
        "https://www.planalto.gov.br/ccivil_03/decreto/Historicos/DPL/_DPL-ano.htm",
    ],
    "alvaras": [
        "https://www.planalto.gov.br/ccivil_03/Alvara/Alvara-quadro.htm",
    ],
    "cartas_regias": [
        "https://www.planalto.gov.br/ccivil_03/Carta_Regia/cartaregia-quadro.htm",
    ],
    "cartas_de_lei": [
        "https://www.planalto.gov.br/ccivil_03/Carta_Lei/cartalei-quadro.htm",
    ],
    "vetos": [
        "https://www.planalto.gov.br/ccivil_03/VETO_TOTAL/principal_ano.htm",
    ],
    "portarias": [
        "https://www.planalto.gov.br/ccivil_03/Portaria/quadro_portaria.htm",
    ],
}

# --- Helper & Parsing Functions ---

def clean_url(url: str) -> str:
    """Normalize URL by stripping query parameters and fragments.

    >>> clean_url("https://www.planalto.gov.br/ccivil_03/LEIS/L10406.htm#art1")
    'https://www.planalto.gov.br/ccivil_03/LEIS/L10406.htm'
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def is_planalto_ccivil_url(url: str) -> bool:
    """Check if URL belongs to the planalto.gov.br ccivil_03 repository.

    >>> is_planalto_ccivil_url("https://www.planalto.gov.br/ccivil_03/LEIS/L10406.htm")
    True
    >>> is_planalto_ccivil_url("https://twitter.com/planalto")
    False
    """
    lower = url.lower()
    return "planalto.gov.br/ccivil_03" in lower or "planalto.gov.br/_ato" in lower


def is_index_or_quadro_url(url: str) -> bool:
    """Identify if a URL is an index/quadro listing page rather than an actual law text.

    >>> is_index_or_quadro_url("https://www.planalto.gov.br/ccivil_03/LEIS/_Lei-Ordinaria.htm")
    True
    >>> is_index_or_quadro_url("https://www.planalto.gov.br/ccivil_03/LEIS/2002/L10406.htm")
    False
    """
    lower = url.lower()
    path = urlparse(lower).path
    filename = Path(path).name

    if filename.startswith("_") or "quadro" in filename or "principal" in filename or "index" in filename:
        return True
    if "consulta" in filename or "resenha" in filename or "veto_total" in lower:
        return True
    return False


def classify_document(url: str) -> str:
    """Infer category folder from URL patterns.

    >>> classify_document("https://www.planalto.gov.br/ccivil_03/Constituicao/Constituicao.htm")
    'constituicao'
    >>> classify_document("https://www.planalto.gov.br/ccivil_03/LEIS/LCP/Lcp101.htm")
    'leis_complementares'
    >>> classify_document("https://www.planalto.gov.br/ccivil_03/LEIS/2002/L10406.htm")
    'leis_ordinarias'
    """
    lower = url.lower()
    stem = Path(url).stem.lower()

    if "constituicao" in lower or "emenda" in lower or "emc" in stem or "emr" in stem:
        return "constituicao"
    if "dlg" in stem or "/dlg" in lower:
        return "decretos_legislativos"
    if "lcp" in stem or "/lcp" in lower:
        return "leis_complementares"
    if "ldl" in stem or "/ldl" in lower:
        return "leis_delegadas"
    if "/lim" in lower:
        return "leis_imperio"
    if "del" in stem or "decreto-lei" in lower or "/del" in lower:
        return "decretos_leis"
    if "mpv" in stem or "/mpv" in lower:
        return "medidas_provisorias"
    if "dsn" in stem or "dnn" in stem or "/dnn" in lower or "/dsn" in lower:
        return "decretos_nao_numerados"
    if "vep" in stem or "/veto" in lower or "/msg" in lower:
        return "vetos"
    if "portaria" in lower or "prt" in stem:
        return "portarias"
    if "codigos" in lower:
        return "codigos"
    if "alvara" in lower:
        return "alvaras"
    if "cartaregia" in lower or "carta_regia" in lower:
        return "cartas_regias"
    if "cartalei" in lower or "carta_lei" in lower:
        return "cartas_de_lei"
    if re.match(r"^d\d+", stem) or "/decreto" in lower or "/dec" in lower:
        return "decretos"
    if re.match(r"^l\d+", stem) or "/lei" in lower:
        return "leis_ordinarias"
    return "outros"


def create_safe_filename(url: str) -> str:
    """Generate a collision-free local filename from URL.

    >>> create_safe_filename("https://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2024/Lei/L15082.htm")
    'Ato2023-2026_2024_Lei_L15082.html'
    """
    parsed = urlparse(url)
    clean_path = parsed.path.strip("/")
    if clean_path.lower().startswith("ccivil_03/"):
        clean_path = clean_path[len("ccivil_03/"):]

    safe_name = clean_path.replace("/", "_").replace("\\", "_")
    if not safe_name.lower().endswith(".html") and not safe_name.lower().endswith(".htm"):
        safe_name += ".html"
    elif safe_name.lower().endswith(".htm"):
        safe_name = safe_name[:-4] + ".html"

    safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', safe_name)
    return safe_name


def is_institutional_header(text: str) -> bool:
    """Check if the text is a governmental layout header rather than an act summary."""
    if not text:
        return True
    low = text.lower()
    return (
        "presidência da república" in low
        or "subchefia para assuntos jurídicos" in low
        or "secretaria especial para assuntos" in low
        or "secretaria de assuntos parlamentares" in low
        or "secretaria-geral" in low
        or "casa civil" in low
        or "este texto não substitui" in low
        or "nota : para procura rápida" in low
        or "texto para impressão" in low
        or "para procura rápida de palavras" in low
        or "clique aqui para" in low
        or "publicado no dou" in low
        or text.strip() == "..."
        or len(text.strip()) < 5
    )


def is_enactment_formula_or_header(text: str) -> bool:
    """Check if the text is a promulgation formula or title heading rather than ementa."""
    t_strip = text.strip()
    return bool(re.match(
        r'^(?:O\s+PRESIDENTE|A\s+PRESIDENTA|O\s+VICE-PRESIDENTE|O\s+MINISTRO|O\s+DIRETOR|A\s+DIRETORIA|Faço\s+saber|Art\.?\s*\d|CAPÍTULO|TÍTULO|SEÇÃO|EMENDA\s+CONST|DECRETO\s+N|LEI\s+N|MEDIDA\s+PROVIS|PORTARIA\s+N|RESOLUÇÃO\s+N|ATO\s+DECLARAT)',
        t_strip,
        re.IGNORECASE
    ))


def extract_ementa_from_soup(soup: BeautifulSoup) -> str:
    """Extract ementa using cascading heuristics designed for Planalto HTML variations:

    1. 2-column or styled metadata tables (Col 1: Notes/Revocations, Col 2: Ementa).
    2. Elements with explicit font color #800000 or maroon.
    3. Paragraphs/Divs with right/justify alignment or lateral margin indentation.
    4. Text span between date header and enactment formula.
    5. Action verb matching on opening content blocks.
    6. Operative sentence extraction for single-paragraph acts (e.g. Atos da Mesa).
    """
    # Tier 1: Table analysis (Planalto 2-column or styled metadata tables)
    for table in soup.find_all("table"):
        tds = table.find_all("td")
        if len(tds) >= 2:
            right_td = re.sub(r"\s+", " ", tds[-1].get_text(separator=" ", strip=True)).strip()
            if right_td and not is_institutional_header(right_td) and not is_enactment_formula_or_header(right_td):
                return right_td
            for td in reversed(tds):
                txt = re.sub(r"\s+", " ", td.get_text(separator=" ", strip=True)).strip()
                if txt and not is_institutional_header(txt) and not is_enactment_formula_or_header(txt) and len(txt) > 10:
                    return txt
        elif len(tds) == 1:
            txt = re.sub(r"\s+", " ", tds[0].get_text(separator=" ", strip=True)).strip()
            if txt and not is_institutional_header(txt) and not is_enactment_formula_or_header(txt) and len(txt) > 10:
                td_style = (tds[0].get("style") or "") + (tds[0].get("align") or "") + (tds[0].get("width") or "")
                if any(k in td_style.lower() for k in ["right", "justify", "50%", "40%", "60%"]):
                    return txt

    # Tier 2: Highlighted Font color (#800000 or maroon)
    for font_elem in soup.find_all(["font", "span", "p"], attrs={"color": re.compile(r"#?800000|maroon", re.IGNORECASE)}):
        txt = re.sub(r"\s+", " ", font_elem.get_text(separator=" ", strip=True)).strip()
        if txt and not is_institutional_header(txt) and not is_enactment_formula_or_header(txt) and len(txt) > 10:
            return txt

    # Tier 3: Paragraphs / Divs with right or justify alignment or lateral margin indentation
    for elem in soup.find_all(["p", "div"]):
        align = (elem.get("align") or "").lower()
        style = (elem.get("style") or "").lower()
        if align in ["right", "justify"] or "margin-left" in style or "text-align: right" in style:
            txt = re.sub(r"\s+", " ", elem.get_text(separator=" ", strip=True)).strip()
            if txt and not is_institutional_header(txt) and not is_enactment_formula_or_header(txt) and len(txt) > 10:
                return txt

    # Tier 4: Fallback Regex on text between Date and Enactment Formula
    text = soup.get_text(separator="\n", strip=True)
    m = re.search(
        r'(?:DE\s+\d{1,2}\s+DE\s+[A-ZÇa-zç]+\s+DE\s+(?:18|19|20)\d{2}\.?)\s*[\n\r]+\s*([^\n\r]+?(?:[\n\r]+[^\n\r]+?){0,3}?)(?=\s*[\n\r]+(?:O\s+PRESIDENTE|A\s+PRESIDENTA|O\s+VICE-PRESIDENTE|O\s+MINISTRO|O\s+DIRETOR|A\s+DIRETORIA|Faço\s+saber|resolve:|RESOLVE:|Resolve:|decreta:|DECRETA:|Art\.?\s*1[º\.\s]|Artigo\s+1))',
        text,
        re.IGNORECASE,
    )
    if m:
        cand = re.sub(r"\s+", " ", m.group(1)).strip()
        if cand and not is_institutional_header(cand) and not is_enactment_formula_or_header(cand) and len(cand) > 10:
            return cand

    # Tier 5: Verb matching on leading elements
    for elem in soup.find_all(["p", "div", "font"]):
        txt = re.sub(r"\s+", " ", elem.get_text(separator=" ", strip=True)).strip()
        if txt and not is_institutional_header(txt) and len(txt) > 15:
            if re.match(
                r'^(?:Dispõe\s+sobre|Altera\s+|Abre\s+ao\s+|Abre\s+crédito|Cria\s+|Institui\s+|Declara\s+|Concede\s+|Fixa\s+|Aprova\s+|Denomina\s+|Revoga\s+|Prorroga\s+|Isenta\s+|Regula\s+|Estabelece\s+|Autoriza\s+|Dá\s+nova\s+redação|Define\s+|Reestrutura\s+|Extingue\s+|Homologa\s+|Outorga\s+|Ratifica\s+|Modifica\s+|Dispõe,\s+|Recomenda\s+)',
                txt,
                re.IGNORECASE,
            ):
                return txt

    # Tier 6: Single-paragraph acts (Atos do Congresso Nacional, Portarias operacionais)
    for p in soup.find_all("p"):
        p_txt = re.sub(r"\s+", " ", p.get_text(separator=" ", strip=True)).strip()
        if p_txt and not is_institutional_header(p_txt) and any(k in p_txt.lower() for k in ["faz saber que", "prorrogada pelo período", "perdeu a eficácia"]):
            return p_txt[:300]

    return "Sem ementa disponível"


def extract_document_metadata(html_text: str, url: str = "", file_path: str = "") -> Dict[str, str]:
    """Extract categorical fields (doc_type, number, date, ementa) from law HTML."""
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(["script", "style", "head", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    doc_type = None
    number = None
    date_iso = None

    # Header regex for Brazilian legal acts
    header_regex = re.compile(
        r'(LEI\s+COMPLEMENTAR|LEI\s+DELEGADA|LEI\s+ORDIN[ÁA]RIA|LEI|DECRETO-LEI|DECRETO\s+LEGISLATIVO|DECRETO\s+N[ÃA]O\s+NUMERADO|DECRETO|MEDIDA\s+PROVIS[ÓO]RIA|EMENDA\s+CONSTITUCIONAL|CONSTITUI[ÇC][ÃA]O|ATO\s+DECLARAT[ÓO]RIO|PORTARIA|RESOLU[ÇC][ÃA]O|CARTA\s+R[ÉE]GIA|CARTA\s+DE\s+LEI|ALVAR[ÁA])'
        r'\s*(?:N[ºo°\.\s]*)?\s*([\d\.\-\/]+)?'
        r'\s*,?\s*(?:DE\s+(\d{1,2})\s+DE\s+([a-zA-ZçÇáéíóúÁÉÍÓÚ]+)\s+DE\s+(\d{4}))?',
        re.IGNORECASE
    )

    match = header_regex.search(text)
    if match:
        raw_type = match.group(1).strip().upper()
        if raw_type == "LEI":
            doc_type = "LEI ORDINÁRIA"
        elif "CONSTITUI" in raw_type:
            doc_type = "CONSTITUIÇÃO"
        else:
            doc_type = raw_type

        number = match.group(2)
        day, month, year = match.group(3), match.group(4), match.group(5)
        if day and month and year:
            m_num = MONTHS_PT.get(month.lower(), "00")
            date_iso = f"{year}-{m_num}-{int(day):02d}"

    # Fallback doc_type from URL / classification
    if not doc_type:
        cat = classify_document(url or file_path)
        doc_type = cat.replace("_", " ").upper()

    # Fallback number from filename
    if not number:
        num_m = re.search(r'([L|D|Mpv|Del|Emc|Dlg]+)[\-_]?(\d+[\.\d]*)', file_path or url, re.IGNORECASE)
        if num_m:
            number = num_m.group(2)

    # Fallback year from path
    if not date_iso:
        yr_m = re.search(r'(?:18|19|20)\d{2}', file_path or url)
        if yr_m:
            date_iso = f"{yr_m.group(0)}-01-01"

    # Multi-tier ementa extraction
    ementa = extract_ementa_from_soup(soup)

    return {
        "doc_type": doc_type or "OUTROS",
        "number": number or "S/N",
        "date": date_iso or "N/D",
        "ementa": ementa[:300],
    }


def extract_in_text_document_links(base_url: str, html_text: str) -> List[str]:
    """Scan document body for internal hyperlinks pointing to referenced laws."""
    discovered_urls = []
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        for a in soup.find_all("a", href=True):
            raw_href = a["href"].strip()
            if not raw_href or raw_href.startswith("#") or raw_href.startswith("javascript:") or raw_href.startswith("mailto:"):
                continue

            full_url = clean_url(urljoin(base_url, raw_href))
            if is_planalto_ccivil_url(full_url) and (full_url.lower().endswith(".htm") or full_url.lower().endswith(".html")):
                if not is_index_or_quadro_url(full_url):
                    discovered_urls.append(full_url)
    except Exception as e:
        logging.debug("Error scanning in-text links for %s: %s", base_url, e)
    return discovered_urls


# --- HTTP Session with Adaptive Retry ---

def get_http_session(timeout: int = 15) -> requests.Session:
    """Create configured requests session with custom headers."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    })
    return session


def fetch_url(url: str, session: Optional[requests.Session] = None, timeout: int = 15, max_retries: int = 3) -> Optional[Tuple[str, bytes, str]]:
    """Fetch URL with retries and return (final_url, content_bytes, encoding)."""
    close_session = False
    if session is None:
        session = get_http_session(timeout=timeout)
        close_session = True

    url = clean_url(url)
    for attempt in range(1, max_retries + 1):
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            if resp.status_code == 200:
                encoding = resp.encoding or "iso-8859-1"
                if encoding.lower() in ("iso-8859-1", "windows-1252", "latin1"):
                    if b"charset=utf-8" in resp.content.lower() or b'charset="utf-8"' in resp.content.lower():
                        encoding = "utf-8"
                return resp.url, resp.content, encoding
            elif resp.status_code == 404:
                return None
            else:
                time.sleep(0.5 * attempt)
        except requests.RequestException:
            if attempt == max_retries:
                return None
            time.sleep(1.0 * attempt)
        finally:
            if close_session:
                session.close()
    return None


# --- Crawler, Harvester & Indexer ---

class PlanaltoScraper:
    """Orchestrates index crawling, in-text link extraction, and categorical cataloging."""

    def __init__(
        self,
        output_dir: Path,
        workers: int = WORKERS,
        timeout: int = 15,
        sync_mode: bool = False,
        save_text: bool = False,
        scan_text_links: bool = True
    ):
        self.output_dir = Path(output_dir)
        self.workers = 1 if sync_mode else max(1, workers)
        self.timeout = timeout
        self.sync_mode = sync_mode or (workers <= 1)
        self.save_text = save_text
        self.scan_text_links = scan_text_links
        self.session = get_http_session(timeout=timeout)
        self.visited_urls: Set[str] = set()
        self.discovered_laws: Set[str] = set()
        self.processed_records: Dict[str, Dict[str, str]] = {}
        self.index_csv_file = self.output_dir / "index.csv"
        self.index_json_file = self.output_dir / "index.json"
        self.manifest_file = self.output_dir / "manifest.json"

        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for cat in list(HUB_ENDPOINTS.keys()) + ["outros"]:
            (self.output_dir / cat).mkdir(parents=True, exist_ok=True)

        # Load existing index if present
        self.load_existing_index()

    def load_existing_index(self) -> None:
        """Load previously saved index records for seamless incremental runs."""
        if self.index_json_file.exists():
            try:
                data = json.loads(self.index_json_file.read_text(encoding="utf-8"))
                for row in data.get("documents", []):
                    if "url" in row:
                        self.processed_records[row["url"]] = row
            except Exception as e:
                logging.debug("Could not parse existing index.json: %s", e)

    def extract_links_from_html(self, base_url: str, html_content: bytes, encoding: str) -> List[str]:
        """Extract all valid internal Planalto hyperlinks from HTML."""
        links = []
        try:
            soup = BeautifulSoup(html_content, "html.parser", from_encoding=encoding)
            for a in soup.find_all("a", href=True):
                raw_href = a["href"].strip()
                if not raw_href or raw_href.startswith("#") or raw_href.startswith("javascript:") or raw_href.startswith("mailto:"):
                    continue

                full_url = clean_url(urljoin(base_url, raw_href))
                if is_planalto_ccivil_url(full_url) and (full_url.lower().endswith(".htm") or full_url.lower().endswith(".html")):
                    links.append(full_url)
        except Exception as e:
            logging.debug("Error parsing HTML links from %s: %s", base_url, e)
        return links

    def crawl_index_pages(self, start_urls: List[str], max_depth: int = 3) -> Set[str]:
        """Crawl hub index tables concurrently with dynamic tqdm progress bar, ETA, and metrics."""
        queue: List[Tuple[str, int]] = [(url, 0) for url in start_urls]
        discovered_quadros: Set[str] = set()

        print(f"[*] Crawling index hierarchies from {len(start_urls)} seeds (Max depth: {max_depth}, Workers: {self.workers})...")

        with tqdm(total=len(queue), desc="Crawling Quadros/Indexes", unit="page") as pbar:
            while queue:
                # Fetch a batch of index/quadro URLs concurrently
                batch_size = min(len(queue), self.workers * 2 if not self.sync_mode else 1)
                batch = queue[:batch_size]
                queue = queue[batch_size:]

                urls_to_fetch = []
                for current_url, depth in batch:
                    if current_url in self.visited_urls:
                        pbar.update(1)
                        continue
                    self.visited_urls.add(current_url)

                    if is_index_or_quadro_url(current_url) or depth == 0:
                        discovered_quadros.add(current_url)
                        urls_to_fetch.append((current_url, depth))
                    else:
                        self.discovered_laws.add(current_url)
                        pbar.update(1)

                if not urls_to_fetch:
                    continue

                if self.sync_mode or self.workers <= 1:
                    for current_url, depth in urls_to_fetch:
                        fetched = fetch_url(current_url, session=self.session, timeout=self.timeout)
                        pbar.update(1)
                        if not fetched:
                            continue
                        final_url, content, encoding = fetched
                        extracted = self.extract_links_from_html(final_url, content, encoding)
                        for link in extracted:
                            if is_index_or_quadro_url(link):
                                if depth + 1 <= max_depth and link not in self.visited_urls:
                                    queue.append((link, depth + 1))
                                    pbar.total += 1
                            else:
                                self.discovered_laws.add(link)
                else:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                        future_to_item = {
                            executor.submit(fetch_url, u, timeout=self.timeout): (u, d)
                            for u, d in urls_to_fetch
                        }
                        for future in concurrent.futures.as_completed(future_to_item):
                            pbar.update(1)
                            u, depth = future_to_item[future]
                            try:
                                fetched = future.result()
                                if not fetched:
                                    continue
                                final_url, content, encoding = fetched
                                extracted = self.extract_links_from_html(final_url, content, encoding)
                                for link in extracted:
                                    if is_index_or_quadro_url(link):
                                        if depth + 1 <= max_depth and link not in self.visited_urls:
                                            queue.append((link, depth + 1))
                                            pbar.total += 1
                                    else:
                                        self.discovered_laws.add(link)
                            except Exception as exc:
                                logging.debug("Error crawling quadro %s: %s", u, exc)

                pbar.set_postfix({
                    "quadros": len(discovered_quadros),
                    "laws_found": len(self.discovered_laws)
                })

        print(f"\n[✓] Index crawl complete: Discovered {len(self.discovered_laws)} law documents across {len(discovered_quadros)} index pages.")
        return self.discovered_laws

    def process_and_download_document(self, url: str) -> Tuple[Optional[Dict[str, str]], List[str]]:
        """Download document, extract categorical metadata, and scan for referenced law links."""
        category = classify_document(url)
        filename = create_safe_filename(url)
        dest_path = self.output_dir / category / filename
        in_text_links: List[str] = []

        # Read cached content or fetch from network
        if dest_path.exists() and dest_path.stat().st_size > 0:
            html_text = dest_path.read_text(encoding="utf-8", errors="replace")
            meta = extract_document_metadata(html_text, url=url, file_path=dest_path.name)
            if self.scan_text_links:
                in_text_links = extract_in_text_document_links(url, html_text)

            record = {
                "doc_type": meta["doc_type"],
                "number": meta["number"],
                "date": meta["date"],
                "scraped_at": self.processed_records.get(url, {}).get("scraped_at", datetime.now(timezone.utc).isoformat()),
                "url": url,
                "category": category,
                "file_path": str(dest_path.relative_to(self.output_dir)),
                "file_size_bytes": str(dest_path.stat().st_size),
                "ementa": meta["ementa"],
                "status": "cached",
            }
            return record, in_text_links

        fetched = fetch_url(url, timeout=self.timeout)
        if not fetched:
            return None, []

        final_url, content, encoding = fetched

        try:
            html_text = content.decode(encoding, errors="replace")
            if "<meta" not in html_text.lower() or "charset" not in html_text.lower():
                html_text = f'<meta charset="utf-8">\n<!-- Scraped from {url} on {datetime.now(timezone.utc).isoformat()} -->\n' + html_text
            dest_path.write_text(html_text, encoding="utf-8")

            if self.save_text:
                soup = BeautifulSoup(html_text, "html.parser")
                for tag in soup(["script", "style", "head", "title", "meta"]):
                    tag.decompose()
                clean_txt = soup.get_text(separator="\n", strip=True)
                dest_path.with_suffix(".txt").write_text(clean_txt, encoding="utf-8")

        except Exception:
            dest_path.write_bytes(content)
            html_text = content.decode("utf-8", errors="ignore")

        # Extract metadata and in-text links
        meta = extract_document_metadata(html_text, url=url, file_path=dest_path.name)
        if self.scan_text_links:
            in_text_links = extract_in_text_document_links(url, html_text)

        record = {
            "doc_type": meta["doc_type"],
            "number": meta["number"],
            "date": meta["date"],
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "url": url,
            "category": category,
            "file_path": str(dest_path.relative_to(self.output_dir)),
            "file_size_bytes": str(dest_path.stat().st_size),
            "ementa": meta["ementa"],
            "status": "downloaded",
        }
        return record, in_text_links

    def download_and_index_corpus(self, initial_urls: Set[str], limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Download documents, recursively discover in-text links, and build index."""
        pending_queue: List[str] = sorted(list(initial_urls))
        if limit:
            pending_queue = pending_queue[:limit]

        processed_urls: Set[str] = set()
        newly_discovered: Set[str] = set()
        failed_urls: List[str] = []

        mode_name = "Synchronous (1 thread)" if self.sync_mode else f"Multithreaded ({self.workers} workers)"
        print(f"[*] Starting download, in-text link extraction & indexing [{mode_name}]...")

        with tqdm(total=len(pending_queue), desc="Corpus Ingestion", unit="doc") as pbar:
            while pending_queue:
                batch_size = min(len(pending_queue), self.workers * 5 if not self.sync_mode else 1)
                current_batch = pending_queue[:batch_size]
                pending_queue = pending_queue[batch_size:]

                if self.sync_mode:
                    for u in current_batch:
                        if u in processed_urls:
                            pbar.update(1)
                            continue
                        processed_urls.add(u)
                        rec, text_links = self.process_and_download_document(u)
                        pbar.update(1)
                        if rec:
                            self.processed_records[u] = rec
                            if self.scan_text_links:
                                for l in text_links:
                                    if l not in processed_urls and l not in newly_discovered and not is_index_or_quadro_url(l):
                                        newly_discovered.add(l)
                                        if not limit or len(processed_urls) + len(pending_queue) < limit:
                                            pending_queue.append(l)
                                            pbar.total += 1
                        else:
                            failed_urls.append(u)
                else:
                    try:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                            future_map = {executor.submit(self.process_and_download_document, u): u for u in current_batch if u not in processed_urls}
                            for u in current_batch:
                                processed_urls.add(u)

                            for future in concurrent.futures.as_completed(future_map):
                                pbar.update(1)
                                u = future_map[future]
                                try:
                                    rec, text_links = future.result()
                                    if rec:
                                        self.processed_records[u] = rec
                                        if self.scan_text_links:
                                            for l in text_links:
                                                if l not in processed_urls and l not in newly_discovered and not is_index_or_quadro_url(l):
                                                    newly_discovered.add(l)
                                                    if not limit or len(processed_urls) + len(pending_queue) < limit:
                                                        pending_queue.append(l)
                                                        pbar.total += 1
                                    else:
                                        failed_urls.append(u)
                                except Exception as exc:
                                    logging.warning("Error processing %s: %s", u, exc)
                                    failed_urls.append(u)
                    except Exception as pool_err:
                        print(f"[!] ThreadPool issue: {pool_err}. Falling back to sync mode.")
                        self.sync_mode = True

                # Periodic checkpoint save every batch
                if len(self.processed_records) % 25 == 0 or len(pending_queue) == 0:
                    self.save_index(list(self.processed_records.values()), silent=True)

        # Retry failed items synchronously
        if failed_urls:
            print(f"[*] Retrying {len(failed_urls)} failed downloads synchronously...")
            for u in failed_urls:
                rec, _ = self.process_and_download_document(u)
                if rec:
                    self.processed_records[u] = rec

        # Final save index.csv, index.json, manifest.json
        records_list = list(self.processed_records.values())
        self.save_index(records_list)
        return records_list

    def save_index(self, records: List[Dict[str, str]], silent: bool = False) -> None:
        """Write index.csv, index.json and manifest.json to docs/ directory."""
        # 1. Save index.csv (Structured catalog with >= 4 columns)
        fieldnames = ["doc_type", "number", "date", "scraped_at", "url", "category", "file_path", "file_size_bytes", "ementa"]
        with open(self.index_csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in sorted(records, key=lambda x: (x.get("doc_type", ""), x.get("date", "")), reverse=True):
                writer.writerow(r)

        # 2. Save index.json
        index_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_documents": len(records),
            "documents": records,
        }
        with open(self.index_json_file, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        # 3. Save manifest.json (Aggregated category metrics)
        manifest = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_documents": len(records),
            "categories": {},
            "doc_types": {},
        }
        for r in records:
            cat = r.get("category", "outros")
            dtype = r.get("doc_type", "OUTROS")
            manifest["categories"][cat] = manifest["categories"].get(cat, 0) + 1
            manifest["doc_types"][dtype] = manifest["doc_types"].get(dtype, 0) + 1

        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        if not silent:
            print(f"\n[✓] Index Catalog Generated:")
            print(f"    - CSV Index:  {self.index_csv_file} ({len(records)} rows)")
            print(f"    - JSON Index: {self.index_json_file}")
            print(f"    - Manifest:   {self.manifest_file}")

    def _parse_single_file_for_reindex(self, html_file: Path) -> Optional[Dict[str, str]]:
        """Parse a single local HTML file to extract metadata."""
        if html_file.name.startswith("_") and "Ato" not in html_file.name:
            return None
        try:
            html_text = html_file.read_text(encoding="utf-8", errors="replace")
            meta = extract_document_metadata(html_text, file_path=html_file.name)
            category = html_file.parent.name
            rel_path = str(html_file.relative_to(self.output_dir))

            scraped_url = f"https://www.planalto.gov.br/ccivil_03/{html_file.name}"
            url_match = re.search(r"<!-- Scraped from (https?://[^\s]+) on ([^\s]+) -->", html_text)
            scraped_at = datetime.now(timezone.utc).isoformat()
            if url_match:
                scraped_url = url_match.group(1)
                scraped_at = url_match.group(2)

            return {
                "doc_type": meta["doc_type"],
                "number": meta["number"],
                "date": meta["date"],
                "scraped_at": scraped_at,
                "url": scraped_url,
                "category": category,
                "file_path": rel_path,
                "file_size_bytes": str(html_file.stat().st_size),
                "ementa": meta["ementa"],
                "status": "indexed",
            }
        except Exception as err:
            logging.debug("Error indexing %s: %s", html_file, err)
            return None

    def reindex_existing_files(self) -> None:
        """Scan all existing HTML files in docs/ in parallel and build index catalog."""
        print(f"[*] Discovering existing HTML files in {self.output_dir}...")
        all_html_files = [f for f in self.output_dir.rglob("*.html")]
        print(f"[*] Found {len(all_html_files)} files. Parsing metadata with {self.workers} workers...")

        records = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = list(tqdm(executor.map(self._parse_single_file_for_reindex, all_html_files), total=len(all_html_files), desc="Reindexing Docs", unit="file"))
            records = [r for r in results if r is not None]

        self.save_index(records)
        print(f"[✓] Re-indexing complete: Successfully indexed {len(records)} local files.")


# --- Self-Validation Sanity Checks ---

def run_sanity_checks() -> None:
    """Run inline asserts to validate core logic."""
    assert clean_url("https://planalto.gov.br/test.htm#section1") == "https://planalto.gov.br/test.htm"
    assert is_planalto_ccivil_url("https://www.planalto.gov.br/ccivil_03/LEIS/L10406.htm") is True
    assert is_planalto_ccivil_url("https://google.com") is False
    assert is_index_or_quadro_url("https://www.planalto.gov.br/ccivil_03/LEIS/_Lei-Ordinaria.htm") is True
    assert is_index_or_quadro_url("https://www.planalto.gov.br/ccivil_03/LEIS/L10406.htm") is False
    assert classify_document("https://www.planalto.gov.br/ccivil_03/Constituicao/Constituicao.htm") == "constituicao"
    assert classify_document("https://www.planalto.gov.br/ccivil_03/LEIS/LCP/Lcp101.htm") == "leis_complementares"
    assert classify_document("https://www.planalto.gov.br/ccivil_03/LEIS/2002/L10406.htm") == "leis_ordinarias"

    sample_html = """
    <html><body>
    <table width="70%"><tr><td></td><td>Presidência da República Casa Civil Subchefia para Assuntos Jurídicos</td></tr></table>
    <a href="http://legislacao.planalto.gov.br/">LEI Nº 12.706, DE 8 DE AGOSTO DE 2012.</a>
    <table width="100%"><tr><td>Mensagem de veto</td><td>Autoriza a criação da empresa pública AMAZUL</td></tr></table>
    <a href="../../../LEIS/L6404consol.htm">Lei 6.404</a>
    </body></html>
    """
    meta = extract_document_metadata(sample_html, file_path="L12706.html")
    assert meta["doc_type"] == "LEI ORDINÁRIA", f"Expected LEI ORDINÁRIA, got {meta['doc_type']}"
    assert meta["number"] == "12.706", f"Expected 12.706, got {meta['number']}"
    assert meta["date"] == "2012-08-08", f"Expected 2012-08-08, got {meta['date']}"
    assert "AMAZUL" in meta["ementa"], f"Expected AMAZUL in ementa, got: {meta['ementa']}"
    assert "Presidência" not in meta["ementa"], f"Institutional header leaked into ementa: {meta['ementa']}"

    # Test font color fallback
    sample_font_html = """
    <html><body>
    <p>DECRETO Nº 5.432, DE 10 DE MAIO DE 2005</p>
    <font color="#800000">Regulamenta os incentivos fiscais para inovação tecnológica.</font>
    <p>O PRESIDENTE DA REPÚBLICA decreta...</p>
    </body></html>
    """
    meta_font = extract_document_metadata(sample_font_html)
    assert "incentivos fiscais" in meta_font["ementa"], f"Expected font color ementa, got: {meta_font['ementa']}"

    links = extract_in_text_document_links("https://www.planalto.gov.br/ccivil_03/LEIS/2012/Lei/L12706.htm", sample_html)
    assert len(links) == 1
    assert "L6404consol.htm" in links[0]
    print("[✓] All internal sanity checks and metadata extractors passed.")


# --- CLI Entrypoint ---

def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(description="Planalto Legislation Scraper & Categorical Indexer")
    parser.add_argument("--category", type=str, default="all", choices=list(HUB_ENDPOINTS.keys()) + ["all"],
                        help="Specific category to scrape (default: all)")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help=f"Destination directory (default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--workers", type=int, default=WORKERS,
                        help=f"Number of multithreading worker threads (default: {WORKERS})")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of documents to download (for testing/spikes)")
    parser.add_argument("--max-depth", type=int, default=3,
                        help="Max crawl recursion depth for index tables (default: 3)")
    parser.add_argument("--timeout", type=int, default=15,
                        help="HTTP timeout in seconds (default: 15)")
    parser.add_argument("--save-text", action="store_true",
                        help="Also extract and save plain text (.txt) alongside HTML")
    parser.add_argument("--no-scan-text-links", action="store_true",
                        help="Disable recursive discovery of links inside document body texts")
    parser.add_argument("--sync", action="store_true",
                        help="Force synchronous single-threaded mode")
    parser.add_argument("--reindex", action="store_true",
                        help="Explicitly re-scan and index all locally downloaded files in docs/corpus without scraping")
    parser.add_argument("--check-only", action="store_true",
                        help="Run sanity asserts and crawl discovery without downloading files")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Step 1: Run inline validation asserts
    run_sanity_checks()

    output_path = Path(args.output)
    scraper = PlanaltoScraper(
        output_dir=output_path,
        workers=args.workers,
        timeout=args.timeout,
        sync_mode=args.sync,
        save_text=args.save_text,
        scan_text_links=not args.no_scan_text_links,
    )

    # Step 2: Explicit Re-index Mode (Only when explicitly passed)
    if args.reindex:
        scraper.reindex_existing_files()
        return

    # Step 3: Determine start URLs
    if args.category == "all":
        seeds = [url for urls in HUB_ENDPOINTS.values() for url in urls]
    else:
        seeds = HUB_ENDPOINTS[args.category]

    # Step 4: Discover all law documents from index pages
    law_urls = scraper.crawl_index_pages(seeds, max_depth=args.max_depth)

    # Step 5: Filter out documents already indexed locally
    already_indexed_urls = set(scraper.processed_records.keys())
    # Also include filenames mapped to URLs
    already_indexed_files = {r.get("file_path", "") for r in scraper.processed_records.values()}
    
    unindexed_urls = set()
    for u in law_urls:
        cat = classify_document(u)
        fname = create_safe_filename(u)
        rel_f = f"{cat}/{fname}"
        if u not in already_indexed_urls and rel_f not in already_indexed_files:
            unindexed_urls.add(u)

    print(f"[*] Crawl Filter: {len(law_urls)} total discovered vs {len(already_indexed_urls)} already in index. {len(unindexed_urls)} new documents to scrape.")

    if args.check_only:
        print(f"[*] Check-only mode: Discovered {len(law_urls)} documents ({len(unindexed_urls)} pending download). Skipping download.")
        return

    # Step 6: Download only missing documents with multithreading, in-text link extraction & indexing
    if unindexed_urls:
        results = scraper.download_and_index_corpus(unindexed_urls, limit=args.limit)
    else:
        print("[✓] All discovered documents are already downloaded and indexed locally!")
        results = list(scraper.processed_records.values())

    # Step 7: Summary Output
    print("\n" + "=" * 65)
    print(f" PLANALTO LEGISLATION SCRAPER & INDEXER SUMMARY")
    print("=" * 65)
    print(f"Destination:     {output_path.resolve()}")
    print(f"Total Indexed:   {len(scraper.processed_records)} documents")
    print(f"Index CSV:       {scraper.index_csv_file.resolve()}")
    print(f"Index JSON:      {scraper.index_json_file.resolve()}")
    print(f"Workers:         {1 if args.sync else args.workers} ({'Sync' if args.sync else 'Multithreaded'})")
    print(f"In-Text Crawler: {'Enabled' if not args.no_scan_text_links else 'Disabled'}")
    print("=" * 65)


if __name__ == "__main__":
    main()
