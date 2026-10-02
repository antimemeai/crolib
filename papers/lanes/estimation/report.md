# Estimation frumentarius report

Research pass: 2026-10-02. Scope: fitting variance/covariance components from balanced, unbalanced, incomplete and sparse observations, with direct generalizability-theory applications distinguished from their statistical foundations. This is a catalogue and acquisition pass, with selected mathematical reading; it is not a completed estimator specification or an assertion that all collected papers have been deeply read.

Acquisition accounting: **37 catalogued works; 18 acquired works plus one acquired mathematical supplement (19 artifacts); 19 works have blocked local full-text acquisition.** Some blocked sources were readable in part through the web tool. Counts distinguish possession from reading.

## What the literature makes clear

An owned crolib estimator engine has at least three independently meaningful families: design-based moment estimation, likelihood estimation, and Bayesian estimation. The family is part of the statistical contract. Projecting a D-study from components is a subsequent operation, and the universe of generalization must remain explicit. Handling irregular rows in storage does not establish statistical estimability or justify an arbitrary D-study transformation.

| Family | Mathematical object | Sources and implementation relevance |
|---|---|---|
| Balanced ANOVA/EMS | Orthogonal sums of squares, expected mean squares and a linear component system | Cornfield–Tukey 1956; Brennan's GT examples; Huebner–Lucht 2019 reproducible worked designs. Best first exact oracle. |
| Henderson I | ANOVA-like moments built using actual unequal subclass counts | Henderson 1953; Huynh 1977 incomplete KR20. Particularly relevant to urGENOVA compatibility. |
| Henderson II | Correct observations for fitted fixed effects before moment estimation | Henderson 1953; Harville 1977 §8.2. Do not silently substitute this procedure for I or III. |
| Henderson III | Reductions in fitted sums of squares for specified models/effects | Henderson 1953; Harville 1977 §8.2; Chiu–Wolfe 2002 as GT sparse-method lineage. Model and adjustment choices need recording. |
| MINQUE/MIVQUE | Quadratic unbiased estimation using a working covariance and invariance/optimality criteria | Rao 1971/1972; Harville 1977; Swallow–Monahan 1984. Generic statistical foundations, rather than new GT theories. |
| ML/REML | A fitted Gaussian covariance model and likelihood objective | Hartley–Rao 1967; Patterson–Thompson 1971; Corbeil–Searle 1976; Marcoulides 1990 and Jiang 2018 are explicit GT bridges. |
| Bayesian | Posterior over components and reliability functions, conditional on likelihood and prior | LoPilato et al. 2015; Jiang–Skorupski 2018; ten Hove et al. 2022/2025; Jiang et al. 2024. Priors and posterior summaries belong in result provenance. |

