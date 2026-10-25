# Mutation characterization of the oracle suites (crolib-hmz)

The new Sage oracles and exact tests in crolib and salib need their power
measured by mutation, on the fleet only (Blackbird).

**Tool.** `cargo-mutants` v27.1.0, installed on neuroses with
`cargo install --locked -j 8`. It is a development tool, like the
`cargo-kani` already there; neither repository depends on it. Builds are
capped at 8 jobs, because both earlier neuroses crashes followed heavy jobs.

**Targets.**
- **crolib:** `src/lib.rs` (the projection kernel) against `cargo test`.
- **salib:** `crates/salib-estimators/src/g_theory.rs` against
  salib-estimators with the `serde` feature, and
  `crates/salib-validation/src/{sobol_g,ishigami}.rs` against
  salib-validation.

**Reading.** Each missed mutant is either equivalent (no observable change;
recorded) or a test gap (strengthen the relevant oracle, test-first).
Timeouts are reported separately. crolib's Python implementation has no
mutation tool on hand; adopting one would be a separate decision, so it is
recorded as a gap.

## Results (run 2026-10-25 on neuroses, crolib 688e149)

crolib `src/lib.rs`: 82 caught, 4 missed, 2 unviable out of 88 mutants.
- **Gap:** the `ProjectionError` `Display` messages were never checked.
  Added `error_messages_name_the_problem`, which pins each variant's text.
- **Equivalent:** `parts` `<` → `<=` at `MIN_POSITIVE`. The subnormal route
  scales by exactly 2^52 and subtracts 52 from the exponent, giving the same
  (mantissa, exponent).
- **Equivalent:** `parts` `|` → `^` when joining mantissa and exponent bits.
  The masked fields do not overlap, so OR equals XOR.
- **Equivalent:** `scale_down` `>= -1022` → `>= 1022`. Callers pass only
  exponents ≤ 0, because terms are normalized to the largest exponent. For
  those, the alternate branch computes the same exact power-of-two product.

salib results are recorded in salib's journal.
