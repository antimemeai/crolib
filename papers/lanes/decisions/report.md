# Decisions, design optimization, cut scores and conditional error

Research date: 2026-10-02. This lane catalogues **45 distinct works: 26 acquired, 7 access-blocked and 12 metadata-only**. The acquired records comprise **23 independently downloaded artifacts (20 PDFs and 3 complete article HTML files)** and **3 manuals in root-acquired reference archives**. One PDF is a complete proceedings volume, retained intact for a chapter on optimization; one is a 387-page collected mastery-testing report. These are artifact counts, not a claim that every page has been read.

The catalogue and acquisition log distinguish the source, local artifact, reading depth, revised version and access obstacle. Each independent acquisition has a SHA256/source/time sidecar. `pdftotext` derivatives support searching; scanned mathematical notation sometimes needs visual confirmation. References were inspected as documents and source, never executed. No dependencies were adopted. Root owns software archives/manifests and shared indexes.

## Coverage and boundaries

The branch is large enough to warrant dedicated machinery, but several statistically different tasks use similar language:

| Task | Quantity and assumptions | Primary spine |
|---|---|---|
| Relative D-study | Rank-order precision; errors interacting with the object; projected facet sampling | Woodward/Joe 1973; Marcoulides/Goldstein series; GENOVA-family manuals in shared collection |
| Absolute D-study | Score-level precision; includes relevant facet main effects/interactions without object | Brennan 1998; Vispoel et al. 2023; foundations books and CASMA #1 |
| Cut-specific squared-error dependability | Agreement/loss referenced to a criterion, potentially varying with distance of population mean from cut | Livingston 1972; Brennan/Kane 1977; Kane/Brennan 1980 |
| Classification consistency | Probability of same category on two replications; raw agreement or chance-corrected kappa | Huynh 1976; Hanson/Brennan 1990; CASMA #7/#9/#13/#18/#22 |
| Classification accuracy | Agreement between observed and latent true classification; false positive and false negative errors | Livingston/Lewis 1995; CASMA #9/#13/#27; Moses/Kim 2015 |
| Standard-setting uncertainty | Variability of the cut itself across panelists/items/rounds, with chosen universe | Yin/Sconing 2008 |
| Conditional measurement error | Score/person-level error, distinct from one marginal SEM | Brennan 1998; CASMA #10/#16/#32 |
| Budgeted design optimization | Integer facet counts, specified error/reliability target, cost model, practical bounds | Marcoulides series; Parkes/Suen 1995; Suh et al. 2016; Jiang et al. 2021; Li 2024 |

Kane/Brennan's acquired 1980 article is the best conceptual bridge: threshold and squared-error loss are special cases of a broader agreement framework, with or without chance correction. Traub/Rowley 1980 and van der Linden 1982 provide primary historical taxonomy. The catalogue tags classification methods as **adjacent-classification**, even when G-theory inputs can feed them. A global dependability coefficient is not a probability of repeating a pass/fail result.

Single-administration consistency/accuracy is inferred under a replication and distribution model. It is not observed test–retest agreement. Distinguish population distributions, conditional observed-score distributions, empirical observed marginals and synthetic alternate-form marginals. BB-CLASS returns both HB-style model marginals and LL-style combinations involving observed marginals; these alternatives change numerical results.

## Acquired materials that support implementation

**Classification author suite.** CASMA #9 BB-CLASS v1.0 supplies the HB/LL methods, two/four-parameter beta choices, effective length, control cards, raw moments and contingency tables. The manual explicitly acknowledges implementation judgment because Livingston/Lewis did not specify every effective-length distinction. It treats observed and true cut scores separately; they need not be numerically equivalent. Samples are ideal future oracles, with branch labels preserved.

