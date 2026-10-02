#!/usr/bin/env python3
"""Acquire a public OSF reference project's files, retaining individual provenance."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path, PurePosixPath
import shutil
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import urllib.request

from acquire import acquire

ROOT = Path(__file__).resolve().parents[1]


def sorted_listing_url(url):
    """Retain pagination parameters while enforcing a stable OSF file order."""
    parts = urlsplit(url)
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
             if key != "sort"]
    query.append(("sort", "name"))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def listing(url):
    while url:
        url = sorted_listing_url(url)
        with urllib.request.urlopen(url, timeout=20) as response:
            page = json.load(response)
        for item in page["data"]:
            if item["attributes"]["kind"] == "folder":
                yield from listing(item["relationships"]["files"]["links"]["related"]["href"])
            else:
                yield item
        url = page.get("links", {}).get("next")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("node")
    parser.add_argument("identifier")
    parser.add_argument("--description", required=True)
    parser.add_argument("--max-files", type=int, default=100,
                        help="Maximum distinct OSF file IDs to acquire (default: 100)")
    parser.add_argument("--max-file-mib", type=float,
                        help="Select files no larger than this size; record omitted files explicitly")
    parser.add_argument("--workers", type=int, default=4,
                        help="Concurrent downloads; use 1 to reduce rate-limit bursts (default: 4)")
    args = parser.parse_args()
    if not args.identifier or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in args.identifier):
        raise ValueError("unsafe reference identifier")
    if args.max_files < 1:
        raise ValueError("max-files must be positive")
    if args.max_file_mib is not None and args.max_file_mib <= 0:
        raise ValueError("max-file-mib must be positive")
    if args.workers < 1:
        raise ValueError("workers must be positive")
    listing_url = sorted_listing_url("https://api.osf.io/v2/nodes/" + args.node + "/files/osfstorage/")
    listed = list(listing(listing_url))
    by_id, duplicates = {}, []
    for entry in listed:
        if entry["id"] in by_id:
            duplicates.append({"osf_file_id": entry["id"],
                               "path": entry["attributes"]["materialized_path"]})
        else:
            by_id[entry["id"]] = entry
    entries = list(by_id.values())
    skipped = []
    if args.max_file_mib is not None:
        skipped = [{"name": item["attributes"]["materialized_path"], "osf_file_id": item["id"],
                    "source_url": item["links"]["download"], "bytes": item["attributes"].get("size"),
                    "reason": "Excluded by explicit --max-file-mib selection"}
                   for item in entries if (item["attributes"].get("size") or 0) > args.max_file_mib * 1024 * 1024]
        skipped_ids = {item["osf_file_id"] for item in skipped}
        entries = [item for item in entries if item["id"] not in skipped_ids]
    if len(entries) > args.max_files or sum(x["attributes"].get("size") or 0 for x in entries) > 100 * 1024 * 1024:
        raise ValueError("project exceeds acquisition bounds; select relevant files explicitly")
    path_ids = {}
    for entry in entries:
        path_ids.setdefault(entry["attributes"]["materialized_path"], []).append(entry["id"])
    conflicts = [{"path": path, "osf_file_ids": ids}
                 for path, ids in path_ids.items() if len(ids) > 1]
    files, failures = [], []

    def download(item):
        attrs = item["attributes"]
        name = PurePosixPath(attrs["materialized_path"].lstrip("/"))
        if ".." in name.parts or "\\" in str(name) or ".git" in name.parts:
            raise ValueError("unsafe OSF path")
        if len(path_ids[attrs["materialized_path"]]) > 1:
            name = PurePosixPath("__osf_path_conflicts") / item["id"] / name
        raw = Path("quarantine/archives") / args.identifier / name
        target = Path("quarantine/references") / args.identifier / name
        url = item["links"]["download"]
        metadata = acquire(url, ROOT / raw, "text", timeout=25)
        expected = attrs.get("extra", {}).get("hashes", {}).get("sha256")
        if expected and metadata["sha256"] != expected:
            raise ValueError("OSF checksum mismatch: " + str(name))
        (ROOT / target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / raw, ROOT / target)
        (ROOT / target).chmod(0o644)
        return {"source_url": url, "raw_path": str(raw), "extracted_path": str(target),
                "sha256": metadata["sha256"], "bytes": metadata["bytes"],
                "osf_file_id": item["id"], "version": attrs.get("current_version"),
                "original_osf_path": attrs["materialized_path"]}

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [(item, pool.submit(download, item)) for item in entries]
        for item, future in futures:
            try:
                files.append(future.result())
            except Exception as error:
                failures.append({"name": item["attributes"]["materialized_path"],
                                 "source_url": item["links"]["download"], "reason": str(error)})
    record = {"id": args.identifier, "kind": "files", "source_url": "https://osf.io/" + args.node + "/",
              "listing_url": listing_url,
              "revision": "OSF file versions and SHA-256 recorded individually", "description": args.description,
              "license_note": "Public author-deposited materials; inspect project and file licenses before reuse",
              "status": "acquired" if files else "acquisition_failed", "files": files, "failed_files": failures,
              "extracted_path": "quarantine/references/" + args.identifier, "extracted_files": len(files),
              "listed_entries": len(listed), "duplicate_file_ids": duplicates,
              "skipped_files": skipped, "max_file_mib": args.max_file_mib,
              "path_conflicts": conflicts, "max_files": args.max_files, "workers": args.workers,
              "restore_command": "python3 scripts/restore_references.py --only " + args.identifier}
    destination = ROOT / "papers/software/records" / (args.identifier + ".json")
    destination.write_text(json.dumps(record, indent=2) + "\n")
    print(args.identifier, len(files), "files acquired;", len(failures), "failed")


if __name__ == "__main__":
    main()
