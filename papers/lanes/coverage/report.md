# Coverage audit: bibliography resolution and conceptual gaps

Audit completed 2026-10-02. This lane completes a **finite audit of all 328 entries** extracted from Brennan and Liao's *Generalizability Theory References: The First Sixty Years* (CASMA report53). It also extends conceptual coverage through primary 2021–2026 papers. It does not establish that every publication in the field has been found or acquired.

The lane catalogue contains **233 distinct works: 22 acquired, 6 access blocked, 205 metadata only**. The 22 acquired artifacts comprise 15 PDFs and seven complete article HTML files. No reference implementation was executed and no dependency was adopted. Other lanes' acquisitions are cited where applicable; class-means1975 and Allal1986 overlap foundations and should be deduplicated in the shared index. Bibliographic records and reports are public; complete PDFs/article HTML, publisher/registry raw responses and private working material remain ignored.

## Finite bibliography audit and its limits

[lead-resolution.json](lead-resolution.json) preserves every original citation, its mechanical shared-catalogue candidates, exact Crossref query URL, three primary registry candidates, title similarity, first-author check, year comparison, outcome and explicit review notes. The original root-generated coverage files were left unchanged. [resolve-leads.py](resolve-leads.py), [review-leads.py](review-leads.py) and [build-catalogue.py](build-catalogue.py) reproduce the registry audit, explicit bibliographic choices and consolidatable catalogue.

| Stage | Entries | Meaning |
| --- | ---: | --- |
| Earlier mechanical shared-catalogue candidates |69|Title/year/first-author discovery only;259 entries had no candidate. |
| Initial strong Crossref matches |177|Title similarity≥.94, first-author agreement and exact registry publication year; no fulltext claim. |
| Initial ambiguous matches |18|Multiple DOI/edition/version candidates; no automatic selection. |
| Initial near matches |20|Close titles/authors with date or typography differences. |
| Initial unresolved registry entries |113|None of the three returned candidates met the strict rule. |
| Explicitly reviewed registry matches |37|Publisher/JSTOR registrations, journal/report/dataset distinctions, title markup, or documented online/print dates adjudicated. |
| Final strong or reviewed matches |214|210 distinct selected DOIs;168 entries previously lacking any mechanical candidate now resolve. |
| Final candidates requiring review |4|NCES chapter versus journal article, editions/dates, and one unresolved online/print date. |
| Final ambiguous registrations |3|Dual publisher registrations retained without choosing one. |
| Final unresolved registry entries |107|Includes books, historical ACT/CASMA reports, dissertations, conference papers, incomplete citations and missed registry records. |

The verified selected records are included as `coverage-registry-*` metadata-only entries in [catalogue.json](catalogue.json), except where merged into a stronger local fulltext record. Original lead IDs, citation and primary registry query URL remain available. **Verified means the primary registry describes that bibliographic work, not that its findings or formulas have been checked.** A registry existence match does not resolve every edition or access issue. Metadata-only records receive no automatic “fulltext read” upgrade.

The lookup was deliberately finite: one full-citation Crossref query per lead, three returned candidates, two workers and a1.2second request interval; cached raw responses are under ignored `context/acquisition/coverage/`. All328 initial queries returned results. A null bibliography year exposed an assumption in the resolver; missing-year comparisons now remain review-only, and the pass resumed from cache. Supplemental DOI-detail requests for date adjudication hit six429responses. Those failures are retained as acquisition/search limitations; unconfirmed date mappings remain unverified unless another primary source independently resolved them.

Important date/version corrections are explicit rather than silently editing the source bibliography:

- Bachman/Lynch/Mason's speaking-test study is1995 in primary publisher/registry metadata despite the1994 bibliography date.
- Brennan's1996 NCES performance-assessment chapter is acquired inside ED399300; a same-title1995 Brennan/Johnson journal article is a distinct publication.
- Efron/Tibshirani's original bootstrap paper, its rejoinder and comments are different works. The original exact title was selected.
- Same-title JEM versus ETS-report records and journal versus PsycEXTRA dataset registrations remain distinct versions. Publisher/JSTOR duplicate registrations have explicit alternative DOIs where the title, authors, year, type and container agree.
- Online-first2014/2016/2017 dates do not replace later2015/2018 issue dates when those are verified. Conversely,1993 ACT93-10 is a precursor to Brennan's1995 group-mean article, and the1975 class-mean conference report is a precursor to the1977 journal article.
- Stull's mood paper is2022; an initial discovery filename says2023. Stenner/Rohlf's ERIC report has publication date[79], not its later accession/discovery year. The catalogue records these corrections.

