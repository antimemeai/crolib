#!/usr/bin/env python3
"""Restore inventoried literature responses; restore reference archives first for manuals."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from acquire import acquire


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="Restore one recorded local path")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    artifacts = json.loads((root / "papers/acquired-artifacts.json").read_text())
    software = json.loads((root / "papers/software/manifest.json").read_text())
    failures, count = [], 0
    for record in artifacts:
        if args.only and args.only != record["local_path"]:
            continue
        try:
            target = root / record["local_path"]
            if record.get("container_path"):
                bundle = next(item for item in software if item.get("archive_path") == record["container_path"])
                source = root / bundle["extracted_path"] / record["container_member"]
                if hashlib.sha256(source.read_bytes()).hexdigest() != record["sha256"]:
                    raise ValueError("manual member checksum differs")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                target.with_name(target.name + ".source.json").write_text(json.dumps(record, indent=2) + "\n")
            else:
                result = acquire(record["source_url"], target, record["kind"])
                if result["sha256"] != record["sha256"]:
                    raise ValueError("upstream literature response changed")
            count += 1
        except Exception as error:
            failures.append({"local_path": record["local_path"], "reason": str(error)})
    if args.only and not count and not failures:
        raise SystemExit("no artifact with local path " + args.only)
    print(json.dumps({"restored": count, "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
