#!/usr/bin/env python3
"""Corpus Classifier & Partitioning Engine for Brazilian Legislation.

Classifies documents in docs/corpus into 'active' (vigente) and 'historical' (revogada /
exaurida / histórica) following a 4-tier deterministic pipeline:
  1. Planalto DOM Strike & Table Metadata Annotations (Explicit Revocations)
  2. Constitutional Epoch & Category Filters (Pre-1988, Imperial, Colonial Acts)
  3. Exhausted / Temporary Norms (Budget Credits, Expired Declaratory Acts)
  4. Cross-Revocation Dependency Graph (Explicit Revocation Clauses)

Preserves the identical category directory layout under active/ and historical/.
"""

import argparse
import concurrent.futures
import csv
import json
import logging
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

WORKERS = 50


# --- Historical Category Mappings ---

HISTORICAL_CATEGORIES = {
    "leis_imperio",
    "alvaras",
    "cartas_regias",
    "cartas_de_lei",
    "leis_delegadas",
}

HISTORICAL_CODES_FILENAMES = {
    "L3071.html",      # Código Civil de 1916 (Substituído pela Lei 10.406/2002)
    "L3071.htm",
    "L0556.html",      # Código Comercial de 1850 (Parcialmente revogado)
    "L0556.htm",
    "L5869.html",      # Código de Processo Civil de 1973 (Substituído pela Lei 13.105/2015)
    "L5869.htm",
    "Del1608.html",    # Código de Processo Civil de 1939
    "Del1608.htm",
    "L6697.html",      # Código de Menores de 1979 (Substituído pelo ECA Lei 8.069/1990)
    "L6697.htm",
    "Del2848.htm",     # Checked individually
}


# --- Tier 1: Planalto Metadata and DOM Heuristics ---

REVOCATION_KEYWORDS_REGEX = re.compile(
    r'(?:'
    r'revogad[oa]\s+pel[oa]|'
    r'revogad[oa]\s+integralmente|'
    r'revogad[oa]\s+expressamente|'
    r'declarad[oa]\s+revogad[oa]|'
    r'declarad[oa]\s+sem\s+efeito|'
    r'declarad[oa]\s+inconstitucional|'
    r'perdeu\s+a\s+efic[áa]cia|'
    r'rejeitad[oa]\s+pel[oa]\s+congresso|'
    r'n[ãa]o\s+recepcionad[oa]|'
    r'vig[êe]ncia\s+encerrada|'
    r'prejudicad[oa]|'
    r'sem\s+efic[áa]cia'
    r')',
    re.IGNORECASE
)

REVOCATION_CLAUSE_REGEX = re.compile(
    r'(?:'
    r'fica(?:m)?\s+revogad[oa]s?\s+([^\n\.;]+)|'
    r'revoga(?:m)?-se\s+([^\n\.;]+)'
    r')',
    re.IGNORECASE
)

TARGET_LAW_REF_REGEX = re.compile(
    r'(?:'
    r'(?:a\s+)?lei\s+(?:ordin[áa]ria\s+|complementar\s+|delegada\s+)?n[ºo°\.\s]*([\d\.\-]+)|'
    r'(?:o\s+)?decreto-lei\s+n[ºo°\.\s]*([\d\.\-]+)|'
    r'(?:o\s+)?decreto\s+n[ºo°\.\s]*([\d\.\-]+)|'
    r'(?:a\s+)?medida\s+provis[óo]ria\s+n[ºo°\.\s]*([\d\.\-]+)|'
    r'(?:o\s+)?ato\s+complementar\s+n[ºo°\.\s]*([\d\.\-]+)'
    r')',
    re.IGNORECASE
)


def has_dom_strike_through(soup: BeautifulSoup) -> bool:
    """Check if the title heading or full document is struck through in Planalto HTML."""
    # Check title link (legislacao.nsf link)
    title_link = soup.find("a", href=re.compile(r"legislacao\.nsf|legisla\.nsf", re.I))
    if title_link:
        if title_link.find_parent(["strike", "s", "del"]) or title_link.find(["strike", "s", "del"]):
            return True
        parent_style = title_link.get("style", "") or (title_link.parent.get("style", "") if title_link.parent else "")
        if "line-through" in parent_style.lower():
            return True

    # Check centered heading paragraphs
    for p in soup.find_all("p", align=re.compile(r"center", re.I))[:3]:
        if p.find(["strike", "s", "del"]):
            return True
        if "line-through" in (p.get("style") or "").lower():
            return True

    return False


