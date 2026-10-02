# Foundations and classical design algebra

Research date: 2026-10-02. This lane catalogues 43 verified sources/editions and acquired eight institutional PDFs. Its scope is the defining G-theory lineage, design algebra, universes/facet semantics, symmetry, and conceptual identifiability. The catalogue records what was actually read, separately from acquisition. Acquisition does not imply a complete mathematical reading.

## The intellectual spine

The defining original sequence is Cronbach, Rajaratnam and Gleser (1963), Gleser, Cronbach and Rajaratnam (1965), and Rajaratnam, Cronbach and Gleser (1965), followed by Cronbach, Gleser, Nanda and Rajaratnam's 1972 *The dependability of behavioral measurements*. The first trio establishes sampling-based generalization, multiple variance sources, and stratified item universes. Publisher/NLM metadata verifies the trilogy; the original full texts remain unavailable in this acquisition. The monograph is a priority operator acquisition, not a locally read source.

Brennan's 1983 *Elements*, its 1992 revision, and his 2001 *Generalizability Theory* form the later computational spine. The 2001 publisher contents span single/multifacet G and D designs, uncertainty, unbalanced designs, multivariate G/D/unbalanced designs, regressed scores, and matrix/variance appendices. This is the central comprehensive book to acquire before specifying the complete implementation. It is not equivalent to a primer or to the existing crossed-component projection API.

The acquired [ACT Technical Bulletin 26](../../downloads/foundations/brennan-1977-act26-principles-procedures.pdf) supplies a substantial public primary starting point: notation, structural terms, component estimation, expected mean squares, object-specific D-study transformations, fixed/random cases, and finite-universe extensions. Its five illustrative designs include crossed facets and nesting on both sides. The acquired version is September 1977. Brennan's bibliography mentions an August 1978 revision; do not silently equate the copies. Its OCR is poor, so numerical formulas must be checked visually in the PDF before becoming an oracle.

Brennan's [CASMA Report 1](../../downloads/foundations/brennan-2003-coefficients-indices.pdf) is a more legible public treatment of relative/absolute errors and coefficient families, with crossed and partially nested worked tables. It is especially useful for separating generalizability coefficients, ordinary dependability coefficients, cut-score indices, signal/noise ratios, error-tolerance ratios and multivariate indices.

## The European lineage changes the API's central objects

Cardinet, Tourneur and Allal's 1976 symmetry paper and 1981 extension paper, Cardinet and Allal's 1983 parameter chapter, Cardinet and Tourneur's 1985 *Assurer la mesure*, and Cardinet, Johnson and Pini's 2010 EduG book are essential complementary sources. The 1976/1981 originals are blocked at the Wiley download endpoint; the books and chapter need operator/library acquisition.

