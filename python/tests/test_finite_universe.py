"""Finite-universe projection: exact fixtures, the admissible region, and exact
rational G and Phi for adversarial inputs (verify/sage/finite_projection.py)."""

import math
import unittest

from crolib import CrossedComponents
from finite_projection_oracle import CASES


def panel():
    # Raters a panel of four. person and person_item are negative, inside
    # person >= -person_rater/4 and person_item >= -residual/4.
    return CrossedComponents(person=-0.125, item=0.5, rater=0.25, person_item=-0.5,
                             person_rater=1, item_rater=0.5, residual=4)


class FiniteUniverseTests(unittest.TestCase):
    def test_negative_components_inside_the_region(self):
        # Universe score 1/8, relative error 1, absolute error 23/16.
        r = panel().project(2, 2, rater_universe=4)
        self.assertEqual(r.generalizability, 1 / 9)
        self.assertEqual(r.dependability, 2 / 25)
        census = panel().project(2, 4, rater_universe=4)
        self.assertEqual(census.generalizability, 1 / 3)
        self.assertEqual(census.dependability, 2 / 11)

    def test_outside_the_region_names_the_bound(self):
        c = CrossedComponents(**{**panel().__dict__, "person_item": math.nextafter(-1.0, -2)})
        with self.assertRaisesRegex(ValueError, "^person_item variance is below its finite-universe bound$"):
            c.project(2, 2, rater_universe=4)
        c = CrossedComponents(**{**panel().__dict__, "person_rater": -1})
        with self.assertRaisesRegex(ValueError, "^person_rater variance must be finite and nonnegative$"):
            c.project(2, 2, rater_universe=4)
        with self.assertRaisesRegex(ValueError, "^person_item variance must be finite and nonnegative$"):
            panel().project(2, 2, item_universe=4)

    def test_infinite_universes_reduce_to_project(self):
        c = CrossedComponents(12, 6, 4, 8, 10, 2, 24)
        self.assertEqual(c.project(4, 2, item_universe=None, rater_universe=None), c.project(4, 2))
        with self.assertRaisesRegex(ValueError, "^person variance must be finite and nonnegative$"):
            panel().project(2, 2)
        near, far = c.project(4, 2, rater_universe=2**50), c.project(4, 2)
        self.assertAlmostEqual(near.generalizability, far.generalizability, places=14)
        self.assertAlmostEqual(near.dependability, far.dependability, places=14)

    def test_facet_swap_symmetry(self):
        c = panel()
        swapped = CrossedComponents(c.person, c.rater, c.item, c.person_rater, c.person_item,
                                    c.item_rater, c.residual)
        self.assertEqual(swapped.project(2, 2, item_universe=4), c.project(2, 2, rater_universe=4))

    def test_invalid_universes(self):
        for size in (0, 1, -3, 2.0, True, 2**64):
            with self.assertRaisesRegex(ValueError, "finite universe needs at least two levels"):
                panel().project(1, 1, rater_universe=size)
        with self.assertRaisesRegex(ValueError, "cannot exceed"):
            panel().project(1, 5, rater_universe=4)
        with self.assertRaisesRegex(ValueError, "must be separated"):
            panel().project(2, 2, item_universe=4, rater_universe=4)
        with self.assertRaisesRegex(ValueError, "^person variance must be finite"):
            CrossedComponents(**{**panel().__dict__, "person": math.nan}).project(2, 2, rater_universe=4)

    def test_finite_projection_is_correctly_rounded(self):
        # Exact rational arithmetic rounds once, so results equal the oracle.
        for c, ni, nr, items, raters, expected in CASES:
            tag = f"{c} at ({ni}, {nr}) in ({items}, {raters})"
            components = CrossedComponents(*c)
            kind = expected[0]
            if kind == "defined":
                r = components.project(ni, nr, item_universe=items, rater_universe=raters)
                self.assertEqual((r.generalizability, r.dependability), expected[1:], tag)
                continue
            message = {
                "invalid": lambda: f"^{expected[1]} variance must be finite and nonnegative$",
                "below": lambda: f"^{expected[1]} variance is below its finite-universe bound$",
                "undefined": lambda: "^reliability is undefined for a zero denominator$",
            }[kind]()
            with self.assertRaisesRegex(ValueError, message, msg=tag):
                components.project(ni, nr, item_universe=items, rater_universe=raters)


if __name__ == "__main__":
    unittest.main()