The Henderson I/II/III names do **not** mean fixed-effect ANOVA Type I/II/III sums of squares. Harville's §8.2 explicitly describes II's correction for fixed effects and contrasts fixed quadratic moment equations with the variance-dependent equations of REML. Agreement between balanced ANOVA and REML is a qualified oracle: the models must match and nonnegativity constraints must not alter the answer. [Harville 1977](https://doi.org/10.1080/01621459.1977.10480998), [Corbeil–Searle 1976](https://doi.org/10.1080/00401706.1976.10489397).

## Irregular designs are several problems

- **Unbalanced but observed:** unequal nested cluster sizes or unequal cell counts. Moment coefficients must use the real incidence pattern. An arithmetic/harmonic average sample size is not a general estimator derivation.
- **Incomplete crossed:** selected person × item × rater cells absent. The observation graph and model matrices determine whether components can be separated. Planned missingness, incidental missingness and informative missingness need different inferential treatment.
- **Sparse operational ratings:** a small fraction of raters score each response. Chiu–Wolfe subdivide data into analyzable crossed, modified balanced incomplete-block and nested pieces. Lin compares that strategy with treating rating slots as a facet; the latter changes the interpretation and must not silently relabel different raters as the same rater. [Chiu–Wolfe 2002](https://doi.org/10.1177/0146621602026003006), [Lin 2017](https://doi.org/10.1177/0265532216638890).
- **Confounding:** one rating per response cannot always separate item, rater and interaction effects. Brennan–Kim–Lee's complex-design examples show why operational data may require an additional G-study or an explicit aggregate component. [Brennan–Kim–Lee 2022](https://doi.org/10.1177/00131644211049746).
- **Longitudinal/ragged:** repeated measurements may require random slopes or serial covariance. Laenen's work extends reliability past exchangeable random-intercept assumptions; it should be a separate model family, not an automatic meaning of a time facet. [Laenen et al. 2006](https://doi.org/10.1348/000711005X66068).

The 2025 planned-incomplete comparison is especially valuable because it compares Bayesian hierarchical, ML random-effects and ML common-factor estimators by bias, coverage, convergence and runtime. It favors ML random effects with Monte Carlo intervals for its studied continuous rating designs. This is evidence against declaring one estimator universally superior; its conclusion is conditional on the simulation designs, models and priors. Its real example has 29 subjects, six raters and two raters per subject. [ten Hove et al. 2025](https://doi.org/10.1080/00273171.2025.2507745).

## Negative components and boundaries need distinct semantics

Negative *moment estimates* can arise even when population variance is nonnegative. Preserve the raw estimates and expose the chosen downstream policy; a clipped projection and a constrained refit are different statistical procedures. A constrained Gaussian ML/REML fit can reach an exact zero or a singular covariance matrix. Boundary solutions need to be distinguished from convergence failure and nonidentifiability. A log-variance parameterization excludes exact zero and is therefore not a neutral numerical substitution.

The lme4 paper explains why its relative covariance factor remains usable when singular, whereas a precision-matrix formulation can fail there. This is a useful numerical reference for an owned sparse engine, without selecting lme4 as a dependency. [Bates et al. 2015](https://doi.org/10.18637/jss.v067.i01). Self–Liang supplies the generic boundary-likelihood foundation; ordinary interior Wald/LRT assumptions should not be reused blindly. [Self–Liang 1987](https://doi.org/10.1080/01621459.1987.10478472).

MINQUE's working covariance choices, iterated variants and nonnegativity policy must be named. Swallow–Monahan compare specific choices in unbalanced one-way Gaussian models, including clipping; the result is not a proof of universal REML dominance. [Swallow–Monahan 1984](https://doi.org/10.1080/00401706.1984.10487921).

## Bayesian and response-scale distinctions

Jiang–Skorupski gives BUGS specifications for single-facet, crossed and nested multivariate GT designs, including covariance matrices. The article has a simulated complete/missing-data example and linked data/mGENOVA syntax. The Wishart/inverse-Wishart treatment is a reference to study, not a universal default to inherit. Gelman's variance-prior paper specifically critiques purportedly noninformative inverse-gamma priors and develops weakly informative alternatives. [Jiang–Skorupski 2018](https://doi.org/10.3758/s13428-017-0986-3), [Gelman 2006](https://doi.org/10.1214/06-BA117A).

Jiang et al. 2024 jointly model mixed-format tests and correlate person effects across formats. Their worked procedure builds separate model code and then combines it in Stan; the application also uses data-dependent priors. A Bernoulli/logit component lives on a latent scale, while a Gaussian rating component lives on a different scale. Raw-score components and logistic components cannot be compared or summed without a declared model-based mapping. Choi's 2013 dissertation explicitly compares these scales using Huynh's incomplete toy data. [Jiang et al. 2024](https://doi.org/10.3758/s13428-024-02472-7), [Choi 2013](https://escholarship.org/uc/item/7qv174cb).

## Validation material and reference bundles

| Source | Available oracle or material | Acquisition/use note |
|---|---|---|
| Huebner–Lucht 2019 | Four crossed/nested designs, ANOVA component tables and D-study tables; self-contained R generation syntax | Local PDF. Read the design, table and calculation sections; translate expected outputs into owned fixtures only after checking indexing and estimator semantics. |
| Huynh 1977 / Brennan 2001 / Choi 2013 | Incomplete 12-person × 6-item dichotomous toy example and comparative estimators | Huynh original local ERIC PDF; Choi university full text blocked locally but discoverable through web extraction. Preserve missing cells as absent, not score zero. |
| urGENOVA | Unbalanced random-effects estimates and manual/sample input | Root acquisition lane owns the package. Iowa explicitly says the program has no D-study capability. |
| Jiang–Skorupski 2018 | Simulated dataset, mGENOVA syntax and BUGS model text | Author ZIP: https://s3-us-west-1.amazonaws.com/zjiang4/data_code.zip; sent to root implementation lane. |
| ten Hove et al. 2022 | Multilevel IRR example, simulation and code/data | OSF https://osf.io/bwk5t/; article and one mathematical supplement local. |
| ten Hove et al. 2025 | Planned-incomplete observational example and three-estimator comparison | Publisher full HTML inspected; PDF acquisition blocked. Supplements linked by publisher/figshare need acquisition. |
| Jiang et al. 2024 | Mixed-format toy/example data and joint Stan code | OSF https://osf.io/wud3x/; author PDF local; root implementation lane notified. |
| Huang–Jeon 2022 | Worked Brennan.3.2 person × (rater:task) example | Article local; gtheory package dataset is an additional root-owned implementation reference. |
| Bates et al. 2015 | Profiled deviance/REML construction, sparse PLS formulation and computational examples | arXiv manuscript acquired as alternate for the same catalogue work. Explicitly not a dependency adoption. |

## Acquisition limits and shopping priorities

The catalogue and search log record exact attempts and successful local paths. Laenen’s 2008 thesis was recovered from the alternate ibiostat university site after the original repository returned 503. Downloads are private research assets; availability on a website is not permission to redistribute or incorporate its code. Original bytes and adjacent `.source.json` files preserve the acquisition source.

Priority operator/library acquisitions if alternate routes remain unavailable:

1. Brennan 2001 chapters 7–8 and 11; core unbalanced/multivariate estimators and examples. Foundations lane catalogues the book.
2. Brennan 1994 chapter *Variance Components in Generalizability Theory*.
3. Marcoulides 1990 REML simulation article and Marcoulides 1987 UCLA dissertation cited by that article.
4. Chiu–Wolfe 2002 sparse method; Lin 2017 is acquired but does not replace the original.
5. Jiang 2018 lme4 bridge article.
6. Patterson–Thompson 1971; Hartley–Rao 1967; Rao 1971/1972; Searle 1971 if direct sources are still inaccessible. Harville/Corbeil are acquired but do not substitute for all originals.
7. ten Hove et al. 2025 publisher PDF and supplemental code/data.
8. LoPilato et al. 2015 PDF if author/SSRN alternatives remain inaccessible locally.

Bibliography expansion was checked against Brennan–Liao's *First Sixty Years* catalogue and publisher references in Brennan 1994, Marcoulides 1990, Chiu–Wolfe 2002 and Jiang's interval paper. Additional named leads remain: Brennan–Jarjoura–Deaton ACT Bulletin 36 (1980), Hartley–Rao–LaMotte's synthesis method (1978), Koch's symmetric-sum procedure (1967/1968), early Fyans Bayesian work (1977), and Marcoulides's 1987 dissertation. These are leads, not counted as acquired/read works in this lane. Searching the entire history of variance-component statistics is outside a finite GT acquisition pass; the catalogue is deliberately substantial rather than falsely certified exhaustive.
