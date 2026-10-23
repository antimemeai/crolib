//! Projection against exact rational G and Phi, correctly rounded, for
//! adversarial inputs (verify/sage/projection.py).
#![cfg(target_pointer_width = "64")]

use crolib::CrossedComponents;

// Included rather than declared as a module so rustfmt leaves the generated
// source byte-identical.
mod oracle {
    include!("oracles/projection.rs");
}

/// Distance in units of the last place between two nonnegative f64 values;
/// their bit patterns are ordered, subnormals included.
fn ulps(a: f64, b: f64) -> u64 {
    a.to_bits().abs_diff(b.to_bits())
}

#[test]
fn projection_matches_exact_coefficients() {
    let mut worst = 0;
    for (bits, ni, nr, g, phi) in oracle::PROJECTION_CASES {
        let c = bits.map(f64::from_bits);
        let (g, phi) = (f64::from_bits(*g), f64::from_bits(*phi));
        let components = CrossedComponents {
            person: c[0],
            item: c[1],
            rater: c[2],
            person_item: c[3],
            person_rater: c[4],
            item_rater: c[5],
            residual: c[6],
        };
        let r = components
            .project(*ni as usize, *nr as usize)
            .expect("oracle cases are defined");
        for (name, got, exact) in [("G", r.generalizability, g), ("Phi", r.dependability, phi)] {
            let d = ulps(got, exact);
            worst = worst.max(d);
            assert!(
                d <= 8,
                "{name} for {c:?} at ({ni}, {nr}): got {got:e}, exact {exact:e}, {d} ulp"
            );
        }
    }
    eprintln!("worst distance: {worst} ulp");
}
