# Generalizability-theory literature and reference acquisition

Requested 2026-10-02: launch a legion of frumentarii to exhaustively catalogue
and acquire generalizability-theory literature and reference implementations.

## Search lanes

1. Foundations, design algebra, universes, fixed/random facets.
2. Variance-component estimation: unbalanced/sparse data, REML, Bayesian methods.
3. Multivariate, composites, covariance, regressed scores, complex designs.
4. Uncertainty, resampling, standard errors, boundaries, simulation evidence.
5. D-study design, optimization, decision accuracy/consistency, conditional error.
6. Applied assessment and current AI/agent evaluation examples with reusable data.
7. Software-specific publications, manuals, source packages, and worked examples.
8. Coverage audit and bibliography expansion after the first synthesis.

Use primary publishers, authors, university repositories, package registries,
and the user's research library. Search both generalizability/generalisability,
G-theory/generalizability theory, historical report names, and author/title/DOI.
Expand bibliographies and citation chains. A finite search cannot prove absolute
exhaustiveness; report searched boundaries, unresolved leads, and access gaps.

## Ownership and output

Each agent owns one `papers/lanes/<lane>/` directory with catalogue, substantive
report, and search log. Root consolidates and deduplicates the final catalogue,
reading order, shopping list, and reference manifest. Full texts and source
archives are retained locally in ignored storage; public Git holds authored
notes and bibliographic metadata, not downloaded copyrighted full texts.

Acquisition statuses must distinguish acquired full text, verified metadata,
and blocked access. Record what was actually read. Full-text reading is a later
depth dimension as well as part of this survey; never label an abstract as read
full text. Invalid HTML/gate responses must not be counted as acquired PDFs.

## Acquisition mechanics

`scripts/acquire.py URL DESTINATION [--kind pdf|archive|html|text]` saves original
bytes plus URL, timestamp, byte count, and SHA-256 provenance. Files are reused
only if their URL and bytes match the recorded source. Keep downloadable source
archives intact. Extracted references are historical material; remove nested
Git metadata, unsafe archive paths, and filesystem detritus. Do not execute
reference implementations or adopt dependencies during acquisition.

Record source revisions, licensing observations, restoration commands, scope,
and candidate mathematical/test oracles for every reference implementation.
Put important inaccessible material in `papers/SHOPPING_LIST.md`.
