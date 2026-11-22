# Where derivation stops: a kernel, a criterion, and a ten-target audit

*Gate-2 bundle note — published in this repository on 2026-11-22.*

## §1 The kernel of c_g = c

**Claim (assembled premise ledger).** The equality of the propagation
speeds of gravity and light is usually presented as resting on two
dynamical postulates: (P1) exact Lorentz invariance of the vacuum and
(P2) universal coupling of gravity to all matter. Both are theorems of
strictly weaker premises:

- **P2 is a theorem** (Weinberg, 1964/65): in a Lorentz-invariant
  S-matrix containing a massless spin-2 state, Lorentz invariance of
  the soft factor forces all species' couplings to coincide. The
  deciding computation is linear algebra: momentum conservation reduces
  the soft condition Σ κᵢ pᵢ = 0 to Σᵢ<ₙ (κᵢ − κₙ) pᵢ = 0, and the
  coupling-difference map is injective — rank 2 for three legs, rank 3
  for four (exact rational arithmetic; the symbolic 2×2 minor
  a₀b₁ − a₁b₀ is a nonzero polynomial). Deser's bootstrap is a second
  route to the same demotion, with the same kernel.
- **P1 is a theorem** (Ignatowski, 1910; Frank–Rothe; Lévy-Leblond) of
  a kinematic axiom set A1 — homogeneity of spacetime, isotropy of
  space, the relativity principle, the group property of boosts, and
  causal ordering of events, all stated for **one shared spacetime** —
  plus one empirical bit A2: κ > 0, where the boost composition law
  u⊕v = (u+v)/(1+κuv) is associative for general κ (associativity
  numerator identically zero, verified symbolically). At κ = s² > 0 the
  speed 1/s is exactly invariant; at κ = 0 the same axioms give
  Galilean kinematics.

**Kernel.** After the demotions, the un-derived content of c_g = c is
exactly two items: **{κ > 0, existence of a massless spin-2 state}**
(premise A3, which also carries the S-matrix setting and the empirical
fact that the coupling is nonzero). κ > 0 is *empirical and irreducible
by consistency*: the composition law is associative for κ > 0, κ = 0
and κ < 0 alike, so consistency cannot choose the sign. Spin-2
existence is *open*: every audited argument assumes it (Deser at step
0, Feynman-style builds at premise 1, Weinberg as hypothesis), and
Weinberg–Witten constrains a composite graviton's nature, not its
existence.

*Credit and novelty.* Both theorems are classical published results
and are credited above. A dedicated search (see
`novelty_search_log.md`) found the components stated in the literature
— including the explicit remark that the axioms fix neither the sign
nor the value of κ — but did **not** find the assembled premise ledger
for c_g = c stated as such. Verdict: assembly (c) not found; this is a
bounded-search verdict, not proof of novelty.

## §2 Erasure vs selection: the tracking-slope criterion

**Definitions.** A mechanism *selects* (picks) a value if its output is
set by its inserted parameters: the output moves when they move. A
mechanism *erases* an input if its output is the same whatever the
input was. The operational test is the **tracking slope**: the
derivative of the output with respect to (a) the input being erased
and (b) the mechanism's inserted parameters. Slope ≈ 0 on both is
erasure; slope ≠ 0 on either is picking.

**Application — the QCD axion (Peccei–Quinn).** With
V(θ_eff) = χ_top(1 − cos θ_eff), θ_eff = θ̄ + a/f_a, the minimum sits
at θ_eff = 0 for *every* input θ̄ ∈ (−π, π], every f_a, and every
χ_top > 0: the tracking slope is **exactly 0** (analytic root-solving
at 50-digit precision; worst |θ_eff,min| = 0.0 over 36 sampled
(θ̄, f_a, χ) combinations, including the θ̄ = π boundary). Zero is not
an arbitrary landing point: it is the CP-restoration point, and the
potential is CP-even and periodic — even harmonics up to ε = 0.3 do
not move the minimum; a CP-odd admixture would, and would itself be a
re-inserted θ̄. Contrasts, computed the same way: a tilted-washboard
halting point tracks its inserted phase with slope exactly 1; a
derived feedback functional from the campaign's own record,
V(χ) = (26 − 16χ)/(1 − χ²) on |χ| < 1, halts at
χ* = (13 − √105)/8 = 0.3441311542550502 (reproduced exactly) with
tracking slope dx*/da = −0.0168 ≠ 0; the campaign's relaxion precedent
recorded slope 0.754911.

