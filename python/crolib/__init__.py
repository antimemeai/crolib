"""Generalizability theory for all-random crossed measurement designs.

Version 0.1.0 projects reliability from supplied variance components; it does
not estimate components from raw observations. No runtime dependencies.
"""

from dataclasses import dataclass
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

    def project(self, n_items: int, n_raters: int) -> Reliability:
        """Project G/Phi for the same population and exchangeable facet universes.

        Counts must be positive integers at most 2**64-1. Variances must be
        finite and nonnegative. Undefined coefficients raise ``ValueError``.
        """
        for count in (n_items, n_raters):
            if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 2**64 - 1:
                raise ValueError("item and rater counts must be positive 64-bit integers")
        values = {}
        for name in self.__dataclass_fields__:
            try:
                value = float(getattr(self, name))
            except (TypeError, ValueError, OverflowError) as error:
                raise ValueError(f"{name} variance must be finite and nonnegative") from error
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} variance must be finite and nonnegative")
            values[name] = value
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