def get_planalto_header_notes(soup: BeautifulSoup) -> str:
    """Extract correlation and alteration notes from Table 2 Col 1."""
    tables = soup.find_all("table")
    notes = []
    for t in tables[:3]:
        tds = t.find_all("td")
        if len(tds) >= 2:
            # Col 1 contains notes, vetos, revocations
            txt = tds[0].get_text(separator=" ", strip=True)
            if txt and len(txt) > 3:
                notes.append(txt)
    return " ".join(notes)


# --- Classification Core Logic ---

def classify_document(
    file_path: Path,
    category: str,
    html_text: str,
    soup: Optional[BeautifulSoup] = None
) -> Tuple[str, str, List[str]]:
    """Classify a single document into 'active' or 'historical' with diagnostic reason.

    Returns:
        (status, status_reason, list_of_revoked_targets_cited)
    """
    if soup is None:
        soup = BeautifulSoup(html_text, "html.parser")

    fname = file_path.name
    revoked_targets: List[str] = []

    # ---------------------------------------------------------
    # Tier 1: Planalto Metadata & DOM Strike (Explicit Revocation)
    # ---------------------------------------------------------
    header_notes = get_planalto_header_notes(soup)
    if REVOCATION_KEYWORDS_REGEX.search(header_notes):
        match = REVOCATION_KEYWORDS_REGEX.search(header_notes)
        keyword = match.group(0) if match else "revogado"
        return ("historical", f"planalto_note: {keyword}", revoked_targets)

    if has_dom_strike_through(soup):
        return ("historical", "dom_strike_through: título/corpo riscado", revoked_targets)

    # ---------------------------------------------------------
    # Tier 2: Constitutional Epoch & Historical Category Filter
    # ---------------------------------------------------------
    if category in HISTORICAL_CATEGORIES:
        return ("historical", f"historical_category: {category}", revoked_targets)

    if fname in HISTORICAL_CODES_FILENAMES:
        return ("historical", f"historical_code: {fname}", revoked_targets)

    # Check for historical constitutions (1824-1969)
    if category == "constituicao":
        # Check if year is prior to 1988
        m_year = re.search(r'(?:18|19)\d{2}', fname)
        if m_year:
            year = int(m_year.group(0))
            if year < 1988:
                return ("historical", f"historical_constitution: {year}", revoked_targets)

    # ---------------------------------------------------------
    # Tier 3: Exhausted / Temporary Norms (Eficácia Exaurida)
    # ---------------------------------------------------------
    # Scan text for single-paragraph expired acts (Ato do Presidente da Mesa)
    doc_text = soup.get_text(separator=" ", strip=True)

    if "ATO DO PRESIDENTE DA MESA DO CONGRESSO" in doc_text:
        if "perdeu a eficácia" in doc_text.lower() or "rejeitada" in doc_text.lower():
            return ("historical", "ato_mesa_perda_eficacia", revoked_targets)

    # Credit/Budget acts from previous financial years
    # E.g. "Abre crédito extraordinário" or "Abre crédito suplementar"
    if re.search(r'^(?:Abre\s+ao\s+Orçamento|Abre\s+crédito\s+extraordinário|Abre\s+crédito\s+suplementar)', doc_text[:400], re.I):
        m_yr = re.search(r'DE\s+\d{1,2}\s+DE\s+[A-Za-zçÇáéíóúÁÉÍÓÚ]+\s+DE\s+(\d{4})', doc_text[:300])
        if m_yr:
            act_year = int(m_yr.group(1))
            current_year = datetime.now().year
            if act_year < current_year:
                return ("historical", f"credito_orcamentario_exaurido: {act_year}", revoked_targets)

    # ---------------------------------------------------------
    # Tier 4: Scan for outgoing revocation clauses (Who this doc revokes)
    # ---------------------------------------------------------
    for m in REVOCATION_CLAUSE_REGEX.finditer(doc_text):
        clause_body = (m.group(1) or m.group(2) or "")[:200]
        for ref_match in TARGET_LAW_REF_REGEX.finditer(clause_body):
            target_num = ref_match.group(1) or ref_match.group(2) or ref_match.group(3) or ref_match.group(4) or ref_match.group(5)
            if target_num:
                revoked_targets.append(target_num.replace(".", "").strip())

    # If no revocation indicators triggered, the document is considered Active (Vigente)
    return ("active", "vigente", revoked_targets)


