# Armada design review: scientific semantics

Reviewer: foundations lane. Date: 2026-10-02. Reviewed `docs/design.md` as
presented on this date and reread the owner's revisions. Original finding line
references below refer to the prerevision version. No design
or runtime files were edited. Scope is universe/score semantics, effect algebra,
identifiability, and supported generalization. This is an architecture review,
not a demand for the deferred estimator algorithms.

## Assessment

The central direction is scientifically sound. The current all-random crossed
formula is correct, the distinction between fixed sampling and fixed-effect
fitting is necessary, and retained fixed-facet interactions are correctly allowed
to contribute to universe-score variance. The document correctly refuses to
infer validity, accuracy, calibration or unexamined-environment generalization
from dependability. It also correctly separates aliasing, numerical failure,
boundary solutions, and positivity/priors as external restrictions.

Three architecture contracts needed clarification in the original version:
which information an alias calculation describes;
how mean effects enter random-selection projection; and whether candidates
measure the same target. These are modest additions rather than an architectural
rewrite. A fourth declaration is needed when finite/fixed object populations
become a supported family. I found no reason to block the existing supplied-
component crossed calculator.

**Resolution on rereview:** S1's moment/full-law/REML distinction is corrected
at revised lines 204–213. S2 is corrected at revised lines 303–309, with the
necessary mean/threshold state also retained by joint uncertainty records.
S3 is corrected by explicit target-preserving versus target-changing comparisons.
Final rereview also confirms that the Fit row accepts identified combinations
with unresolved aliases and projection consumes those combinations directly.
The object-population weighting and superpopulation versus realized finite-panel
variance distinction now resolve S4's architecture declaration. Their family-
specific formulas remain correctly deferred.
No remaining blocking scientific error was found in the revised overarching
design. All four findings are resolved at the appropriate architecture level.

## S1 — Name the information operator and preserve its aliases in the fit

**Architecture correction; medium severity.** Locations: lines 120, 191–210,
237–243, and 261–269.

Resolution: accepted. Final rereview confirms both the information-scope
correction and the explicit Fit handoff for identified combinations/unresolved
aliases. No remaining architecture correction is requested.

The null-space rule at lines 199–204 is right for a declared linear information
map, but `A theta = t` does not say whether `A` is the observation-law map, an
EMS map, or a particular estimator's reduced statistics. Those are different
questions. EMS relations are `E[T] = A theta` (with any known offsets included);
solving `A theta_hat = T_observed` is an estimation step, not the definition of
observational equivalence. An arbitrary choice of insufficient moment summaries
can lose information without the observation design itself losing it. Conversely,
REML can lack component information that is present in an unprojected covariance
map. The preceding paragraph recognizes this, but the alias rule does not carry
that distinction through its contract.

The Fit row also requires values and component identities, without explicitly
allowing identified combinations to be the fitted quantities. If later APIs
force a complete individual component vector, an arbitrary decomposition can
silently re-enter through this boundary, defeating the stated alias rule.

**Proposed correction:** identify the operator and information basis in the alias
report: observation distribution, covariance map, restricted-likelihood error
contrasts, or declared estimating moments. State `E[T] = A theta` for the moment
case. A null-space conclusion is relative to that operator and its admissible
parameter domain; it is not automatically a theorem about all information in the
original observations. Fits may carry identified combinations and their joint
uncertainty, together with the remaining parameter fiber. Projection must be
constant over that fiber for a point estimate to be supported. It must not
require arbitrary individual component values when the requested quantity only
uses identified combinations. Exact operators, algorithms and tolerances remain
in the later family specifications.

**Direct falsifier:** with one observation per person–item cell, let the residual
identify only `c = theta_person_item + theta_observation`. For an independently
sampled mean over `I` items, its residual contribution `c/I` is supported. Adding
`k > 1` independent observations of each of the same cells requires
`theta_person_item/I + theta_observation/(I*k)`. This is not constant on
`theta_person_item + theta_observation = c` and is unsupported without further
information. Positive decompositions of the same `c` must agree on the first
request and must not yield a fabricated point answer for the second. This is a
simple reviewer-derived fixture under the stated independent effect model.

