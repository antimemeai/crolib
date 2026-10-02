# Armada design tribunal: estimation and uncertainty

Review date:2026-10-02. Reviewed `docs/design.md` and the original Armada extraction `context/design/measurement-armada.txt`, especially Armada pages6 and10. No design or runtime changes were made. Primary material was reread locally where acquired; literature lane reports supplied the coverage map. Recommendations below are my architectural/mathematical assessment, not claims that the cited papers prescribe crolib's interfaces.

## Recheck and current disposition

Rechecked the root revision at 2026-10-02T15:08:03.885281+00:00; design SHA-256 `26dcf6c1ec4934903d7a0bc8554a2b4f35dfa0b1bc2036f2d9ac6b1191207f52`. **Pass for the overarching estimation/uncertainty architecture; no remaining architectural blocker in this review.** This authorizes proceeding to appropriately scoped mathematical specifications and their tribunal, not unreviewed runtime implementation or unsupported inferential claims. Original findings below are retained for traceability; their line references refer to the first reviewed draft. Resolution references in this section refer to the rechecked revision.

| Finding | Resolution status | Remaining obligation |
|---|---|---|
| H1 singularity/likelihood domain | **Resolved architecturally**, current lines259–264 distinguish random-effect singularity, full observation covariance, declared space, a separately derived lower-dimensional model and unavailable likelihood; silent ridge prohibited. | Gaussian family specification must still define REML contrast domain, no-error-contrast behavior, unbounded likelihood versus finite boundary optimum and constrained termination checks. These are anticipated by the deferred mathematical work. |
| H2 invalid/undefined uncertainty realizations | **Resolved**, lines375–380 enumerate fit/projection/denominator/transformation failures, require justified treatment and withhold an interval without it. Recording failures does not license conditioning on success. | Concrete methods must specify realization statuses, denominators and retry policy, and evaluate that complete procedure in simulations. |
| H3 selection/adaptive claim scope | **Resolved**, lines401–408 distinguish predeclared, marginal, selected and simultaneous requests; unsupported selection-regime intervals are unavailable. Adaptive guarantees still require a derived method. | Campaign specification must state acquisition/stopping assumptions and validate whole-campaign inference; until then return unsupported adaptive claims. |
| M1 tagged draw/full parameter state | **Resolved**, lines388–393 identify bootstrap/posterior/approximation draws, coordinate/scale/constraints, required mean/threshold state and supplied uncertainty provenance. | Each interval family still defines inversion/pivot/summary semantics rather than treating all draw arrays as posterior probabilities. |
| M2 population dependability versus future estimator prediction | **Deferred target-definition clarification, not a blocker.** Named estimands and compositional support already prevent a generic method from promising every prediction. | Future pilot precision/expected interval width needs its own future observation/refitting model; do not infer it from a population-reliability component transform. |
| M3 independent effect-block scope | **Resolved** in the final scoped reread: lines214–215 explicitly assume independent effect blocks and require explicit joint covariance kernels/parameters for correlated blocks. | Correlated extensions still need their family-specific kernels and derivations; no open wording issue remains. |
| L1 worked example provenance | **Resolved** in the final scoped reread: lines537–538 identify supplied README components; lines578–580 explicitly disclaim demonstration of fitting, interval coverage or a completed acquisition round trip. | No remaining provenance correction; arithmetic remains correct. |

Final scoped reread at 2026-10-02T15:12:41.094025+00:00, design SHA-256 `dfb3ac48613494229ae40e8c5072686eb7eba8e525d93f3d90bf367d1557b4a7`, confirmed M3 and L1 resolved. Their table references identify that later revision; H1/H2/H3/M1 resolution references retain the earlier recheck above. Original findings remain historical review evidence. **No open wording issue or architectural blocker remains from this review.** No new tribunal or runtime work was undertaken.

