# Initial release design and plan

The operator authorized a Blackbird repository and immediate publication of
the `crolib` name on crates.io and PyPI. Publish useful, bounded functionality:
D-study projection from supplied variance components, rather than a placeholder.

## Mathematical contract

For an all-random, crossed person × item × rater design, accept seven finite,
nonnegative variance components: person, item, rater, person_item, person_rater,
item_rater, and residual (the unreplicated three-way interaction plus residual).
Reject zero counts, nonfinite/negative components, and undefined coefficients.

Given positive item and rater counts I and R:

    relative_error = person_item/I + person_rater/R + residual/I/R
    absolute_error = relative_error + item/I + rater/R + item_rater/I/R
    G = person / (person + relative_error)
    Phi = person / (person + absolute_error)

The projection assumes the pilot components describe the same population and
exchangeable item/rater universes as the intended measurement design. Fixed
facets, fitting observations, uncertainty intervals, and general design syntax
are outside this release.

Represent each count-weighted component as a binary mantissa and exponent,
normalize denominator terms by the greatest represented exponent, and perform
the signal/denominator division before applying its final power-of-two scale.
This avoids sum overflow, premature component underflow, and overflow in I*R.
Zero person variance is valid if both coefficients have positive denominators;
a zero denominator is an error, rather than a fabricated reliability of zero.

## Ownership and packaging

Rust and Python implement the small contract independently, without runtime
dependencies. Python uses the already-installed setuptools packaging tool.
This is an initial portable Python implementation, not a Rust extension.
Use MIT licensing and a public `antimemeai/crolib` GitHub repository.

## Plan

1. Review this mathematical and release contract independently (completed;
   review identified premature underflow in the original raw-max normalization,
   motivating the binary representation above).
2. Write failing exact-oracle and metamorphic tests, then implement the kernel.
3. Run tests, lint, package checks, and independent code/release review; address
   findings before publishing.
4. Commit, publish the repository, then publish the crate and Python artifacts.
5. Verify public registry metadata, journal the outcome, and record follow-up work.

Source: Brennan (2001), *Generalizability Theory*, especially the multifacet
D-study treatment. The existing SALib method documentation provides the same
crossed-design equations; its implementation is not copied or modified.
