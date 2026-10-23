# Sage oracles for the projection (crolib-hmz target 4)

`verify/sage/projection.py` generates exact projection oracles. It is plain
Python run with the Sage environment's interpreter, because Sage's
preparser turns literals into Sage numbers that `Fraction` rejects.
- Every f64 input is an exact rational, so G and Phi are exact rationals
  under the README's definitions.
- Python's `Fraction` → `float` rounds correctly, subnormals included.
  Sage's `RealField(53)` has no subnormals and would round the tiniest cases
  wrongly.
- There are 49 cases: README examples, 1e308 components, subnormal
  components, counts of 10¹⁹ and 2⁶⁴ − 1, mixed 1e±300 magnitudes, and 40
  mixed-magnitude cases from a script-local LCG (no Sage RNG).

The script emits `tests/oracles/projection.rs` (bit patterns, because
`f64::from_bits` is const only from Rust 1.83 and the MSRV is 1.74) and
`python/tests/projection_oracle.py`. Both are included unformatted, so
`scripts/sage-check.sh` detects drift against HEAD.

**Result:** both implementations are within 1 ulp of the correctly rounded
exact value on every case. The tests assert 8 ulp, the order of the worst
case for seven rounded terms and one division.

Replaced, under the one-layer rule:
- Python's Decimal-oracle test (`test_tiny_representable_coefficient_decimal_oracle`);
- Rust's hand-bounded `count_scaling_preserves_representable_tiny_coefficient`.

Both covered the 1e-200/1e150 case at 10¹⁹ counts, which is now an exact
oracle case. The hand-computed spec tests stay.

`scripts/sage-check.sh` skips `balanced.sage`, which is a library loaded by
salib's scripts, and runs `.sage` files through Sage and `.py` files through
the Sage environment's python.

## Review

A fresh reviewer confirmed the exact computation is right:
- `Fraction`-to-float conversion rounds correctly, subnormals included;
- all 49 cases are defined;
- the generator is byte-identical on re-run;
- `unittest discover` imports the oracle under the CI layout, and both the
  sdist and `cargo package` include the oracles.

The case set was weak, though. Four plausible bugs in the binary-scaling code
passed every test, the old ones included:
- treating subnormals as normal;
- an off-by-one exponent in `parts`;
- a −1074 cutoff where the code uses −1078;
- scaling before dividing.

The reasons:
- 20 of the 49 cases had G ∈ {0, 1}, and 33 reduced to a single division;
- subnormals never mixed with normal components;
- no result landed in the lowest exponent window;
- bit distance cannot tell 0 from 2^-1074, which are 1 ulp apart.

Fixed:
- added the reviewer's two mixed subnormal/normal cases, and an exact
  G = 2^-1074 case (person 1.5·2^-139, residual 2^1000, counts 2^32 − 1);
- added 60 nondegenerate cases, in which all seven count-weighted terms sit
  within ±4 bits of a common base, with unequal counts. That makes 112 cases
  in all, only 18 of them with G ∈ {0, 1};
- the tests require zero-ness to match exactly, and 1 ulp when the exact
  value is subnormal (a single final rounding). Otherwise the bound stays at
  8 ulp.

The reviewer reported that its proposed cases kill all four bugs. I did not
re-run those injected-bug checks here: mutation runs belong on the fleet.
Characterizing the suite with mutants is recorded on crolib-hmz.
