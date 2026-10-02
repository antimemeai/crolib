#!/usr/bin/env python3
"""Publish the crate using local credentials and a consistent Rust toolchain."""

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
    environment = os.environ.copy()
    if args.credential_file.is_file():
        for line in args.credential_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            name, separator, value = line.partition("=")
            if separator and name.strip().upper() in {"CRATES", "CRATES_TOKEN", "CARGO_REGISTRY_TOKEN"}:
                parts = shlex.split(value, comments=True)
                if len(parts) == 1:
                    environment["CARGO_REGISTRY_TOKEN"] = parts[0]
                    break
    toolchain = environment.get("CROLIB_RUST_TOOLCHAIN", "1.95.0")
    compiler = Path(subprocess.check_output(["rustup", "which", "--toolchain", toolchain, "rustc"], text=True).strip())
    environment["PATH"] = str(compiler.parent) + os.pathsep + environment.get("PATH", "")
    environment["RUSTC"] = str(compiler)
    environment["RUSTDOC"] = str(compiler.parent / "rustdoc")
    command = [str(compiler.parent / "cargo"), "publish"]
    if args.dry_run:
        command.append("--dry-run")
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(subprocess.run(command, cwd=root, env=environment).returncode)


if __name__ == "__main__":
    main()
