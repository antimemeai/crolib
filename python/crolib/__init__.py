"""Generalizability theory for crossed person × item × rater designs.

Projects reliability from supplied variance components, with items and raters
drawn from infinite universes or, for one facet, a finite universe. It does
not estimate components from raw observations. No runtime dependencies.
"""

from dataclasses import dataclass
from fractions import Fraction
import math

__version__ = "0.1.0"
__all__ = ["CrossedComponents", "Reliability", "__version__"]


@dataclass(frozen=True)
class Reliability:
    """Relative reliability (G) and absolute dependability (Phi)."""

    generalizability: float
    dependability: float


@dataclass(frozen=True)
class CrossedComponents:
    """Seven variances for an all-random person × item × rater design.

    These are random-model components, the values an ANOVA G study estimates.
    ``residual`` combines the three-way interaction and observational error
    for unreplicated data. Validation occurs when calling ``project``.
    """

    person: float = 0.0
    item: float = 0.0
    rater: float = 0.0
    person_item: float = 0.0
    person_rater: float = 0.0
    item_rater: float = 0.0
    residual: float = 0.0

    def project(self, n_items: int, n_raters: int, *, item_universe=None,
                rater_universe=None) -> Reliability:
        """Project G/Phi for the same population and the given facet universes.

        Counts must be positive integers at most 2**64-1. A universe is
        ``None`` (infinite, exchangeable levels) or a finite number of levels
        from 2 to 2**64-1, sampled without replacement; at most one facet may
        be finite. With both infinite, variances must be finite and
        nonnegative. With one finite facet of size N, its finite-universe
        components must be nonnegative (Brennan 1977), so three variances may
        be negative: with raters finite, ``person >= -person_rater/N``,
        ``item >= -item_rater/N`` and ``person_item >= -residual/N``; with items
        finite, ``person >= -person_item/N``, ``rater >= -item_rater/N`` and
        ``person_rater >= -residual/N``. Invalid or undefined projections
        raise ``ValueError``.
        """
        for count in (n_items, n_raters):
            if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 2**64 - 1:
                raise ValueError("item and rater counts must be positive 64-bit integers")
        for size, count in ((item_universe, n_items), (rater_universe, n_raters)):
            if size is None:
                continue
            if isinstance(size, bool) or not isinstance(size, int) or not 2 <= size <= 2**64 - 1:
                raise ValueError("a finite universe needs at least two levels, at most 2**64-1")
            if count > size:
                raise ValueError("a count cannot exceed its facet's finite universe")
        if item_universe is not None and rater_universe is not None:
            raise ValueError("with both facets finite, the residual's interaction and error must be separated")
        if item_universe is None and rater_universe is None:
            return self._project_infinite(n_items, n_raters, self._values(()))
        return self._project_finite(n_items, n_raters, item_universe, rater_universe)

    def _values(self, may_be_negative):
        values = {}
        for name in self.__dataclass_fields__:
            try:
                value = float(getattr(self, name))
            except (TypeError, ValueError, OverflowError) as error:
                raise ValueError(f"{name} variance must be finite and nonnegative") from error
            if not math.isfinite(value) or (value < 0 and name not in may_be_negative):
                raise ValueError(f"{name} variance must be finite and nonnegative")
            values[name] = value
        return values

    def _project_finite(self, n_items, n_raters, item_universe, rater_universe):
        # Exact rational arithmetic, rounded once per coefficient.
        if rater_universe is not None:
            size, n, m = rater_universe, n_raters, n_items
            cross, nested, main, facet = "person_item", "person_rater", "item", "rater"
        else:
            size, n, m = item_universe, n_items, n_raters
            cross, nested, main, facet = "person_rater", "person_item", "rater", "item"
        bounds = {"person": nested, main: "item_rater", cross: "residual"}
        q = {name: Fraction(value) for name, value in self._values(bounds).items()}
        finite = {}
        for name in self.__dataclass_fields__:
            if name in bounds:
                finite[name] = q[name] + q[bounds[name]] / size
                if finite[name] < 0:
                    raise ValueError(f"{name} variance is below its finite-universe bound")
        fpc = Fraction(size - n, size)
        tau = finite["person"]
        relative = finite[cross] / m + fpc * q[nested] / n + fpc * q["residual"] / (m * n)
        absolute = relative + finite[main] / m + fpc * q[facet] / n + fpc * q["item_rater"] / (m * n)
        if tau + relative == 0:
            raise ValueError("reliability is undefined for a zero denominator")
        return Reliability(float(tau / (tau + relative)), float(tau / (tau + absolute)))

    def _project_infinite(self, n_items, n_raters, values):
        items, raters = math.frexp(n_items), math.frexp(n_raters)
        signal = math.frexp(values["person"])

        def weighted(name, first=(0.5, 1), second=(0.5, 1)):
            mantissa, exponent = math.frexp(values[name])
            return mantissa / first[0] / second[0], exponent - first[1] - second[1]

        relative = [signal, weighted("person_item", items), weighted("person_rater", raters),
                    weighted("residual", items, raters)]
        absolute = relative + [weighted("item", items), weighted("rater", raters),
                               weighted("item_rater", items, raters)]

        def coefficient(terms):
            nonzero = [(mantissa, exponent) for mantissa, exponent in terms if mantissa > 0]
            if not nonzero:
                raise ValueError("reliability is undefined for a zero denominator")
            if signal[0] == 0:
                return 0.0
            max_exponent = max(exponent for _, exponent in nonzero)
            denominator = math.fsum(math.ldexp(mantissa, exponent - max_exponent)
                                    for mantissa, exponent in nonzero)
            return math.ldexp(signal[0] / denominator, signal[1] - max_exponent)

        return Reliability(coefficient(relative), coefficient(absolute))
