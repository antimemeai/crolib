# crolib

Read [BLACKBIRD.md](BLACKBIRD.md) before working here. Workspace library policy
also applies: own the machinery; discuss proposed dependencies before adoption.

This repository develops generalizability theory and measurement design for
Rust and Python. The first release projects relative and absolute reliability
from supplied variance components for an all-random, crossed person × item ×
rater design. It does not fit components from observations.

Keep research in `papers/`, source references in ignored `quarantine/`, private
working material in ignored `context/`, decisions in `journal/`, and actionable
work in `issues/`. Ignore acquired PDFs and preserve source archives intact.

Run `scripts/check.sh` before a release. Public documentation must distinguish
implemented behavior from future work. Never put registry credentials in files
tracked by Git, command arguments, logs, or prompts.
