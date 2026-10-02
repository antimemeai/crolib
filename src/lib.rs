//! Generalizability theory for all-random, crossed person × item × rater designs.
//!
//! Supply estimated **variance** components and project reliability to a new
//! number of exchangeable items and raters. This release does not fit raw data.
//!
//! ```
//! use crolib::CrossedComponents;
//! let c = CrossedComponents { person: 12.0, item: 6.0, rater: 4.0,
//!     person_item: 8.0, person_rater: 10.0, item_rater: 2.0, residual: 24.0 };
//! let result = c.project(4, 2)?;
//! assert!((result.generalizability - 6.0 / 11.0).abs() < 1e-14);
//! # Ok::<(), crolib::ProjectionError>(())
//! ```

use std::fmt;

/// Seven variance components for an all-random crossed design.
///
/// Values must be finite and nonnegative. Validation occurs in [`Self::project`].
#[derive(Debug, Clone, Copy, Default, PartialEq)]
pub struct CrossedComponents {
    /// Variance across objects of measurement (persons).
    pub person: f64,
    /// Item variance.
    pub item: f64,
    /// Rater variance.
    pub rater: f64,
    /// Person × item interaction variance.
    pub person_item: f64,
    /// Person × rater interaction variance.
    pub person_rater: f64,
    /// Item × rater interaction variance.
    pub item_rater: f64,
    /// Three-way interaction plus observational error for unreplicated data.
    pub residual: f64,
}

/// Relative and absolute reliability for a proposed measurement design.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Reliability {
    /// G (Eρ²): reliability for relative decisions.
    pub generalizability: f64,
    /// Phi (Φ): dependability for absolute decisions.
    pub dependability: f64,
}

/// Invalid or undefined D-study projection.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProjectionError {
    /// Item and rater counts must both be positive.
    InvalidCount,
    /// The named component is negative or nonfinite.
    InvalidComponent(&'static str),
    /// At least one coefficient has a zero denominator.
    UndefinedCoefficient,
}

impl fmt::Display for ProjectionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidCount => f.write_str("item and rater counts must be positive"),
            Self::InvalidComponent(name) => {
                write!(f, "{name} variance must be finite and nonnegative")
            }
            Self::UndefinedCoefficient => {
                f.write_str("reliability is undefined for a zero denominator")
            }
        }
    }
}

impl std::error::Error for ProjectionError {}

impl CrossedComponents {
    /// Project G and Phi to positive item and rater counts.
    ///
    /// The supplied components must describe the same population and random
    /// item/rater universes as the proposed design. Fixed facets are unsupported.
    /// Zero signal is allowed when both error denominators are positive.
    pub fn project(&self, n_items: usize, n_raters: usize) -> Result<Reliability, ProjectionError> {
        if n_items == 0 || n_raters == 0 {
            return Err(ProjectionError::InvalidCount);
        }
        for (name, value) in [
            ("person", self.person),
            ("item", self.item),
            ("rater", self.rater),
            ("person_item", self.person_item),
            ("person_rater", self.person_rater),
            ("item_rater", self.item_rater),
            ("residual", self.residual),
        ] {
            if !value.is_finite() || value < 0.0 {
                return Err(ProjectionError::InvalidComponent(name));
            }
        }
        let items = parts(n_items as f64);
        let raters = parts(n_raters as f64);
        let signal = parts(self.person);
        let relative = [
            signal,
            weighted(self.person_item, items, (1.0, 0)),
            weighted(self.person_rater, raters, (1.0, 0)),
            weighted(self.residual, items, raters),
        ];
        let absolute = [
            relative[0],
            relative[1],
            relative[2],
            relative[3],
            weighted(self.item, items, (1.0, 0)),
            weighted(self.rater, raters, (1.0, 0)),
            weighted(self.item_rater, items, raters),
        ];
        Ok(Reliability {
            generalizability: coefficient(signal, &relative)?,
            dependability: coefficient(signal, &absolute)?,
        })
    }
}

// Keep count-weighted terms in binary scientific notation until the final
// division. This avoids both sum overflow and premature subnormal underflow.
fn parts(value: f64) -> (f64, i32) {
    if value == 0.0 {
        return (0.0, 0);
    }
    if value < f64::MIN_POSITIVE {
        let (mantissa, exponent) = parts(value * 4_503_599_627_370_496.0); // exact 2^52
        return (mantissa, exponent - 52);
    }
    let bits = value.to_bits();
    let exponent = ((bits >> 52) & 0x7ff) as i32 - 1023;
    let mantissa = f64::from_bits((bits & ((1_u64 << 52) - 1)) | (1023_u64 << 52));
    (mantissa, exponent)
}

fn weighted(value: f64, first: (f64, i32), second: (f64, i32)) -> (f64, i32) {
    let (mantissa, exponent) = parts(value);
    (mantissa / first.0 / second.0, exponent - first.1 - second.1)
}

fn scale_down(value: f64, exponent: i32) -> f64 {
    if exponent >= -1022 {
        value * 2.0_f64.powi(exponent)
    } else if exponent >= -1078 {
        // Scale in the normal range first, then round to the subnormal result.
        (value * 2.0_f64.powi(exponent + 1022)) * f64::MIN_POSITIVE
    } else {
        0.0
    }
}

fn coefficient(signal: (f64, i32), terms: &[(f64, i32)]) -> Result<f64, ProjectionError> {
    let max_exponent = terms
        .iter()
        .filter(|term| term.0 > 0.0)
        .map(|term| term.1)
        .max()
        .ok_or(ProjectionError::UndefinedCoefficient)?;
    if signal.0 == 0.0 {
        return Ok(0.0);
    }
    let denominator: f64 = terms
        .iter()
        .filter(|term| term.0 > 0.0)
        .map(|term| scale_down(term.0, term.1 - max_exponent))
        .sum();
    // Divide before tiny scaling: a denominator < 1 can rescue a representable
    // subnormal numerator that would otherwise disappear.
    Ok(scale_down(signal.0 / denominator, signal.1 - max_exponent))
}
