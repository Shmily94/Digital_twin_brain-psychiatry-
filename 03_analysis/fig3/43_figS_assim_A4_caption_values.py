"""figS_assim_A4_caption_values.csv | Supplementary Fig. S10 (04_figures/supp_assim/figS_assim_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code does not actually compute anything: the dictionary S that
    supplies the rows is initialized empty and never populated before
    being written out. As written, the script would produce a table with
    zero rows, since the CSV is built directly from the (empty) contents
    of S using a dict comprehension over its items. One row of the
    intended output would represent a single key value pair, with the key
    column holding some named quantity relevant to the supp_assim figure
    and the value column holding that quantity's value cast to a string,
    but no such pair is ever assigned in this code. To match a shipped
    file with three rows, additional code that populates S with three
    entries must have existed elsewhere and is missing from this recovered
    snippet.

INPUT FILES
    assim5_edges_mid.csv
    assim5_stats.csv

OUTPUT FILE
    figS_assim_A4_caption_values.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_assim/figS_assim_A4_caption_values.csv

STATISTICAL TESTS
    intraclass correlation (ICC)
    standard error of the mean

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    fixed in the original run (seed = 0, 1)

PROVENANCE
    execution-log cell : be0edf77-3b6a-4e23-a4a8-b39d75ca515a
    frame              : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
    ran                : 2026-09-24 22:51:05 UTC
    conda environment  : (not recorded)
    verbatim archive   : recovered/fig3/figS_assim_A4_caption_values__cell_be0edf77.py
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
#     /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_assim/figS_assim_A4.py
#   which performs this computation itself.  The code below is that script up
#   to and including the statement that writes this table (prints dropped).
#   HERE and sys.path point at the package copy of that figure directory.
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_assim")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_assim")
HERE = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_assim"

# ---- computation: recovered from execution-log cell be0edf77
import os, sys, itertools
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_assim")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce, panel_title
from fig_export import collect_text_records
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT
DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_assim_A4" if WITH_CAP else "figS_assim_A4_nocaption"
SUPP_NO = "S1"
apply_np_style()
K.apply_page_style()
E = pd.read_csv(os.path.join(HERE, "data", "assim5_edges_mid.csv"))
ST = pd.read_csv(os.path.join(HERE, "data",
                              "assim5_stats.csv")).set_index("statistic")["value"]
RUNS = ["run1", "run2", "run3", "run4", "run5"]
R = E[RUNS].values
COL = C("np12")
S_PT = 13.0
S = {}
def p_a(ax):
    x = np.arange(len(E))
    ax.bar(x, E["mean"], width=.62, facecolor="0.92", edgecolor="black",
           zorder=2, label="across-run mean")
    rng = np.random.default_rng(0)
    for r in RUNS:
        ax.scatter(x + rng.uniform(-.17, .17, len(E)), E[r], s=S_PT,
                   facecolor=COL, edgecolor="none", alpha=.85, zorder=3)
    ax.axhline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.set_xticks(x)
    ax.set_xticklabels([f'{e.replace("edge", "e")}\n{p}'
                        for e, p in zip(E.edge, E.pair_217space)],
                       fontsize=TICK_PT)
    ax.set_ylabel("Simulated FC", fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.scatter([], [], s=S_PT, facecolor=COL, edgecolor="none",
               label=f"individual run ({len(RUNS)})")
    ax.legend(loc="upper left", fontsize=ANNOT_PT, frameon=False,
              borderaxespad=.2, handletextpad=.5, labelspacing=.25)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + (hi - lo) * .20)
    panel_title(ax, "Five independent runs, six reward-task NP edges")
    ax.title.set_fontsize(LABEL_PT)
def p_b(ax):
    lo, hi = R.min(), R.max()
    pad = (hi - lo) * .10
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="0.6",
            ls=(0, (2.6, 1.7)), zorder=1)
    for i, j in itertools.combinations(range(len(RUNS)), 2):
        ax.scatter(R[:, i], R[:, j], s=S_PT, facecolor=COL, edgecolor="none",
                   alpha=.7, zorder=3)
    ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(lo - pad, hi + pad)
    ax.set_xlabel("Run $i$ (simulated FC)", fontsize=LABEL_PT)
    ax.set_ylabel("Run $j$ (simulated FC)", fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.text(.03, .97, f'ICC(3,1) = {ST["ICC(3,1), runs fixed"]:.3f}',
            transform=ax.transAxes, ha="left", va="top", fontsize=ANNOT_PT,
            color="0.35")
    panel_title(ax, "Runs agree edge by edge")
    ax.title.set_fontsize(LABEL_PT)
def p_c(ax):
    sig, noi = float(ST["SD between edges (signal)"]), E["sd"].values
    ax.bar([0], [sig], width=.55, facecolor="0.92", edgecolor="black", zorder=2)
    ax.bar([1], [noi.mean()], width=.55, facecolor="0.92", edgecolor="black",
           zorder=2)
    rng = np.random.default_rng(1)
    ax.scatter(1 + rng.uniform(-.14, .14, len(noi)), noi, s=S_PT,
               facecolor=COL, edgecolor="none", alpha=.85, zorder=3)
    ax.set_yscale("log")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["between\nedges", "between\nruns"], fontsize=TICK_PT)
    ax.set_xlim(-.6, 1.6)
    ax.set_ylabel("SD of simulated FC (log scale)", fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ratio = float(ST["signal/noise SD ratio"])
    ax.text(.5, .97, f"{ratio:.1f}\u00d7 in SD\n({ratio ** 2:.0f}\u00d7 in "
            f"variance)", transform=ax.transAxes, ha="center", va="top",
            fontsize=ANNOT_PT, color="0.35")
    panel_title(ax, "Signal versus run noise")
    ax.title.set_fontsize(LABEL_PT)
    S["sig_sd"] = sig
    S["noise_sd"] = float(noi.mean())
    S["ratio"] = ratio
PANEL_FN = {"a": p_a, "b": p_b, "c": p_c}
GUT = K.LETTER_W + K.LETTER_PADX
GAPX, GAP = 6.0, K.GAP
LETTER_BAND, MB = K.LETTER_BAND, K.MB
XB = 7.0
MAX_H = 48.0
ROW = ["a", "b", "c"]
BLOCK = {"a": 76.0, "b": 52.0, "c": 46.0}
def col_geom(fig, panels):
    """One x per column: each panel keeps its own label block, the visible gap
    between columns is GAPX and the row ends exactly on the text width."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    geom, x = {}, ML
    for p in panels:
        ax = p["axes"][0]
        bb, pos = ax.get_tightbbox(rend), ax.get_position()
        L = max(pos.x0 * PW - mm(bb.x0), 0.0)
        R_ = max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0)
        geom[p["ch"]] = (x, x + GUT + L, BLOCK[p["ch"]] - GUT - L - R_)
        x += BLOCK[p["ch"]] + GAPX
    return geom
