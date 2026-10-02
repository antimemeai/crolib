#!/usr/bin/env python3
"""Acquire a source without executing it; preserve bytes and provenance locally."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request


def acquire(url, destination, kind="pdf", timeout=45):
    destination = Path(destination)
    provenance = destination.with_name(destination.name + ".source.json")
    if destination.exists():
        if not provenance.exists():
            raise ValueError("existing destination lacks provenance; choose a new destination")
        result = json.loads(provenance.read_text())
        if result["source_url"] != url:
            raise ValueError("existing destination belongs to a different source")
        if hashlib.sha256(destination.read_bytes()).hexdigest() != result["sha256"]:
            raise ValueError("existing destination differs from its recorded source")
        return result
    request = urllib.request.Request(url, headers={"User-Agent": "crolib-literature-research/0.1", "Accept": "*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read(100 * 1024 * 1024 + 1)
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
    if len(data) > 100 * 1024 * 1024:
        raise ValueError("source exceeds the 100 MiB acquisition limit")
    if not data:
        raise ValueError("empty source response")
    if kind == "pdf" and b"%PDF-" not in data[:1024]:
        raise ValueError("response is not a PDF (possibly an access page)")
    if kind == "archive" and not (data.startswith(b"PK") or data.startswith(b"\x1f\x8b") or data[257:262] == b"ustar"):
        raise ValueError("response is not a supported ZIP/tar archive")
    if kind == "html" and b"<" not in data[:1024]:
        raise ValueError("response does not appear to be HTML")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part")
    temporary.write_bytes(data)
    temporary.replace(destination)
    result = {"source_url": url, "final_url": final_url, "local_path": str(destination),
              "kind": kind, "content_type": content_type, "bytes": len(data),
              "sha256": hashlib.sha256(data).hexdigest(),
              "acquired_at": datetime.now(timezone.utc).isoformat()}
    provenance.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("destination", type=Path)
    parser.add_argument("--kind", choices=["pdf", "archive", "html", "text"], default="pdf")
    parser.add_argument("--timeout", type=int, default=45)
    args = parser.parse_args()
    try:
        result = acquire(args.url, args.destination, args.kind, args.timeout)
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(json.dumps({"source_url": args.url, "status": "failed", "reason": str(error)}), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
