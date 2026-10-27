# Plain Python, run with the Sage environment's python (no preparser). Claim:
# crolib's project_in returns G and Phi within a few ulp of the exact
# coefficient for one finite facet, and refuses exactly the components outside
# the finite-universe region, naming the first violated bound.
#
# Method: every f64 input is an exact rational. The coefficients come from the
# covariance form of the D study (verify/sage/finite_universe.sage, claim 4,
# with the other facet's universe infinite):
#   universe score = σ²(p) + σ²(p×finite)/N
#   relative error = σ²(p×other)/m + σ²(p×finite)(1/n − 1/N) + residual/(m n)
#   absolute error = relative + σ²(other)/m + σ²(finite)(1/n − 1/N) + σ²(i×r)/(m n)
# which crolib does not evaluate (it uses the finite-universe components). The
# region is Brennan's σ²(e|N) >= 0 with σ²(pir) = residual (claims 3 and 5).
# Python's Fraction -> float division rounds correctly, subnormals included.
# Cases are fixed or come from a script-local LCG. Emits
# tests/oracles/finite_projection.rs and python/tests/finite_projection_oracle.py.
import math, os, hashlib, struct, sage.version
from fractions import Fraction
CROLIB = os.environ["CROLIB_ROOT"]
TINY = float.fromhex("0x1p-1074")
U64_MAX = 2**64 - 1
FIELDS = ["person", "item", "rater", "person_item", "person_rater", "item_rater", "residual"]

def outcome(c, ni, nr, items, raters):
    """('defined', G, Phi), ('invalid', name), ('below', name) or ('undefined',)."""
    assert (items is None) != (raters is None)
    q = dict(zip(FIELDS, [Fraction(v) for v in c]))
    if raters is not None:
        N, n, m = raters, nr, ni
        cross, nested, main, facet = "person_item", "person_rater", "item", "rater"
    else:
        N, n, m = items, ni, nr
        cross, nested, main, facet = "person_rater", "person_item", "rater", "item"
    region = {"person": q["person"] + q[nested] / N,
              main: q[main] + q["item_rater"] / N,
              cross: q[cross] + q["residual"] / N}
    for name in FIELDS:
        if name not in region and q[name] < 0:
            return ("invalid", name)
    for name in FIELDS:
        if name in region and region[name] < 0:
            return ("below", name)
    w = Fraction(1, n) - Fraction(1, N)
    tau = q["person"] + q[nested] / N
    rel = q[cross] / m + q[nested] * w + q["residual"] / (m * n)
    ab = rel + q[main] / m + q[facet] * w + q["item_rater"] / (m * n)
    if tau + rel == 0:
        return ("undefined",)
    return ("defined", float(tau / (tau + rel)), float(tau / (tau + ab)))

def below(x):
    return math.nextafter(x, -math.inf)

