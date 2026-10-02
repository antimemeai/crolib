#!/usr/bin/env python3
"""Import CASMA53 PDF text as unverified discovery leads, not verified citations."""

import argparse
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    result = subprocess.run(["pdftotext", "-layout", str(args.pdf), "-"], capture_output=True, text=True, check=True)
    citations, current, started, era = [], [], False, "20th century"
    for raw in result.stdout.splitlines():
        line = raw.replace("\f", "")
        stripped = line.strip()
        if stripped.startswith("Algina, J."):
            started = True
        if not started or not stripped or "Brennan and Liao" in line or stripped.isdigit():
            continue
        if stripped == "21st Century":
            if current:
                citations.append((era, " ".join(current)))
                current = []
            era = "21st century"
            continue
        if not line.startswith(" ") and current:
            citations.append((era, " ".join(current)))
            current = []
        if current and re.search(r"[a-z]-$", current[-1]) and re.match(r"^[a-z]", stripped):
            current[-1] = current[-1][:-1] + stripped
        else:
            current.append(stripped)
    if current:
        citations.append((era, " ".join(current)))
    records = []
    for index, (era, citation) in enumerate(citations, 1):
        match = re.search(r"\([^)]*?(\d{4})[a-z]?[^)]*\)", citation)
        records.append({"id": "casma53-lead-{:03d}".format(index), "citation": citation,
                        "year": int(match.group(1)) if match else None, "era": era,
                        "status": "bibliography_lead",
                        "evidence": "Cited in Brennan & Liao CASMA Report 53 (2020); not independently verified by this import. Source typography/date errors may be retained.",
                        "source_url": "https://education.uiowa.edu/sites/education.uiowa.edu/files/2026-04/casma-research-report-53-archived.pdf"})
    destination = Path(__file__).resolve().parents[1] / "papers/bibliography-leads.json"
    destination.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    print(len(records), "bibliography entries imported as leads")


if __name__ == "__main__":
    main()
