#!/usr/bin/env python3
"""Restore recorded reference archives without executing their contents."""

import argparse
import json
from pathlib import Path
import shutil

from acquire import acquire
from ingest_reference import ingest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="Restore one reference id")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    records = sorted((root / "papers/software/records").glob("*.json"))
    found = False
    for path in records:
        record = json.loads(path.read_text())
        if args.only and record["id"] != args.only:
            continue
        if record.get("status") != "acquired":
            continue
        found = True
        if record.get("kind") == "files":
            for item in record["files"]:
                metadata = acquire(item["source_url"], root / item["raw_path"], "text")
                if metadata["sha256"] != item["sha256"]:
                    raise SystemExit("upstream source changed: " + item["source_url"])
                target = root / item["extracted_path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / item["raw_path"], target)
                target.chmod(0o644)
            print(record["id"], len(record["files"]), "files restored")
            continue
        result = ingest(record["id"], record["archive_url"], record["source_url"], record["revision"],
                        record["license_note"], record["description"], record.get("strip_root", False),
                        expected_sha256=record["archive_sha256"])
        print(result["id"], result["extracted_files"], "files restored")
    if args.only and not found:
        raise SystemExit("no acquired reference with id " + args.only)


if __name__ == "__main__":
    main()