The acquired primary author exposition, [Allal's 1986 symposium paper](../../downloads/foundations/allal-1986-symmetry-europe.pdf), provides the actual conceptual expansion: any factor can become an object of measurement; a population of objects can itself comprise crossed or nested facets; and both object and observation facets can be infinite-random, finite-random, or fixed. Its school-district × nested-pupil and crossed-item-classification example shows a component moving from universe-score variation to error when the decision changes. The inference for crolib is that a generic engine needs a declaration of what is being differentiated, what is averaged/generalized over, and how levels are sampled. A hardcoded person axis cannot express the full classical theory.

The [IRDP author bibliography](../../downloads/foundations/irdp-2017-cardinet-bibliography.pdf) reveals technical archival gaps: the 1985 French/English definition reports and the 1987 *Definition of the components of generalizability parameters* manuscript, revised in 1989 and explicitly unpublished. These are not safely replaced with guesses from later summaries. The bibliography also identifies French translations/reprints that could be lawful alternative acquisitions.

## Design algebra and estimand semantics

ACT 26 explains main and interaction terms through crossing/nesting indices; combinations that repeat a nesting index do not generate independent effects. This gives a route toward a design compiler grounded in a primary algorithm rather than accumulating special-case cubes. Its EMS relation sums the applicable variance components with replication multipliers. Cornfield and Tukey (1956), and Millman and Glass (1967), are the underlying algebra sources; both are catalogued, neither original PDF acquired.

For an all-random, infinite-universe D study, CASMA 1 divides G-study components by applicable D-study counts, assigns the object component to universe-score variance, assigns all non-object terms to absolute error, and assigns object-containing nuisance terms to relative error. The same report gives mixed-model term reassignment. Fixing a facet can move object×fixed-facet variation into universe-score variance, rather than merely subtracting a nuisance main effect.

**Those simplified mixed-model rules have explicit restrictions:** random-model G-study components; each D facet either fixed or infinite-random; balanced observations and constant nested counts. Finite universes and incomplete/unbalanced records require other machinery. ACT 26 treats finite sampling distinctly from both infinite-random and fixed effects; a finite universe requires its size and sampling semantics. A bare boolean `fixed` is therefore inadequate for the full theory.

The acquired [1975 class-means conference report](../../downloads/foundations/brennan-kane-1975-class-means.pdf) supplies a primary aggregation precursor to Kane and Brennan's final 1977 article. Treat these as versions of one research line, not two independent mathematical corroborations. Split-plot and class-mean sources make clear why dependability must be evaluated at the declared object level, such as pupil, class, or school.

## Identifiability is a semantic requirement

Brennan's acquired [2017 Report 51, The Problem of One](../../downloads/foundations/brennan-2017-confounded-effects.pdf), deserves early design-stage attention. A single sampled prompt, rater, or automated scoring engine can confound component families even when the observed data table looks complete. A person×rater study with one prompt cannot independently recover person and person×prompt variance. The apparent coefficient answers a restricted question and can overstate dependability for the intended random-prompt universe. Larger sample sizes and repeated studies with the same confounding preserve this problem; an auxiliary study with multiple levels can supply missing information.

The engineering inference is that crolib should represent the intended universe separately from the observation structure and preserve aliases/confounded component sums. Before allowing a D-study projection, it must determine whether the fitted information identifies that projection. Estimation uncertainty and structural nonidentifiability are different issues; adding bootstrap intervals cannot repair the latter.

[CASMA Report 8](../../downloads/foundations/brennan-2004-measurement-model-inconsistencies.pdf) and Kane's 1982 sampling-model article further motivate explicit replication/universe semantics. Classical, G-theory and IRT coefficients can differ because they embody different true/universe scores, errors, scoring and replication definitions. The library's numerical result should retain enough semantics to make its interpretation inspectable.

## Acquisition priorities and correction hazards

Highest-priority operator/library items:

1. Cronbach et al. 1972 original monograph, Wiley ISBN 0471188506.
2. Brennan 2001 complete Springer ebook, DOI [10.1007/978-1-4757-3456-0](https://link.springer.com/book/10.1007/978-1-4757-3456-0).
3. Cardinet/Tourneur 1985 *Assurer la mesure*, Peter Lang ISBN 9783261035066; Cardinet/Johnson/Pini 2010 [EduG book](https://www.routledge.com/Applying-Generalizability-Theory-using-EduG/Cardinet-Johnson-Pini/p/book/9781848728295).
4. Original 1963/1965 trilogy; Cardinet 1976 and 1981 papers **with 1982 errata** (JEM 19(4), 331–332).
5. ACT reports 31, 36 and 46; Cardinet/Allal 1983 parameter chapter and IRDP 1985/1987/1989 manuscripts.
6. Shavelson/Webb 1991 [Sage Primer](https://www.sagepub.com/shop/buy-a-book/generalizability-theory-1-3375) and Webb/Shavelson/Haertel 2006 Handbook chapter, kept distinct.
7. Brennan/Kane 1977 signal/noise article **with its 1978 erratum**, Psychometrika 43(2), p.289.

Do not mistake current website posting dates for historical publication years: Cambridge's Psychometrika migration displays 2025 for 1965 papers; Wiley sometimes displays 2005/2006 for 1970s/2001 articles. CASMA 51's acquired PDF is January 2017 despite citations to a 2016 draft. ResearchGate's 1991 Primer record is contaminated with unrelated DOI/ISBN metadata and a link that actually exposes the 2006 Handbook chapter. These discrepancies are recorded in individual entries.

## Breadth and remaining work

The acquired [Brennan/Liao 2020 field bibliography](../../downloads/foundations/brennan-liao-2020-first-sixty-years.pdf) contains more than 300 references. It is now a reusable local discovery spine for the other lanes. It explicitly says its list is incomplete and is not an endorsement of included works. The IRDP bibliography broadens coverage beyond English journal indexing. Seventy-one focused query strings, bibliography expansion paths and failed acquisition URLs are retained in `search-log.json`.

This lane has thoroughly mapped the central foundational branches and exposed material access/version gaps. It has not exhaustively acquired every historical item, nor closely derived every formula. Before implementation design, the priority books, corrections, finite-universe parameter conventions, and alias-preserving EMS algebra need a dedicated mathematical reading. Later uncertainty, sparse/unbalanced and multivariate papers are owned by the neighboring lanes.
