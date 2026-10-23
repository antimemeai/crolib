# Balanced fully crossed random-effects designs from their definitions.
#
# T terms (Brennan 2001, p. 217; CASMA 21 Eq. 67) and their expected values
# (CASMA 21 Eq. 68), with the boot-λ modification (CASMA 21 Eq. 69-70).
# Solving the expected-T-term system for the observed T terms gives the
# unbiased ANOVA estimates; solving the boot-λ system for a resample's T terms
# gives Brennan's bias-corrected replicate. Nothing here restates any
# implementation's estimator formulas.
#
# Shared by crolib and salib verification scripts (crolib-hmz). Load with
#   load(os.path.join(CROLIB, "verify/sage/balanced.sage"))
import itertools

def effects(facets):
    """Every nonempty subset of the facets, as tuples in facet order."""
    return [c for k in range(1, len(facets) + 1) for c in itertools.combinations(facets, k)]

def prod_sizes(sizes, idx):
    return prod([sizes[f] for f in idx]) if idx else 1

def t_terms(y, facets, sizes):
    """T(α) = n(~α) Σ_α (mean over ~α)² for every effect, plus T(µ) = N·(grand mean)²."""
    cells = list(itertools.product(*[range(sizes[f]) for f in facets]))
    N = len(cells)
    out = {}
    for a in effects(facets) + [()]:
        pos = [facets.index(f) for f in a]
        sums = {}
        for c in cells:
            key = tuple(c[k] for k in pos)
            sums[key] = sums.get(key, 0) + y[c]
        per = N // prod_sizes(sizes, a)          # cells per level of α
        out[a] = per * sum((s / per)^2 for s in sums.values())
    return out

def et_coefficient(alpha, beta, facets, sizes, boot=()):
    """Coefficient of σ²(α) in E T(β) under boot-λ (CASMA 21 Eq. 70); α = () means µ²."""
    if alpha == ():
        return prod_sizes(sizes, facets)
    outside = [f for f in facets if f not in alpha and f not in beta]
    k = prod_sizes(sizes, beta) * prod_sizes(sizes, outside)
    for f in boot:
        if f in alpha and f not in beta:
            k *= QQ(2 * sizes[f] - 1) / sizes[f]
    return k

def estimate(y, facets, sizes, boot=()):
    """Solve the (boot-λ) expected-T-term system; returns {effect: σ̂²}."""
    unknowns = [()] + effects(facets)
    rows = [()] + effects(facets)
    A = matrix(QQ, [[et_coefficient(a, b, facets, sizes, boot) for a in unknowns] for b in rows])
    T = t_terms(y, facets, sizes)
    sol = A.solve_right(vector(QQ, [T[b] for b in rows]))
    return {a: sol[k] for k, a in enumerate(unknowns) if a != ()}

def resamples(facets, sizes, facet):
    """Every with-replacement redraw of one facet's levels (equally likely)."""
    return itertools.product(range(sizes[facet]), repeat=sizes[facet])

def apply_resample(y, facets, sizes, facet, draw):
    k = facets.index(facet)
    out = {}
    for c in itertools.product(*[range(sizes[f]) for f in facets]):
        src = list(c); src[k] = draw[c[k]]
        out[c] = y[tuple(src)]
    return out
