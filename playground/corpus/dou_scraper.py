# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
#     "pypdf>=5.0.0",
#     "tqdm>=4.66.0",
# ]
# ///
#!/usr/bin/env python3
"""DOU (Diário Oficial da União) Multi-Section & Archive Scraper.

Crawls and downloads all Brazilian Federal Official Gazette (DOU) editions from
a start date (default: 2001-01-01) up to today across all configured sections
(Seções 1, 2, e 3 por padrão, com suporte a Edições Extras).
Iterates day by day, downloads pages in parallel, extracts text from PDFs via pypdf,
and maintains a structured catalog in docs/dou/index_dou.csv.
"""

import argparse
import concurrent.futures
import csv
import io
import json
import logging
import os
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import requests
from pypdf import PdfReader
from tqdm import tqdm

# --- Constants & Configuration ---

BASE_VIEWER_URL = "https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer"
BASE_INDEX_URL = "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp"

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "dou"
DEFAULT_START_DATE = "2001-01-01"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 DOU-Scraper/1.0"

JORNAL_NAMES = {
    1: "secao_1",
    2: "secao_2",
    3: "secao_3",
    1000: "edicao_extra",
    515: "edicao_suplementar",
}

DEFAULT_SECTIONS = [1, 2, 3]

# --- Helper Functions ---

def parse_date_to_object(date_str: str) -> date:
    """Parse string date to datetime.date object.

    >>> parse_date_to_object("2001-01-01")
    datetime.date(2001, 1, 1)
    >>> parse_date_to_object("01/01/2001")
    datetime.date(2001, 1, 1)
    """
    date_str = date_str.strip()
    if "/" in date_str:
        p = date_str.split("/")
        return date(int(p[2]), int(p[1]), int(p[0]))
    elif "-" in date_str:
        p = date_str.split("-")
        return date(int(p[0]), int(p[1]), int(p[2]))
    raise ValueError(f"Invalid date: {date_str}. Use YYYY-MM-DD or DD/MM/YYYY.")


def format_date_tuple(d: date) -> Tuple[str, str]:
    """Return (br_format: DD/MM/YYYY, iso_format: YYYY-MM-DD)."""
    return d.strftime("%d/%m/%Y"), d.strftime("%Y-%m-%d")


def get_http_session(timeout: int = 15) -> requests.Session:
    """Create configured requests session."""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    })
    return session


def discover_edition_metadata(date_br: str, jornal: int = 1, timeout: int = 15) -> Tuple[int, Optional[int]]:
    """Query index.jsp to get total page count and edition number."""
    url = f"{BASE_INDEX_URL}?data={date_br}&jornal={jornal}&pagina=1"
    session = get_http_session(timeout=timeout)
    try:
        resp = session.get(url, timeout=timeout)
        if resp.status_code == 200:
            match_total = re.search(r"totalArquivos=(\d+)", resp.text)
            total_pages = int(match_total.group(1)) if match_total else 0

            match_ed = re.search(r"n[úu]mero\s+(\d+)", resp.text, re.IGNORECASE)
            edition_num = int(match_ed.group(1)) if match_ed else None

            return total_pages, edition_num
    except Exception as e:
        logging.warning("Error querying metadata for %s (jornal %d): %s", date_br, jornal, e)
    finally:
        session.close()
    return 0, None


# --- Page Downloader & Text Extractor ---

