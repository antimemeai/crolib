"""Projection against exact rational G and Phi, correctly rounded, for
adversarial inputs (verify/sage/projection.py)."""

import struct
import unittest

from crolib import CrossedComponents
from projection_oracle import CASES


def ulps(a, b):
    """Distance in units of the last place between nonnegative floats."""
    bits = lambda v: struct.unpack("<Q", struct.pack("<d", v))[0]
    return abs(bits(a) - bits(b))


class SageOracleTests(unittest.TestCase):
    def test_projection_matches_exact_coefficients(self):
        worst = 0
        for c, ni, nr, g, phi in CASES:
            r = CrossedComponents(*c).project(ni, nr)
            for name, got, exact in (("G", r.generalizability, g), ("Phi", r.dependability, phi)):
                d = ulps(got, exact)
                worst = max(worst, d)
                self.assertLessEqual(d, 8, f"{name} for {c} at ({ni}, {nr}): got {got!r}, exact {exact!r}")
        print(f"worst distance: {worst} ulp")


if __name__ == "__main__":
    unittest.main()
