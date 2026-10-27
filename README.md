# crolib

Generalizability theory and measurement design for Rust and Python.
Named for Lee Cronbach, a founder of generalizability theory.

**Initial release (0.1.0):** project relative reliability (G) and absolute
dependability (Phi) from supplied variance components for an all-random,
crossed person × item × rater design. Both implementations have no runtime
dependencies. Python is currently a portable implementation, not a Rust binding.

## Python

```sh
pip install crolib
```

```python
from crolib import CrossedComponents

components = CrossedComponents(
    person=12.0, item=6.0, rater=4.0,
    person_item=8.0, person_rater=10.0, item_rater=2.0, residual=24.0,
)
reliability = components.project(n_items=4, n_raters=2)
print(reliability.generalizability)  # 0.5454545454545454
print(reliability.dependability)     # 0.46601941747572817
```

## Rust

```toml
[dependencies]
crolib = "0.1"
```

```rust
use crolib::CrossedComponents;

let components = CrossedComponents {
    person: 12.0, item: 6.0, rater: 4.0,
    person_item: 8.0, person_rater: 10.0, item_rater: 2.0, residual: 24.0,
};
let reliability = components.project(4, 2).expect("valid crossed components");
assert!((reliability.generalizability - 6.0 / 11.0).abs() < 1e-14);
```

## Mathematical scope

For item count I and rater count R:

```text
relative_error = person_item/I + person_rater/R + residual/I/R
absolute_error = relative_error + item/I + rater/R + item_rater/I/R
G   = person / (person + relative_error)
Phi = person / (person + absolute_error)
```

The residual component combines the three-way interaction and observational
error in an unreplicated design. Inputs are variances, not standard deviations.
Components must be finite and nonnegative; counts must be positive integers.
Undefined coefficients produce an error. Negative estimates are rejected rather
than silently clipped. Binary scaling avoids overflowing sums and premature
underflow of count-weighted components.

Projection assumes the supplied components describe the same population and
exchangeable item/rater universes as the proposed design (see below for finite
universes on `main`). This release does not
estimate components from raw observations, support fixed/nested facets, or
calculate uncertainty intervals. General design support, fitting, unbalanced
estimation, and multivariate G-theory are planned research and development.

Reference: Brennan, R. L. (2001), *Generalizability Theory*, Springer,
[doi:10.1007/978-1-4757-3456-0](https://doi.org/10.1007/978-1-4757-3456-0).

## Finite universes (on `main`, unreleased)

One facet may be drawn from a finite universe of N levels, such as a fixed
panel of raters. Its n ≤ N levels are sampled without replacement, and the
universe score averages over all N. The components are still the
random-model components a G study estimates. Brennan's (1977, ACT Technical
Bulletin 26, Eq. 27) finite-universe components then set the projection. With
raters finite and c = 1 − n_raters/N:

```text
universe_score = person + person_rater/N
relative_error = (person_item + residual/N)/I + c person_rater/R + c residual/I/R
absolute_error = relative_error + (item + item_rater/N)/I + c rater/R + c item_rater/I/R
```

and symmetrically for finite items. Each finite-universe component must be
nonnegative, which is exactly the condition for the score covariance to be
positive semidefinite. Three components may therefore be negative within a
bound: with raters finite, `person >= -person_rater/N`,
`item >= -item_rater/N` and `person_item >= -residual/N`. A component outside
its bound is rejected by name, and the check is exact. Negative values are
neither clipped nor repaired. Both facets finite is refused: the projection
would then depend on how the residual divides between three-way interaction
and replication error, which an unreplicated design does not separate.

```rust
use crolib::{CrossedComponents, Universe};

let panel = CrossedComponents {
    person: -0.125, item: 0.5, rater: 0.25,
    person_item: -0.5, person_rater: 1.0, item_rater: 0.5, residual: 4.0,
};
let r = panel.project_in(2, 2, Universe::Infinite, Universe::Finite(4)).unwrap();
assert_eq!(r.generalizability, 1.0 / 9.0);
assert_eq!(r.dependability, 2.0 / 25.0);
```

```python
from crolib import CrossedComponents

panel = CrossedComponents(person=-0.125, item=0.5, rater=0.25, person_item=-0.5,
                          person_rater=1, item_rater=0.5, residual=4)
r = panel.project(2, 2, rater_universe=4)   # item_universe=None: infinite
print(r.generalizability, r.dependability)  # 0.1111111111111111 0.08
```

`verify/sage/finite_universe.sage` derives the region and the formulas from
the covariance model, by symbolic algebra and by brute force over finite
universes. Rust's rounding error is at most 23 ulp (2 observed on the exact
oracle cases); Python computes in exact rationals and rounds once.

## Development

Read `AGENTS.md` and `BLACKBIRD.md`. Run `scripts/check.sh` to check Rust and
Python behavior. The [overarching design](docs/design.md) connects the acquired
corpus to the Measurement Armada and describes proposed study, fitting,
projection, uncertainty and allocation contracts. Its future capabilities are
distinct from the implemented 0.1.0 API above.

The [research corpus](papers/README.md) lives in `papers/`, decisions in
`journal/`, and the work queue in `issues/`. Project-specific references and
private working material belong in ignored `quarantine/` and `context/`.

MIT licensed.
