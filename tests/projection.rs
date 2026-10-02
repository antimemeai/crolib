use crolib::{CrossedComponents, ProjectionError};

fn example() -> CrossedComponents {
    CrossedComponents {
        person: 12.0,
        item: 6.0,
        rater: 4.0,
        person_item: 8.0,
        person_rater: 10.0,
        item_rater: 2.0,
        residual: 24.0,
    }
}

#[test]
fn hand_computed_projection() {
    let result = example().project(4, 2).unwrap();
    // Relative error = 2+5+3; absolute error adds 1.5+2+0.25.
    assert!((result.generalizability - 6.0 / 11.0).abs() < 1e-14);
    assert!((result.dependability - 48.0 / 103.0).abs() < 1e-14);
}

#[test]
fn scale_and_facet_swap_invariance() {
    let base = example().project(4, 2).unwrap();
    for scale in [1e-300, 1e300] {
        let mut c = example();
        c.person *= scale;
        c.item *= scale;
        c.rater *= scale;
        c.person_item *= scale;
        c.person_rater *= scale;
        c.item_rater *= scale;
        c.residual *= scale;
        let actual = c.project(4, 2).unwrap();
        assert!((actual.generalizability - base.generalizability).abs() < 1e-14);
        assert!((actual.dependability - base.dependability).abs() < 1e-14);
    }
    let c = example();
    let swapped = CrossedComponents {
        item: c.rater,
        rater: c.item,
        person_item: c.person_rater,
        person_rater: c.person_item,
        ..c
    };
    assert_eq!(swapped.project(2, 4).unwrap(), base);
}

#[test]
fn more_measurements_improve_reliability() {
    let c = example();
    let small = c.project(2, 2).unwrap();
    let large = c.project(4, 4).unwrap();
    assert!(large.generalizability > small.generalizability);
    assert!(large.dependability > small.dependability);
    assert!(large.dependability <= large.generalizability);
}

#[test]
fn large_sums_and_subnormal_components() {
    let c = CrossedComponents {
        person: 1e308,
        person_item: 1e308,
        ..CrossedComponents::default()
    };
    assert_eq!(c.project(1, 1).unwrap().generalizability, 0.5);
    let tiny = f64::from_bits(1);
    let c = CrossedComponents {
        person: tiny,
        residual: tiny,
        ..CrossedComponents::default()
    };
    assert_eq!(c.project(2, 1).unwrap().generalizability, 2.0 / 3.0);
}

#[cfg(target_pointer_width = "64")]
#[test]
fn count_scaling_preserves_representable_tiny_coefficient() {
    let c = CrossedComponents {
        person: 1e-200,
        residual: 1e150,
        ..CrossedComponents::default()
    };
    let actual = c
        .project(10_000_000_000_000_000_000, 10_000_000_000_000_000_000)
        .unwrap()
        .generalizability;
    // Decimal evaluation: 1e-200 / (1e-200 + 1e150 / 1e19 / 1e19).
    assert!(actual > 0.0);
    assert!((actual - 1e-312).abs() <= f64::from_bits(2));
}

#[test]
fn zero_signal_is_valid_when_error_is_positive() {
    let c = CrossedComponents {
        person_item: 1.0,
        ..CrossedComponents::default()
    };
    let result = c.project(1, 1).unwrap();
    assert_eq!(result.generalizability, 0.0);
    assert_eq!(result.dependability, 0.0);
}

#[test]
fn reject_invalid_and_undefined_inputs() {
    assert!(matches!(
        example().project(0, 1),
        Err(ProjectionError::InvalidCount)
    ));
    for bad in [-1.0, f64::NAN, f64::INFINITY] {
        let c = CrossedComponents {
            person: bad,
            ..example()
        };
        assert!(matches!(
            c.project(1, 1),
            Err(ProjectionError::InvalidComponent("person"))
        ));
    }
    assert!(matches!(
        CrossedComponents::default().project(1, 1),
        Err(ProjectionError::UndefinedCoefficient)
    ));
    let c = CrossedComponents {
        item: 1.0,
        ..CrossedComponents::default()
    };
    assert!(matches!(
        c.project(1, 1),
        Err(ProjectionError::UndefinedCoefficient)
    ));
}
