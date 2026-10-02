#!/usr/bin/env python3
"""Preserve a reference archive, extract safe regular files, and record restoration."""

import argparse
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import zipfile

from acquire import acquire

ROOT = Path(__file__).resolve().parents[1]
DETRITUS = {".git", ".DS_Store", "__MACOSX", "._.DS_Store", "Thumbs.db",
            ".Rhistory", ".RData", ".Rproj.user", "__pycache__", ".pytest_cache", ".gradle"}


def extract(archive, destination, strip_root=False):
    destination = Path(destination)
    if zipfile.is_zipfile(archive):
        container = zipfile.ZipFile(archive)
        members = [(item.filename, item.file_size, not item.is_dir() and (item.external_attr >> 16) & 0o170000 != 0o120000, item) for item in container.infolist()]
        read = container.open
    else:
        container = tarfile.open(archive)
        members = [(item.name, item.size, item.isfile(), item) for item in container.getmembers()]
        read = container.extractfile
    try:
        if len(members) > 30000 or sum(size for _, size, regular, _ in members if regular) > 250 * 1024 * 1024:
            raise ValueError("reference archive exceeds extraction bounds")
        roots = {PurePosixPath(name).parts[0] for name, _, regular, _ in members if regular and PurePosixPath(name).parts}
        if strip_root and len(roots) != 1:
            raise ValueError("archive does not have one top-level directory")
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True, exist_ok=True)
        count = 0
        excluded = []
        for name, _, regular, item in members:
            path = PurePosixPath(name)
            parts = path.parts
            if path.is_absolute() or ".." in parts or "\\" in name:
                excluded.append(name)
                continue
            if any(part in DETRITUS or part.startswith("._") or (part.startswith("gsLog_") and part.endswith(".log")) for part in parts) or not regular:
                if regular or not name.endswith("/"):
                    excluded.append(name)
                continue
            if strip_root:
                parts = parts[1:]
            if not parts:
                continue
            output = destination.joinpath(*parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            with read(item) as source, output.open("wb") as target:
                shutil.copyfileobj(source, target)
            output.chmod(0o644)
            count += 1
        return count, excluded
    finally:
        container.close()


def ingest(identifier, archive_url, source_url, revision, license_note, description, strip_root=False, expected_sha256=None):
    if not identifier or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in identifier):
        raise ValueError("reference id must contain only lowercase letters, digits, hyphens, underscores")
    archive_path = Path("quarantine/archives") / (identifier + (".tar.gz" if "/tar.gz/" in archive_url or ".tar.gz" in archive_url else ".zip"))
    metadata = acquire(archive_url, ROOT / archive_path, "archive")
    if expected_sha256 and metadata["sha256"] != expected_sha256:
        raise ValueError("upstream archive changed: " + identifier)
    extracted_path = Path("quarantine/references") / identifier
    count, excluded = extract(ROOT / archive_path, ROOT / extracted_path, strip_root)
    record = {"id": identifier, "source_url": source_url, "revision": revision,
              "archive_url": archive_url, "archive_path": str(archive_path),
              "archive_sha256": metadata["sha256"], "archive_bytes": metadata["bytes"],
              "extracted_path": str(extracted_path), "extracted_files": count,
              "excluded_paths": excluded, "strip_root": strip_root,
              "license_note": license_note, "description": description,
              "status": "acquired", "acquired_at": metadata["acquired_at"],
              "restore_command": "python3 scripts/restore_references.py --only " + identifier}
    records_dir = ROOT / "papers/software/records"
    records_dir.mkdir(parents=True, exist_ok=True)
    (records_dir / (identifier + ".json")).write_text(json.dumps(record, indent=2) + "\n")
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("identifier")
    parser.add_argument("archive_url")
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--revision", default="unversioned upstream distribution")
    parser.add_argument("--license-note", default="Not yet inspected; reference study only")
    parser.add_argument("--description", default="Generalizability-theory reference")
    parser.add_argument("--strip-root", action="store_true")
    args = parser.parse_args()
    record = ingest(args.identifier, args.archive_url, args.source_url, args.revision, args.license_note, args.description, args.strip_root)
    print(json.dumps({key: record[key] for key in ["id", "status", "archive_bytes", "extracted_files", "revision"]}))


if __name__ == "__main__":
    main()
