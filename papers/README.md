# Generalizability-theory research corpus

Frumentarii acquisition pass, 2026-10-02. Start with the
[research synthesis](SYNTHESIS.md), browse the [catalogue](CATALOGUE.md), and
consult the [shopping list](SHOPPING_LIST.md) for unavailable originals.
Exact counts are generated in [summary.json](summary.json).

| Resource | Contents |
| --- | --- |
| [catalogue.json](catalogue.json) | Deduplicated verified works, statuses, paths, sources, lane aliases and reading evidence |
| [bibliography-leads.json](bibliography-leads.json) | All 328 entries imported from Brennan/Liao's sixty-year bibliography as discovery leads |
| [bibliography-coverage.json](bibliography-coverage.json) | Mechanical candidate matches and unresolved leads; editions still need confirmation |
| [acquired-artifacts.json](acquired-artifacts.json) | Original response URLs, SHA-256, acquisition dates and local paths, including supplements |
| [software/MANIFEST.md](software/MANIFEST.md) | Reference packages, revisions and restoration commands |
| [software/manifest.json](software/manifest.json) | Machine-readable archive and individual-file provenance |

## Research lanes

Each lane retains its own `catalogue.json` and `search-log.json` beside the report.

- [Foundations, universes, symmetry and design algebra](lanes/foundations/report.md)
- [Variance/covariance estimation and irregular observations](lanes/estimation/report.md)
- [Multivariate scores, profiles and model bridges](lanes/multivariate/report.md)
- [Uncertainty, resampling and boundaries](lanes/uncertainty/report.md)
- [D-studies, allocation and classification decisions](lanes/decisions/report.md)
- [Applied measurement and current evaluation research](lanes/applications/report.md)
- [Software methods, manuals, fixtures and capabilities](lanes/software/report.md)
- [Bibliography expansion and coverage audit](lanes/coverage/report.md)

## Acquisition and restoration

Full texts reside locally in ignored `papers/downloads/`. Original reference
archives and loose sources remain intact under ignored `quarantine/archives/`;
extracted copies reside in `quarantine/references/`. Public Git contains authored
reports, bibliographic metadata and restoration records. Extraction removes
nested Git metadata and filesystem detritus; archived instructions are historical.

From the repository root:

```sh
python3 scripts/restore_references.py
python3 scripts/restore_papers.py
python3 scripts/catalogue.py
```

Use `--only ID` for a reference package or `--only LOCAL_PATH` for a literature
artifact. Restore reference archives before their extracted manuals. Changed
checksums raise errors and require source reconciliation; upstream access can
change. Acquisition helpers use Python's standard library. Importing the
historical bibliography also uses the system `pdftotext` utility.

## Evidence boundaries

`acquired` records indicate a local full text/document with checked identity.
They do not assert complete reading or numerical validation. Individual records
distinguish selected mathematical reading, abstract inspection and metadata.
Published papers, preprints, manuals and source documentation remain identified.
Artifact counts also include supplements and discovery responses; they are not
counts of independently read papers. Downloaded implementations have not been
executed or adopted as dependencies.

A finite search cannot establish absolute exhaustiveness. The coverage audit
records searched branches, unresolved bibliography leads, inaccessible books,
request-only data and newer work beyond the 2020 bibliography. See the
[acquisition plan](ACQUISITION_PLAN.md) for ownership and search boundaries.
