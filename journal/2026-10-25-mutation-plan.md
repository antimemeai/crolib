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
