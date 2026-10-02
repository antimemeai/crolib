#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Selecting all Rust executables together avoids mixing a Homebrew Cargo
# subcommand/compiler with a rustup toolchain.
if command -v rustup >/dev/null 2>&1; then
    crolib_compiler="$(rustup which --toolchain "${CROLIB_RUST_TOOLCHAIN:-1.95.0}" rustc)"
    crolib_toolchain_bin="$(dirname "$crolib_compiler")"
    export PATH="$crolib_toolchain_bin:$PATH"
    export RUSTC="$crolib_compiler"
    export RUSTDOC="$crolib_toolchain_bin/rustdoc"
fi

cargo fmt -- --check
cargo clippy --all-targets -- -D warnings
cargo test
"${CROLIB_PYTHON:-python3}" -c 'import sys; assert sys.version_info >= (3, 10), "crolib needs Python 3.10+; set CROLIB_PYTHON"'
PYTHONPATH=python "${CROLIB_PYTHON:-python3}" -m unittest discover -s python/tests -v