cases = [
    # Hand fixture (README): raters a panel of 4, two sampled; person_item and
    # person negative inside the region.
    ((-0.125, 0.5, 0.25, -0.5, 1.0, 0.5, 4.0), 2, 2, None, 4),
    ((-0.125, 0.5, 0.25, -0.5, 1.0, 0.5, 4.0), 2, 4, None, 4),     # census of the panel
    ((-0.125, 0.5, 0.25, -0.5, 1.0, 0.5, 4.0), 2, 1, None, 4),
    ((12.0, 6.0, 4.0, 8.0, 10.0, 2.0, 24.0), 4, 2, None, 2),         # README components
    ((12.0, 6.0, 4.0, 8.0, 10.0, 2.0, 24.0), 4, 2, 6, None),
    ((12.0, 6.0, 4.0, 8.0, 10.0, 2.0, 24.0), 4, 2, 4, None),         # census of the items
    # Exactly on each bound (zero finite-universe component), then one ulp below.
    ((-0.25, 0.0, 1.0, -1.0, 1.0, 0.0, 4.0), 2, 2, None, 4),
    ((below(-0.25), 0.0, 1.0, 0.0, 1.0, 0.0, 4.0), 2, 2, None, 4),
    ((1.0, -0.25, 1.0, 0.0, 1.0, 1.0, 4.0), 2, 2, None, 4),
    ((1.0, below(-0.25), 1.0, 0.0, 1.0, 1.0, 4.0), 2, 2, None, 4),
    ((1.0, 0.0, 1.0, below(-1.0), 1.0, 0.0, 4.0), 2, 2, None, 4),
    ((1.0, 0.0, 1.0, 1.0, -0.25, 0.0, 1.0), 2, 2, 4, None),
    ((1.0, 0.0, 1.0, 1.0, below(-0.25), 0.0, 1.0), 2, 2, 4, None),
    ((-0.5, 0.0, -0.5, 2.0, 1.0, 2.0, 1.0), 3, 2, 4, None),
    ((below(-0.5), 0.0, 1.0, 2.0, 1.0, 0.0, 1.0), 3, 2, 4, None),
    ((1.0, 0.0, below(-0.5), 2.0, 1.0, 2.0, 1.0), 3, 2, 4, None),
    # A bound that is not a dyadic rational: fl(1/3) < 1/3 leaves a tiny positive
    # component, and the next float below crosses the bound.
    ((1.0, 0.0, 0.0, -(1 / 3), 0.0, 0.0, 1.0), 1, 1, None, 3),
    ((1.0, 0.0, 0.0, below(-(1 / 3)), 0.0, 0.0, 1.0), 1, 1, None, 3),
    ((-(1 / 3), 0.0, 0.0, 0.0, 1.0, 0.0, 1.0), 1, 1, None, 3),
    # Self-bounded components stay nonnegative.
    ((1.0, 0.0, -1e-300, 0.0, 0.0, 0.0, 1.0), 1, 1, None, 3),
    ((1.0, 0.0, 0.0, 0.0, 0.0, -1e-300, 1.0), 1, 1, 3, None),
    ((1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -TINY), 1, 1, 3, None),
    # Undefined: zero signal and zero error at a census.
    ((-0.5, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0), 1, 2, None, 2),
    ((0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), 1, 2, None, 2),
    # Zero signal on the bound, positive error.
    ((-0.5, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0), 1, 1, None, 2),
    # Extremes: huge components, counts and universes near 2^64, subnormals.
    ((1e308, 1e308, 1e308, -1e308, 1e308, 1e308, 1.7e308), 1, 1, None, 2),
    ((-1e308, 1e308, 1e308, 1e308, 1.7e308, 1e308, 1e308), 1, 1, None, 2),
    ((1e-300, 0.0, 0.0, -1e-300, 0.0, 0.0, 1e-280), U64_MAX - 1, U64_MAX - 1, None, U64_MAX),
    ((-TINY, 0.0, 0.0, 0.0, 3 * TINY, 0.0, TINY), 1, 2, None, 3),
    ((-TINY, 0.0, 0.0, 0.0, 2 * TINY, 0.0, TINY), 1, 1, None, 3),
    ((1.0, 0.0, 0.0, -TINY, 0.0, 0.0, 1e-300), 3, 1, None, 2**60),
    ((1e300, 0.0, 0.0, -1e-300, 0.0, 0.0, 1e300), 1, 1, None, U64_MAX),
    ((-1e-300, 1e300, 0.0, 0.0, 1e-280, 0.0, 1.0), 2**40, 7, None, 2**53 + 1),
]
# Review: a two-term signal over a small denominator mantissa rounds up to the
# smallest subnormal, past a scaling cutoff that once returned zero.
_N = 2**20 - 1
_a = -float(Fraction(2.0**1000) / _N)
if _N * Fraction(_a) + Fraction(2.0**1000) < 0:
    _a = math.nextafter(_a, 0)
cases.append(((math.ldexp(1.99, -116), 0.0, 0.0, _a, math.ldexp(1.99, -97), 0.0, 2.0**1000),
              _N, 2**19 - 1, None, _N))
# A fixed LCG drives the mixed cases.
state = 20261026
def lcg():
    global state
    state = (6364136223846793005 * state + 1442695040888963407) % 2**64
    return state

def size():
    return 2 + lcg() % (2**int(1 + lcg() % 63) - 1)

for _ in range(80):
    comps = []
    for _ in range(7):
        e = int(lcg() % 1201) - 600
        m = 1 + (lcg() % 2**52) / 2**52
        comps.append(0.0 if lcg() % 9 == 0 else float(Fraction(m) * Fraction(2)**e))
    N = min(size(), U64_MAX)
    n = 1 + lcg() % N
    other = 1 + lcg() % 2**int(1 + lcg() % 63)
    raters_finite = lcg() % 2 == 0
    ni, nr = (other, n) if raters_finite else (n, other)
    # Make each correctable component negative, near or past its bound.
    q = dict(zip(FIELDS, comps))
    if raters_finite:
        pairs = [("person", "person_rater"), ("item", "item_rater"), ("person_item", "residual")]
    else:
        pairs = [("person", "person_item"), ("rater", "item_rater"), ("person_rater", "residual")]
    for a, b in pairs:
        if lcg() % 3:
            ratio = Fraction(int(lcg() % 2**20), 2**20) * Fraction(int(lcg() % 3) + 1, 2)  # in [0, 1.5)
            q[a] = -float(Fraction(q[b]) / N * ratio)
    cases.append((tuple(q[f] for f in FIELDS), int(ni), int(nr),
                  None if raters_finite else int(N), int(N) if raters_finite else None))