**Classification.** The axion is **erasure-as-a-distinct-kind**:
neither a derivation from consistency alone nor a selection shape.
Target status: **solved-by-erasure under named premises** — the PQ
structure is inserted (a structural input, not a measured number);
**the axion is undetected**; Vafa–Witten positivity (χ_top > 0 /
CP-even potential); PQ quality (the global symmetry must survive
Planck-suppressed breaking to high accuracy).

*Credit and novelty.* The distinction in substance is **implicit** in
the literature: 't Hooft naturalness (1980) singles out
symmetry-restoration points; the Barbieri–Giudice measure (1988) is a
derivative-of-output-with-respect-to-input criterion; the axion
literature's standard language is that the minimum lies at θ_eff = 0
"independent of microscopic details", while the relaxion literature's
own verb for its halting is "selects"; the self-tuning literature
frames input-independence as the desideratum (and Weinberg's no-go
theorem limits it). What the search did **not** find is the
tracking-slope as a single binary classifier applied across mechanism
classes with computed slopes. Verdict: distinction (b) implicit;
criterion-as-classifier (c) not found.

## §3 Ten-target taxonomy

Each target was audited under one discipline: measured numbers are
bullseyes and checks, never inputs; a route consuming a measured
dimensionless number is *transport*, not derivation; every route
carries a full input ledger. Statuses (deciding computations in the
campaign record; three spot re-computed independently by the gate —
Koide Q, Starobinsky N, tracker slope — all reproduced):

| # | Target | Status | Named remainder |
|---|---|---|---|
| 1 | BH coefficient 1/4 | Derived semiclassically (1/4 = (2π)/(8π)); microscopic remainder re-aimed | G-calculability (m_p/M_Pl = 7.685×10⁻²⁰ from zero measured inputs) — unmoved |
| 2 | c_g = c | Rests on classified kernel (§1) | κ > 0 empirical-irreducible; spin-2 existence open |
| 3 | α | Open — transport everywhere | A consistency condition outputting a U(1) coupling — not found |
| 4 | sin²θ_W | Blind: sweeps (0,1) with all consistency conditions satisfied | Any forcing must be non-anomaly and coupling-sensitive — none audited |
| 5 | m_p/m_e | Transport-with-ledger (lattice QCD: ≥2 measured dimensionless inputs + named scale input + measured m_e) | Fewer measured inputs than outputs — none audited |
| 6 | Lepton ratios | Open — Koide is bookkeeping (identity of its ansatz); rest insertion/transport | A forcing of Yukawa ratios — none audited |
| 7 | Ω_Λ/Ω_m | Open — tracker erases initial conditions (slope 8.3×10⁻⁷/dex) but picks by parameters (d ln Ω/d ln λ = −2) | A mechanism with both slopes ≈ 0 and no measured input — none audited |
| 8 | n_s | Open — insertion-with-a-formula everywhere (Starobinsky: implied N = 56.98, dn_s/dN = +6.16×10⁻⁴ ≠ 0, N reheating-inserted) | A tilt tracking nothing inserted — none audited |
| 9 | η_B | Open — every route fits (smallest ledger: thermal leptogenesis, ≥3 unmeasured free entries) | CP asymmetry as an output — none audited |
| 10 | θ̄_QCD | Solved-by-erasure under named premises (§2) | PQ inserted; axion undetected; Vafa–Witten positivity; PQ quality |

**Bottom line.** Of ten measured numbers, none is derived from
consistency alone with zero remainder: one is derived
semiclassically, one rests on a two-element kernel, one is erased
under premises, two are transported, one is invisible to consistency,
and four are open with every audited route inserting, fitting, or
transporting.

*Novelty.* Parameter-counting treatments of the constants exist
(e.g. Uzan's count of 19 unexplained dimensionless parameters; the
Duff–Okun–Veneziano discussion of which constants are fundamental).
An audited per-target taxonomy with input ledgers and deciding
computations over this target set was **not found** in the searched
sources. Verdict: (c) not found, bounded as stated.