# --- Cross-Revocation Graph Resolver ---

def apply_cross_revocation_graph(
    record_map: Dict[str, Dict],
    revocation_edges: List[Tuple[str, str, str]]
) -> int:
    """Apply graph edges to mark targets as historical if they were revoked by an active/later act.

    Returns the number of newly updated records.
    """
    updated = 0
    # Map from law number / normalized identifier to record keys
    num_to_keys = defaultdict(list)
    for k, rec in record_map.items():
        num = rec.get("number", "").replace(".", "").strip()
        cat = rec.get("category", "")
        if num and num != "S/N":
            num_to_keys[(cat, num)].append(k)
            num_to_keys[num].append(k)

    for revoker_file, target_num, clause_snippet in revocation_edges:
        target_keys = num_to_keys.get(target_num, [])
        for tk in target_keys:
            target_rec = record_map[tk]
            if target_rec["status"] == "active":
                target_rec["status"] = "historical"
                target_rec["status_reason"] = f"revogado_por_lei: {revoker_file}"
                updated += 1

    return updated


# --- Corpus Manager ---

class CorpusClassifierManager:
    """Orchestrates classification, partitioning, file moving, and index generation."""

    def __init__(self, corpus_dir: Path, workers: int = WORKERS):
        self.corpus_dir = corpus_dir.resolve()
        self.workers = workers
        self.index_csv = self.corpus_dir / "index.csv"
        self.index_json = self.corpus_dir / "index.json"
        self.manifest_json = self.corpus_dir / "manifest.json"
        self.revocation_manifest = self.corpus_dir / "revocation_manifest.json"
        self.revocation_graph_file = self.corpus_dir / "revocation_graph.json"

    def scan_and_classify_all(self) -> Tuple[Dict[str, Dict], List[Tuple[str, str, str]]]:
        """Scan all HTML files in corpus directory and classify status."""
        html_files: List[Path] = []
        for root, _, files in os.walk(self.corpus_dir):
            rpath = Path(root)
            # Skip existing active / historical subfolders if already created
            if "active" in rpath.parts or "historical" in rpath.parts:
                continue
            for f in files:
                if f.endswith(".html") or f.endswith(".htm"):
                    html_files.append(rpath / f)

        print(f"[*] Found {len(html_files)} HTML documents to classify across {self.corpus_dir}")

        records: Dict[str, Dict] = {}
        revocation_edges: List[Tuple[str, str, str]] = []

        def _process_file(fpath: Path):
            try:
                rel_p = fpath.relative_to(self.corpus_dir)
                category = rel_p.parts[0] if len(rel_p.parts) > 1 else "outros"
                html_text = fpath.read_text(encoding="utf-8", errors="replace")
                soup = BeautifulSoup(html_text, "html.parser")

                status, reason, targets = classify_document(fpath, category, html_text, soup=soup)
                
                # Number extraction fallback
                num_m = re.search(r'([L|D|Mpv|Del|Emc|Dlg]+)[\-_]?(\d+[\.\d]*)', fpath.name, re.I)
                doc_number = num_m.group(2) if num_m else "S/N"

                return {
                    "file_path": str(rel_p),
                    "full_path": str(fpath),
                    "filename": fpath.name,
                    "category": category,
                    "number": doc_number,
                    "status": status,
                    "status_reason": reason,
                    "file_size_bytes": fpath.stat().st_size,
                    "targets": [(fpath.name, t, reason) for t in targets]
                }
            except Exception as exc:
                logging.debug("Error processing %s: %s", fpath, exc)
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = list(tqdm(
                executor.map(_process_file, html_files),
                total=len(html_files),
                desc="Classifying Corpus",
                unit="doc"
            ))

        for r in results:
            if r:
                records[r["file_path"]] = r
                for edge in r["targets"]:
                    revocation_edges.append(edge)

        # Apply Cross-revocation graph resolution
        newly_revoked = apply_cross_revocation_graph(records, revocation_edges)
        print(f"[✓] Initial Classification complete: {len(records)} documents processed. {newly_revoked} updated via cross-revocation graph.")
        return records, revocation_edges

    def partition_files(self, records: Dict[str, Dict], dry_run: bool = True) -> None:
        """Move files to active/<category>/ or historical/<category>/ preserving hierarchy."""
        active_dir = self.corpus_dir / "active"
        historical_dir = self.corpus_dir / "historical"

        moves = []
        for rel_path, rec in records.items():
            src_path = Path(rec["full_path"])
            if not src_path.exists():
                continue

            status = rec["status"]  # "active" or "historical"
            category = rec["category"]
            fname = rec["filename"]

            dest_dir = (active_dir if status == "active" else historical_dir) / category
            dest_path = dest_dir / fname

            moves.append((src_path, dest_path, dest_dir, rel_path, status, category))

        print(f"\n[*] Partition Plan ({'DRY RUN' if dry_run else 'EXECUTING MOVES'}):")
        print(f"    - Total Files: {len(moves)}")
        active_count = sum(1 for m in moves if m[4] == "active")
        hist_count = sum(1 for m in moves if m[4] == "historical")
        print(f"    - Active (Vigente):    {active_count} ({active_count/len(moves)*100:.1f}%)")
        print(f"    - Historical (Inativo): {hist_count} ({hist_count/len(moves)*100:.1f}%)")

        if dry_run:
            print("\n[!] Dry run mode: No files were moved. Run without --dry-run to execute physical moves.")
            return

        # Perform moves
        print(f"\n[*] Executing physical moves into {active_dir} and {historical_dir}...")
        for src_path, dest_path, dest_dir, rel_path, status, category in tqdm(moves, desc="Moving Files", unit="file"):
            dest_dir.mkdir(parents=True, exist_ok=True)
            if src_path != dest_path:
                shutil.move(str(src_path), str(dest_path))
                # Update record with new relative path
                records[rel_path]["new_file_path"] = str(dest_path.relative_to(self.corpus_dir))
                records[rel_path]["full_path"] = str(dest_path)

        # Cleanup empty source category folders
        for root, dirs, files in os.walk(self.corpus_dir, topdown=False):
            rpath = Path(root)
            if rpath != self.corpus_dir and rpath != active_dir and rpath != historical_dir:
                if not any(rpath.iterdir()):
                    try:
                        rpath.rmdir()
                    except OSError:
                        pass

        print("[✓] All files partitioned successfully.")

    def save_updated_catalogs(
        self,
        records: Dict[str, Dict],
        revocation_edges: List[Tuple[str, str, str]],
        dry_run: bool = False
    ) -> None:
        """Write updated index.csv, index.json, manifest.json and revocation_manifest.json."""
        if dry_run:
            print("\n[*] Dry-run mode: Catalog files will not be overwritten.")
            return

        records_list = list(records.values())

        # 1. Update CSV Index
        fieldnames = [
            "doc_type", "number", "date", "scraped_at", "url", "category",
            "status", "status_reason", "file_path", "file_size_bytes", "ementa"
        ]
        
        # Load existing metadata from old index.csv if available to preserve ementas and dates
        existing_meta = {}
        if self.index_csv.exists():
            with open(self.index_csv, "r", encoding="utf-8", errors="ignore") as f:
                for row in csv.DictReader(f):
                    existing_meta[row.get("file_path", "")] = row

        csv_rows = []
        for r in records_list:
            old_rel = r["file_path"]
            new_rel = r.get("new_file_path", old_rel)
            ex = existing_meta.get(old_rel, {})

            csv_rows.append({
                "doc_type": ex.get("doc_type", r.get("category", "OUTROS").upper()),
                "number": ex.get("number", r.get("number", "S/N")),
                "date": ex.get("date", "N/D"),
                "scraped_at": ex.get("scraped_at", datetime.now(timezone.utc).isoformat()),
                "url": ex.get("url", ""),
                "category": r.get("category", "outros"),
                "status": r.get("status", "active"),
                "status_reason": r.get("status_reason", ""),
                "file_path": new_rel,
                "file_size_bytes": r.get("file_size_bytes", 0),
                "ementa": ex.get("ementa", "Sem ementa disponível")
            })

        with open(self.index_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)

        # 2. Write JSON Catalog
        catalog_data = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_documents": len(csv_rows),
            "active_count": sum(1 for r in csv_rows if r["status"] == "active"),
            "historical_count": sum(1 for r in csv_rows if r["status"] == "historical"),
            "documents": csv_rows
        }
        with open(self.index_json, "w", encoding="utf-8") as f:
            json.dump(catalog_data, f, indent=2, ensure_ascii=False)

        # 3. Write Manifest
        manifest = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_documents": len(csv_rows),
            "status_distribution": Counter(r["status"] for r in csv_rows),
            "category_distribution": Counter(r["category"] for r in csv_rows),
            "reason_distribution": Counter(r["status_reason"] for r in csv_rows),
        }
        with open(self.manifest_json, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        # 4. Write Revocation Graph
        graph_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_edges": len(revocation_edges),
            "edges": [
                {"revoker": e[0], "target_number": e[1], "reason": e[2]}
                for e in revocation_edges
            ]
        }
        with open(self.revocation_graph_file, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)

        print(f"[✓] Updated Index Catalogs saved to {self.corpus_dir}")


