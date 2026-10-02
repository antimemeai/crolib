import math
import unittest
from decimal import Decimal, localcontext

from crolib import CrossedComponents


def example():
    return CrossedComponents(12, 6, 4, 8, 10, 2, 24)


class ProjectionTests(unittest.TestCase):
    def test_hand_computed(self):
        result = example().project(4, 2)
        self.assertAlmostEqual(result.generalizability, 6 / 11, places=14)
        self.assertAlmostEqual(result.dependability, 48 / 103, places=14)

    def test_scale_and_swap(self):
        expected = example().project(4, 2)
        for scale in (1e-300, 1e300):
            result = CrossedComponents(*(v * scale for v in (12, 6, 4, 8, 10, 2, 24))).project(4, 2)
            self.assertAlmostEqual(result.generalizability, expected.generalizability, places=14)
            self.assertAlmostEqual(result.dependability, expected.dependability, places=14)
        self.assertEqual(CrossedComponents(12, 4, 6, 10, 8, 2, 24).project(2, 4), expected)

    def test_more_measurements(self):
        small, large = example().project(2, 2), example().project(4, 4)
        self.assertGreater(large.generalizability, small.generalizability)
        self.assertGreater(large.dependability, small.dependability)
        self.assertLessEqual(large.dependability, large.generalizability)

    def test_large_and_subnormal_components(self):
        self.assertEqual(CrossedComponents(person=1e308, person_item=1e308).project(1, 1).generalizability, .5)
        tiny = math.ulp(0.0)
        self.assertEqual(CrossedComponents(person=tiny, residual=tiny).project(2, 1).generalizability, 2 / 3)

    def test_tiny_representable_coefficient_decimal_oracle(self):
        result = CrossedComponents(person=1e-200, residual=1e150).project(10**19, 10**19)
        with localcontext() as context:
            context.prec = 100
            signal = Decimal.from_float(1e-200)
            error = Decimal.from_float(1e150) / Decimal(10**19) / Decimal(10**19)
            expected = float(signal / (signal + error))
        self.assertGreater(result.generalizability, 0)
        self.assertLessEqual(abs(result.generalizability - expected), math.ulp(expected))

    def test_zero_signal(self):
        result = CrossedComponents(person_item=1).project(1, 1)
        self.assertEqual(result.generalizability, 0)
        self.assertEqual(result.dependability, 0)

    def test_invalid_inputs(self):
        for bad in (-1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                CrossedComponents(person=bad).project(1, 1)
        for count in (0, -1, 1.5, True, 10**400):
            with self.assertRaises(ValueError):
                example().project(count, 1)
        for c in (CrossedComponents(), CrossedComponents(item=1)):
            with self.assertRaises(ValueError):
                c.project(1, 1)


if __name__ == "__main__":
    unittest.main()