def download_and_extract_page(
    date_br: str,
    iso_date: str,
    page_num: int,
    jornal: int,
    output_dir: Path,
    session: Optional[requests.Session] = None,
    timeout: int = 15,
    max_retries: int = 3,
    save_text: bool = True
) -> Optional[Dict[str, str]]:
    """Download single DOU PDF page, extract text, and return metadata."""
    jornal_folder = JORNAL_NAMES.get(jornal, f"jornal_{jornal}")
    year, month, _ = iso_date.split("-")
    page_dir = output_dir / jornal_folder / year / month / iso_date
    page_dir.mkdir(parents=True, exist_ok=True)

    pdf_filename = f"DOU_{jornal_folder}_{iso_date}_pag_{page_num:04d}.pdf"
    txt_filename = f"DOU_{jornal_folder}_{iso_date}_pag_{page_num:04d}.txt"

    txt_path = page_dir / txt_filename

    # Resume check: Check if text file already exists and is non-empty
    if txt_path.exists() and txt_path.stat().st_size > 0:
        extracted_text = txt_path.read_text(encoding="utf-8", errors="ignore")
        return {
            "data": iso_date,
            "secao": jornal_folder,
            "jornal": str(jornal),
            "pagina": str(page_num),
            "file_txt": str(txt_path.relative_to(output_dir)),
            "char_count": str(len(extracted_text)),
            "size_bytes": str(txt_path.stat().st_size),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "status": "cached",
        }

    close_session = False
    if session is None:
        session = get_http_session(timeout=timeout)
        close_session = True

    url = f"{BASE_VIEWER_URL}?jornal={jornal}&pagina={page_num}&data={date_br}&captchafield=firstAccess"

    for attempt in range(1, max_retries + 1):
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code == 200 and resp.headers.get("Content-Type") == "application/pdf":
                pdf_bytes = resp.content

                # Extract text in-memory using pypdf without saving PDF to disk
                extracted_text = ""
                try:
                    reader = PdfReader(io.BytesIO(pdf_bytes))
                    if reader.pages:
                        extracted_text = reader.pages[0].extract_text() or ""
                except Exception as pdf_err:
                    logging.debug("Text extraction error on page %s: %s", page_num, pdf_err)

                # Save ONLY the extracted text file
                txt_path.write_text(extracted_text, encoding="utf-8")

                return {
                    "data": iso_date,
                    "secao": jornal_folder,
                    "jornal": str(jornal),
                    "pagina": str(page_num),
                    "file_txt": str(txt_path.relative_to(output_dir)),
                    "char_count": str(len(extracted_text)),
                    "size_bytes": str(txt_path.stat().st_size),
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                    "status": "downloaded",
                }
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


# --- Batch Scraper & Multi-Day Orchestrator ---

