# Claims for finite-universe projection (crolib-3bk).
#
# Covariance reading of the crossed p × i × r random model: the score array has
#   Cov(y) = σ²(∅) J + Σ_a σ²(a) K_a,   K_a[x, x'] = 1 when x and x' agree on every facet in a,
# for signed σ²(a). σ²(∅) is a common shift of every score: it cannot be
# identified from data and cancels from every universe score and error below.
# The residual adds σ²(e) on the diagonal: replication error, averaged away in
# the universe score. A facet f in F is sampled without replacement from a
# universe of N_f levels; the others are infinite.
#
# 1. Cov(y) on any n_p × n_i × n_r array has eigenvalue EMS_e(n) = Σ_{a⊇e} σ²(a)
#    Π_{f∉a} n_f with multiplicity Π_{f∈e}(n_f − 1) on the contrasts, so its
#    contrast eigenvalues are the expected mean squares. Exact matrices.
# 2. Brennan (1977, ACT Technical Bulletin 26, Eqs. 27 and 29): with the finite-universe
#    components σ²(e|N) = Σ_{b⊇e, b∖e⊆F} σ²(b) / Π_{f∈b∖e} N_f,
#      EMS_e(n) = Σ_{b⊇e} σ²(b|N) Π_{f∉b} n_f Π_{f∈(b∖e)∩F} (1 − n_f/N_f).
#    Symbolic, every F ⊆ {p, i, r}. These σ²(e|N) are the Cornfield–Tukey components.
# 3. Admissible region: Cov(y) is PSD on the contrasts at every admissible count
#    (n_f ≤ N_f on F) iff every σ²(e|N) ≥ 0. Sufficiency is (2) term by term.
#    Necessity: at n_f = N_f on F∖e, EMS_e(n) / Π_{f∉e, f∉F} n_f tends to
#    σ²(e|N) Π_{f∈F∖e} N_f as those counts grow. With F empty the region is every σ²(e) ≥ 0.
# 4. D study: mean over n_i of N_i items and n_r of N_r raters, sampled without
#    replacement. Universe-score, relative and absolute error variances by brute
#    force on exact matrices, averaged over every sample, match a closed form and
#    do not depend on σ²(∅).
# 5. With one finite facet the projection depends on σ²(pir) and σ²(e) only through
#    the residual σ²(pir) + σ²(e); with both finite it does not, so the split is
#    needed. Every σ²(e|N) is nondecreasing in σ²(pir) at a fixed residual, so the
#    residual is admissible for some split iff the region holds with σ²(pir) =
#    residual. The infinite-facet limits of (4) are the formulas crolib implements,
#    and they reproduce Brennan's (1977, printed p. 55) items-finite p × i × o example.
import itertools, os, random
CROLIB = os.environ["CROLIB_ROOT"]
load(os.path.join(CROLIB, "verify", "sage", "balanced.sage"))   # effects()

FACETS = ['p', 'i', 'r']
EFFECTS = effects(FACETS)
NAME = {('p',): 'person', ('i',): 'item', ('r',): 'rater', ('p', 'i'): 'person_item',
        ('p', 'r'): 'person_rater', ('i', 'r'): 'item_rater', ('p', 'i', 'r'): 'residual'}

def supersets(e):
    return [a for a in EFFECTS if set(e) <= set(a)]

def ems(e, s, n):
    """Σ_{a⊇e} σ²(a) Π_{f∉a} n_f."""
    return sum(s[a] * prod([n[f] for f in FACETS if f not in a]) for a in supersets(e))

def finite_components(s, N, F):
    """Brennan's Eq. 27: σ²(e|N) = Σ_{b⊇e, b∖e⊆F} σ²(b)/Π_{b∖e} N_f."""
    return {e: sum(s[b] / prod([N[f] for f in b if f not in e])
                   for b in supersets(e) if set(b) - set(e) <= set(F))
            for e in EFFECTS}

rng = random.Random(int(20261026))  # Python's random, seeded; no Sage RNG state
def rand_q(lo=-3, hi=3):
    return QQ(rng.randint(lo * 8, hi * 8)) / 8

# --- 1. Contrast eigenvalues of the covariance ----------------------------
def covariance(s, s0, sizes):
    cells = list(itertools.product(*[range(sizes[f]) for f in FACETS]))
    K = lambda a, x, y: all(x[FACETS.index(f)] == y[FACETS.index(f)] for f in a)
    return cells, matrix(QQ, [[s0 + sum(s[a] for a in EFFECTS if K(a, x, y)) for y in cells]
                              for x in cells])