# Nondegenerate cases: every term of the error variances within a few bits of
# a common base, so G and Phi depend on all of them, with the correctable
# components negative and their finite-universe components comparable too.
for _ in range(60):
    base_e = int(lcg() % 1801) - 900
    N = 2 + lcg() % 2**int(1 + lcg() % 40)
    n = 1 + lcg() % (N - 1)                     # n < N: every term present
    m = 1 + lcg() % 2**int(lcg() % 40)
    raters_finite = lcg() % 2 == 0
    fpc = Fraction(N - n, N * n)
    def near(weight):
        mant = Fraction(1) + Fraction(int(lcg() % 2**52), 2**52)
        return float(mant * Fraction(2)**(base_e + int(lcg() % 9) - 4) * weight)
    ok = True
    comps = {}
    # Positive parts first: nested, facet, item_rater, residual; then the
    # corrected components as (target finite-universe component) - b/N.
    comps["residual"] = near(1 / (Fraction(m) * fpc))
    comps["item_rater"] = near(1 / (Fraction(m) * fpc))
    nested, facet = ("person_rater", "rater") if raters_finite else ("person_item", "item")
    cross, main = ("person_item", "item") if raters_finite else ("person_rater", "rater")
    comps[nested] = near(1 / fpc)
    comps[facet] = near(1 / fpc)
    for a, b, weight in (("person", nested, 1), (main, "item_rater", m), (cross, "residual", m)):
        target = Fraction(near(weight))
        comps[a] = float(target - Fraction(comps[b]) / N)
    vals = tuple(comps[f] for f in FIELDS)
    if all(math.isfinite(v) for v in vals):
        ni, nr = (int(m), int(n)) if raters_finite else (int(n), int(m))
        cases.append((vals, ni, nr, None if raters_finite else int(N), int(N) if raters_finite else None))

rows = [(c, ni, nr, items, raters, outcome(c, ni, nr, items, raters)) for c, ni, nr, items, raters in cases]
kinds = {}
for row in rows:
    kinds[row[-1][0]] = kinds.get(row[-1][0], 0) + 1

h = hashlib.sha256(open(os.path.join(CROLIB, "verify", "sage", "finite_projection.py"), "rb").read()).hexdigest()
head = "@generated by verify/sage/finite_projection.py; do not edit. sha256(script) = %s; SageMath %s" % (h, sage.version.version)
rb = lambda v: "0x%016x" % struct.unpack('<Q', struct.pack('<d', v))[0]
rust = ["// " + head, "// Exact finite-universe G and Phi, correctly rounded, and the expected refusals.", "",
        "/// What `project_in` must return. Bits, not f64 literals, because",
        "/// `f64::from_bits` is const only from Rust 1.83 (crolib's MSRV is 1.74).",
        "pub enum Expected {",
        "    /// Bit patterns of the correctly rounded exact (G, Phi).",
        "    Defined(u64, u64),",
        "    InvalidComponent(&'static str),",
        "    BelowUniverseBound(&'static str),",
        "    UndefinedCoefficient,",
        "}",
        "",
        "/// Component bit patterns (person, item, rater, person_item, person_rater,",
        "/// item_rater, residual), counts (items, raters), universe sizes (items,",
        "/// raters; 0 is infinite), and the expected result.",
        "pub type FiniteCase = ([u64; 7], u64, u64, u64, u64, Expected);",
        "",
        "pub const FINITE_CASES: &[FiniteCase] = &["]
py = ["# " + head, '"""Exact finite-universe G and Phi, correctly rounded, and the expected refusals."""', "",
      "# (components, n_items, n_raters, item_universe, rater_universe, expected) with",
      "# floats as exact hex literals; expected is ('defined', G, Phi), ('invalid', name),",
      "# ('below', name) or ('undefined',).", "CASES = ["]
for c, ni, nr, items, raters, out in rows:
    if out[0] == "defined":
        rexp, pexp = "Expected::Defined(%s, %s)" % (rb(out[1]), rb(out[2])), "('defined', float.fromhex(%r), float.fromhex(%r))" % (out[1].hex(), out[2].hex())
    elif out[0] == "invalid":
        rexp, pexp = "Expected::InvalidComponent(%r)" % out[1], "('invalid', %r)" % out[1]
    elif out[0] == "below":
        rexp, pexp = "Expected::BelowUniverseBound(%r)" % out[1], "('below', %r)" % out[1]
    else:
        rexp, pexp = "Expected::UndefinedCoefficient", "('undefined',)"
    rexp = rexp.replace("'", '"')
    rust.append("    ([%s], %d, %d, %d, %d, %s)," % (", ".join(rb(v) for v in c), ni, nr, items or 0, raters or 0, rexp))
    py.append("    ((%s), %d, %d, %r, %r, %s)," % (", ".join("float.fromhex(%r)" % v.hex() for v in c), ni, nr, items, raters, pexp))
rust.append("];")
py.append("]")
open(os.path.join(CROLIB, "tests", "oracles", "finite_projection.rs"), "w").write("\n".join(rust) + "\n")
open(os.path.join(CROLIB, "python", "tests", "finite_projection_oracle.py"), "w").write("\n".join(py) + "\n")
print("ok: %d finite-universe cases: %s" % (len(rows), ", ".join("%d %s" % (v, k) for k, v in sorted(kinds.items()))))
