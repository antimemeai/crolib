#!/usr/bin/env python3
"""Publish built artifacts using a local credential, never a command argument."""

import argparse
import os
from pathlib import Path
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credential-file", type=Path, default=Path(__file__).resolve().parents[2] / ".env")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    token = os.environ.get("UV_PUBLISH_TOKEN")
    if not token and args.credential_file.is_file():
        for line in args.credential_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            name, separator, value = line.partition("=")
            if separator and name.strip().upper() in {"PYPI", "PYPI_TOKEN", "PYPI_API_TOKEN", "UV_PUBLISH_TOKEN", "TWINE_PASSWORD"}:
                parts = shlex.split(value, comments=True)
                if len(parts) == 1:
                    token = parts[0]
                    break
    if not token or not token.startswith("pypi-"):
        raise SystemExit("A PyPI API token is required in UV_PUBLISH_TOKEN or the local credential file.")
    environment = os.environ.copy()
    environment["UV_PUBLISH_TOKEN"] = token
    command = ["uv", "publish", "--trusted-publishing", "never"]
    if args.dry_run:
        command.append("--dry-run")
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(subprocess.run(command, cwd=root, env=environment).returncode)


if __name__ == "__main__":
    main()