for sizes in ({'p': 2, 'i': 2, 'r': 2}, {'p': 3, 'i': 2, 'r': 4}, {'p': 2, 'i': 3, 'r': 3}):
    s = {a: rand_q() for a in EFFECTS}
    cells, C = covariance(s, rand_q(), sizes)
    # Restrict to the contrasts: an orthonormal-free basis is enough for eigenvalues.
    B = matrix(QQ, [[1 if k == j else (-1 if k == len(cells) - 1 else 0)
                     for k in range(len(cells))] for j in range(len(cells) - 1)]).transpose()
    contrast = (B.transpose() * B).inverse() * B.transpose() * C * B
    expected = {}
    for e in EFFECTS:
        lam = ems(e, s, sizes)
        expected[lam] = expected.get(lam, 0) + prod([sizes[f] - 1 for f in e])
    actual = dict(contrast.charpoly().roots(QQ))
    assert actual == expected, (sizes, actual, expected)
print("ok: the contrast eigenvalues of Cov(y) are EMS_e(n), multiplicity Π(n_f − 1)")

# --- 2. Brennan's transform gives the Cornfield–Tukey form -----------------
sv = {a: var('s_' + ''.join(a)) for a in EFFECTS}
nv = {f: var('n_' + f) for f in FACETS}
Nv = {f: var('N_' + f) for f in FACETS}
SUBSETS = [F for k in range(len(FACETS) + 1) for F in itertools.combinations(FACETS, k)]
for F in SUBSETS:
    c = finite_components(sv, Nv, F)
    for e in EFFECTS:
        ct = sum(c[b] * prod([nv[f] for f in FACETS if f not in b])
                 * prod([1 - nv[f] / Nv[f] for f in b if f not in e and f in F])
                 for b in supersets(e))
        assert bool((ems(e, sv, nv) - ct).simplify_full() == 0), (F, e)
    if not F:
        assert all(bool(c[e] == sv[e]) for e in EFFECTS)
print("ok: EMS_e(n) = Σ σ²(b|N) Π n_f Π (1 − n_f/N_f) for every finite set F (Brennan 1977, Eqs. 27, 29)")

# --- 3. Necessity: the eigenvalue at the universe sizes tends to σ²(e|N) ---
t = var('t')
for F in SUBSETS:
    c = finite_components(sv, Nv, F)
    for e in EFFECTS:
        n = {f: (Nv[f] if f in F else t) for f in FACETS}
        grow = [f for f in FACETS if f not in e and f not in F]
        lam = ems(e, sv, n) / t^len(grow) / prod([Nv[f] for f in F if f not in e])
        assert bool((limit(lam, t=oo) - c[e]).simplify_full() == 0), (F, e)
print("ok: Cov(y) is PSD on the contrasts at every admissible count iff every σ²(e|N) >= 0")

# --- 4. D study by brute force on finite universes ------------------------
def d_study_closed(s, se, n, N):
    """Universe score, relative and absolute error variance; σ²(e) has an infinite universe."""
    w = lambda a: prod([1 / n[f] for f in a]) - prod([1 / N[f] for f in a])
    tau = sum(s[a] / prod([N[f] for f in a if f != 'p']) for a in supersets(('p',)))
    rel = sum(s[a] * w([f for f in a if f != 'p']) for a in supersets(('p',)) if a != ('p',)) \
          + se / (n['i'] * n['r'])
    ab = rel + sum(s[a] * w(a) for a in EFFECTS if 'p' not in a)
    return tau, rel, ab

def d_study_brute(s, s0, se, n, N):
    sizes = {'p': 2, 'i': N['i'], 'r': N['r']}
    cells, C = covariance(s, s0, sizes)
    index = {x: k for k, x in enumerate(cells)}
    def mean_weights(person, items, raters):
        v = vector(QQ, len(cells))
        for i in items:
            for r in raters:
                v[index[(person, i, r)]] += 1 / (len(items) * len(raters))
        return v
    universe = [mean_weights(q, range(N['i']), range(N['r'])) for q in (0, 1)]
    du = universe[0] - universe[1]
    tau = du * C * du / 2
    rel, ab, count = 0, 0, 0
    noise = se / (n['i'] * n['r'])                     # e is independent across cells
    for items in itertools.combinations(range(N['i']), n['i']):
        for raters in itertools.combinations(range(N['r']), n['r']):
            delta = [mean_weights(q, items, raters) - universe[q] for q in (0, 1)]
            ab += delta[0] * C * delta[0] + noise
            dd = delta[0] - delta[1]                   # the two persons' relative errors
            rel += (dd * C * dd + 2 * noise) / 2
            count += 1
    return tau, rel / count, ab / count

