//! Generalizability theory for crossed person × item × rater designs.
//!
//! Supply estimated **variance** components and project reliability to a new
//! number of items and raters, drawn from infinite universes or, for one facet,
//! from a finite universe. This release does not fit raw data.
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
/// These are random-model components, the values an ANOVA G study estimates.
/// Values must be finite. [`Self::project`] requires them to be nonnegative;
/// [`Self::project_in`] admits the negative values a finite universe allows.
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

/// The universe a D-study facet's levels are drawn from.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Universe {
    /// Exchangeable levels from an unbounded universe, as in [`CrossedComponents::project`].
    Infinite,
    /// A universe of this many levels (at least two), sampled without replacement.
    Finite(usize),
}

/// Invalid or undefined D-study projection.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProjectionError {
    /// Item and rater counts must both be positive.
    InvalidCount,
    /// The named component is nonfinite, or negative where its bound is zero.
    InvalidComponent(&'static str),
    /// At least one coefficient has a zero denominator.
    UndefinedCoefficient,
    /// A finite universe has fewer than two levels.
    InvalidUniverse,
    /// A count exceeds its facet's finite universe.
    CountExceedsUniverse,
    /// Both facets are finite. The residual's three-way interaction and its
    /// replication error then project differently and are not separated.
    ResidualSplitRequired,
    /// The named component is below its finite-universe bound: the implied
    /// score covariance is not positive semidefinite.
    BelowUniverseBound(&'static str),
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
            Self::InvalidUniverse => f.write_str("a finite universe needs at least two levels"),
            Self::CountExceedsUniverse => {
                f.write_str("a count cannot exceed its facet's finite universe")
            }
            Self::ResidualSplitRequired => f.write_str(
                "with both facets finite, the residual's interaction and error must be separated",
            ),
            Self::BelowUniverseBound(name) => {
                write!(f, "{name} variance is below its finite-universe bound")
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
        self.project_in(n_items, n_raters, Universe::Infinite, Universe::Infinite)
    }

    /// Project G and Phi with items and raters drawn from the given universes.
    ///
    /// With both universes infinite this is [`Self::project`]. With one facet
    /// finite, of size N, its n levels are sampled without replacement, and the
    /// universe score averages over all N. Brennan's (1977) finite-universe
    /// components then set the projection:
    ///
    /// ```text
    /// raters finite, c = 1 - n_raters/N:
    /// universe score = person + person_rater/N
    /// relative error = (person_item + residual/N)/I + c person_rater/R + c residual/(I R)
    /// absolute error = relative error + (item + item_rater/N)/I + c rater/R + c item_rater/(I R)
    /// ```
    ///
    /// and symmetrically for finite items. Each finite-universe component must
    /// be nonnegative, which is exactly positive semidefiniteness of the score
    /// covariance. Three components may therefore be negative: with raters
    /// finite, `person >= -person_rater/N`, `item >= -item_rater/N` and
    /// `person_item >= -residual/N`; with items finite, `person >= -person_item/N`,
    /// `rater >= -item_rater/N` and `person_rater >= -residual/N`. The residual
    /// bound takes all of it as three-way interaction, the most permissive split;
    /// the projection does not depend on the split. These checks are exact.
    ///
    /// Both facets finite is refused: the projection would then depend on how
    /// the residual divides between interaction and replication error.
    ///
    /// ```
    /// use crolib::{CrossedComponents, ProjectionError, Universe};
    /// let panel = CrossedComponents { person: -0.125, item: 0.5, rater: 0.25,
    ///     person_item: -0.5, person_rater: 1.0, item_rater: 0.5, residual: 4.0 };
    /// let r = panel.project_in(2, 2, Universe::Infinite, Universe::Finite(4))?;
    /// assert_eq!((r.generalizability, r.dependability), (1.0 / 9.0, 2.0 / 25.0));
    /// let outside = CrossedComponents { person_item: -1.5, ..panel };
    /// assert_eq!(
    ///     outside.project_in(2, 2, Universe::Infinite, Universe::Finite(4)),
    ///     Err(ProjectionError::BelowUniverseBound("person_item"))
    /// );
    /// # Ok::<(), ProjectionError>(())
    /// ```
    pub fn project_in(
        &self,
        n_items: usize,
        n_raters: usize,
        items: Universe,
        raters: Universe,
    ) -> Result<Reliability, ProjectionError> {
        if n_items == 0 || n_raters == 0 {
            return Err(ProjectionError::InvalidCount);
        }
        let item_size = universe_size(items, n_items)?;
        let rater_size = universe_size(raters, n_raters)?;
        // Name the facets by role: `n` is the facet that may be finite, `m` the other.
        let roles = match (item_size, rater_size) {
            (Some(_), Some(_)) => return Err(ProjectionError::ResidualSplitRequired),
            (Some(size), None) => Roles {
                size: Some(size),
                m: n_raters,
                n: n_items,
                cross: self.person_rater,
                nested: self.person_item,
                main: self.rater,
                facet: self.item,
                corrected: ["person", "rater", "person_rater"],
            },
            (None, size) => Roles {
                size,
                m: n_items,
                n: n_raters,
                cross: self.person_item,
                nested: self.person_rater,
                main: self.item,
                facet: self.rater,
                corrected: ["person", "item", "person_item"],
            },
        };
        let fields = [
            ("person", self.person),
            ("item", self.item),
            ("rater", self.rater),
            ("person_item", self.person_item),
            ("person_rater", self.person_rater),
            ("item_rater", self.item_rater),
            ("residual", self.residual),
        ];
        let may_be_negative = |name| roles.size.is_some() && roles.corrected.contains(&name);
        for (name, value) in fields {
            if !value.is_finite() || (value < 0.0 && !may_be_negative(name)) {
                return Err(ProjectionError::InvalidComponent(name));
            }
        }
        // The finite-universe components a + b/N, in field order.
        let signal = roles.bounded(roles.corrected[0], self.person, roles.nested)?;
        let main = roles.bounded(roles.corrected[1], roles.main, self.item_rater)?;
        let cross = roles.bounded(roles.corrected[2], roles.cross, self.residual)?;

        let m = parts(roles.m as f64);
        let n = parts(roles.n as f64);
        // A finite facet divides the corrected components by N and multiplies
        // its sampling terms by c = (N - n)/N. With no finite facet both lists
        // are empty, which keeps 0.1.0's arithmetic exactly.
        let (size, fpc) = match roles.size {
            Some(size) => (
                vec![parts(size as f64)],
                vec![parts((size - roles.n) as f64)],
            ),
            None => (vec![], vec![]),
        };
        let over_n: Vec<_> = size.iter().copied().chain([n]).collect();
        let over_mn: Vec<_> = size.iter().copied().chain([m, n]).collect();
        let mut signal_terms = Vec::new();
        signal.push_terms(&mut signal_terms, &size, &[]);
        let mut relative = signal_terms.clone();
        cross.push_terms(&mut relative, &size, &[m]);
        relative.push(scaled(roles.nested, &fpc, &over_n));
        relative.push(scaled(self.residual, &fpc, &over_mn));
        let mut absolute = relative.clone();
        main.push_terms(&mut absolute, &size, &[m]);
        absolute.push(scaled(roles.facet, &fpc, &over_n));
        absolute.push(scaled(self.item_rater, &fpc, &over_mn));
        Ok(Reliability {
            generalizability: coefficient(&signal_terms, &relative)?,
            dependability: coefficient(&signal_terms, &absolute)?,
        })
    }
}

fn universe_size(universe: Universe, count: usize) -> Result<Option<usize>, ProjectionError> {
    match universe {
        Universe::Infinite => Ok(None),
        Universe::Finite(size) if size < 2 => Err(ProjectionError::InvalidUniverse),
        Universe::Finite(size) if count > size => Err(ProjectionError::CountExceedsUniverse),
        Universe::Finite(size) => Ok(Some(size)),
    }
}

/// The components in their roles for a D study in which facet `n` may be finite.
struct Roles {
    size: Option<usize>,
    m: usize,
    n: usize,
    /// Person × the infinite facet.
    cross: f64,
    /// Person × the possibly finite facet.
    nested: f64,
    /// The infinite facet.
    main: f64,
    /// The possibly finite facet.
    facet: f64,
    /// Fields whose finite-universe component adds a higher term over N.
    corrected: [&'static str; 3],
}

/// A finite-universe component a + b/N, held as nonnegative binary terms.
enum Bounded {
    /// a ≥ 0: the terms a and b/N.
    Split(f64, f64),
    /// a < 0: the exact N·a + b, rounded once, to be divided by N.
    Joint((f64, i32)),
}

impl Roles {
    fn bounded(&self, name: &'static str, a: f64, b: f64) -> Result<Bounded, ProjectionError> {
        match self.size {
            None => Ok(Bounded::Split(a, 0.0)),
            Some(_) if a >= 0.0 => Ok(Bounded::Split(a, b)),
            Some(size) => scaled_sum(a, b, size)
                .map(Bounded::Joint)
                .ok_or(ProjectionError::BelowUniverseBound(name)),
        }
    }
}

impl Bounded {
    /// Push this component divided by `divisors` as nonnegative terms.
    fn push_terms(
        &self,
        terms: &mut Vec<(f64, i32)>,
        size: &[(f64, i32)],
        divisors: &[(f64, i32)],
    ) {
        let over_size = [size, divisors].concat();
        match *self {
            Bounded::Split(a, b) => {
                terms.push(scaled(a, &[], divisors));
                if !size.is_empty() {
                    terms.push(scaled(b, &[], &over_size));
                }
            }
            Bounded::Joint(joint) => terms.push(scaled_parts(joint, &[], &over_size)),
        }
    }
}

/// N·a + b for a < 0 ≤ b, with its sign decided exactly: `None` when it is
/// negative, otherwise its binary parts after one rounding.
fn scaled_sum(a: f64, b: f64, size: usize) -> Option<(f64, i32)> {
    let (ma, ea) = integer_parts(-a);
    let (mb, eb) = integer_parts(b);
    if mb == 0 {
        return None;
    }
    let product = u128::from(ma) * size as u128; // < 2^117, at exponent ea
    let bits = |x: u128| 128 - x.leading_zeros();
    let (high, low, exponent) = if eb >= ea {
        let shift = (eb - ea) as u32;
        if bits(u128::from(mb)) + shift > 127 {
            // b ≥ 2^127 · 2^ea > 2^10 · |a|N: no cancellation, so subtracting
            // the rounded product costs about one rounding.
            let (bm, be) = parts(b);
            let (pm, pe) = parts(product as f64);
            return Some(parts_shift(parts(bm - scale_down(pm, pe + ea - be)), be));
        }
        (u128::from(mb) << shift, product, ea)
    } else {
        let shift = (ea - eb) as u32;
        if bits(product) + shift > 127 {
            return None; // |a|N ≥ 2^126 · 2^eb > b
        }
        (u128::from(mb), product << shift, eb)
    };
    if high < low {
        return None;
    }
    Some(parts_shift(parts((high - low) as f64), exponent))
}

/// A finite nonnegative f64 as an integer mantissa and exponent, exactly.
fn integer_parts(value: f64) -> (u64, i32) {
    let bits = value.to_bits();
    let exponent = ((bits >> 52) & 0x7ff) as i32;
    let fraction = bits & ((1_u64 << 52) - 1);
    if exponent == 0 {
        (fraction, -1074)
    } else {
        (fraction | (1_u64 << 52), exponent - 1075)
    }
}

fn parts_shift(value: (f64, i32), exponent: i32) -> (f64, i32) {
    (value.0, value.1 + exponent)
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

/// value · Π multipliers / Π divisors, as binary parts; one rounding per factor.
fn scaled(value: f64, multipliers: &[(f64, i32)], divisors: &[(f64, i32)]) -> (f64, i32) {
    scaled_parts(parts(value), multipliers, divisors)
}

fn scaled_parts(
    value: (f64, i32),
    multipliers: &[(f64, i32)],
    divisors: &[(f64, i32)],
) -> (f64, i32) {
    let (mut mantissa, mut exponent) = value;
    for factor in multipliers {
        mantissa *= factor.0;
        exponent += factor.1;
    }
    for divisor in divisors {
        mantissa /= divisor.0;
        exponent -= divisor.1;
    }
    (mantissa, exponent)
}

fn scale_down(value: f64, exponent: i32) -> f64 {
    if exponent >= -1022 {
        value * 2.0_f64.powi(exponent)
    } else if exponent >= -1100 {
        // Scale in the normal range first, then round to the subnormal result.
        // Values reach almost 2^5 (a two-term finite-universe signal over a
        // denominator mantissa near 1/8), so the cutoff leaves room: below it
        // the result is under half the smallest subnormal.
        (value * 2.0_f64.powi(exponent + 1022)) * f64::MIN_POSITIVE
    } else {
        0.0
    }
}

fn coefficient(signal: &[(f64, i32)], terms: &[(f64, i32)]) -> Result<f64, ProjectionError> {
    let max_exponent = terms
        .iter()
        .filter(|term| term.0 > 0.0)
        .map(|term| term.1)
        .max()
        .ok_or(ProjectionError::UndefinedCoefficient)?;
    let Some(signal_exponent) = signal.iter().filter(|t| t.0 > 0.0).map(|t| t.1).max() else {
        return Ok(0.0);
    };
    let sum = |terms: &[(f64, i32)], top: i32| -> f64 {
        terms
            .iter()
            .filter(|term| term.0 > 0.0)
            .map(|term| scale_down(term.0, term.1 - top))
            .sum()
    };
    let denominator = sum(terms, max_exponent);
    // Divide before tiny scaling: a denominator < 1 can rescue a representable
    // subnormal numerator that would otherwise disappear.
    Ok(scale_down(
        sum(signal, signal_exponent) / denominator,
        signal_exponent - max_exponent,
    ))
}