class DOUScraper:
    """Orchestrates multi-day, multi-section crawling, downloading and cataloging."""

    def __init__(self, output_dir: Path, workers: int = 10, timeout: int = 15, sync_mode: bool = False, save_text: bool = True):
        self.output_dir = Path(output_dir)
        self.workers = 1 if sync_mode else max(1, workers)
        self.timeout = timeout
        self.sync_mode = sync_mode or (workers <= 1)
        self.save_text = save_text
        self.index_csv_file = self.output_dir / "index_dou.csv"
        self.index_json_file = self.output_dir / "index_dou.json"
        self.manifest_file = self.output_dir / "manifest_dou.json"
        self.record_map: Dict[str, Dict[str, str]] = {}

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.load_existing_index()

    def load_existing_index(self) -> None:
        """Load catalog from disk."""
        if self.index_json_file.exists():
            try:
                data = json.loads(self.index_json_file.read_text(encoding="utf-8"))
                for r in data.get("documents", []):
                    key = f"{r['data']}_{r['secao']}_{int(r['pagina']):04d}"
                    self.record_map[key] = r
            except Exception as e:
                logging.debug("Could not read index_dou.json: %s", e)

    def scrape_single_edition(
        self,
        target_date: date,
        jornal: int = 1,
        pages_limit_per_day: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Scrape all pages for a specific day and section."""
        date_br, iso_date = format_date_tuple(target_date)
        jornal_name = JORNAL_NAMES.get(jornal, f"jornal_{jornal}")

        total_pages, edition_num = discover_edition_metadata(date_br, jornal=jornal, timeout=self.timeout)
        if total_pages == 0:
            return []

        ed_title = f"Edição Nº {edition_num}" if edition_num else "Edição Normal"
        pages_to_fetch = list(range(1, total_pages + 1))
        if pages_limit_per_day:
            pages_to_fetch = pages_to_fetch[:pages_limit_per_day]

        print(f"\n[*] {iso_date} | {jornal_name.upper()} ({ed_title}): Downloading {len(pages_to_fetch)}/{total_pages} pages...")

        results: List[Dict[str, str]] = []
        failed_pages: List[int] = []

        if self.sync_mode:
            session = get_http_session(timeout=self.timeout)
            for p in tqdm(pages_to_fetch, desc=f"{iso_date} [{jornal_name}]", unit="pag", leave=False):
                res = download_and_extract_page(
                    date_br, iso_date, p, jornal, self.output_dir,
                    session=session, timeout=self.timeout, save_text=self.save_text
                )
                if res:
                    results.append(res)
                else:
                    failed_pages.append(p)
            session.close()
        else:
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                    future_to_page = {
                        executor.submit(
                            download_and_extract_page,
                            date_br, iso_date, p, jornal, self.output_dir,
                            None, self.timeout, 3, self.save_text
                        ): p for p in pages_to_fetch
                    }
                    for future in tqdm(concurrent.futures.as_completed(future_to_page), total=len(pages_to_fetch), desc=f"{iso_date} [{jornal_name}]", unit="pag", leave=False):
                        p = future_to_page[future]
                        try:
                            res = future.result()
                            if res:
                                results.append(res)
                            else:
                                failed_pages.append(p)
                        except Exception as exc:
                            logging.warning("Error on page %d: %s", p, exc)
                            failed_pages.append(p)
            except Exception as pool_err:
                print(f"[!] ThreadPool exception: {pool_err}. Falling back to sync.")
                session = get_http_session(timeout=self.timeout)
                remaining = set(pages_to_fetch) - {int(r["pagina"]) for r in results}
                for p in remaining:
                    res = download_and_extract_page(date_br, iso_date, p, jornal, self.output_dir, session, self.timeout, 3, self.save_text)
                    if res:
                        results.append(res)
                session.close()

        # Retry failed pages
        if failed_pages:
            session = get_http_session(timeout=self.timeout)
            for p in failed_pages:
                time.sleep(0.5)
                res = download_and_extract_page(date_br, iso_date, p, jornal, self.output_dir, session, self.timeout, 3, self.save_text)
                if res:
                    results.append(res)
            session.close()

        # Update in-memory record map
        for r in results:
            key = f"{r['data']}_{r['secao']}_{int(r['pagina']):04d}"
            self.record_map[key] = r

        return results

    def crawl_range(
        self,
        start_date: date,
        end_date: date,
        sections: List[int] = DEFAULT_SECTIONS,
        pages_limit_per_day: Optional[int] = None,
        days_limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Iterate day by day from start_date to end_date across all requested sections."""
        total_days = (end_date - start_date).days + 1
        if days_limit:
            total_days = min(total_days, days_limit)

        sec_str = ", ".join([JORNAL_NAMES.get(s, str(s)).upper() for s in sections])
        print(f"[*] Crawling DOU Archive from {start_date.isoformat()} to {end_date.isoformat()} ({total_days} days) | Sections: {sec_str}...")
        print(f"[*] Concurrency: {self.workers} worker threads per section (Multithreaded).")

        current_d = start_date
        processed_days_count = 0
        total_pages_saved = 0

        with tqdm(total=total_days, desc="DOU Archive Progress", unit="day") as day_pbar:
            while current_d <= end_date:
                if days_limit and processed_days_count >= days_limit:
                    print(f"[*] Reached days limit of {days_limit}. Stopping.")
                    break

                day_has_content = False
                for sec in sections:
                    day_sec_results = self.scrape_single_edition(
                        target_date=current_d,
                        jornal=sec,
                        pages_limit_per_day=pages_limit_per_day
                    )
                    if day_sec_results:
                        day_has_content = True
                        total_pages_saved += len(day_sec_results)

                processed_days_count += 1
                day_pbar.update(1)
                day_pbar.set_postfix({"cumulative_pages": total_pages_saved, "current": current_d.isoformat()})

                if day_has_content:
                    self.save_catalog()

                current_d += timedelta(days=1)

        self.save_catalog()
        return list(self.record_map.values())

    def save_catalog(self) -> None:
        """Write master CSV, JSON and Manifest."""
        all_records = sorted(list(self.record_map.values()), key=lambda x: (x["data"], x["secao"], int(x["pagina"])))

        fieldnames = ["data", "secao", "jornal", "pagina", "file_txt", "char_count", "size_bytes", "scraped_at", "status"]
        with open(self.index_csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in all_records:
                writer.writerow(r)

        catalog_data = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_pages": len(all_records),
            "documents": all_records,
        }
        with open(self.index_json_file, "w", encoding="utf-8") as f:
            json.dump(catalog_data, f, indent=2, ensure_ascii=False)

        manifest = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_pages": len(all_records),
            "sections": {},
            "dates": {},
        }
        for r in all_records:
            sec = r.get("secao", "outros")
            dt = r.get("data", "")
            manifest["sections"][sec] = manifest["sections"].get(sec, 0) + 1
            manifest["dates"][dt] = manifest["dates"].get(dt, 0) + 1

        with open(self.manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)


