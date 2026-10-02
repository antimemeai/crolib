# Multivariate and advanced generalizability theory reconnaissance

2026-10-02. Lane owner: multivariate frumentarius. The [catalogue](catalogue.json)
contains 39 verified sources. Twenty-eight have acquired full text, including one
shared foundations artifact; 27 artifacts were acquired directly in this lane
(24 PDFs and 3 complete article HTML files). Seven identified full-text attempts
failed and four sources remain metadata-only. Acquired artifacts have original
bytes and provenance sidecars. Text extractions are reading aids, not replacements
for PDFs. Acquisition is distinct from reading: selected abstracts, mathematical
sections, worked examples, discussions and reference lists were inspected, not
every line of every paper. [Search log](search-log.json) records discovery and
acquisition accounting.

## What this branch requires of crolib

Multivariate GT is a coherent extension of the theory, not a collection of
independent univariate reliabilities. Each effect can contribute a covariance
matrix across fixed categories; the design determines which off-diagonal terms
exist and are estimable. An item sampled independently within each domain has a
different covariance structure from one essay rated on several traits. In the
latter case, correlated errors matter. The acquired [Jiang et al. (2020)](https://doi.org/10.3758/s13428-020-01399-z)
tutorial illustrates both patterns using glmmTMB, and is useful for deriving
reference cases. Its code should be studied, not selected as a dependency.

For a specified composite with weight vector w, universe-score and error
variances are quadratic forms in their corresponding component matrices.
Component estimation, permissible D-study changes, score aggregation and weight
selection therefore need explicit design semantics. This is an architectural
inference from the acquired sources, not an implementation plan.

The [Brennan, Kim and Lee (2022)](https://doi.org/10.1177/00131644211049746)
extended MGT article exposes a further requirement: different fixed categories
can have different random-effects designs. Their mixed-format and testlet
examples cannot faithfully be collapsed into one common design. They also show
that an operational single rating per response leaves rater effects confounded;
special additional ratings are needed to study them. Future APIs must represent
observed design, intended universe and estimable components separately. This
paper only develops the simpler covariance case with one linked facet; its
references direct multiple-linked-facet work to Brennan (2001), pp. 286–293.

## Coverage map and reading route

| Branch | Acquired or verified anchors | Why read it |
| --- | --- | --- |
| Matrix-valued G/D studies | Brennan (2001), chapters 9–12; Jiang et al. (2020); Jiang & Skorupski (2018) | Core covariance decomposition, projection, regression and estimation alternatives |
| Fixed/stratified facets | Rajaratnam, Cronbach & Gleser (1965); acquired Jarjoura & Brennan (1982); Keller et al. (2010) | Fixed content categories change the intended parallel-form universe |
| Weighted composites | Acquired CASMA #50, #42, #44, #46; Joe & Woodward (1976); Marcoulides (1994) | Score metrics, utility, intervals and weight/allocation optimization |
| Subscores and profiles | Acquired Jiang & Raymond (2018), Raymond & Jiang (2020), CASMA #33 | Profile consistency, mean differences, conditional precision and added value |
| Regressed scores | Brennan (2001), chapter 12; acquired CASMA Technical Note #5 | Universe-score prediction and interpretation limits |
| Difference/change scores | Acquired CASMA #59 (2025); Grochowalski, Liu & Siedlecki (2016) | Correlated pre/post errors and nested group structures |
| Heterogeneous designs | Acquired extended MGT (2022), Moses & Kim (2015), CASMA #29 | Mixed formats, testlets, ratings versus raters, separate component topologies |
| Unbalanced multivariate estimation | Brennan (2001), chapter 11; acquired Jiang et al. (2020), Jiang & Skorupski (2018) | Unequal component designs, missing cells and inferential alternatives |
| SEM/congeneric/bifactor bridge | Acquired Jorgensen (2021); Vispoel et al. (2023, 2024, 2025) | Mean/threshold structure, scale coarseness and less restrictive factor relations |
| IRT and categorical outcomes | Acquired Briggs & Wilson (2007), Choi & Wilson (2018), Jiang et al. (2024); Ark (2015); Vispoel et al. (2019) | Expected-response GT, mixed-outcome links and latent-response metrics |
| Randomly parallel testing | Lee, Kim & Shin (2026), openly readable publisher text; PDF acquisition blocked | Item-within-person and fixed-template domains; conditional SEMs |
| Real multivariate examples | Acquired CASMA #4/#25/#29/#34; Nußbaum (1984) | Bar exams, reading, portfolios and multi-criterion art ratings |

Start with the balanced matrix examples and the 2022 heterogeneous-design paper,
then CASMA #50 for score conventions. Follow with the unbalanced chapter and
estimation tutorials. Study profile/difference outputs after the covariance
semantics are understood. Treat SEM, IRT and ordinal models as explicit model
extensions with their own targets and assumptions.

## Findings that should prevent incorrect machinery

**Weights carry a metric.** [CASMA #50](https://education.uiowa.edu/sites/education.uiowa.edu/files/2026-04/casma-research-report-50-archived.pdf)
distinguishes four scenarios involving mean versus total subtest scores and
different composite ranges. A policy that MC and FR each contribute half the
possible composite points does not automatically mean applying numerical weights
0.5 and 0.5 to their raw scores. Its example converts variance and covariance
components between metrics and discusses effective weights. Any future weight
API should identify the score metric and intended range contribution.

**Profile reliability and subscore usefulness are different outputs.**
[Jiang & Raymond (2018)](https://doi.org/10.1177/0146621618758698)
study a profile index sensitive to differences in subtest means. Correlation-based
value-added measures answer another question. Their simulation and certification
example provide useful comparisons, and caution that a population profile index
cannot decide whether a particular person's profile is useful.
[Raymond & Jiang (2020)](https://doi.org/10.1177/0013164419846936)
extend this work to individuals/subgroups and conditional error. Do not expose
one number as though these targets coincide.

**Nested difference scores need correlated error and an object of measurement.**
[CASMA #59](https://education.uiowa.edu/sites/education.uiowa.edu/files/2026-04/casma-research-report-59-archived.pdf)
uses persons within groups within sites, with pre/post tests as a multivariate
facet. Different D-studies target persons, groups or sites. Omitting lower
levels inflated site-level reliability in its data. Difference scores cannot be
computed correctly from two marginal reliabilities alone; shared universe and
error covariance are needed. The report's design diagrams and component tables
are strong future worked examples.

**Absolute error in SEM depends on means/thresholds.**
[Jorgensen (2021)](https://doi.org/10.3390/psych3020011)
shows how one SEM can capture the needed information through constrained mean
and threshold structures. A covariance-only translation misses this part of
dependability. It also describes limits for planned missing multirater data.
Its uncertainty methods and illustrative R syntax are reference material.

**Congeneric and bifactor models alter the model assumptions.**
[Vispoel, Lee & Chen (2024)](https://doi.org/10.3390/math12081164)
compare GT-style essential tau-equivalence with congeneric structures, and supply
prophecy formulas. [Their 2025 tutorial](https://doi.org/10.3390/math13061001)
adds absolute-error estimation, multiple response scales and general/group
factor partitions. Comparable coefficients in examples do not establish general
equivalence between models. Retain model structure when reporting results.

**Latent-response reliability is a separate estimand.** The verified
[Vispoel, Morris & Kilinc (2019)](https://doi.org/10.1037/met0000177)
paper and Ark dissertation address scale coarseness through continuous latent
responses underlying categorical scores. Their outputs require that latent
interpretation; a coefficient on that scale should not silently label the
reliability of the original ordinal sum. The newer acquired
[Jiang et al. (2024)](https://doi.org/10.3758/s13428-024-02472-7)
uses a tailored mixed-format Bayesian model with distinct outcome links and
examines priors. Its normal assumptions, response metric and inference target
must be read carefully before implementing a general categorical backend.

**IRT integration has several meanings.**
[Briggs & Wilson (2007)](https://doi.org/10.1111/j.1745-3984.2007.00031.x)
perform GT analysis on expected response matrices within a random-effects IRT
framework. [Choi & Wilson (2018)](https://www.psychologie-aktuell.com/fileadmin/download/ptam/1-2018_20180323/PTAM-1-2018_Sammlung_v2.pdf)
use generalized linear latent/mixed models for rater effects. These support a
bridge, not a claim that GT and IRT are interchangeable or that raw-score ANOVA
components equal latent-scale components.

**Estimator constraints are consequential.**
[Jiang & Skorupski (2018)](https://doi.org/10.3758/s13428-017-0986-3)
provide six multivariate designs and BUGS code, with prior discussion including
variance/covariance constraints. Positive definiteness, boundary estimates,
convergence and prior sensitivity are future design issues. An unrestricted
ANOVA covariance estimate and a constrained Bayesian estimate need not agree.

## Reference implementations and reproducible artifacts

Root owns quarantine ingestion. No third-party code was executed or adopted by
this lane. Sources and acquisition leads sent to root:

- mGENOVA, urGENOVA and GENOVA are available from the [official CASMA program page](https://education.uiowa.edu/casma/computer-programs).
  mGENOVA is restricted by design; urGENOVA estimates unbalanced random-effects
  G-study components and has no D-study functionality. Their manuals and examples
  are useful comparisons, not a complete reference for all advanced cases.
- CASMA #44 embeds R code and examples for composite utility; the program page
  separately links COMPOSITE SCORE UTILITY code and example files.
- Jiang et al. (2020) glmmTMB tutorial and Jiang & Skorupski (2018) BUGS tutorial
  supply alternative covariance-component constructions and examples.
- Jiang et al. (2024) publish code/data at [OSF wud3x](https://osf.io/wud3x/)
  and a supplementary DOCX on the publisher page.
- Vispoel et al. (2023, 2024, 2025) provide instructional supplements with R
  analyses; the latest supplement is [math13061001/s1](https://www.mdpi.com/article/10.3390/math13061001/s1).
- A current official UEA output describes [facet: framework for Generalizability Theory](https://research-portal.uea.ac.uk/en/publications/facet-framework-for-generalizability-theory/),
  with multiple estimation backends and multivariate analysis; forwarded to root
  for software discovery, not yet independently inspected by this lane.

## Gaps, acquisition work and interpretation limits

Highest-priority operator acquisitions:

1. **Brennan (2001), Generalizability Theory, chapters 9–12**, especially
   chapter 11, DOI 10.1007/978-1-4757-3456-0_11. The whole-book PDF URL returned
   an access page. The acquired works reference these derivations, but do not
   replace the full multivariate unbalanced treatment.
2. **Ark (2015) ordinal dissertation**, DOI 10.14288/1.0166304. UBC's official
   item and public media URLs returned a block/access document, not a thesis PDF.
3. **Vispoel et al. (2019)**, DOI 10.1037/met0000177. Primary abstract/metadata
   verified; no acquired full text yet. Its instructional supplement should also
   be obtained for latent-response equations and code.
4. **Vispoel et al. (2023), Applying Multivariate GT**, DOI 10.1037/met0000606.
   An indexed publisher supplemental full-article PDF was readable through search
   extraction but direct acquisition returned 404. Root should seek another
   author/publisher copy or obtain it through institutional access.
5. **Vispoel et al. (2018), CTT/SEM links**, DOI 10.1037/met0000107. Indexed APA
   full article was inspected in part; direct PDF request returned an access page.
6. **Rajaratnam et al. (1965)** stratified-parallel tests; **Keller et al. (2010)**
   fixed content stratification; **Schoonen (2005)** writing/SEM; **Joe & Woodward
   (1976)** maximum composites; **Marcoulides (1994)** weight/allocation coupling.
   These are verified important originals with no acquired full text in this lane.
7. **Lee et al. (2026)** randomly parallel testing, DOI 10.1111/jedm.70029.
   Publisher full text and institutional PDF were discoverable; ordinary direct
   PDF and HTML acquisition attempts returned 403. This is an automation blocker
   for an openly licensed source, not evidence of a paywall.

Bibliography expansion remains useful: CASMA #53 provides over 300 historical
references, but explicitly excludes some meeting presentations and does not claim
complete coverage. Follow its entries for Conger/Lipshitz profile theory,
multiple-group designs, conditional SEMs, multivariate weighting/budget methods
and latent-state-trait bridges. Newer publisher citation lists already add the
2022 heterogeneous-design and 2024–2025 SEM/Bayesian updates absent from the
2020 bibliography. The 2026 NCME program also announces **Confidence Interval
Estimation in Multivariate Generalizability Theory: A Bootstrap Approach**
(Stella Kim, Sungyeun Kim and Qiao Liu); this is a conference lead, not an
acquired or validated method paper.

This lane covers the major requested advanced branches with primary-source
anchors. It does not prove literature saturation. Multiple linked random facets,
general multivariate unbalanced covariance algorithms, ordinal observed-scale
dependability and uncertainty of constrained covariance estimates need deeper
full-text comparison before a complete design can be written.
