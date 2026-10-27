#!/usr/bin/env bash
# Run every verify/sage check: .sage scripts through Sage (preparsed, for
# symbolic work) and .py scripts through the Sage environment's python.
# Generator scripts rewrite committed oracles; the run fails if any script
# fails or a regenerated oracle differs from HEAD. Local and neuroses only;
# CI runs the committed oracles through cargo test and unittest.
set -euo pipefail
cd "$(dirname "$0")/.."
export CROLIB_ROOT="$PWD"
SAGE="${SAGE:-/opt/homebrew/anaconda3/envs/sage/bin/sage}"
SAGE_PYTHON="${SAGE_PYTHON:-$(dirname "$SAGE")/python}"
[ -x "$SAGE" ] || { echo "sage not found at $SAGE; set SAGE (see verify/sage/environment.yml)" >&2; exit 1; }
# Libraries loaded by other scripts, not checks themselves.
LIBRARIES="verify/sage/balanced.sage"
for script in verify/sage/*.sage verify/sage/*.py; do
    [ -e "$script" ] || continue
    case " $LIBRARIES " in *" $script "*) continue ;; esac
    echo "== $script"
    case "$script" in
        *.sage) "$SAGE" "$script" ;;
        *.py) "$SAGE_PYTHON" -I "$script" ;;
    esac
done
oracles=(':(glob)tests/oracles/**' 'python/tests/projection_oracle.py' 'python/tests/finite_projection_oracle.py')
if [ -n "$(git status --porcelain --untracked-files=all -- "${oracles[@]}")" ]; then
    git status --short --untracked-files=all -- "${oracles[@]}" >&2
    echo "generated oracles differ from HEAD; review and commit" >&2
    exit 1
fi