**Primary basis:** Brennan CASMA1, printed p. 7, equations 8–10, separates EMS
relations from their observed-moment solutions. Brennan CASMA51, printed pp. 2–4,
equations 3–8, shows the operational one-prompt quantity differs from the intended
new-prompt quantity. Harville (1977), section 4.3, defines REML through error
contrasts satisfying `u'X = 0`. These sources were read locally, not inferred
from catalogue metadata.

## S2 — Mean structure must participate in general projection

**Architecture correction; high severity for the advertised general projection
route, no defect in the existing all-random formula.** Locations: lines 178–189,
261–278, and 306–318.

Resolution: accepted in revised lines 303–309; no remaining correction needed
at overarching-design level.

The covariance identity for `S - U` is exact. The missing contract is the
probability law under which its covariance is computed. Conditional observation
covariance `Cov(y | assignment)` alone does not supply the covariance of a score
whose assignment is randomly selected. The mean structure can vary with the
selected conditions and contribute to absolute error even when it is represented
by fixed coefficients rather than by a random-effect covariance kernel.

**Counterexample:** consider a finite pool with deterministic item offsets
`mu_i`, a random person effect of variance `sigma_p^2`, and independent
observation errors of variance `sigma_e^2`. Draw `I` items independently with
replacement and average them. The universe score is the person's effect plus
the pool-weighted mean offset. Absolute error variance is
`Var_selection(mu_i)/I + sigma_e^2/I`. Conditional on the selected item labels,
`Cov(y)` has no item-offset variance component. Projecting only that covariance
misses `Var_selection(mu_i)/I`, although the numerical scale, protocol and object
population all match. Without-replacement sampling changes the selection term;
it does not remove the need to carry it.

**Proposed correction:** state that general projection consumes the relevant mean
and covariance representation together with the sampling/score operators. When
assignments are random, include both terms of total covariance:

```text
Cov(V) = E_D[Cov(V | D)] + Cov_D(E[V | D]),  V = (S, U).
```

Declare which means/effects are held conditional and which vary under the
replication law. A response/SEM bridge must supply mean/threshold information
when the requested absolute quantity needs it, or explicitly certify that its
mapped covariance already incorporates those contributions. Missing required
mean information makes that projection unsupported. The finite/SEM formulas
themselves can remain deferred.

This finding does **not** claim that absolute G-theory error must automatically
include an external truth-bias term. With `U` defined as the replication
expectation, the overall error mean is zero under that same replication law.
Accuracy relative to an external reference remains a separate contract, as the
design already states.

**Primary basis:** Jorgensen (2021), printed pp. 116–117, Figure 1 and equation 6,
derives the item variance required for absolute dependability from item intercepts
in the SEM mean structure. CFA covariance parameters directly represent the
person-containing components, while the item main-effect contribution needs the
mean structure. Read locally in the acquired full text. The finite-pool example
and total-covariance expression above are direct mathematical deductions, not
claims that Jorgensen specifies that exact sampling design.

## S3 — Comparison must expose a changed universe-score target

**Architecture correction; medium severity.** Locations: lines 143–153,
255–265, and 363–378.

Resolution: accepted in revised lines 283–288; no remaining correction needed
at overarching-design level.

The document allows candidate panels, retained conditions, weights and score
definitions to change, and the universe score is correctly defined from those
choices. Consequently, candidates need not share a target. Compatibility of
component population, scale and protocol does not establish target equivalence.
An optimizer can otherwise report a higher coefficient achieved by narrowing
the generalization universe rather than improving the original measurement.

This is a concrete G-theory failure mode: fixing the essay prompts shifts
person-by-prompt variation into universe-score variation. Both G and Phi can
increase while the procedure has ceased to generalize to new prompts. The
change is legitimate if requested, but it is not evidence of improved precision
for the original new-prompt target. Changing composite weights similarly changes
what is measured; a total over `I` items has universe score `I` times the
mean-score target and requires an explicit mapping when counts change.

**Proposed correction:** every candidate carries its derived universe-score
target, conditioning and metric. Comparison/optimization declares either a
common target, supported explicit mappings to a common target (including units
and thresholds), or an objective that deliberately trades across different
targets. A changed target must be visible in the result and cannot pass silently
as improved dependability for the original target. Do not prohibit legitimate
target tradeoffs or require a general target-equivalence algorithm now.