# --- Self-Tests & Sanity Asserts ---

def run_classifier_sanity_checks() -> None:
    """Unit asserts for classification pipeline layers."""
    # Test 1: Planalto Note Revocation
    html_note = "<table><tr><td>(Revogado pelo Decreto nº 10.000, de 2019)</td><td>Ementa</td></tr></table>"
    status, reason, _ = classify_document(Path("test.html"), "leis_ordinarias", html_note)
    assert status == "historical", f"Expected historical, got {status}"
    assert "planalto_note" in reason

    # Test 2: DOM Strike through
    html_strike = "<p align='center'><strike>LEI Nº 5.000</strike></p>"
    status, reason, _ = classify_document(Path("test2.html"), "leis_ordinarias", html_strike)
    assert status == "historical", f"Expected historical, got {status}"
    assert "dom_strike_through" in reason

    # Test 3: Historical Category
    html_imp = "<html><body>Lei imperial</body></html>"
    status, reason, _ = classify_document(Path("LIM-12-10-1832.html"), "leis_imperio", html_imp)
    assert status == "historical", f"Expected historical, got {status}"
    assert "historical_category" in reason

    # Test 4: Historical Code
    status, reason, _ = classify_document(Path("L3071.html"), "codigos", "<html>Código Civil 1916</html>")
    assert status == "historical"

    # Test 5: Modern Active Law
    html_active = "<table><tr><td></td><td>Estabelece a lei de responsabilidade fiscal do esporte.</td></tr></table>"
    status, reason, _ = classify_document(Path("L13155.html"), "leis_ordinarias", html_active)
    assert status == "active", f"Expected active, got {status}"

    print("[✓] All classifier sanity checks passed successfully.")