def build(plot_h, geom=None):
    f = plt.figure(figsize=panel(PW, PH))
    out = []
    top = MT + LETTER_BAND
    x = ML
    for ch in ROW:
        slot, ax_x, ax_w = (geom[ch] if geom else
                            (x, x + GUT + 14.0, BLOCK[ch] - GUT - 14.0 - 2.0))
        ax = K.axes_mm(f, ax_x, top, ax_w, plot_h)
        PANEL_FN[ch](ax)
        out.append(dict(ch=ch, x=slot, axes=[ax],
                        txt=K.letter(f, slot, top - 1.2, ch)))
        x += BLOCK[ch] + GAPX
    enforce(f)
    return f, out, top + plot_h + XB
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Reproducibility of the "
             "assimilation procedure.")
def caption_runs():
    icc3 = float(ST["ICC(3,1), runs fixed"])
    icc2 = float(ST["ICC(2,1), runs random"])
    rm, rlo, rhi = (float(ST["mean between-run profile r"]),
                    float(ST["min between-run profile r"]),
                    float(ST["max between-run profile r"]))
    n_run, n_edge = int(ST["n runs"]), int(ST["n reward-task edges"])
    n_pair = n_run * (n_run - 1) // 2
    cap = [
        ("", f"Five independent HMDA assimilation runs (ensemble Kalman "
             f"filter, 30 parallel realisations) on the reward-task (MID) "
             f"BOLD of one representative healthy control at the "
             f"100-million-neuron scale. Each run repeated assimilation and "
             f"forward simulation from scratch, so the spread shown includes "
             f"both the filter and the Ornstein-Uhlenbeck forward noise. Unit "
             f"of observation is one run \u00d7 edge, n = {n_run} runs "
             f"\u00d7 {n_edge} edges = {n_run * n_edge} values. "),
        ("a", f", the six reward-task NP edges plotted run by run: bars are "
              f"the across-run mean, points the {n_run} individual runs, and "
              f"the edge labels give the parcel pair in 217-region space. "),
        ("b", f", edge-wise agreement between runs: every one of the "
              f"{n_pair} run pairs is plotted against the identity line, "
              f"{n_pair} pairs \u00d7 {n_edge} edges = {n_pair * n_edge} "
              f"points. Reliability of the edge profile across runs is "
              f"ICC(3,1) = {icc3:.4f} (two-way mixed, runs fixed, single "
              f"measurement) and ICC(2,1) = {icc2:.4f} (two-way random, "
              f"absolute agreement); the mean between-run profile "
              f"correlation is r = {rm:.3f} (range {rlo:.3f}-{rhi:.3f}). "),
        ("c", f", the same spread expressed as standard deviations on a "
              f"logarithmic axis: between-edge s.d. {S['sig_sd']:.3f} "
              f"(the biological signal the model has to carry) against a mean "
              f"between-run s.d. of {S['noise_sd']:.4f}, a signal-to-noise "
              f"ratio of {S['ratio']:.1f}-fold in s.d. and "
              f"{S['ratio'] ** 2:.0f}-fold in variance. Points are the six "
              f"edges' individual between-run s.d. values. "),
        ("", "This is a descriptive reliability analysis; no null-hypothesis "
             "test is performed. Scope limitation: the repeats exist only for "
             "the MID edges and only for this one subject, so what is "
             "quantified here is the run-to-run stability of the assimilation "
             "procedure, not between-subject generalisability. Source values "
             "are in assim5_edges_mid.csv and assim5_stats.csv. "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs
_f0, _p0, _ = build(36.0)
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
for _ in range(3):                      # tick labels move when the width does
    _f2, _p2, _ = build(PLOT_H, geom=_geom)
    _geom = col_geom(_f2, _p2)
    plt.close(_f2)
fig, PANELS, BOTTOM = build(PLOT_H, geom=_geom)
K.place_letters(fig, PANELS, rows=[ROW])
runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
png, pdf, ppt = (os.path.join(HERE, STEM + ext) for ext in (".png", ".pdf", ".pptx"))
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")
K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
              collect_text_records=collect_text_records)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
    os.path.join(HERE, "figS_assim_A4_caption_values.csv"), index=False)
