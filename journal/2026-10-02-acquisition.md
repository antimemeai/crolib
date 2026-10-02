# 2026-10-02 — Generalizability-theory frumentarii

The operator requested exhaustive literature and reference-implementation
catalogue/acquisition. Started three independent first-wave lanes: foundations,
estimation, and multivariate theory. Subsequent waves cover uncertainty,
D-study/decision design, applied examples, software, and a coverage audit.
Root owns acquisition utilities, software ingestion, consolidation, and review.

The plan lives in `papers/ACQUISITION_PLAN.md`. Downloads remain ignored;
tracked bibliographic records, lane reports, and shopping lists will retain
provenance and exact distinctions between acquisition and reading depth.
This work adopts no library dependencies and does not change the released API.

The first wave produced foundation, estimation and multivariate reports. The
second covered intervals/resampling, D-study/classification design and applied
measurement. The final work inspects reference software and resolves the entire
328-entry CASMA bibliography against primary registry metadata, preserving
ambiguous leads separately.

Added standard-library acquisition, safe extraction, OSF ingestion, bibliography
import, consolidation and restoration utilities. Sources remain intact with
SHA-256 provenance; extracted archives exclude nested Git metadata, symlinks,
unsafe paths and filesystem detritus. Original archives and downloaded full
texts remain ignored. Tracked source records distinguish legacy binaries/manuals
from actual source implementations. All 38 initial reference packages restored
successfully; later imaging/EEG packages are included in the final check.

Selected reading exposed important semantic and oracle hazards: finite sampling
differs from fixing a facet, one-level facets can confound required components,
moment clipping differs from constrained fitting, multivariate weights need
score metrics, coefficient terminology sometimes disagrees with formulas, and
a published integer-allocation example apparently exchanges facet counts. Lane
reports preserve the actual evidence and correction/version qualifications.

The private stacks library was attempted through status, catalogue and BM25
search tools, but calls returned no results within explicit time bounds. This
corpus is an access gap, not a searched collection with zero holdings. Public
publisher, author, institutional, ERIC, registry, GitHub and OSF searches remain
documented. Core books and inaccessible originals are in the shopping list.

Final consolidation: 526 lane records deduplicated into 459 catalogued works;
176 acquired works/documents, 210 metadata-only records and 73 blocked local
full texts. The retained acquisition inventory has 168 responses, including
133 PDFs, 26 HTML responses and 9 text/XML responses. These response counts
include supplements/discovery material and differ from bibliographic works.
All eight lane reports, the synthesis, reading route, shopping list and
19-family static software/fixture matrix are retained.

All 328 historical leads received primary-registry queries: 177 strong matches,
37 explicitly reviewed matches, 107 unresolved entries, 4 review candidates and
3 ambiguous registrations. Registry existence is metadata evidence, not a
mathematical endorsement or a full-text reading claim. The identity audit split
two precursor reports from their unacquired final journal articles, corrected
deposited author names and clarified the jGENOVA source snapshot year.

Acquired 47 reference packages, preserving pinned archives and individual OSF
file versions. Stable OSF name sorting fixed a pagination issue that omitted
five connectivity tables; all 121 ICED CSVs are now acquired. Serial retries
resolved transient429 failures in the regression/dyadic source bundles; final
acquired packages have zero file download failures. Four large generated
posterior/factor-score output dumps (~2.5GB) were explicitly omitted from the
many-reliabilities package; its model code, input data and supplements are local
and omissions are inventoried.

Validation: all 47 packages restored, all 168 inventoried literature responses
restored/reused with matching hashes, acquired-path/schema and original-byte
audits passed, ZIP/tar traversal/symlink/metadata exclusion cases passed, helper
compilation passed and Git whitespace checks passed. Released Rust/Python
numerical code remains untouched; release tests were not rerun for this research
corpus change. Public Git contains authored notes, metadata and utilities;
downloaded full texts/source archives remain ignored.