# --- Inline Validation ---

def run_sanity_checks() -> None:
    """Validate date and parser logic."""
    d = parse_date_to_object("2001-01-01")
    assert d == date(2001, 1, 1)
    br, iso = format_date_tuple(d)
    assert br == "01/01/2001" and iso == "2001-01-01"
    assert JORNAL_NAMES[1] == "secao_1"
    assert JORNAL_NAMES[2] == "secao_2"
    assert JORNAL_NAMES[3] == "secao_3"
    print("[✓] All internal sanity checks passed.")


# --- CLI Entrypoint ---

def main() -> None:
    today_iso = date.today().strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser(description="DOU Archive Scraper (All Sections: 1, 2, 3 from Start Date to Today)")
    parser.add_argument("--start-date", type=str, default=DEFAULT_START_DATE,
                        help=f"Start date (YYYY-MM-DD or DD/MM/YYYY). Default: {DEFAULT_START_DATE}")
    parser.add_argument("--end-date", type=str, default=today_iso,
                        help=f"End date (YYYY-MM-DD or DD/MM/YYYY). Default: {today_iso} (Today)")
    parser.add_argument("--sections", type=int, nargs="+", default=DEFAULT_SECTIONS,
                        help="DOU sections to scrape. Default: 1 2 3 (Seções 1, 2 e 3)")
    parser.add_argument("--pagina", type=int, default=None,
                        help="Download a single specific page only (e.g. --pagina 65)")
    parser.add_argument("--limit-pages-per-day", type=int, default=None,
                        help="Limit number of pages downloaded per day (for testing)")
    parser.add_argument("--limit-days", type=int, default=None,
                        help="Limit total number of calendar days to crawl")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help=f"Destination directory (default: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--workers", type=int, default=10,
                        help="Number of concurrent worker threads (default: 10)")
    parser.add_argument("--timeout", type=int, default=15,
                        help="HTTP timeout in seconds (default: 15)")
    parser.add_argument("--no-text", action="store_true",
                        help="Disable text extraction from PDF (.txt)")
    parser.add_argument("--sync", action="store_true",
                        help="Force single-threaded synchronous mode")

    args = parser.parse_args()

    run_sanity_checks()

    start_d = parse_date_to_object(args.start_date)
    end_d = parse_date_to_object(args.end_date)

    if start_d > end_d:
        print(f"[!] Error: start-date ({start_d}) is after end-date ({end_d}).")
        sys.exit(1)

    output_path = Path(args.output)
    scraper = DOUScraper(
        output_dir=output_path,
        workers=args.workers,
        timeout=args.timeout,
        sync_mode=args.sync,
        save_text=not args.no_text,
    )

    # Handle single page download
    if args.pagina:
        date_br, iso_date = format_date_tuple(start_d)
        target_jornal = args.sections[0] if args.sections else 1
        res = download_and_extract_page(
            date_br, iso_date, args.pagina, target_jornal, output_path,
            None, args.timeout, 3, not args.no_text
        )
        if res:
            scraper.record_map[f"{res['data']}_{res['secao']}_{int(res['pagina']):04d}"] = res
            scraper.save_catalog()
            print(f"[✓] Successfully downloaded and indexed page {args.pagina} of {date_br} ({JORNAL_NAMES.get(target_jornal)}).")
        else:
            print(f"[!] Failed to download page {args.pagina} of {date_br}.")
        return

    # Crawl full range and sections
    scraper.crawl_range(
        start_date=start_d,
        end_date=end_d,
        sections=args.sections,
        pages_limit_per_day=args.limit_pages_per_day,
        days_limit=args.limit_days
    )

    print("\n" + "=" * 65)
    print(f" DOU MULTI-SECTION ARCHIVE SCRAPER COMPLETE")
    print("=" * 65)
    print(f"Range:        {start_d.isoformat()} → {end_d.isoformat()}")
    print(f"Sections:     {', '.join([JORNAL_NAMES.get(s, str(s)).upper() for s in args.sections])}")
    print(f"Catalog CSV:  {scraper.index_csv_file.resolve()}")
    print(f"Total Pages:  {len(scraper.record_map)}")
    print(f"Destination:  {output_path.resolve()}")
    print("=" * 65)


if __name__ == "__main__":
    main()