The new alias paragraph also correctly uses `E[t]=A theta`, explicitly says observed moment statistics are noisy, and separates selected-moment, full-law and REML-contrast identification. That strengthens the contract beyond the original draft. No additional family derivation was smuggled in as an implemented capability.

## Original verdict

**Conditional pass for the overarching architecture.** The document makes the central scientific distinctions correctly and its balanced crossed G/Phi equations are correct under the stated all-random infinite-universe model. I found no reason to replace its estimation/projection architecture or require a complete derivation of every future family before scoping a balanced-family specification.

Three contracts need firmer wording before the associated capabilities receive implementation plans: **the domain of the Gaussian likelihood at singularity; treatment of failed/undefined uncertainty realizations; and the claim scope of selected/adaptively obtained intervals**. These are behavioral gates, not demands to implement additional algorithms now. Their absence would allow an implementation to satisfy the present prose while returning scientifically misleading results. Further full-parameter uncertainty and predictive-versus-estimation semantics should be specified before extending the generic uncertainty interface.

The architecture can advance through a restricted balanced moment-estimation specification while Gaussian likelihood, interval/allocation and campaign claims remain disabled until their respective gates are met. If the tribunal requires one revision before any plan, make the three gates explicit in the overarching design and keep the advertised capability sequence scoped accordingly.

## What is already sound

- Lines191–210 distinguish mean rank, covariance identifiability, numerical weakness, estimator-specific REML information and identifiable functions. The null-space test applies to linear functionals; nonlinear invariance needs its own check. It correctly avoids promoting a prior or optimizer-selected decomposition into observed information.
- Lines237–248 preserve signed moment estimates, separate clipping from constrained refitting, permit valid negative covariance off-diagonals and separate a successful boundary fit from numerical failure. This reconciles Betebenner's signed EMS combinations with the Bates covariance-factor treatment of singular random effects.
- Lines267–302 distinguish the absolute-error covariance operator from the relative comparison target, explicitly separate G and Phi, reject fabricated answers at zero denominators, and retain the residual/three-way confounding of the unreplicated design.
- Lines333–361 distinguish measurement, estimation, projected-design and Monte Carlo uncertainty; prohibit componentwise intervals from standing in for joint coefficient intervals; and correctly state that joint draw propagation alone proves neither simultaneous coverage nor adaptive validity.
- Lines376–379 separate plug-in thresholds, confidence bounds, posterior probabilities and loss. Lines405–409 make support compositional. These are useful enforcement foundations, rather than a suggestion to implement all combinations.

## Contract gates and actionable corrections

### H1. Random-effect singularity and singular observation covariance are different states

**Location:** lines178–197,225–248,474,519–520.

The design allows boundary zeros and singular covariance as successful fits, but never states which covariance may be singular while the ordinary Gaussian likelihood remains defined. A singular random-effect covariance `G` can be entirely legitimate when the marginal observation covariance `V=ZGZ'+R` remains positive definite. It does not follow that an ordinary full-rank Gaussian density remains available when `V` itself is singular. A covariance that is PSD is not enough for the usual log-determinant/inverse likelihood.

For REML, the relevant requirement is positive definiteness on the error-contrast space, not a blanket statement about every random-effect block. A separately specified degenerate-Gaussian model on a fixed lower-dimensional support may be legitimate; silently substituting pseudo-inverses or pseudo-determinants into the existing likelihood is a different model/measure and is not an automatic boundary extension.

**Correction:** add an estimator-domain contract: identify the matrix whose positive definiteness is required, the support/measure of the likelihood, and whether any degenerate observation model is supported. Distinguish `random_covariance_on_boundary` from `marginal_likelihood_undefined`, `no_error_contrasts`, `likelihood_unbounded/no_finite_optimum`, and numerical failure. Permit exact zero random-effect variance without substituting a log-variance parameterization; never silently impose a positive epsilon variance floor.

**When blocking:** before a constrained Gaussian engine plan, not before raw balanced moments. The numerical boundary algorithm and tolerances are deliberately deferred family-level work; the likelihood-domain/failure meanings should be architectural now.