Registry nonresolution is not nonexistence. CASMA reports and source manuals with no DOI already acquired by other lanes remain authoritative. Incomplete entries such as “Cronbach(1947)” or “Block and Norman(2015)” cannot be assigned a specific work solely because a plausible author/year record appears. `in press` entries and old conference presentations may now have published successors, but these require explicit identity review.

## Missing conceptual branches now represented

### State, trait and reliability of change

[Vispoel/Xu/Schneider2022](https://doi.org/10.1037/met0000290) connects latent state-trait theory with GT within SEM. The primary university abstract verifies that common GT designs can be expressed as special LST cases, while effect labels, targets, indices and fit interpretation differ. Main PDF access is blocked; instructional supplement DOI10.1037/met0000290.supp is a concrete acquisition target.

[Child/Medvedev2024](https://doi.org/10.1007/s12144-023-05072-4) is acquired and provides a three-occasion resilience application. [Cranford et al.2006](https://doi.org/10.1177/0146167206287721) supplies the deeper methods foundation: stable person differences, reliability on a fixed versus random day, averages over a fixed diary period and reliability of within-person change are different coefficients. A stable person×item effect belongs in a fixed-item true-score target; treating every interaction as error regardless of the target is wrong.

A usable numerical oracle comes from Cranford's Bar Exam Study anxious-mood components, three items: person×day variance.469 and residual variance.292 give change reliability `.469 / (.469 + .292/3) = .8281341966…`, which agrees with the rounded.83 in Table3. Table3's near.99 reliability of averages across fixed diary days does **not** imply near.99 reliability of daily change. The table's rounded component values limit the expected numerical tolerance.

### EMA, temporal sampling and nested couples

[Shiyko/Ram2011](https://doi.org/10.1080/00273171.2011.625310) uses multilevel variance decompositions to study process speed under sparse, irregular EMA. This is an adjacent temporal-design extension, not a standard exchangeable-rater D-study. [Stull et al.2022](https://doi.org/10.1037/pas0001160) separates person, person×day and person×moment sources and combines GT with multilevel CFA. Within-person and between-person covariance structures can differ.

[Schönbrodt et al.2022](https://doi.org/10.3758/s13428-021-01701-7) adds moments, days, persons nested in couples, and items; it derives between-couple, between-person, within-person/between-day and within-person/between-moment reliabilities. Its fuller model enumerates cross-level interactions before simplifying; a casual nested random-intercept model is not automatically equivalent. [DiGiovanni/Cornelius/Bolger2022online/2023issue](https://doi.org/10.1177/19485506221116989) extends this to within-couple changes with fixed day/item targets.

[Castro-Alvarez et al.2025 WARN-D](https://doi.org/10.1037/pas0001410), acquired, compares six approaches: GT, multilevel modeling, multilevel CFA, pooled time-series factor analysis, two-dimensional reliability modeling and measurement-error structural-time-series modeling. The reliability target may be global, between-person, within-person or person-specific; temporal correlations require a model, not merely larger counts. Root acquired the companion Zenodo22914689 archive. Its migrated September2026 deposit declares an original August2024 date and contains model code, preregistration, supplement and derived outputs rather than complete response data; paper year is2025.

The broader [many-reliabilities review](https://doi.org/10.1037/met0000778) is2025online/2026issue. Its main PDF remains blocked. **Published erratum [10.1037/met0000811](https://pubmed.ncbi.nlm.nih.gov/42113119/) corrects 2RDM computations, Figure3, supplementary results and an unrelated impact statement.** PubMed assigns April2026 publication; a PsycInfo2027record identifier in the original abstract is not an event date. Require corrected supplement/version before using this paper's numerical results as an oracle.

### Nonadditivity and nonstationarity

[Zhang/Lin2016](https://doi.org/10.1177/0146621616651603) and [Lin/Zhang2018](https://doi.org/10.1111/jedm.12164), both acquired, address one-facet mixed/nonadditive models, Tukey's test and bias in subject-component estimates. Their specific distinction between removable and genuine interaction cannot be reduced to “GT cannot contain interactions”: ordinary crossed GT explicitly models interaction variance. Implementing their correction requires the paper's exact fixed/random interpretation and additivity-index estimator. The2018 operational example changes a negative estimated subject component into a positive one; blindly clipping the original estimate would represent another estimator.

[Casabianca/Lockwood/McCaffrey2015](https://doi.org/10.1177/0013164414539163), acquired, augments GT with smooth temporal effects to distinguish instruction trends from rater drift. A crossed design with exchangeable stationary facet effects omits this mechanism. Treating known measurement drift as a random interchangeable-rater population risks interpreting systematic temporal bias as ordinary repeatability error.

### Matrix/incidence sampling and linking

[Boodoo1982](https://doi.org/10.3102/10769986007004311) and [Sirotnik/Wellington1977](https://doi.org/10.1111/j.1745-3984.1977.tb00050.x) are verified historical priorities but publisher PDFs return403. Their incidence/GSM estimators need the observation assignment matrix and, for uncertainty, the appropriate sampling design. Counts alone cannot define a planned incomplete design. Gao/Brennan/Shavelson's1994 matrix-sampled science presentation is present in the CASMA bibliography but no original public fulltext was verified this pass.

[Glas/Jorgensen/ten Hove2024](https://doi.org/10.1007/s11336-024-09967-4), acquired, supplies a modern bridge: ordinal IRT maps responses to a latent scale, GT decomposes latent measurements, and regression propagates this measurement structure rather than using noisy point scores. The paper includes linked rater assignments, conditional/global precision, scale identification and an explicit requirement for item-model fit and invariance. Its familiar-looking relative/absolute ratios use **latent-scale posterior variance components**, so they cannot be silently substituted into an observed-score ANOVA contract. Public OpenBUGS/JAGS/R scripts and data are linked at OSFknzw9; root is acquiring source material separately.

### Weights, multiple standards and composite interpretation

[Wu/Tzou2015](https://doi.org/10.1177/0146621615577972), acquired, uses covariance components across basic/proficient/advanced standards and fixed content strata under modified Angoff procedures. Multiple standard-setting rounds and nonrandom-parallel panel groups require explicit conditioning. D-study panel sizes/test lengths address precision of the estimated cut scores; they do not estimate examinee classification accuracy directly. The full NCES1996 report, acquired, preserves Brennan's GT chapter alongside validity, comparability and multistage standard-setting chapters, rather than treating those questions as a single coefficient.

[Yan/Li2025](https://doi.org/10.1038/s41598-025-08550-w), acquired, is a nested unbalanced multivariate teacher-evaluation example, with nominal/effective/estimation weights and individual conditional errors. Its preferred reliability weights are sample/model-specific. Maximizing reliability alone is not construct validation, fairness or a guarantee that future populations should use those weights. **Covariance-table upper triangles contain correlations and lower triangles contain covariances**; parse the stated representation rather than importing a visually symmetric array.

Optimization, budget constraints, relative versus absolute error, and decision consistency/accuracy are treated in the completed [decisions lane](../decisions/report.md). Nominal weights, weighted/regressed scores, differences, profiles and multivariate design constraints are treated in [multivariate](../multivariate/report.md). The newly resolved historical records add differential weighting, group-mean and sampling references without claiming their original methods have been read.

### Symmetry, group targets and interdependence

[Allal1986](https://eric.ed.gov/?id=ED270486), acquired, operationalizes the principle of symmetry: the object of differentiation can be a person, item, standard, class or other factor. The1975 class-mean report derives multiple coefficients under different universes. [Brennan's ACT93-10](https://eric.ed.gov/?id=ED368773), acquired, shows that aggregating people does not necessarily increase reliability when the universe also changes; the person count in `(p:g)×i` is persons **per group**, not the total sample. The1995 primary journal metadata corrects the bibliography's erroneous volume14 to32(4).

[ten Hove/Jorgensen/van der Ark2025](https://doi.org/10.1080/00273171.2024.2444940), acquired, extends the social-relations model with external-rater effects. Actor, partner, relationship and integrated scores are separate targets, with reciprocal dyadic covariances. Their Table2 divides actor-rater, partner-rater and relationship-residual errors by rater count in the corresponding coefficient. A search-engine table rendering substituted epsilon into several denominators; the actual acquired PDF and Equation19 disagree with that extraction, so the PDF is the reference. OSF9az5x supplies reference simulation/code and OSFb4nvf supplies social-mimicry data. Root received these sources.

### Measurement invariance and contemporary forward citations

[Jentsch et al.2022](https://doi.org/10.18261/9788215045054-2021-04) explicitly combines invariance and GT for classroom observations; publisher connections failed TLS, while primary metadata and an author-uploaded CC-BY copy are discoverable. [Senden et al.2025](https://doi.org/10.3389/feduc.2025.1483092), acquired, is a forward-citation application of context-sensitive adaptation in Norwegian primary education.

[Finch/French/Immekus2026](https://doi.org/10.3390/psycholint8010019), acquired, compares reliability coefficients across groups using multiple-group SEM. Equality of reliability ratios is not scalar or metric measurement invariance. Text describes200/350/500 **total** sample sizes while Table1 labels them “per group”; simulation reproduction must resolve this discrepancy before treating the condition table as an oracle.

[Sharma2026 MRBenchV2](https://proceedings.mlr.press/v339/sharma26a.html), acquired from the official PMLR repository, combines GT, IRT, CFA and measurement-invariance checks for an LLM tutoring benchmark. A repeatable assessment can still differ in measurement meaning across model groups. Its workshop scope and specific benchmark population limit transport claims. Rast/Clayson2026 heteroscedastic GT and associated EEG code/data were acquired by applications; see that lane rather than duplicating files here. Recent binary/ordinal/SEM/IRT branches are also represented in multivariate and uncertainty.

## Library design implications and candidate oracles

Future owned machinery should encode: object(s) of differentiation; fixed/random facets and their population interpretation; nesting/crossing/incidence assignments; observed versus latent scale; replication and aggregation rules; linear contrast/composite weights; covariance representation; temporal stationarity/correlation assumptions; reliability target and decision loss. These contracts are prerequisites for fitting or optimizing the model. A formula for one contract cannot silently serve another because its denominator happens to be a variance sum.

Useful independent checks include the rounded Cranford change-reliability example above; covariance-matrix quadratic forms for composite/difference scores; recovery of simple crossed/nested cases from richer models; person-versus-group coefficients under fixed versus random sampling; distinct actor/partner/relationship targets under reciprocity; and the corrected-versus-uncorrected nonadditivity example. Numerical published outputs are candidate oracles, subject to reading the exact design, estimator and rounding convention. No code or supplement was run in this lane, so statistical replication remains future design work.

The existing release's all-random crossed person×item×rater projection is much narrower than these branches. This research catalogue does not indicate that component fitting, SEM/IRT, matrix-sampling inference, temporal reliability, classification decisions, multivariate scores or design optimization have been implemented.

## Remaining acquisitions and search boundary

Priority blocked originals: Vispoel/Xu/Schneider LST bridge and instructional supplement; Boodoo incidence estimates; Sirotnik/Wellington integrated matrix theory; Jentsch invariance chapter; corrected Castro-Alvarez many-reliabilities review and supplements; Ji2026 nations-nested MGT. Historical ACT technical bulletins, unpublished presentations/dissertations, the1960s/1972 foundational books, group/profile/equating originals and weighting papers remain valuable operator-library targets where other lanes lack them. The bulk metadata inventory should not displace those method-rich originals in acquisition priority.

Forward searches combined `generalizability theory`/`generalisability theory` with state/trait, EMA/diary, nonadditivity, linking, matrix/incidence sampling, weights, multistage standards, invariance, symmetry, budget and explicit2021–2026 years. Primary publisher pages, university author repositories, PMC, ERIC, PMLR and Crossref were used to verify selected works. Search-engine lead discovery is not equivalent to a bibliographic database's complete citation graph. The finite bibliography lookups and selected primary forward-citation chains are complete as logged; field-wide saturation is **not** established, particularly for non-English books, theses, workshop proceedings, newly indexed2026papers and materials outside the author bibliography.

Private library access was attempted by root: `library_status` exceeded30seconds; `stacks.list_papers(query='generalizability',limit=100)` and `stacks.search_chunks_bm25(query='"generalizability theory" OR "generalisability theory"',limit=50)` were attempted in parallel with explicit15second bounds and neither returned. This corpus was **unavailable**, not searched with zero hits. Subscription/paywall access was not bypassed. Ordinary publisher/repository failures and public alternative-copy leads are recorded for operator acquisition.
