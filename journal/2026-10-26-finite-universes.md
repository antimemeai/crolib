# Finite universes: admissible region and projection (crolib-3bk)

## The open question

The bead asked whether to parameterize a finite universe with covariance
components or with Cornfield–Tukey finite-population variances:

- **Covariance components** may be negative within the PSD bound, e.g.
  σ²(pi) ≥ −σ²(pir)/N_r.
- **Cornfield–Tukey variances** are never negative.

**Answer: there is nothing to choose; the two are one model in two
coordinates.** Brennan's ACT 26 (1977) Eq. 27 turns the random-model
components into finite-universe components:

σ²(e|N) = Σ_{b⊇e, b∖e⊆F} σ²(b)/Π_{b∖e} N_f

His Eq. 29 then writes every expected mean square as a sum of σ²(b|N) with
coefficients Π n_f Π (1 − n_f/N_f). Under the covariance reading, the expected
mean squares are the contrast eigenvalues of Cov(y). So the covariance is PSD
at every admissible count exactly when every σ²(e|N) ≥ 0.

- Sufficiency holds term by term.
- Necessity: hold each finite facet at its universe size, let the other counts
  grow, and the eigenvalue tends to σ²(e|N) Π_{F∖e} N_f.

The equation numbers were checked against the PDF, pages 55–57: the OCR text is
unreliable.

## What was easy to get wrong

**The grand-mean direction.** The constant eigenvector of Cov(y) also carries a
common shift σ²(∅)J. Under Cornfield–Tukey, finite effects sum to zero, and
that makes σ²(∅) negative whenever a facet is finite. A common shift cannot be
identified from data, and it cancels from every universe score and error
variance; the brute force adds a random σ²(∅) to check this. Admissibility
therefore concerns only the contrast eigenvalues. A first draft of the Sage
check included the grand-mean eigenvalue and failed for F = {p}.

**The residual.** The unreplicated residual is σ²(pir) + σ²(e). Replication
error σ²(e) has an infinite universe, so a finite facet does not correct it.

- With one finite facet the projection depends only on the sum.
- Every σ²(e|N) is nondecreasing in σ²(pir), so the residual is admissible for
  some split exactly when the region holds with σ²(pir) = residual.
- With both facets finite, the error variances depend on the split
  (∂/∂σ²(pir) − ∂/∂σ²(e) = −1/(N_i N_r)). crolib refuses that case
  (`ResidualSplitRequired`). Brennan's two-facet correction implicitly takes
  σ²(e) = 0, which is right only if the universe has no replications.

## Decisions

- **Scope.** One finite facet, items or raters, of the crossed p × i × r
  family. Persons stay an infinite population. A finite universe needs N ≥ 2;
  a single level is a fixed condition, a separate entry in docs/design.md.
- **API.**
  - Rust: `project_in(n_items, n_raters, Universe, Universe)`, with
    `Universe::{Infinite, Finite(N)}`. `project` delegates with both
    infinite, and its arithmetic is unchanged bit for bit.
  - Python: keyword arguments `item_universe` and `rater_universe` on
    `project`.
- **Errors.** New `ProjectionError` variants: `InvalidUniverse`,
  `CountExceedsUniverse`, `ResidualSplitRequired` and
  `BelowUniverseBound(name)`. A component whose bound is zero still gets
  `InvalidComponent`. Corrected bounds are checked after every
  self-bounded component, so a negative residual is reported as the residual,
  not as the component whose bound it feeds. **Adding variants breaks
  exhaustive matches**, so the next release is 0.2.0.
- **Exactness.** The sign of a + b/N decides admissibility, so it is computed
  exactly. Rust aligns integer mantissas in u128. Python uses `Fraction` for
  the whole finite path and rounds each coefficient once. For a negative a,
  Rust also forms N·a + b exactly and rounds it once, which keeps cancellation
  near the bound accurate.

## Verification

- `verify/sage/finite_universe.sage`:
  - contrast eigenvalues on exact matrices;
  - Brennan's identity, symbolic for every finite set F ⊆ {p, i, r};
  - the necessity limits;
  - universe-score, relative and absolute error variances by brute force
    over every without-replacement sample of small finite universes;
  - the residual-split derivatives;
  - the infinite-facet limits, which equal the implemented formulas;
  - Brennan's printed p. 55 items-finite example.
- `verify/sage/finite_projection.py` emits 173 exact cases: 139 defined, 29
  outside the region, 3 invalid, 2 undefined. It computes from the covariance
  form, which the implementations do not evaluate. The cases cover:
  - components exactly on each bound and one ulp below;
  - a non-dyadic bound (fl(1/3));
  - subnormals, 1e308, and counts and universes near 2^64;
  - 80 mixed-magnitude LCG cases;
  - 60 cases in which every term matters.
- **Rust** is within 2 ulp of every case. The test asserts 24, the bound from
  counting roundings, for subnormal and zero results too.
- **Python** equals the correctly rounded value on every case.

## Review

A fresh reviewer fuzzed 30k boundary cases, plus 23k sweeping eb − ea from
−200 to 200. Every admissibility decision matched exact arithmetic. The
infinite path was bit-identical to 0.1.0 on 5M random inputs. Rust and Python
check their errors in the same order.

**Found:**

- **A real bug.** `scale_down` returned 0 below exponent −1078. That was safe
  only for values under 2^4, which 0.1.0 always passed. The finite path can
  pass almost 2^5: a two-term signal over a denominator mantissa near 1/8. In
  that case Rust returned 0 where the exact G, 1.49·2^-1075, rounds to 5e-324.
  - **Fix:** the cutoff is now −1100. Results for 0.1.0's inputs are
    unchanged, since below −1078 they round to 0 either way.
  - **Tests:** the case is now an oracle row, and
    `smallest_subnormal_result_survives_scaling` asserts exactly 5e-324. That
    test fails with the old cutoff.
- **Two test claims the error analysis did not support.** The oracle test had
  used a 1-ulp bound for subnormal results and required zero results to be
  exact. Both now use the 24-ulp bound. A dedicated test checks that a zero
  universe score gives exactly 0.

**Limitation:** the brute force runs with both facets finite, at three
universe-size pairs. The one-facet formulas are symbolic limits of a closed
form that the brute force spot-checks at those sizes; it is not a proof for
every N. They also reproduce Brennan's example.

**Not done:** mutation testing of the new code (crolib-nqq). It runs on the
fleet only.