**Direct challenge fixtures:** (a) `G=0` with positive residual variance: valid ordinary Gaussian likelihood; (b) singular `V` outside a specified degenerate-model family: explicit unsupported/undefined likelihood; (c) `y` exactly in the fitted mean space with a variance allowed to approach zero: distinguish an unbounded likelihood limit from a finite boundary optimum; (d) REML with zero residual contrast dimension: fail its fitting request explicitly.

**Grounding:** Bates etal2015 §3.1 and the discussion comparing covariance-factor and precision formulations allow singular `Lambda_theta` while retaining a positive residual observation model. Harville1977 §2 assumes nonsingular observation covariance; §4 constructs REML from `n-rank(X)` error contrasts. These support separate domains, not an indiscriminate singularity exception. [Bates](https://doi.org/10.18637/jss.v067.i01), [Harville](https://doi.org/10.1080/01621459.1977.10480998).

### H2. Logging failed replicates does not define a valid interval

**Location:** lines237–243,338–348,353–354,497.

The uncertainty output records successful and failed replicates, but the contract does not forbid silently computing interval quantiles or decision probabilities over successes only. Nonconvergence, inadmissible normal-approximation component draws, undefined ratio draws, and deliberately retained signed moment estimates are statistically different events. Combining them under one failed-replicate count is insufficient.

An implementation could draw an unconstrained multivariate approximation to component estimators, discard negative components because population covariance projection rejects them, and report quantiles of the remaining coefficient draws. It would then estimate a distribution conditional on admissibility, not the original approximation. Similarly, if an undefined coefficient preferentially occurs at low signal or zero total variance, dropping those replicates can distort a threshold probability. Preserving a count does not repair the distortion.

**Correction:** uncertainty realizations need separate fit status, component-policy status, target-definition status and numerical status. State the interval/probability denominator and the method-specific failure policy. A procedure must either define a justified treatment of these events, return an explicitly conditional descriptive distribution, or withhold the inferential result. No implicit reject-and-redraw, silent clipping/PSD repair, estimator-switching or successes-only coverage claim. A declared retry procedure is part of the method and must be simulated as such.

**When blocking:** before interval or uncertainty-aware allocation plans. Pure deterministic supplied-component projection and raw moment fitting remain available. Do not demand an arbitrary universal minimum-success fraction; the acceptable behavior is method- and target-specific.

**Important qualification:** an unconstrained estimate outside the population parameter domain is not automatically a failed estimator. Signed raw moments can be valid statistics, and an interval may still target a nonnegative population variance. Intersecting an already constructed confidence set with a known parameter domain differs from deleting/truncating its generating statistics. A raw coefficient outside `[0,1]` can be a labeled historical statistic; it cannot silently become an admissible population covariance model or a physical SEM.

**Direct challenge fixtures:** raw negative person component with a recorded moment fit; uncertainty realizations with negative components; a zero-denominator realization; a nonconverged refit; and a successful exact-boundary refit. Each must retain its own reason and explicit inferential treatment. Verify that no hidden conditioning changes the reported sample size, tail probability or confidence interpretation.

**Grounding:** Morris/White/Crowther2019 §5.1 explicitly treats missing simulation estimates as a missing-data problem, usually not completely at random; a model-changing retry changes the evaluated procedure. Betebenner1998 distinguishes signed EMS combinations from methods for positive combinations. Self–Liang1987 requires its regularity/identifiability conditions and has boundary cases that are not simple chi-square mixtures. [Morris etal](https://doi.org/10.1002/sim.8086), [Betebenner primary report](https://files.eric.ed.gov/fulltext/ED423304.pdf), [Self–Liang](https://doi.org/10.1080/01621459.1987.10478472).

### H3. Selection and adaptation need an enforced claim scope, not only a warning

**Location:** lines356–361,365–379,381–386,399–409,475–477.

The design correctly acknowledges selection and adaptive inference, yet still permits optimizing a lower confidence bound and returning a selected design's interval. That is a legitimate numerical objective only if the resulting claim remains explicit. A pointwise bound for a predeclared candidate cannot acquire simultaneous or post-selection coverage simply by becoming the largest bound in a grid. The present warning leaves room for an implementation that labels the winner generically as a95%confidence result without recording its selection context.

**Correction:** every inferential result should carry its claim scope: fixed predeclared candidate, pointwise candidate collection, simultaneous declared family, validated post-selection procedure, or explicitly unvalidated selected summary. Preserve the candidate/search domain and selection rule in the result. Unsupported selected-design guarantees must fail capability checks, while descriptive pointwise results may remain available with their narrower scope. A selected lower-bound objective must not imply that the winning procedure meets a threshold at the nominal confidence level unless the method supports that claim.

Adaptive campaign support additionally needs either a modeled/justified assignment and stopping mechanism or an explicit fixed-design restriction. Merely recording actual assignments is not a guarantee that response-dependent assignment can be ignored. Under Bayesian inference an ignorable adaptive policy may leave the likelihood unchanged, but that needs a stated model and assumptions; not every adaptive policy biases every estimator, and not every Bayesian posterior is automatically valid under selection.

**When blocking:** before selected-design confidence guarantees or campaign inference. Finite enumeration of plug-in objectives is already coherent. Simultaneous, selective and sequential algorithms are deliberately deferred; the architecture needs a gate that rejects their claims until derived.

**Grounding:** Armada page10 explicitly requires full sequential-campaign evaluation including stopping/acquisition bias, while page6 distinguishes interval meaning and evidence authority. The uncertainty lane identifies simultaneous-grid/selection inference as an unresolved research branch; acquired conventional GT interval papers do not supply a generic solution. Shin/Raudenbush2012 separates G-study uncertainty from D-study planning, but is not a theorem for arbitrary post-pilot design searches. [Shin/Raudenbush primary manuscript](https://wtgrantfoundation.org/wp-content/uploads/2015/09/Confidence-Bounds-and-Power-for-the-Reliability-of-Observational-Measures-on-the-Quality-of-a-Social-Setting.pdf).

## Further interface corrections before extensions

### M1. A joint draw array needs a statistical identity

**Location:** lines96–98,338–348; model/fit/result records.

`joint component draws` can denote posterior parameter draws, bootstrap refitted estimator draws, an asymptotic estimator distribution, or a calibrated confidence construction. They are not interchangeable probability statements. An array plus a method name should not implicitly become a posterior distribution of the true components.

Name the random object, generating/refitting procedure, centering/pivot/inversion if relevant, conditioning, parameter coordinates, scale and supported use. Percentile transforms, confidence-set inversion and posterior credible intervals remain separately specified methods. Preserve supplied-component uncertainty provenance; a covariance matrix alone does not uniquely determine a joint distribution, though it can support a named delta-method approximation.

For future fixed-facet, response-scale and classification targets, propagate the **full required parameter state**, not just variance components: mean/fixed-effect uncertainty, response parameters and their relevant joint dependence may be needed. The document already acknowledges required mean information at lines521–522; the generic uncertainty payload must accommodate it. This is a forward interface correction, not a blocker for the current mean-free balanced G/Phi family.

### M2. Separate uncertainty about population dependability from prediction of a future fitted coefficient

**Location:** lines333–348,381–386.

Projecting pilot component uncertainty through a fixed candidate operator describes uncertainty about that candidate's population dependability under the model. It does not automatically predict the coefficient that a new finite G-study would estimate, future confidence-interval width, or success of a stopping rule. Those targets need the future observation/refitting distribution, generally an additional simulation/integration layer.

Add distinct estimands for candidate population reliability, future observed score/error, future estimator distribution and expected study precision. The acquisition interface should require the appropriate model rather than treating one component-draw transform as all four. Shin/Raudenbush's planning derivations make this distinction concrete; their family-specific formulas can remain deferred.

### M3. Make cross-effect independence explicit in the displayed Gaussian model

**Location:** lines178–189,306–323.

`Cov(y)=sum_e theta_e K_e` follows from the displayed additive model only under the declared independent/uncorrelated block structure, or when cross-effect covariance is explicitly included in the kernels. The initial conventional GT family can state that assumption directly. More general correlated effect families need `Z_e Cov(b_e,b_f) Z_f'` contributions or an equivalent combined block representation. Covariance across dimensions within an effect is not the same as arbitrary covariance between effects. This is a scope clarification, not evidence that the initial conventional formula is wrong.

### L1. Correct the worked campaign's provenance wording

**Location:** line427 versus line434.

The example first says the pilot estimates the seven components, then correctly says they are illustrative supplied parameters. Replace the former description with a supplied illustrative decomposition or explicitly imagined pilot. The numbers and computed G/Phi examples are internally consistent; the fault is provenance language, not algebra.

## Deliberately deferred work that is not an architectural error

- Exact EMS systems, fixed/finite transformations, constrained parameterizations, KKT/termination diagnostics, rank tolerances and boundary interval calibrations belong to the estimator-family specifications already requested at lines510–525.
- General multivariate PSD constraints, ordinal observed-scale mappings, conditional SEM and partial-identification bounds may remain unsupported. Their absence should produce capability failures, not speculative implementations.
- No generic resampling method needs to support arbitrary incidence. ACT87-7's finite-universe experiments use without-replacement sampling whereas bootstrap replicates use replacement; preserving that distinction matters more than immediately implementing every finite correction.
- The document already avoids generic Wald fallback and blanket prior defaults. Do not add a universal chi-square mixture, a generic PSD repair, or an automatic log-variance parameterization to fill a perceived gap.
- ML/REML must remain method-specific. A useful exact REML challenge is `X=1`, `K_1=11'`, `K_2=I`: for contrasts `C'X=0`, `C'K_1C=0`, so the common random-intercept component disappears from restricted information. This does **not** assert that ML and REML have identical identifiability or that a distinct unprojected kernel always supplies practically adequate information. The current prose correctly anticipates this distinction.

## Acceptance evidence for the next scoped specifications

| Capability | Necessary tribunal evidence |
|---|---|
| Balanced moment fitting | Signed EMS values retained; raw estimator success separated from admissible downstream covariance; alias-preserving function support; no fabricated zero/one or physical SEM for undefined targets. |
| Constrained Gaussian fitting | H1 domain states specified; exact boundary permitted; unbounded/undefined likelihood distinct from optimizer failure; estimator-specific contrast identifiability and constrained optimality checks. |
| Joint intervals and D-study propagation | H2 realization/failure policy plus M1 random-object semantics; same joint realizations across candidates; target-specific coverage/MCSE evidence with failures retained. |
| Uncertainty-aware allocation | H3 claim-scope enforcement; predeclared search domain and objective; selected guarantee only when supported; independent enumeration verifies optimization, not coverage. |
| Adaptive campaigns | Modeled or justified selection/stopping mechanism; full campaign simulation under stated generators; conventional fixed-design fallback remains useful. |

Jiang etal2022 is an especially useful negative acceptance fixture: its title says generalizability coefficient, but its equations and footnote target **absolute-error Phi**; its best studied bootstrap still gives roughly81%coverage in a nested polytomous case. Reproducing the code's best method is therefore not proof of a95%interval for relative G, arbitrary incidence or a searched D-study. Test target identity and empirical calibration separately. [Acquired primary fulltext](https://pmc.ncbi.nlm.nih.gov/articles/PMC9228698/).

This tribunal recommends clarifying the gates, then writing narrow mathematical specifications with explicit unsupported combinations. It does not recommend runtime implementation or algorithm adoption before those specifications and their direct acceptance evidence are reviewed.
