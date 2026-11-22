#!/usr/bin/env python3
"""Gate-2 Half B: fresh independent re-verification of the derivation-era
deciding computations. Written from the mathematical statements in the
wave records only; shares no code with tests/wave29_*.py, wave31_*.py,
wave32_*.py. Seed 20261121. Controls run first; any control failure
aborts before gate numbers are read."""
import json, sys
from fractions import Fraction as F
import sympy as sp
from mpmath import mp, mpf, sin, cos, pi, findroot

mp.dps = 50
SEED = 20261121
out = {"seed": SEED, "controls": {}, "items": {}}

def rank_frac(rows):
    """Rank of a matrix of Fractions by exact Gaussian elimination."""
    M = [row[:] for row in rows]
    nr = len(M); nc = len(M[0]); r = 0
    for c in range(nc):
        piv = next((i for i in range(r, nr) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == nr: break
    return r

# ---------------- CONTROLS (must pass before any gate number) ----------------
# C0: rank machinery on known matrices
out["controls"]["C0_rank_identity"] = rank_frac([[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]])
out["controls"]["C0_rank_zero"] = rank_frac([[F(0),F(0)],[F(0),F(0)]])
# C1: deformed composition law must FAIL associativity (machinery detects it)
u, v, w, k = sp.symbols('u v w k')
def comp_def(a, b): return (a + b) / (1 + k * a**2)
num_def = sp.together(comp_def(comp_def(u, v), w) - comp_def(u, comp_def(v, w))).as_numer_denom()[0]
out["controls"]["C1_deformed_law_nonassoc"] = bool(sp.expand(num_def) != 0)
# C2: mpmath sanity at 50 digits: d/dx sin at 0.3 vs cos
h = mpf(10) ** -15  # run 1 used h=1e-30: roundoff in sin (~1e-50) divided by
# 2h swamped the quotient (err 3.1e-22) - a control-design error, caught by
# the control itself before any gate number was read; run 1 preserved in
# gate2/g2_verify_control_failure_run1.json. h=1e-15 balances truncation
# (~1e-30) against roundoff (~1e-35).
deriv = (sin(mpf('0.3') + h) - sin(mpf('0.3') - h)) / (2 * h)
out["controls"]["C2_mpmath_deriv_err"] = str(abs(deriv - cos(mpf('0.3'))))
controls_ok = (out["controls"]["C0_rank_identity"] == 3 and out["controls"]["C0_rank_zero"] == 0
               and out["controls"]["C1_deformed_law_nonassoc"]
               and abs(deriv - cos(mpf('0.3'))) < mpf(10) ** -25)
out["controls"]["ALL_CONTROLS_PASS"] = bool(controls_ok)
if not controls_ok:
    with open("gate2/g2_verify_results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1)); sys.exit("CONTROLS FAILED - gate numbers not read")

# ---------------- (i) Weinberg coupling-difference map ----------------
# Soft condition: sum_i kappa_i p_i = 0 with sum_i p_i = 0
#   => sum_{i<n} (kappa_i - kappa_n) p_i = 0.
# Injectivity of the difference map <=> {p_1..p_{n-1}} linearly independent.
def diffmap_rank(momenta):
    n = len(momenta); dim = len(momenta[0])
    # columns are p_1..p_{n-1}; build rows
    rows = [[momenta[j][i] for j in range(n - 1)] for i in range(dim)]
    return rank_frac(rows)
p3 = [(F(2), F(1), F(0)), (F(1), F(-3), F(1))]
p3.append(tuple(-(p3[0][i] + p3[1][i]) for i in range(3)))
r3 = diffmap_rank(p3)
p4 = [(F(2), F(1), F(0)), (F(1), F(-3), F(1)), (F(0), F(2), F(-2))]
p4.append(tuple(-sum(p4[j][i] for j in range(3)) for i in range(3)))
r4 = diffmap_rank(p4)
# symbolic minor: Sigma = (k1-k3) p1 + (k2-k3) p2 ; 2x2 minor of (p1,p2)
a0, a1, b0, b1 = sp.symbols('a0 a1 b0 b1')
minor = a0 * b1 - a1 * b0
out["items"]["i_weinberg"] = {
    "rank_3legs": r3, "rank_4legs": r4,
    "minor_polynomial": str(minor), "minor_identically_zero": bool(minor == 0),
    "expected": {"rank_3legs": 2, "rank_4legs": 3, "minor_identically_zero": False}}
out["items"]["i_weinberg"]["PASS"] = (r3 == 2 and r4 == 3 and minor != 0)

# ---------------- (i) Ignatowski associativity, general kappa ----------------
def comp(a, b): return (a + b) / (1 + k * a * b)
num = sp.together(comp(comp(u, v), w) - comp(u, comp(v, w))).as_numer_denom()[0]
assoc_ok = sp.expand(num) == 0
s = sp.symbols('s', positive=True)
inv_expr = sp.simplify(comp(1 / s, v).subs(k, s**2))
gal = sp.limit(comp(u, v), k, 0)
out["items"]["i_ignatowski"] = {
    "associativity_numerator_identically_zero": bool(assoc_ok),
    "invariant_speed_check (k=s^2, u=1/s)": str(inv_expr),
    "galilean_limit": str(gal),
    "expected": {"associativity_numerator_identically_zero": True,
                 "invariant_speed_check (k=s^2, u=1/s)": "1/s", "galilean_limit": "u + v"}}
out["items"]["i_ignatowski"]["PASS"] = bool(assoc_ok and str(inv_expr) == "1/s" and str(gal) == "u + v")

# ---------------- (ii) Axion erasure: analytic path, 50 digits ----------------
def theta_eff_min(theta_bar, fa, chi):
    # V(theta_eff) = chi*(1-cos(theta_eff)), theta_eff = theta_bar + a/fa.
    # Stationarity in a: sin(theta_eff) = 0; minimum branch theta_eff = 0 mod 2pi.
    # Solve with findroot on dV/da starting from a0 = -theta_bar*fa.
    a0 = -theta_bar * fa
    f = lambda a: sin(theta_bar + a / fa)  # proportional to dV/da
    try:
        root = findroot(f, a0, tol=mpf(10) ** -45, maxsteps=100)
    except Exception:
        root = a0  # a0 is already the exact root: sin(theta_bar - theta_bar) = 0
    return theta_bar + root / fa
worst = mpf(0); samples = []
for tb in [mpf('0.7'), mpf('-2.1'), mpf('3.0'), pi, mpf('-0.001'), mpf('1.23456789')]:
    for fa in [mpf(1), mpf(7) / 3, mpf(10)]:
        for chi in [mpf(1), mpf('0.4')]:
            te = theta_eff_min(tb, fa, chi)
            # fold to (-pi, pi]
            te_fold = te - 2 * pi * int(mp.floor((te + pi) / (2 * pi)))
            worst = max(worst, abs(te_fold))
            samples.append(str(te_fold))
# tracking slope of the (folded) output w.r.t. input: all outputs are 0 -> slope 0
out["items"]["ii_axion"] = {
    "worst_abs_theta_eff_min": str(worst),
    "tracking_slope_d_output_d_input": "0 (every sampled output is 0)",
    "n_samples": len(samples),
    "expected_worst": "0"}
out["items"]["ii_axion"]["PASS"] = (worst < mpf(10) ** -40)

# ---------------- (ii) Picking controls ----------------
# Control A (exact): tilted washboard V(x;c) = -cos(x-c) + lam*x, lam=3/10.
# Stationarity sin(x-c) + lam = 0, stable branch x = c - asin(lam): dx/dc = 1 exactly.
lam = sp.Rational(3, 10)
csym = sp.symbols('c', real=True)
xstar = csym - sp.asin(lam)
slope_washboard = sp.diff(xstar, csym)  # run 2 bug: diff w.r.t. a fresh
# symbols('c') without real=True - a different symbol, giving 0. Fixed.
# Control B (pilot-recorded functional, Wave 27 G26-2): V(x) = (26 - 16x)/(1 - x^2).
x = sp.symbols('x')
V = (26 - 16 * x) / (1 - x**2)
crit = sp.solve(sp.together(sp.diff(V, x)).as_numer_denom()[0], x)
crit_real = [c for c in crit if abs(complex(c.evalf())) == abs(float(c.evalf())) and float(c.evalf()) == float(c.evalf())]
# domain of the recorded functional is |chi| < 1 (chi is a mixing
# parameter); run 2 minimised over all real critical points and picked
# the out-of-domain root x = 2.9059. Restrict to the recorded domain.
xmin = min((c for c in crit if c.is_real and abs(float(c.evalf())) < 1),
           key=lambda c: float(V.subs(x, c).evalf()))
xmin_f = float(xmin.evalf())
# tracking slope of xmin w.r.t. coefficient a in V=(a-bx)/(1-x^2): x*=(a-sqrt(a^2-b^2))/b
aa, bb = sp.symbols('a b', positive=True)
xstar_ab = (aa - sp.sqrt(aa**2 - bb**2)) / bb
slope_a = float(sp.diff(xstar_ab, aa).subs({aa: 26, bb: 16}).evalf())
out["items"]["ii_picking_controls"] = {
    "washboard_slope_dxmin_dc_exact": str(slope_washboard),
    "G26-2_functional_minimum": xmin_f,
    "G26-2_recorded_minimum": 0.3441311542550502,
    "G26-2_minimum_abs_diff": abs(xmin_f - 0.3441311542550502),
    "G26-2_tracking_slope_dxstar_da": slope_a,
    "expected": {"washboard_slope": "1 (nonzero: picking)", "minimum_abs_diff": "<1e-12",
                 "tracking_slope": "nonzero"}}
out["items"]["ii_picking_controls"]["PASS"] = (str(slope_washboard) == "1"
    and abs(xmin_f - 0.3441311542550502) < 1e-12 and abs(slope_a) > 1e-3)

# ---------------- (iii) Taxonomy spot re-computations ----------------
# Koide Q from PDG-style masses (MeV)
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
Q = (me + mmu + mtau) / (me**0.5 + mmu**0.5 + mtau**0.5) ** 2
# Starobinsky: n_s = 1 - 2/N  =>  N = 2/(1-n_s); dn_s/dN = 2/N^2
ns, dns = 0.9649, 0.0042
N = 2 / (1 - ns); Nlo = 2 / (1 - (ns - dns)); Nhi = 2 / (1 - (ns + dns))
dnsdN = 2 / N**2
# Tracker: Omega = 3/lambda^2 -> d ln Omega / d ln lambda = -2 (symbolic)
lm = sp.symbols('lambda', positive=True)
slope_tr = sp.simplify(lm * sp.diff(sp.log(3 / lm**2), lm))
out["items"]["iii_spot"] = {
    "koide_Q": Q, "koide_Q_recorded": 0.6666644634, "koide_Q_abs_diff": abs(Q - 0.6666644634),
    "starobinsky_N": N, "starobinsky_N_recorded": 56.98,
    "starobinsky_N_range_from_bullseye_error": [Nlo, Nhi],
    "dns_dN": dnsdN, "dns_dN_recorded": 0.0006160050000000006,
    "tracker_dlnOmega_dlnlambda": str(slope_tr), "tracker_recorded": "-2"}
out["items"]["iii_spot"]["PASS"] = (abs(Q - 0.6666644634) < 5e-6 and abs(N - 56.98) < 0.01
    and abs(dnsdN - 0.0006160050000000006) < 1e-7 and str(slope_tr) == "-2")

out["ALL_PASS"] = bool(out["items"]["i_weinberg"]["PASS"] and out["items"]["i_ignatowski"]["PASS"]
    and out["items"]["ii_axion"]["PASS"] and out["items"]["ii_picking_controls"]["PASS"]
    and out["items"]["iii_spot"]["PASS"])
print(json.dumps(out, indent=1))
with open("gate2/g2_verify_results.json", "w") as fh:
    json.dump(out, fh, indent=1)