**Primary basis:** Brennan CASMA1, printed p. 4, explicitly places the prompt
interaction in universe-score variance after fixing prompts, and explains that
the increased coefficients accompany a narrower universe. CASMA51, equations
6 and 8, gives different coefficients for the fixed-prompt and intended
random-prompt interpretations of the same operational data. Armada pp. 5–6 and
12 require target and support conditions to survive the experimental loop.

## S4 — Name the object-population measure when finite objects are supported

**Later-family declaration with a small architecture clarification; low severity.**
Locations: lines 115–116, 137–153, and 292–293.

Resolution: accepted. Final rereview confirms explicit object-population weighting
and the distinction between superpopulation component variance and variance over
a realized finite panel. Specific finite-family transforms remain deferred.

The records name an object population and facet selection probabilities, but do
not say which measure defines reported universe-score variance over objects.
For a finite fixed object set, empirical population variance uses the population
weights (equal weights imply a divisor `N`), whereas an ANOVA component commonly
uses `N-1`. They are not interchangeable numerators. Conditional precision for a
particular object also differs from the population-averaged summary.

**Proposed clarification:** target metadata identifies the object population
measure or weights and whether a result is object-conditional or averaged over
that measure. Finite/fixed-object family specifications state the variance
convention and its relation to their estimated components. No Whimbey correction
should be added globally; that would repeat the blanket finite-correction mistake
the document already avoids.

**Primary basis:** acquired EduG user guide, Appendix A, printed pp. 37–38,
derives the `(N-1)/N` relation for a fixed/finite object facet. This is evidence of
a convention that must be declared, not a recommendation to reproduce every EduG
coefficient family or to equate a fixed facet with a random census.

## Correct boundaries and deferred work

- The definition of universe score as a replication expectation is appropriate.
  Later family specifications must make its conditioning operational, including
  the object-specific state/effects retained in that expectation.
- Aliases need not prevent all inference. The one-prompt example and nonlinear
  invariance requirement are correctly included; S1 makes their data boundary
  enforceable.
- No automatic `1-n/N` rule, automatic dropping of fixed interactions, or
  arbitrary latent-logit/raw-score conversion is advertised. Those safeguards
  should remain.
- Time dependence, informative missingness, heterogeneous multivariate linkage,
  nonlinear response mapping, irregular scoring, and finite sampling deserve
  family-specific derivations. Their absence is explicitly acknowledged and is
  not an overarching-design flaw.
- The capability intersection rule and typed unsupported results are adequate
  guards against an overbroad claim that every declared feature combination is
  implemented. Exact kernel-rank tests and estimator tolerances can remain later
  specifications.
- Armada's distinction between observational ambiguity and hidden generating
  truth is preserved. Learned warnings are correctly denied authority to replace
  the algebraic support check.

## Evidence inspected

Local full-text sections, rather than metadata alone, were inspected for the
findings above:

1. Operator's *Measurement Armada Architecture Notes*, extracted full text and
   `papers/MEASUREMENT_ARMADA.md`, especially pp. 5–6, 8–10 and 12.
2. [Brennan (2003), CASMA1](https://education.uiowa.edu/sites/education.uiowa.edu/files/2026-04/casma-research-report-1-archived.pdf),
   local `papers/downloads/foundations/brennan-2003-coefficients-indices.txt`.
3. [Brennan (2017), CASMA51](https://education.uiowa.edu/sites/education.uiowa.edu/files/2026-04/casma-research-report-51-archived.pdf),
   local `papers/downloads/foundations/brennan-2017-confounded-effects.txt`.
4. [Jorgensen (2021)](https://doi.org/10.3390/psych3020011), local
   `papers/downloads/multivariate/multivariate-sem-absolute-2021.txt`.
5. Harville (1977), local `papers/downloads/estimation/harville-1977.txt`,
   section 4.3; OCR has two-column artifacts, so only the legible error-contrast
   definition and accompanying argument are used.
6. EduG user guide (2010), local
   `papers/downloads/software/edug-user-guide-2010.txt`, Appendix A.

The foundations, multivariate and estimation lane reports supplied context and
source locators. No reference implementation was executed and no dependency was
adopted during this review.