# --- CLI Interface ---

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LEX Corpus Classifier & Partitioning Tool")
    parser.add_argument("--corpus-dir", type=str, default=str(Path(__file__).resolve().parent.parent / "docs" / "corpus"),
                        help="Path to docs/corpus directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run in simulation mode without moving files or updating catalogs (Default is to execute physical moves)")
    parser.add_argument("--workers", type=int, default=WORKERS,
                        help=f"Number of concurrent worker threads (Default: {WORKERS})")
    parser.add_argument("--check-only", action="store_true",
                        help="Run sanity check asserts and exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_classifier_sanity_checks()

    if args.check_only:
        return

    corpus_path = Path(args.corpus_dir)
    manager = CorpusClassifierManager(corpus_dir=corpus_path, workers=args.workers)

    # Step 1: Scan and classify
    records, edges = manager.scan_and_classify_all()

    # Step 2: Partition files
    dry_run = args.dry_run
    manager.partition_files(records, dry_run=dry_run)

    # Step 3: Save catalogs
    manager.save_updated_catalogs(records, edges, dry_run=dry_run)

    # Step 4: Summary
    print("\n" + "=" * 65)
    print(" CORPUS CLASSIFICATION & PARTITION SUMMARY")
    print("=" * 65)
    print(f"Corpus Directory: {corpus_path}")
    print(f"Mode:             {'DRY RUN (Simulation)' if args.dry_run else 'PHYSICAL MOVE EXECUTED'}")
    print(f"Total Documents:  {len(records)}")
    active_n = sum(1 for r in records.values() if r["status"] == "active")
    hist_n = sum(1 for r in records.values() if r["status"] == "historical")
    print(f"Active (Vigente): {active_n} ({active_n/len(records)*100:.1f}%) -> active/<category>/")
    print(f"Historical:       {hist_n} ({hist_n/len(records)*100:.1f}%) -> historical/<category>/")
    print(f"Revocation Edges: {len(edges)} cross-references captured")
    print("=" * 65)


if __name__ == "__main__":
    main()
