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
let reliability = components.project(4, 2)?;
assert!((reliability.generalizability - 6.0 / 11.0).abs() < 1e-14);
# Ok::<(), crolib::ProjectionError>(())
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
than silently clipped. Computations normalize components to avoid overflow.

Projection assumes the supplied components describe the same population and
exchangeable item/rater universes as the proposed design. This release does not
estimate components from raw observations, support fixed/nested facets, or
calculate uncertainty intervals. General design support, fitting, unbalanced
estimation, and multivariate G-theory are planned research and development.

Reference: Brennan, R. L. (2001), *Generalizability Theory*, Springer,
[doi:10.1007/978-1-4757-3456-0](https://doi.org/10.1007/978-1-4757-3456-0).

## Development

Read `AGENTS.md` and `BLACKBIRD.md`. Run `scripts/check.sh` to check Rust and
Python behavior. Research lives in `papers/`, decisions in `journal/`, and the
initial work queue in `issues/`. Project-specific references and private working
material belong in ignored `quarantine/` and `context/`.

MIT licensed.
