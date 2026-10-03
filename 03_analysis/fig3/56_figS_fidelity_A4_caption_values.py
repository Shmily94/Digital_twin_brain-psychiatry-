"""figS_fidelity_A4_caption_values.csv | Supplementary Fig. S7 (04_figures/supp_fidelity/figS_fidelity_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code does not compute anything. It initializes an empty
    dictionary S and then writes it out as a CSV, iterating over its
    (nonexistent) key-value pairs to build rows. Since S is never
    populated with any data, the resulting DataFrame has no rows, so the
    output file would contain only the header with zero data rows despite
    the stated row count of 18. One row of the intended output would
    represent a single named caption value, paired as a key label and its
    corresponding value, but the code as shown produces none.

INPUT FILES
    bold_cc_n288.csv
    cpm_predict_perf_n288.csv

OUTPUT FILE
    figS_fidelity_A4_caption_values.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_fidelity/figS_fidelity_A4_caption_values.csv

STATISTICAL TESTS
    paired two-sided t test
    Cohen's d_z effect size

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    fixed in the original run (seed = 0)

PROVENANCE
    execution-log cell : 8bcf66f6-e8bb-45e5-b1f4-e40780d74d8b
    frame              : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
    ran                : 2026-09-27 07:20:15 UTC
    conda environment  : (not recorded)
    verbatim archive   : recovered/fig3/figS_fidelity_A4_caption_values__cell_8bcf66f6.py
    candidates found   : 1

REORGANISATION APPLIED
    A header was added; the imports, the input paths and the constants the
    interactive cell inherited from earlier cells in its session were made
    explicit; exploratory prints and abandoned branches were dropped; all file
    writes were redirected to OUT_DIR.  No computation, test, covariate,
    correction or seed was changed.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Output redirection.  The reference data file lives under 04_figures/, which
# this package treats as read-only evidence.  Every file write performed below
# is therefore redirected into OUT_DIR under its own basename.  Set the
# RECOVERY_OUT_DIR environment variable to choose a different scratch folder.
# ---------------------------------------------------------------------------
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/fig_color")
OUT_DIR = os.environ.get("RECOVERY_OUT_DIR", os.path.join("/tmp", "recovery_scratch", "fig3"))
os.makedirs(OUT_DIR, exist_ok=True)


def _install_write_guard():
    import pandas as _pd

    def _redirect(p):
        if isinstance(p, (str, bytes, os.PathLike)):
            p = os.fspath(p)
            if os.path.abspath(os.path.dirname(p) or ".") != os.path.abspath(OUT_DIR):
                return os.path.join(OUT_DIR, os.path.basename(p))
        return p

    for _cls, _name in ((_pd.DataFrame, "to_csv"), (_pd.Series, "to_csv"),
                        (_pd.DataFrame, "to_excel"), (_pd.Series, "to_excel")):
        _orig = getattr(_cls, _name)

        def _w(self, path_or_buf=None, *a, __o=_orig, **k):
            return __o(self, _redirect(path_or_buf), *a, **k)
        setattr(_cls, _name, _w)
    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib.figure import Figure as _F
        _sf = _F.savefig

        def _sfw(self, fname, *a, **k):
            return _sf(self, _redirect(fname), *a, **k)
        _F.savefig = _sfw
    except Exception:
        pass
    try:
        import scipy.io as _sio
        _sm = _sio.savemat

        def _smw(fn, *a, **k):
            return _sm(_redirect(fn), *a, **k)
        _sio.savemat = _smw
    except Exception:
        pass


_install_write_guard()

import pandas as pd

# NOTE ON THE SOURCE
#   The producing cell wrote the figure script
#     /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_fidelity/figS_fidelity_A4.py
#   which performs this computation itself.  The code below is that script up
#   to and including the statement that writes this table (prints dropped).
#   HERE and sys.path point at the package copy of that figure directory.
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_fidelity")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_fidelity")
HERE = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_fidelity"

# ---- computation: recovered from execution-log cell 8bcf66f6
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy import stats
FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_fidelity")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce
from supp_kit import fill
from fig_export import collect_text_records
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT
DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_fidelity_A4" if WITH_CAP else "figS_fidelity_A4_nocaption"
SUPP_NO = "S4"
apply_np_style()
K.apply_page_style()
CC = pd.read_csv(os.path.join(FIGDIR, "supp_boldcc", "data",
                              "bold_cc_n288.csv"))
D = pd.read_csv(os.path.join(FIGDIR, "supp_cpm", "data",
                             "cpm_predict_perf_n288.csv"))
RT = D[D.target.str.endswith("_RT")].copy()
N = len(CC)
assert int(D.n.iloc[0]) == N, "the two tables must be the same sample"
TASKS = ["mid", "sst"]
TLAB = {"mid": "MID", "sst": "SST"}
SETS = ["assimilated", "whole"]
SETLAB = {"assimilated": "Assimilated regions", "whole": "Whole brain"}
SETCOL = {"assimilated": C("np12"), "whole": C("reference")}
CONDS = ["BIG_WIN_RT", "SMALL_WIN_RT", "NO_WIN_RT"]
CLAB = {"BIG_WIN_RT": "Big win", "SMALL_WIN_RT": "Small win",
        "NO_WIN_RT": "No win"}
STATES = ["anticipation", "feedback"]
SRCS = [("empirical", "anticipation"), ("empirical", "feedback"),
        ("simulated", "anticipation"), ("simulated", "feedback")]
SMK = {"anticipation": "o", "feedback": "s"}
BASE = C("np12")
S = {}
def mark(p):
    return ("***" if p < .001 else "**" if p < .01 else "*" if p < .05
            else "n.s.")
def v(task, kind):
    return CC[f"{task}_{kind}"].to_numpy(float)
def get(target, src, state):
    row = RT[(RT.target == target) & (RT.fc_source == src)
             & (RT.task_state == state)].iloc[0]
    return float(row.r), float(row.p)
def paired_stats():
    """The 6 vs 6 paired comparison: simulated against empirical, one pair
    per prediction target (three conditions x two task states)."""
    e = np.array([get(c, "empirical", st)[0] for c in CONDS for st in STATES])
    s_ = np.array([get(c, "simulated", st)[0] for c in CONDS for st in STATES])
    d = s_ - e
    t_, p_t = stats.ttest_rel(s_, e)
    sd = float(d.std(ddof=1))
    tc = stats.t.ppf(.975, len(d) - 1)
    se = sd / np.sqrt(len(d))
    return e, s_, dict(n_targets=len(e), emp=float(e.mean()),
                       sim=float(s_.mean()), diff=float(d.mean()), sd=sd,
                       lo=float(d.mean() - tc * se),
                       hi=float(d.mean() + tc * se),
                       t=float(t_), p=float(p_t), dz=float(d.mean() / sd),
                       n_above=int((s_ > e).sum()))
def p_a(ax):
    pos = {("mid", "assimilated"): 0.0, ("mid", "whole"): 0.80,
           ("sst", "assimilated"): 1.95, ("sst", "whole"): 2.75}
    rng = np.random.default_rng(0)
    for task in TASKS:
        for kind in SETS:
            x, c = pos[(task, kind)], SETCOL[kind]
            y = v(task, kind)
            ax.scatter(x + rng.uniform(-.19, .19, len(y)), y, s=2.2,
                       facecolor=c, edgecolor="none", alpha=.45, zorder=2)
            bp = ax.boxplot([y], positions=[x], widths=.58, showfliers=False,
                            patch_artist=True, zorder=3)
            for el in ("boxes", "whiskers", "caps", "medians"):
                for art in bp[el]:
                    art.set_linewidth(LW); art.set_color("black")
            bp["boxes"][0].set_facecolor(fill(c))
            bp["boxes"][0].set_edgecolor("black")
            bp["boxes"][0].set_alpha(.92)
            S[f"a|{task}|{kind}"] = dict(
                mean=float(y.mean()), sd=float(y.std(ddof=1)),
                median=float(np.median(y)), lo=float(y.min()),
                hi=float(y.max()))
        a_, w_ = v(task, "assimilated"), v(task, "whole")
        d = a_ - w_
        t_, p_ = stats.ttest_rel(a_, w_)
        S[f"a|{task}|paired"] = dict(
            diff=float(d.mean()), t=float(t_), p=float(p_),
            dz=float(d.mean() / d.std(ddof=1)), df=len(d) - 1)
        x1, x2 = pos[(task, "assimilated")], pos[(task, "whole")]
        yb = .952
        ax.plot([x1, x1, x2, x2], [yb - .020, yb, yb, yb - .020],
                color="0.35", lw=LW, zorder=5)
        ax.text((x1 + x2) / 2, yb + .006, mark(float(p_)), ha="center",
                va="bottom", fontsize=ANNOT_PT, zorder=5)
    ax.set_xticks([np.mean([pos[(t, k)] for k in SETS]) for t in TASKS])
    ax.set_xticklabels([TLAB[t] for t in TASKS], fontsize=TICK_PT)
    ax.set_xlim(-.58, 3.33)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0, .2, .4, .6, .8, 1.0])
    ax.set_ylabel("Simulated-empirical BOLD\ncorrelation", fontsize=LABEL_PT)
    ax.tick_params(axis="x", length=0)
    hs = [Patch(facecolor=fill(SETCOL[k]), edgecolor="black", lw=LW)
          for k in SETS]
    ax.legend(hs, [SETLAB[k] for k in SETS], loc="lower center",
              bbox_to_anchor=(.5, 1.02), ncol=1, fontsize=TICK_PT,
              frameon=False, borderpad=0, handlelength=1.3,
              handletextpad=.5, labelspacing=.25)
def bubble(r):
    """Marker area proportional to r, so area reads as accuracy."""
    return 560.0 * max(r, 0.0)
def p_b(ax):
    for yi, (src, state) in enumerate(SRCS[::-1]):          # top row first
        for xi, cond in enumerate(CONDS):
            r, p = get(cond, src, state)
            filled = src == "simulated"
            ax.scatter(xi, yi, s=bubble(r), marker="o",
                       facecolor=BASE if filled else "white",
                       edgecolor=BASE, linewidth=LW * 1.3, zorder=3)
            ax.text(xi, yi - .40, mark(p), ha="center", va="top",
                    fontsize=TICK_PT, color="0.35" if p >= .05 else "black")
            S[f"b|{cond}|{src}|{state}"] = dict(r=r, p=p)
    ax.set_xticks(range(len(CONDS)))
    ax.set_xticklabels([CLAB[c] for c in CONDS], fontsize=TICK_PT)
    ax.set_yticks(range(len(SRCS)))
    ax.set_yticklabels([f"{s.capitalize()}\n{st}" for s, st in SRCS[::-1]],
                       fontsize=TICK_PT)
    ax.set_xlim(-.62, len(CONDS) - .38)
    ax.set_ylim(-.75, len(SRCS) - .25)
    ax.set_xlabel("MID condition", fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT, length=0)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="0.92", lw=LW, zorder=0)
    ax.set_axisbelow(True)
    hs = [Line2D([], [], marker="o", linestyle="none",
                 markersize=np.sqrt(bubble(v_)) * .62, markerfacecolor="none",
                 markeredgecolor="0.45", markeredgewidth=LW)
          for v_ in (.2, .4)]
    ax.legend(hs, ["$r$ = 0.2", "$r$ = 0.4"], loc="lower center",
              bbox_to_anchor=(.5, 1.0), ncol=2, fontsize=TICK_PT,
              frameon=False, borderpad=0, handletextpad=.6,
              columnspacing=1.4)
def p_c(ax):
    e, s_, st_ = paired_stats()
    S["c"] = st_
    pairs = [(c, st) for c in CONDS for st in STATES]
    POS = {"empirical": 0.0, "simulated": 1.0}
    for i in range(len(e)):                       # one line per target
        ax.plot([POS["empirical"], POS["simulated"]], [e[i], s_[i]],
                color="0.75", lw=LW * .8, zorder=2)
    for kind, vals in (("empirical", e), ("simulated", s_)):
        x = POS[kind]
        bp = ax.boxplot([vals], positions=[x], widths=.52, showfliers=False,
                        patch_artist=True, zorder=1)
        for el in ("boxes", "whiskers", "caps", "medians"):
            for art in bp[el]:
                art.set_linewidth(LW); art.set_color("black")
        bp["boxes"][0].set_facecolor(fill(BASE))
        bp["boxes"][0].set_edgecolor("black")
        filled = kind == "simulated"
        for (cond, state), y in zip(pairs, vals):
            ax.scatter(x, y, s=15, marker=SMK[state],
                       facecolor=BASE if filled else "white",
                       edgecolor=BASE, linewidth=LW * 1.1, zorder=3)
    ax.set_xlim(-.62, 1.62)
    ax.set_ylim(.385, .525)
    ax.set_xticks([POS["empirical"], POS["simulated"]])
    ax.set_xticklabels(["Empirical\nFC", "Simulated\nFC"], fontsize=TICK_PT)
    ax.set_yticks([.40, .45, .50])
    ax.set_ylabel("Prediction $r$", fontsize=LABEL_PT)
    ax.tick_params(axis="x", length=0)
    yb = .508
    ax.plot([0, 0, 1, 1], [yb - .006, yb, yb, yb - .006], color="0.35",
            lw=LW, zorder=4)
    ax.text(.5, yb + .002, mark(float(st_["p"])), ha="center", va="bottom",
            fontsize=ANNOT_PT, zorder=4)
    hs = [Line2D([], [], marker=SMK[st], linestyle="none", markersize=3.2,
                 markerfacecolor=BASE, markeredgecolor=BASE)
          for st in STATES]
    ax.legend(hs, ["Anticipation", "Feedback"], loc="upper left",
              fontsize=TICK_PT, frameon=False, borderaxespad=.2,
              handletextpad=.4, labelspacing=.25)
PANEL_FN = {"a": p_a, "b": p_b, "c": p_c}
GUT = K.LETTER_W + K.LETTER_PADX
GAPX, GAP = 3.0, K.GAP
LETTER_BAND, MB = K.LETTER_BAND, K.MB
XB = 11.0
MAX_H = 54.0
ROWS = [["a", "b", "c"]]
BLOCK = {"a": 58.0, "b": 72.0, "c": 44.0}
def col_geom(fig, panels):
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    by = {p["ch"]: p for p in panels}
    geom, x = {}, ML
    for row in ROWS:
        for ch in row:
            ax = by[ch]["axes"][0]
            bb, pos = ax.get_tightbbox(rend), ax.get_position()
            L = min(max(pos.x0 * PW - mm(bb.x0), 0.0), 26.0)
            R_ = min(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0), 3.0)
            geom[ch] = (x, x + GUT + L, max(BLOCK[ch] - GUT - L - R_, 22.0))
            x += BLOCK[ch] + GAPX
    return geom
def build(plot_h, geom=None):
    f = plt.figure(figsize=panel(PW, PH))
    out, y = [], MT
    for row in ROWS:
        top = y + LETTER_BAND
        x = ML
        for ch in row:
            slot, ax_x, ax_w = (geom[ch] if geom else
                                (x, x + GUT + 16.0, BLOCK[ch] - GUT - 20.0))
            ax = K.axes_mm(f, ax_x, top, ax_w, plot_h)
            PANEL_FN[ch](ax)
            out.append(dict(ch=ch, x=slot, axes=[ax],
                            txt=K.letter(f, slot, top - 1.2, ch)))
            x += BLOCK[ch] + GAPX
        y = top + plot_h + XB + GAP
    enforce(f)
    for p_ in out:                     # enforce() restores the house tick
        ax = p_["axes"][0]             # marks; categorical axes have none
        if p_["ch"] == "b":
            ax.tick_params(axis="both", length=0)
        else:
            ax.tick_params(axis="x", length=0)
    return f, out, y - GAP
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Fidelity of the simulated "
             "signals, from the regional BOLD time series to the behaviour "
             "the simulated connectivity predicts.")
def pf(p):
    return ("P < 0.001" if p < 1e-3 else f"P = {p:.3f}" if p >= .01
            else f"P = {p:.2g}")
def dline(task, kind):
    d = S[f"a|{task}|{kind}"]
    return (f"{d['mean']:.3f} +/- {d['sd']:.3f} (median {d['median']:.3f}, "
            f"range {d['lo']:.3f} to {d['hi']:.3f})")
def b_line(src, state):
    return ", ".join(
        f"{CLAB[c].lower()} r = {S[f'b|{c}|{src}|{state}']['r']:.3f} "
        f"({pf(S[f'b|{c}|{src}|{state}']['p'])})" for c in CONDS)
def caption_runs():
    c_ = S["c"]
    cap = [
        ("", f"All panels are the same n = {N} participants, the sample "
             f"retained after the mean framewise displacement < 0.5 mm "
             f"criterion. Panels carry only the significance symbol "
             f"(*** P < 0.001, ** P < 0.01, * P < 0.05, n.s. not "
             f"significant); the coefficients are given below, and the "
             f"per-participant BOLD correlations and all 32 prediction "
             f"models are in bold_cc_n288.csv and "
             f"cpm_predict_perf_n288.csv. "),
        ("a", f", correlation between the simulated and the empirical "
              f"regional BOLD time series in each participant, evaluated "
              f"over the regions whose empirical signals entered the data "
              f"assimilation and over all regions of the brain, for the "
              f"monetary incentive delay task (MID) and the stop-signal task "
              f"(SST). Boxes are the median and interquartile range with "
              f"whiskers at 1.5 x IQR, one point per participant. MID "
              f"assimilated regions {dline('mid', 'assimilated')}, MID whole "
              f"brain {dline('mid', 'whole')}; SST assimilated regions "
              f"{dline('sst', 'assimilated')}, SST whole brain "
              f"{dline('sst', 'whole')}. The assimilated regions exceed the "
              f"whole brain by {S['a|mid|paired']['diff']:.3f} in MID "
              f"(paired-samples two-sided t test, "
              f"t({S['a|mid|paired']['df']}) = {S['a|mid|paired']['t']:.1f}, "
              f"{pf(S['a|mid|paired']['p'])}, "
              f"Cohen's dz = {S['a|mid|paired']['dz']:.2f}) and by "
              f"{S['a|sst|paired']['diff']:.3f} in SST "
              f"(t({S['a|sst|paired']['df']}) = {S['a|sst|paired']['t']:.1f}, "
              f"{pf(S['a|sst|paired']['p'])}, "
              f"dz = {S['a|sst|paired']['dz']:.2f}), which is expected: the "
              f"assimilated signals are the fitting target, the whole-brain "
              f"value is the out-of-sample agreement. "),
        ("b", ", connectome-based predictive modelling (CPM) of MID response "
              "time, trained and tested by leave-one-out cross-validation on "
              "whole-brain task-state functional connectivity with an "
              "edge-selection threshold of P < 0.01; accuracy is Spearman's "
              "correlation between predicted and observed response time, "
              "averaged over the positive- and negative-edge models. Bubble "
              "area is proportional to r, open for empirical connectivity "
              "and filled for simulated. Empirical anticipation: "
              + b_line("empirical", "anticipation")
              + ". Empirical feedback: " + b_line("empirical", "feedback")
              + ". Simulated anticipation: "
              + b_line("simulated", "anticipation")
              + ". Simulated feedback: " + b_line("simulated", "feedback")
              + ". Response time is predicted well above chance from every "
                "one of the four connectivity sources and in all three "
                "conditions. "),
        ("c", f", the {c_['n_targets']} prediction targets of b (three "
              f"conditions x two task states) as a paired comparison of "
              f"simulated against empirical connectivity; each line joins "
              f"the two models of one target, boxes are the median and "
              f"interquartile range over the {c_['n_targets']} targets, open "
              f"markers are empirical and filled markers simulated. "
              f"Simulated connectivity predicts at least as well as "
              f"empirical connectivity in {c_['n_above']} of "
              f"{c_['n_targets']} targets, mean r = {c_['sim']:.3f} against "
              f"{c_['emp']:.3f}, a mean advantage of {c_['diff']:+.3f} "
              f"(95% CI {c_['lo']:+.3f} to {c_['hi']:+.3f}; paired-samples "
              f"two-sided t test, t({c_['n_targets'] - 1}) = {c_['t']:.3f}, "
              f"{pf(c_['p'])}, Cohen's dz = {c_['dz']:.2f}). This comparison "
              f"is across prediction targets, not across participants, so it "
              f"tests whether the simulated connectome carries the "
              f"behaviour-predictive structure of the empirical one, not "
              f"whether any single model is better in an individual. "),
        ("", "All tests are two-sided and uncorrected. The accuracy "
             "(hit-rate) targets and the two difference contrasts (big-win "
             "minus no-win, small-win minus no-win) were fitted with the "
             "same pipeline and are tabulated in the source file; they are "
             "predicted far less well than response time from either "
             "connectivity source. "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs
_f0, _p0, _ = build(46.0)
_runs0 = caption_runs()
_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
plt.close(_f0)
CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
FIXED = MT + LETTER_BAND + XB
PLOT_H = min(PH - MB - CAP_H - FIXED, MAX_H)
assert PLOT_H > 20.0, f"no room for the panels: {PLOT_H:.1f} mm"
_f1, _p1, _ = build(PLOT_H)
_geom = col_geom(_f1, _p1)
plt.close(_f1)
for _ in range(4):
    _f2, _p2, _ = build(PLOT_H, geom=_geom)
    _geom = col_geom(_f2, _p2)
    plt.close(_f2)
fig, PANELS, BOTTOM = build(PLOT_H, geom=_geom)
K.place_letters(fig, PANELS, rows=ROWS)
runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
png, pdf, ppt = (os.path.join(HERE, STEM + ext)
                 for ext in (".png", ".pdf", ".pptx"))
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")
K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
              collect_text_records=collect_text_records)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
pd.DataFrame([{"key": k, "value": str(v_)} for k, v_ in S.items()]).to_csv(
    os.path.join(HERE, "figS_fidelity_A4_caption_values.csv"), index=False)