MULT-CLASS v3.0 has authored input/output for dichotomous and mixed-format scores; CASMA #10/#13/#16 supply multinomial, compound-multinomial and Dirichlet-multinomial derivations. The IRT-CLASS 2.0 manual and CASMA #27 cover dichotomous/polytomous/mixed response models, theta distributions and raw-to-scale transformations. NM-CLASS 1.0 is an authored R implementation/manual dated August 2019, anchored in Peng/Subkoviak and Kim/Lee normal approximation. Root has the archives and sample data/output. These are comparative references, not selected dependencies.

**Bias and bootstrap.** CASMA #7 gives item-resampling and stratified Boot-i for complex scoring. CASMA #18 explains plug-in probability bias and correction. CASMA #22 compares NM, BL, LL, BW and CM as cut counts, test length, construct equivalence and scale transformations vary. Together these prevent a superficially plausible agreement implementation from silently changing the replication model. Moses/Kim 2015 connects scoring design and composite weights to reliability/classification, and reports LL fitting failures at some extreme weights/distributions.

**Mastery/testing decision theory.** Huynh/Saunders's 1980 report includes 17 primary contributions on minimax and Bayesian passing scores, budgetary considerations, agreement/kappa inference, false decisions, sample sizes and sensitivity. The acquired report contains the 1978 memorandum *Computation and Inference...*; the 1979 journal article is titled *Statistical Inference...*. They should not be merged without version comparison. The report provides a considerable bibliography expansion backlog and older program listings, not a ready contemporary API.

**Integer and complex allocations.** Parkes/Suen 1995 demonstrates branch-and-bound allocation of writing prompts, modes and raters under four decision priorities. Suh/Hwang/Quan/Lee 2016 studies school-level reliability with persons nested in schools and crossed tasks/raters. Its cost is `33*n_person + n_person*n_task + 12*n_person*n_task*n_rater`; bounds include 15–286 persons, 2–12 tasks and 2–6 raters. The objective is minimum cost subject to a reliability target, not maximum reliability without practical limits. This supports bounded integer enumeration as an owned oracle even if later optimization algorithms are more elaborate.

Li 2024 derives continuous Lagrange solutions for `(s:t)×i`, `(s:t)×(i:v)` and `(s:t)×(i:v)×o`, optimizing students/items with dimensions/occasions supplied. Its empirical example selects 17 students and 4 items per dimension. The paper's Step 4 recommends rounding; a library must independently check the resulting integer cost and constraints. Rounding is not a feasibility or optimality proof.

Jiang et al. 2022 PRECOG-A supplies a cost-effectiveness workflow and financial-driver example. Vispoel et al. 2023 provides absolute/relative components and prophecy formulas for bifactor SEM designs, including changes in items, occasions and universe. Both help keep the cost/measurement design explicit rather than pretending every facet level has interchangeable cost or meaning.

## Numerical oracle opportunities and an apparent published discrepancy

BB-CLASS #9's HB worked example uses 40 items, raw cut 24, true cut .6, sample size 151050 and four-parameter beta/binomial input. Its **model-marginal** output gives classification accuracy .94427, false positive .03795, false negative .01778, consistency .92204, chance agreement .68031 and kappa .75613. The later empirical-marginal tables are different: they must not be substituted as the same expected output. Source precision is five decimal places; eventual tolerance should reflect printing and integration precision. Archived data/control cards provide provenance for an oracle without running the original executable.

An independent arithmetic check identified two inconsistencies in the acquired PMC rendering of Jiang/ Shi/DiStefano 2021. The optimization prose requires a **minimum** reliability, but the displayed cost-minimization constraint uses `coefficient <= beta`. The implementation contract should require `coefficient >= beta`, after reconciling prose, equation, figure/code and table.

The same article states universe variance 6.30, person×item 1.60, person×occasion .30, residual 1.95, unit product cost 5 and budget 100. It reports `(n_item,n_occasion)=(2,10)` with generalizability about .94. Applying its crossed relative-error formula gives:

