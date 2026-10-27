//! Finite-universe projection: exact fixtures, the admissible region, and
//! exact rational G and Phi for adversarial inputs (verify/sage/finite_projection.py).
#![cfg(target_pointer_width = "64")]

use crolib::{CrossedComponents, ProjectionError, Universe};

mod oracle {
    include!("oracles/finite_projection.rs");
}

fn panel() -> CrossedComponents {
    // Raters a panel of four. person and person_item are negative, inside
    // person >= -person_rater/4 and person_item >= -residual/4.
    CrossedComponents {
        person: -0.125,
        item: 0.5,
        rater: 0.25,
        person_item: -0.5,
        person_rater: 1.0,
        item_rater: 0.5,
        residual: 4.0,
    }
}

#[test]
fn negative_components_inside_the_region_are_projected() {
    // Universe score 1/8; relative error (1/2)/2 + (1/2)(1/2) + (1/2)(4/4) = 1;
    // absolute error adds (5/8)/2 + (1/2)(1/4)/2 + (1/2)(1/2)/4 = 7/16.
    let r = panel()
        .project_in(2, 2, Universe::Infinite, Universe::Finite(4))
        .unwrap();
    assert_eq!(r.generalizability, 1.0 / 9.0);
    assert_eq!(r.dependability, 2.0 / 25.0);
    // Observing the whole panel leaves only the item terms.
    let census = panel()
        .project_in(2, 4, Universe::Infinite, Universe::Finite(4))
        .unwrap();
    assert_eq!(census.generalizability, 1.0 / 3.0);
    assert_eq!(census.dependability, 2.0 / 11.0);
}

#[test]
fn zero_signal_on_the_bound_is_exactly_zero() {
    // person = -person_rater/4 exactly: the universe score is zero.
    let c = CrossedComponents {
        person: -0.25,
        ..panel()
    };
    let r = c
        .project_in(2, 2, Universe::Infinite, Universe::Finite(4))
        .unwrap();
    assert_eq!((r.generalizability, r.dependability), (0.0, 0.0));
}

#[test]
fn smallest_subnormal_result_survives_scaling() {
    // Review: a two-term signal over a denominator mantissa near 1/8 scales from
    // below 2^5. The exact G is 1.49 * 2^-1075, well past the rounding midpoint,
    // so it must round to 2^-1074; a scaling cutoff once returned zero.
    let size = (1 << 20) - 1;
    let c = CrossedComponents {
        person: 1.99 * 2.0_f64.powi(-116),
        person_item: f64::from_bits(0xfd30000100001000), // -fl(2^1000 / size), inside
        person_rater: 1.99 * 2.0_f64.powi(-97),
        residual: 2.0_f64.powi(1000),
        ..CrossedComponents::default()
    };
    let r = c
        .project_in(
            size,
            (1 << 19) - 1,
            Universe::Infinite,
            Universe::Finite(size),
        )
        .unwrap();
    assert_eq!(r.generalizability, f64::from_bits(1));
}

#[test]
fn outside_the_region_names_the_violated_bound() {
    let c = CrossedComponents {
        person_item: -1.0 - f64::EPSILON,
        ..panel()
    };
    assert_eq!(
        c.project_in(2, 2, Universe::Infinite, Universe::Finite(4)),
        Err(ProjectionError::BelowUniverseBound("person_item"))
    );
    // A component whose bound is zero is invalid when negative.
    let c = CrossedComponents {
        person_rater: -1.0,
        ..panel()
    };
    assert_eq!(
        c.project_in(2, 2, Universe::Infinite, Universe::Finite(4)),
        Err(ProjectionError::InvalidComponent("person_rater"))
    );
    // With items finite instead, person_item's bound is zero.
    assert_eq!(
        panel().project_in(2, 2, Universe::Finite(4), Universe::Infinite),
        Err(ProjectionError::InvalidComponent("person_item"))
    );
}

#[test]
fn infinite_universes_reduce_to_project() {
    let c = CrossedComponents {
        person: 12.0,
        item: 6.0,
        rater: 4.0,
        person_item: 8.0,
        person_rater: 10.0,
        item_rater: 2.0,
        residual: 24.0,
    };
    assert_eq!(
        c.project_in(4, 2, Universe::Infinite, Universe::Infinite),
        c.project(4, 2)
    );
    // Every component must then be nonnegative, the first negative one named.
    assert_eq!(
        panel().project_in(2, 2, Universe::Infinite, Universe::Infinite),
        Err(ProjectionError::InvalidComponent("person"))
    );
    // A universe far larger than the counts approaches the infinite result.
    let near = c
        .project_in(4, 2, Universe::Infinite, Universe::Finite(1 << 50))
        .unwrap();
    let far = c.project(4, 2).unwrap();
    assert!((near.generalizability - far.generalizability).abs() < 1e-14);
    assert!((near.dependability - far.dependability).abs() < 1e-14);
}