for N in ({'i': 2, 'r': 3}, {'i': 3, 'r': 2}, {'i': 3, 'r': 4}):
    for ni in range(1, N['i'] + 1):
        for nr in range(1, N['r'] + 1):
            s = {a: rand_q() for a in EFFECTS}
            se = rand_q(0, 2)
            n = {'i': ni, 'r': nr}
            assert d_study_brute(s, rand_q(), se, n, N) == d_study_closed(s, se, n, N), (N, n)
print("ok: universe-score, relative and absolute error variances match brute force on finite universes")

# --- 5. The residual split, limits, and the formulas crolib implements ----
se_v, R = var('s_e R')
n_i, n_r, N_i, N_r = nv['i'], nv['r'], Nv['i'], Nv['r']
both = d_study_closed(sv, se_v, {'i': n_i, 'r': n_r}, {'i': N_i, 'r': N_r})
pir = sv[('p', 'i', 'r')]
split = lambda q: (diff(q, pir) - diff(q, se_v)).simplify_full()
assert bool(split(both[1]) == -1 / (N_i * N_r)) and bool(split(both[2]) == -1 / (N_i * N_r))
print("ok: with both facets finite the projection depends on how the residual splits")

p, i, r, pi, pr, ir = [sv[e] for e in EFFECTS[:6]]
def crolib_formulas(finite):
    """crolib's projection with one finite facet, from the finite-universe components."""
    if finite == 'r':
        N, n, m, cross, nested, main, facet = N_r, n_r, n_i, pi, pr, i, r
    else:
        N, n, m, cross, nested, main, facet = N_i, n_i, n_r, pr, pi, r, i
    # cross: person × the infinite facet; nested: person × the finite facet.
    fpc = 1 - n / N
    tau = p + nested / N
    rel = (cross + R / N) / m + fpc * nested / n + fpc * R / (m * n)
    ab = rel + (main + ir / N) / m + fpc * facet / n + fpc * ir / (m * n)
    return tau, rel, ab

REGION = {  # components whose bound involves the universe size, as crolib checks them
    'r': {'person': p + pr / N_r, 'item': i + ir / N_r, 'person_item': pi + R / N_r},
    'i': {'person': p + pi / N_i, 'rater': r + ir / N_i, 'person_rater': pr + R / N_i},
}
for finite, infinite in (('r', N_i), ('i', N_r)):
    for q, f in zip(both, crolib_formulas(finite)):
        lim = limit(q, **{str(infinite): oo})
        assert bool(split(lim) == 0)                   # only the residual sum matters
        assert bool((lim.subs({se_v: R - pir}) - f).simplify_full() == 0), (finite, lim, f)
    c = finite_components(sv, Nv, (finite,))
    N = {'r': N_r, 'i': N_i}[finite]
    assert all(bool(diff(c[e], pir) == 0) or bool(diff(c[e], pir) == 1 / N) or e == ('p', 'i', 'r')
               for e in EFFECTS)                       # nondecreasing in σ²(pir), N >= 2
    own = lambda e: R if e == ('p', 'i', 'r') else sv[e]
    corrected = {NAME[e]: c[e].subs({pir: R}) for e in EFFECTS
                 if not bool((c[e].subs({pir: R}) - own(e)).simplify_full() == 0)}
    assert set(corrected) == set(REGION[finite]), corrected
    assert all(bool((corrected[k] - REGION[finite][k]).simplify_full() == 0) for k in corrected)
    print("   %s finite: %s" % (finite, "; ".join("%s >= 0" % v for v in corrected.values())))
# Brennan (1977, printed p. 55), items finite, occasions in place of raters:
#   σ²(τ) = σ²(p) + σ²(pi)/N_i,
#   σ²(δ) = (1 − n_i/N_i) σ²(pi)/n_i + σ²(po)/n_o + σ²(pio)/(n_i n_o).
tau_i, rel_i, _ = crolib_formulas('i')
assert bool((tau_i - (p + pi / N_i)).simplify_full() == 0)
assert bool((rel_i - ((1 - n_i / N_i) * pi / n_i + pr / n_r + R / (n_i * n_r))).simplify_full() == 0)
print("ok: one finite facet: crolib's formulas are the limits and match Brennan's example; the region takes σ²(pir) = residual")