```
error(2,10) = 1.60/2 + .30/10 + 1.95/20 = .9275
G(2,10)     = 6.30/(6.30 + .9275) = .8716707022
error(10,2) = 1.60/10 + .30/2 + 1.95/20 = .4075
G(10,2)     = 6.30/(6.30 + .4075) = .9392471114
```

Independent bounded enumeration of all positive integer pairs satisfying `5*n_item*n_occasion <= 100` selects `(10,2)`. This suggests exchanged labels/counts in the printed example, not a verified erratum in the original 1990 source. The 1990 article remains unacquired. Preserve the published artifact and record the discrepancy; do not silently adjust its reported example or call the heuristic output a proof of global optimality.

## Proposed library contracts — inferences from the sources

1. A D-study request should identify the object, universe, fixed/random facets, nesting/crossing, G-to-D design changes, score metric, weights, sampling counts and requested interpretation. Changing a nested design is more than changing a divisor.
2. Return relative and absolute error decompositions alongside coefficients and SEMs. Report unidentified/confounded components and unsupported projections explicitly.
3. Budget optimization should accept integer bounds, target direction, cost expressions and practical constraints. Return feasibility, objective, attained precision, candidate design and a search/optimality qualification; support an exact small bounded enumeration oracle.
4. Classification should explicitly select conditional error model, population model, empirical/model marginals, cut equality convention, ordered category boundaries, true versus observed cuts, bias correction and scaling. Return conditional/marginal contingency tables, raw agreement, chance agreement, kappa, accuracy and false-positive/negative components.
5. Conditional SEM, cut uncertainty, prediction intervals and marginal classification accuracy need distinct result types. Jiang et al. 2024's PredC is the fraction of person prediction intervals overlapping a candidate cut, not a classification-accuracy probability or a substantive method for deciding the competence standard.
6. Zero probabilities, degenerate marginals, denominator-zero kappa, infeasible reliability targets, unsupported raw-to-scale conversions, beta moment fitting failures and heuristic nonconvergence need documented results/errors. No silent clipping or silent global fallback.

## Access gaps and further bibliography expansion

Blocked items with concrete operator acquisition paths are the original Huynh1976, Brennan/Kane1977, Hanson/Brennan1990, Livingston/Lewis1995, Brennan1998 conditional-SEM paper and Jiang et al. 2024 PredC paper. Publisher downloads returned403 or access HTML, with no credentials used. Meyer/Liu/Mashburn2014's author-hosted Columbia PDF remains indexed but returns404; publisher abstract is verified. Obtain through a library/ILL or author copy. Schauber/Homer2025 was initially blocked at Wiley but recovered as a CC-BY accepted manuscript from Leeds/WhiteRose; the supplementary figure is not the article.

The oldest optimization sequence (1973,1990–1997), Kane1996 precision and Livingston1972 are metadata/abstract/bibliography verified, not fulltext read. Prioritize the 1990 and1991 integer-allocation articles to resolve the later numerical reversal, then Meyer2014 for nested-design formula reconciliation. Marcoulides1994 weighting is already in the multivariate lane; Brennan2001 and CASMA #1/#51/#53 are in foundations; Lee/Harris2025 chapter and CASMA #58 belong to uncertainty. Shared aliases should deduplicate at DOI/title/year, not multiply whole works.

Additional primary bibliography leads remain: Peng/Subkoviak1980 normal approximation; Subkoviak1976 and1988 single-admin mastery reliability; Kim/Lee2019 replication assumptions; Huynh1978 multiple classifications and1982 decision efficiency; Brennan/Lee1999 scale-score CSEM; Lee/Brennan/Kolen2000 and2002 scaling/interval studies; Kane2011 error tolerance; Breyer/Lewis1994 split-half/step-up; conditional-error loss under local item dependence; variable-cost/fixed-facet and unbalanced optimization. This is deep coverage of the assigned branch with an explicit continuing backlog, not a claim that the full field is exhausted.
