#!/usr/bin/env python3
"""Regenerate the figure in this folder from this bundle's own record.

Sources (all inside this bundle):
  - verification/g2_verify_results.json -- the gate's independent
    re-verification results (axion slope, washboard slope, G26-2
    feedback-functional slope, tracker parameter slope, Starobinsky
    dn_s/dN). Values marked [V] below are read from that file.
  - note.md -- two further values are the campaign's recorded slopes
    as stated in the note and are NOT re-derived by the gate's
    verification: the tracker initial-condition slope (note.md §3
    table, target 7) and the relaxion precedent slope (note.md §2).
    Values marked [N].

Figure:
  tracking_slopes.png -- the recorded tracking slopes, with the
  zero line that separates erasure (slope ~ 0) from picking.

Run:  python3 make_figures.py        (requires matplotlib)
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
V = json.loads((HERE.parent / "verification" / "g2_verify_results.json")
               .read_text())

# [V] gate-reproduced values, read from the verification results file.
axion = 0.0  # ii_axion: "0 (every sampled output is 0)"
washboard = float(V["items"]["ii_picking_controls"]
                  ["washboard_slope_dxmin_dc_exact"])          # 1
g26_2 = float(V["items"]["ii_picking_controls"]
              ["G26-2_tracking_slope_dxstar_da"])              # -0.01679...
tracker_par = float(V["items"]["iii_spot"]
                    ["tracker_dlnOmega_dlnlambda"])           # -2
starobinsky = float(V["items"]["iii_spot"]["dns_dN"])          # +0.000616...

# [N] campaign-record values stated in note.md, not gate-re-derived.
tracker_ic = 8.3e-7     # note.md §3, target 7: "slope 8.3e-7/dex"
relaxion = 0.754911     # note.md §2: "relaxion precedent recorded slope"

# (label, slope, value-as-printed, erases-this-input?)
ROWS = [
    ("Tracker - d ln Omega / d ln lambda (parameter)", tracker_par,
     "-2 (exact)", False),
    ("Feedback functional (G26-2) - dx*/da", g26_2, "-0.0168", False),
    ("Axion - theta_eff minimum vs input theta-bar", axion,
     "0 (exact)", True),
    ("Tracker - Omega vs initial conditions, per dex", tracker_ic,
     "8.3e-7 /dex", True),
    ("Starobinsky - dn_s/dN", starobinsky, "+6.16e-4", False),
    ("Relaxion precedent (recorded) - halting point", relaxion,
     "+0.754911", False),
    ("Tilted washboard - halting point vs inserted phase", washboard,
     "+1 (exact)", False),
]


def fig_slopes():
    labels = [r[0] for r in ROWS]
    vals = [r[1] for r in ROWS]
    colours = ["#2e7d32" if r[3] else "#c62828" for r in ROWS]
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    y = range(len(ROWS))
    ax.barh(list(y), vals, color=colours, height=0.62)
    ax.axvline(0, color="black", lw=1.2)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlim(-2.35, 1.45)
    for yi, r in zip(y, ROWS):
        v, txt = r[1], r[2]
        if v >= 0:
            ax.text(v + 0.05, yi, txt, va="center", fontsize=8.5)
        elif v <= -1.5:
            # long bar: put the value inside it, at its left end
            ax.text(v + 0.06, yi, txt, va="center", ha="left",
                    fontsize=8.5, color="white")
        else:
            ax.text(v - 0.05, yi, txt, va="center", ha="right", fontsize=8.5)
    ax.set_xlabel("tracking slope: d(output) / d(input or inserted parameter), "
                  "linear scale")
    ax.set_title("Tracking slopes recorded in the Gate-2 note (note.md §2-§3)",
                 fontsize=11)
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(HERE / "tracking_slopes.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    fig_slopes()
    print("wrote tracking_slopes.png")
