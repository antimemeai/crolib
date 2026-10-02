#!/usr/bin/env python3
"""Consolidate lane catalogues and audit acquired artifacts directly."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def normalized(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", value)


def main():
    entries = []
    lanes = {}
    for path in sorted((ROOT / "papers/lanes").glob("*/catalogue.json")):
        records = json.loads(path.read_text())
        lanes[path.parent.name] = dict(Counter(record["status"] for record in records))
        for record in records:
            record = dict(record, lane=path.parent.name)
            if record["status"] == "acquired":
                if not record.get("local_path") or not (ROOT / record["local_path"]).is_file():
                    raise ValueError("missing acquired full text: " + record["id"])
            entries.append(record)
    # Union matching DOI or normalized title/year. Versions and editions retain different titles/years.
    groups, keys = [], {}
    for record in entries:
        identities = [("title", normalized(record["title"]), record["year"])]
        if record.get("doi"):
            doi = record["doi"].lower().strip().removeprefix("https://doi.org/")
            identities.append(("doi", doi))
        matches = {keys[key] for key in identities if key in keys}
        if matches:
            group = min(matches)
            for other in matches - {group}:
                groups[group].extend(groups[other])
                groups[other] = []
                keys = {key: group if val == other else val for key, val in keys.items()}
        else:
            group = len(groups)
            groups.append([])
        groups[group].append(record)
        for key in identities:
            keys[key] = group
    consolidated = []
    ranking = {"acquired": 0, "access_blocked": 1, "metadata_only": 2}
    for group in groups:
        if not group:
            continue
        preferred = min(group, key=lambda record: ranking.get(record["status"], 3))
        item = dict(preferred)
        item.pop("lane")
        item["aliases"] = [record["id"] for record in group]
        item["lanes"] = sorted({record["lane"] for record in group})
        item["topics"] = sorted({topic for record in group for topic in record["topics"]})
        item["local_paths"] = sorted({record["local_path"] for record in group if record.get("local_path")})
        item["lane_records"] = [{"id": r["id"], "lane": r["lane"], "status": r["status"],
                                 "source_url": r["source_url"], "evidence": r["evidence"],
                                 "acquisition_note": r["acquisition_note"]} for r in group]
        consolidated.append(item)
    consolidated.sort(key=lambda record: (record["year"] or 9999, record["title"].lower()))
    artifacts = []
    for sidecar in sorted((ROOT / "papers/downloads").rglob("*.source.json")):
        path = sidecar.with_name(sidecar.name.removesuffix(".source.json"))
        metadata = json.loads(sidecar.read_text())
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != metadata["sha256"]:
            raise ValueError("artifact checksum differs: " + str(path))
        if metadata["kind"] == "pdf" and b"%PDF-" not in data[:1024]:
            raise ValueError("invalid acquired PDF: " + str(path))
        artifacts.append(dict(metadata, local_path=str(path.relative_to(ROOT))))
    software = [json.loads(path.read_text()) for path in sorted((ROOT / "papers/software/records").glob("*.json"))]
    acquired_software = [record for record in software if record["status"] == "acquired"]
    for record in acquired_software:
        if record.get("kind") == "files":
            sources = [(item["raw_path"], item["sha256"]) for item in record["files"]]
        else:
            sources = [(record["archive_path"], record["archive_sha256"])]
        for path, sha in sources:
            if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha:
                raise ValueError("reference checksum differs: " + path)
        extracted = ROOT / record["extracted_path"]
        if any(part.name in {".git", ".DS_Store", "__MACOSX", ".Rhistory", ".Rproj.user"} for part in extracted.rglob("*")):
            raise ValueError("reference contains extraction detritus: " + record["id"])
    summary = {"lane_records": len(entries), "distinct_catalogued_works": len(consolidated),
               "statuses": dict(Counter(record["status"] for record in consolidated)),
               "acquired_artifacts": len(artifacts), "artifact_kinds": dict(Counter(a["kind"] for a in artifacts)),
               "acquired_reference_packages": len(acquired_software), "lanes": lanes,
               "bibliography_leads": len(json.loads((ROOT / "papers/bibliography-leads.json").read_text()))}
    resolutions_path = ROOT / "papers/lanes/coverage/lead-resolution.json"
    if resolutions_path.exists():
        summary["historical_registry_audit"] = dict(Counter(
            item["resolution_status"] for item in json.loads(resolutions_path.read_text())))
    summary["reference_download_failures"] = sum(len(item.get("failed_files", [])) for item in acquired_software)
    summary["explicitly_omitted_reference_files"] = sum(len(item.get("skipped_files", [])) for item in acquired_software)
    for name, content in [("catalogue.json", consolidated), ("acquired-artifacts.json", artifacts), ("summary.json", summary)]:
        (ROOT / "papers" / name).write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "papers/software/manifest.json").write_text(json.dumps(software, indent=2) + "\n")
    rows = ["# Generalizability-theory catalogue", "", "Generated from lane catalogues by `python3 scripts/catalogue.py`. Acquisition is not a claim of complete reading. See lane records for evidence and failures.", "", "| Year | Work | Status | Lanes |", "| --- | --- | --- | --- |"]
    for record in consolidated:
        title = record["title"].replace("|", "\\|").replace("[", "(").replace("]", ")")
        rows.append("| {} | [{}]({}) | {} | {} |".format(record["year"] or "undated", title, record["source_url"], record["status"], ", ".join(record["lanes"])))
    (ROOT / "papers/CATALOGUE.md").write_text("\n".join(rows) + "\n")
    leads = json.loads((ROOT / "papers/bibliography-leads.json").read_text())
    coverage = []
    for lead in leads:
        citation = normalized(lead["citation"])
        surname = normalized(lead["citation"].split(",", 1)[0])
        candidates = [record["id"] for record in consolidated
                      if record["year"] == lead["year"]
                      and len(normalized(record["title"])) >= 10
                      and normalized(record["title"]) in citation
                      and surname in normalized(" ".join(record["authors"]))]
        coverage.append({"lead_id": lead["id"], "candidate_catalogue_ids": candidates,
                         "status": "candidate_match" if candidates else "unresolved_lead",
                         "note": "Mechanical title/year/author candidate; confirm editions and source errors in a reading pass."})
    (ROOT / "papers/bibliography-coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
    rows = ["# Acquisition shopping list", "", "Generated unresolved-work inventory. Sources marked `metadata_only` have verified records but no local full text; `access_blocked` records include failed attempts. Lane reports give priorities and possible alternatives. Acquisition gaps remain even where a publisher abstract or indexed text was readable.", "", "## First acquisitions", "", "1. Cronbach, Gleser, Nanda & Rajaratnam (1972), *The dependability of behavioral measurements*. Wiley, ISBN 0471188506.", "2. Brennan (2001), *Generalizability Theory*, complete book including chapters 7–12. [Publisher ebook](https://doi.org/10.1007/978-1-4757-3456-0).", "3. Original 1963/1965 trilogy, Cardinet's symmetry/extension papers with their errata, and Cardinet/Tourneur (1985) *Assurer la mesure*.", "4. Cardinet/Johnson/Pini (2010), *Applying Generalizability Theory using EduG*, and Shavelson/Webb (1991), *Generalizability Theory: A Primer*.", "5. Inaccessible original sparse-estimation, ordinal and multivariate derivations identified below; their acquired tutorials do not replace them.", "", "## Verified works without acquired full text", "", "| Year | Work | Status | Acquisition note |", "| --- | --- | --- | --- |"]
    for record in consolidated:
        if record["status"] == "acquired":
            continue
        title = record["title"].replace("|", "\\|")
        note = record["acquisition_note"].replace("|", "\\|").replace("\n", " ")
        rows.append("| {} | [{}]({}) | {} | {} |".format(record["year"] or "undated", title, record["source_url"], record["status"], note))
    rows.extend(["", "## Missing software and supplements", "", "- Original GENOVA Fortran and mGENOVA/urGENOVA C sources: acquired distributions contain executables, manuals and examples; jGENOVA Java source is available locally.", "- EduG current/corrected executable/source distribution; its original2010 user guide has been recovered. FANTAB (Brown1969, ERICED143704) source appendix and GAPID (ACT34,1979) original source/manual remain unresolved.", "- Jiang–Skorupski2018 BUGS/data/mGENOVA supplement: original author ZIP returns404. Core2018paper and2024mixed-formatStan/OSF materials are acquired.", "- APA Vispoel instructional supplements and MDPI2025 R supplement where direct access is blocked. See software search log for final outcomes and recovered alternatives.", "- Recent AI papers' request-only datasets/code must be requested from their authors if needed; public aggregate data do not establish availability of the response-level data used in their decompositions.", "", "The 328 bibliography entries in [bibliography-leads.json](bibliography-leads.json) are discovery leads, not 328 independently verified works. [bibliography-coverage.json](bibliography-coverage.json) records mechanical candidate matches and remaining leads. The coverage audit documents which unresolved branches need further expansion."])
    rows.extend(["", "## Supplementary data acquisition boundaries", "", "The many-reliabilities package retains its nine small source, input-data, supplementary and report files. Four derived posterior/factor-score dumps totalling about2.5GB were explicitly omitted and inventoried in its source record; these are generated outputs rather than missing model source. All acquired OSF source-package files now have zero download failures. Transient429 failures were resolved by later serial retries."])
    (ROOT / "papers/SHOPPING_LIST.md").write_text("\n".join(rows) + "\n")
    rows = ["# Reference implementation manifest", "", "Original sources reside in ignored `quarantine/archives/`; inspected copies in `quarantine/references/`. Exact checksums, revisions, exclusions and restoration commands are in [manifest.json](manifest.json). No acquired implementation has been executed or adopted as a dependency.", "", "| Reference | Revision | Files | Scope |", "| --- | --- | --- | --- |"]
    for record in acquired_software:
        rows.append("| [{}]({}) | {} | {} | {} |".format(record["id"], record["source_url"], record["revision"], record["extracted_files"], record["description"]))
    rows.extend(["", "Restore all acquired references with `python3 scripts/restore_references.py`, or select one using `--only ID`. Sources that change checksum are rejected before extraction. Loose-file packages preserve each original separately."])
    (ROOT / "papers/software/MANIFEST.md").write_text("\n".join(rows) + "\n")
    (ROOT / "quarantine").mkdir(exist_ok=True)
    (ROOT / "quarantine/MANIFEST.md").write_text(
        "# Quarantine manifest\n\n"
        "The authoritative tracked inventory is [papers/software/MANIFEST.md](../papers/software/MANIFEST.md) "
        "with exact records in [manifest.json](../papers/software/manifest.json).\n\n"
        "Original archives and loose files remain intact in `archives/`; inspected regular-file copies "
        "are in `references/`. Nested Git metadata and filesystem detritus are excluded. "
        "Archived instructions are historical; no reference code has been executed.\n\n"
        "Restore from the repository root with `python3 scripts/restore_references.py`.\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