#[test]
fn facet_swap_symmetry() {
    let c = panel();
    let swapped = CrossedComponents {
        item: c.rater,
        rater: c.item,
        person_item: c.person_rater,
        person_rater: c.person_item,
        ..c
    };
    assert_eq!(
        swapped.project_in(2, 2, Universe::Finite(4), Universe::Infinite),
        c.project_in(2, 2, Universe::Infinite, Universe::Finite(4))
    );
}

#[test]
fn reject_invalid_universes() {
    let c = panel();
    for size in [0, 1] {
        assert_eq!(
            c.project_in(1, 1, Universe::Infinite, Universe::Finite(size)),
            Err(ProjectionError::InvalidUniverse)
        );
    }
    assert_eq!(
        c.project_in(1, 5, Universe::Infinite, Universe::Finite(4)),
        Err(ProjectionError::CountExceedsUniverse)
    );
    assert_eq!(
        c.project_in(0, 1, Universe::Infinite, Universe::Finite(4)),
        Err(ProjectionError::InvalidCount)
    );
    assert_eq!(
        c.project_in(2, 2, Universe::Finite(4), Universe::Finite(4)),
        Err(ProjectionError::ResidualSplitRequired)
    );
    let c = CrossedComponents {
        person: f64::NAN,
        ..panel()
    };
    assert_eq!(
        c.project_in(2, 2, Universe::Infinite, Universe::Finite(4)),
        Err(ProjectionError::InvalidComponent("person"))
    );
}

#[test]
fn error_messages_name_the_problem() {
    assert_eq!(
        ProjectionError::BelowUniverseBound("person_item").to_string(),
        "person_item variance is below its finite-universe bound"
    );
    assert_eq!(
        ProjectionError::InvalidUniverse.to_string(),
        "a finite universe needs at least two levels"
    );
    assert_eq!(
        ProjectionError::CountExceedsUniverse.to_string(),
        "a count cannot exceed its facet's finite universe"
    );
    assert_eq!(
        ProjectionError::ResidualSplitRequired.to_string(),
        "with both facets finite, the residual's interaction and error must be separated"
    );
}

fn ulps(a: f64, b: f64) -> u64 {
    a.to_bits().abs_diff(b.to_bits())
}

/// Each term carries at most eight roundings (four count conversions and four
/// operations), summing at most ten terms nine more, the signal four and the
/// final division one: 22 units of roundoff, so 23 ulp after the oracle's own
/// rounding. Subnormal results are no better: those roundings precede the
/// last one, and near a rounding midpoint even zero can differ by an ulp.
const BOUND: u64 = 24;

#[test]
fn finite_projection_matches_exact_oracle() {
    use oracle::Expected;
    let universe = |size: u64| match size {
        0 => Universe::Infinite,
        n => Universe::Finite(n as usize),
    };
    let mut worst = 0;
    for (bits, ni, nr, items, raters, expected) in oracle::FINITE_CASES {
        let c = bits.map(f64::from_bits);
        let components = CrossedComponents {
            person: c[0],
            item: c[1],
            rater: c[2],
            person_item: c[3],
            person_rater: c[4],
            item_rater: c[5],
            residual: c[6],
        };
        let got = components.project_in(
            *ni as usize,
            *nr as usize,
            universe(*items),
            universe(*raters),
        );
        let tag = format!("{c:?} at ({ni}, {nr}) in ({items}, {raters})");
        match expected {
            Expected::Defined(g, phi) => {
                let r = got.unwrap_or_else(|e| panic!("{tag}: {e}"));
                for (name, got, exact) in [
                    ("G", r.generalizability, f64::from_bits(*g)),
                    ("Phi", r.dependability, f64::from_bits(*phi)),
                ] {
                    let d = ulps(got, exact);
                    assert!(
                        d <= BOUND,
                        "{name} for {tag}: {got:e} vs {exact:e}, {d} ulp"
                    );
                    worst = worst.max(d);
                }
            }
            Expected::InvalidComponent(name) => {
                assert_eq!(got, Err(ProjectionError::InvalidComponent(name)), "{tag}")
            }
            Expected::BelowUniverseBound(name) => {
                assert_eq!(got, Err(ProjectionError::BelowUniverseBound(name)), "{tag}")
            }
            Expected::UndefinedCoefficient => {
                assert_eq!(got, Err(ProjectionError::UndefinedCoefficient), "{tag}")
            }
        }
    }
    eprintln!("worst distance: {worst} ulp");
}
