"""Supplementary Fig. S14 | every scatter the longitudinal prediction cites.

Eight panels on one A4 page, all drawn from the subject-level table
(data/long_subject_level_n85.csv) in one grammar: points, an ordinary
least-squares fit and its 95% mean confidence band.

  a  the mapping itself -- the empirical NP at age 19 against the concurrent
     internalising total
  b  AMPA index against later symptom change, baseline symptoms as covariates
     (added-variable plot: both axes residualised on the four items)
  c  predicted against empirical symptom change for the model of b
  d  AMPA restoration index against the baseline empirical NP
  e  AMPA restoration index against the baseline internalising total
  f  GABA-A index, baseline symptoms as covariates
  g  GABA-A index, baseline empirical NP as covariate
  h  the same prediction for the model of g, the GABA-A model that reaches
     significance

b and f-g are the increments the text reports; c and h show what the two models
that reach significance predict; d and e ask whether the index is a repackaging
of the baseline scan or of baseline symptoms.  The AMPA index against later
change with the empirical NP as covariate is Fig. 5f of the main figure and is
NOT repeated here -- its statistics are given in the caption of d instead.  The
partial correlation and the nested F test of a panel are the same test on the
same residual degrees of freedom, so their P values agree by construction.

Every statistic is recomputed here and checked against the stored tables
(long_nested_increments_n85.csv and the permutation nulls of
long_permutation_nulls.npz); panels carry the effect size only and the exact
statistics live in the caption and in
figS14_longscatter_A4_caption_values.csv.

    python figS14_longscatter_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_longitudinal")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce
from fig_export import collect_text_records
from supp_kit import fill, pt_edge
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT

D = os.path.join(HERE, "data")
DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = ("figS14_longscatter_A4" if WITH_CAP
        else "figS14_longscatter_A4_nocaption")
SUPP_NO = "S14"
apply_np_style()
K.apply_page_style()

# ------------------------------------------------------------------- the data
T = pd.read_csv(os.path.join(D, "long_subject_level_n85.csv"))
INC = pd.read_csv(os.path.join(D, "long_nested_increments_n85.csv"))
NUL = np.load(os.path.join(D, "long_permutation_nulls.npz"))
ITEMS = [f"baseline_behaviour_{i}" for i in (3, 4, 5, 6)]
NPCOL = ["empirical_baseline_np_sum"]
assert len(T) == 85 and (T[ITEMS].sum(axis=1) == T.baseline_symptom_sum_4).all()

Y = T.fu3_symptom_change.values                 # age 23 minus age 19
N = len(T)
S = {}                                          # dumped to CSV


def resid(v, cov):
    Z = sm.add_constant(T[cov].values)
    return v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0]


def simple(a, b):
    r = stats.pearsonr(a, b)
    lo, hi = np.tanh(np.arctanh(r.statistic)
                     + np.array([-1, 1]) * 1.96 / np.sqrt(N - 3))
    return dict(n=N, r=float(r.statistic), p=float(r.pvalue), df=N - 2,
                ci=(float(lo), float(hi)))


def nested(index_col, cov, key):
    """Increment of one index over `cov`, with the partial correlation on the
    same residual degrees of freedom as the F test."""
    Z = sm.add_constant(T[cov].values)
    red = sm.OLS(Y, Z).fit()
    full = sm.OLS(Y, sm.add_constant(
        np.column_stack([T[index_col].values, T[cov].values]))).fit()
    df2 = int(full.df_resid)
    dr2 = float(full.rsquared - red.rsquared)
    F = dr2 / (1 - full.rsquared) * df2
    r = float(stats.pearsonr(resid(T[index_col].values, cov),
                             resid(Y, cov)).statistic)
    t = r * np.sqrt(df2 / (1 - r ** 2))
    lo, hi = np.tanh(np.arctanh(r)
                     + np.array([-1, 1]) * 1.96 / np.sqrt(df2 - 1))
    row = INC[(INC["index"] == key.split("|")[0])
              & (INC.covariates == key.split("|")[1])].iloc[0]
    null = NUL[key]
    p_perm = float((null >= dr2).sum()) / len(null)
    assert abs(dr2 - float(row.delta_R2)) < 5e-4, f"{key}: dR2 vs table"
    assert abs(p_perm - float(row.p_perm_deltaR2)) <= 2 / len(null)
    return dict(index=key.split("|")[0], covariates=key.split("|")[1], n=N,
                r_partial=r, ci=(float(lo), float(hi)), df=df2, t=float(t),
                p_partial=float(2 * stats.t.sf(abs(t), df2)),
                r2_reduced=float(red.rsquared), r2_full=float(full.rsquared),
                dr2=dr2, F=float(F), p_F=float(stats.f.sf(F, 1, df2)),
                p_perm=p_perm, n_perm=int(len(null)),
                model_F=float(full.fvalue), model_p=float(full.f_pvalue),
                model_df=(int(full.df_model), df2),
                fitted=np.asarray(full.fittedvalues))


MAP = simple(T.empirical_baseline_np_sum.values, T.baseline_symptom_sum_4.values)
A_NP = simple(T.ampa_index.values, T.empirical_baseline_np_sum.values)
A_SY = simple(T.ampa_index.values, T.baseline_symptom_sum_4.values)
G_NP = simple(T.gaba_index.values, T.empirical_baseline_np_sum.values)
G_SY = simple(T.gaba_index.values, T.baseline_symptom_sum_4.values)
A_ITEM = nested("ampa_index", ITEMS, "AMPA|4 baseline behaviour scores")
A_NPC = nested("ampa_index", NPCOL, "AMPA|baseline empirical NP")
G_ITEM = nested("gaba_index", ITEMS, "GABA-A|4 baseline behaviour scores")
G_NPC = nested("gaba_index", NPCOL, "GABA-A|baseline empirical NP")


def pred_of(res, letter):
    """Predicted-versus-observed for one model; in-sample, so the correlation
    IS that model's multiple R."""
    return dict(r=float(stats.pearsonr(res["fitted"], Y).statistic),
                r2=res["r2_full"], n=N, model_F=res["model_F"],
                model_p=res["model_p"], model_df=res["model_df"],
                note=f"in-sample fitted values of the model of {letter}")


PRED_A = pred_of(A_ITEM, "d")
PRED_G = pred_of(G_NPC, "f")
for k, v in [("a_mapping", MAP), ("b_ampa_vs_np", A_NP),
             ("c_ampa_vs_symptoms", A_SY), ("d_ampa_over_symptoms", A_ITEM),
             ("e_gaba_over_symptoms", G_ITEM), ("f_gaba_over_np", G_NPC),
             ("g_predicted_ampa", PRED_A), ("h_predicted_gaba", PRED_G),
             ("ampa_over_np_main_fig5f", A_NPC), ("gaba_vs_np", G_NP),
             ("gaba_vs_symptoms", G_SY)]:
    S[k] = {kk: vv for kk, vv in v.items() if kk != "fitted"}

# --------------------------------------------------------------- the grammar
S_PT = 14.0
DY = "Symptom change,\nage 19\u201323"


def eff(r):
    return f"$r$ = {r:.2f}".replace("-", "\u2212")


def scatter(ax, x, y, col, head, xlab, ylab, r):
    ax.scatter(x, y, s=S_PT, facecolor=col, edgecolor=pt_edge(col),
               linewidth=LW * .5, alpha=.9, zorder=3)
    xs = np.linspace(float(x.min()), float(x.max()), 100)
    pr = (sm.OLS(y, sm.add_constant(x)).fit()
          .get_prediction(sm.add_constant(xs)).summary_frame(alpha=.05))
    ax.fill_between(xs, pr.mean_ci_lower, pr.mean_ci_upper, color=fill(col),
                    alpha=.55, lw=0, zorder=2)
    ax.plot(xs, pr["mean"], color=col, lw=LW * 1.6, zorder=4)
    lo = float(min(y.min(), pr.mean_ci_lower.min()))
    hi = float(max(y.max(), pr.mean_ci_upper.max()))
    # heading and effect size form ONE left-aligned block in the top-left
    # corner: at 33-40 mm of axes width there is no room for the effect size
    # beside a condition name, and the corner keeps them out of the data
    txt = head + "\n" + eff(r)
    ax.set_ylim(lo - .06 * (hi - lo),
                hi + (.30 + .15 * txt.count("\n")) * (hi - lo))
    ax.set_xlabel(xlab, fontsize=LABEL_PT)
    ax.set_ylabel(ylab, fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.text(.02, .99, txt, transform=ax.transAxes, ha="left", va="top",
            fontsize=ANNOT_PT, linespacing=1.25)


def p_map(ax):
    scatter(ax, T.empirical_baseline_np_sum.values,
            T.baseline_symptom_sum_4.values, C("np12"), "Age 19",
            "Empirical NP", "Internalising total,\nage 19", MAP["r"])


def p_ampa_np(ax):
    scatter(ax, T.ampa_index.values, T.empirical_baseline_np_sum.values,
            C("ampa"), "AMPA", "Restoration index",
            "Empirical NP,\nage 19", A_NP["r"])


def p_ampa_sym(ax):
    scatter(ax, T.ampa_index.values, T.baseline_symptom_sum_4.values,
            C("ampa"), "AMPA", "Restoration index",
            "Internalising total,\nage 19", A_SY["r"])


def _added(ax, index_col, cov, col, head, res):
    # the heading names the covariate set on its own line, so the effect size
    # keeps the top-left corner of a 33 mm-wide panel readable
    scatter(ax, resid(T[index_col].values, cov), resid(Y, cov), col, head,
            "Restoration index\n(residual)", DY + "\n(residual)",
            res["r_partial"])


def p_ampa_items(ax):
    _added(ax, "ampa_index", ITEMS, C("ampa"), "AMPA\ncovariate: symptoms",
           A_ITEM)


def p_gaba_items(ax):
    _added(ax, "gaba_index", ITEMS, C("gaba"), "GABA-A\ncovariate: symptoms",
           G_ITEM)


def p_gaba_np(ax):
    _added(ax, "gaba_index", NPCOL, C("gaba"),
           "GABA-A\ncovariate: empirical NP", G_NPC)


def p_pred_ampa(ax):
    scatter(ax, A_ITEM["fitted"], Y, C("ampa"), "Model of b\n(AMPA + items)",
            "Predicted symptom change", DY, PRED_A["r"])


def p_pred_gaba(ax):
    scatter(ax, G_NPC["fitted"], Y, C("gaba"),
            "Model of g\n(GABA-A + empirical NP)",
            "Predicted symptom change",
            DY, PRED_G["r"])


# --------------------------------------------------------------- page geometry
GUT = K.LETTER_W + K.LETTER_PADX    # gutter that holds the panel letter
GAP, MB, LETTER_BAND = K.GAP, K.MB, K.LETTER_BAND
GAPX = 8.5                          # visible gap between columns
LAB_L = 17.0                        # provisional y label + y ticks
PLOT_H, XB = 33.0, 11.5             # axes height / two-line x label block
W = PW - ML - MR
ROWS = [["a", "b", "c"], ["d", "e", "f"], ["g", "h"]]
COLS = [["a", "d", "g"], ["b", "e", "h"], ["c", "f"]]
# reading order: the mapping, what the AMPA index adds and what that model
# predicts, then the two specificity checks, then the same for GABA-A
FN = dict(a=p_map, b=p_ampa_items, c=p_pred_ampa, d=p_ampa_np,
          e=p_ampa_sym, f=p_gaba_items, g=p_gaba_np, h=p_pred_gaba)
NCOL = len(COLS)


def col_geom(fig, panels):
    """One x per COLUMN so the frames of a column line up, with the visible
    gaps between columns equal to GAPX; the column's widest label block sets
    its ink line and every column gets the same axes width."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    by = {q["ch"]: q for q in panels}
    L, R = [], []
    for col in COLS:
        ll, rr = [], []
        for ch in col:
            ax = by[ch]["axes"][0]
            bb, pos = ax.get_tightbbox(rend), ax.get_position()
            ll.append(max(pos.x0 * PW - mm(bb.x0), 0.0))
            rr.append(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0))
        L.append(max(ll)); R.append(max(rr))
    w = (W - (NCOL - 1) * GAPX - NCOL * GUT - sum(L) - sum(R)) / NCOL
    geom, x = {}, ML
    for j, col in enumerate(COLS):
        for ch in col:
            geom[ch] = (x, x + GUT + L[j], w)
        x += GUT + L[j] + w + R[j] + GAPX
    return geom


def build(shift=None, geom=None):
    shift = shift or {}
    f, out, y = plt.figure(figsize=panel(PW, PH)), [], MT
    for row in ROWS:
        top = y + LETTER_BAND
        for j, ch in enumerate(row):
            slot, ax_x, ax_w = (geom[ch] if geom else
                                (ML + j * (W / NCOL),
                                 ML + j * (W / NCOL) + LAB_L,
                                 W / NCOL - LAB_L - GAPX))
            ax = K.axes_mm(f, ax_x, top + shift.get(ch, 0.0), ax_w, PLOT_H)
            FN[ch](ax)
            out.append(dict(ch=ch, x=slot, axes=[ax],
                            txt=K.letter(f, slot, top - 1.2, ch)))
        y = top + max(shift.get(ch, 0.0) for ch in row) + PLOT_H + XB + GAP
    enforce(f)
    return f, out, y - GAP


# ------------------------------------------------------------------- caption
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Longitudinal prediction of "
             f"symptom trajectories from the virtual perturbations.")


def pf(p):
    return (f"P = {p:.3g}" if p >= 1e-3 else
            f"P = {p:.2g}" if p >= 1e-4 else f"P = {p:.1e}")


def sline(d):
    return (f"r = {d['r']:+.2f} (95% CI {d['ci'][0]:+.2f} to "
            f"{d['ci'][1]:+.2f}, {pf(d['p'])})")


def nline(d):
    return (f"partial r = {d['r_partial']:+.3f} (95% CI "
            f"{d['ci'][0]:+.2f} to {d['ci'][1]:+.2f}), df = {d['df']}, "
            f"t = {d['t']:.2f}, {pf(d['p_partial'])}; delta R2 = "
            f"{d['dr2']:.4f} (R2 {d['r2_reduced']:.4f} to "
            f"{d['r2_full']:.4f}), F(1, {d['df']}) = {d['F']:.2f}, "
            f"{pf(d['p_F'])}, permutation P = {d['p_perm']:.4f}")


def mline(d, p):
    return (f"r = {p['r']:.3f}, R2 = {p['r2']:.4f}, F({p['model_df'][0]}, "
            f"{p['model_df'][1]}) = {p['model_F']:.2f}, {pf(p['model_p'])}")


def caption_runs():
    cap = [
        ("", f"Unit of observation, one participant; n = {N} IMAGEN "
             f"participants with a digital twin at age 19 and a symptom "
             f"assessment at age 23. The symptom measure is the internalising "
             f"total, the sum of items 3-6 of the battery; the outcome is its "
             f"change from age 19 to 23. The restoration index is the "
             f"difference between the symptom score predicted from the "
             f"simulated baseline twin and from the perturbed twin, computed "
             f"separately for the AMPA and the GABA-A perturbation with the "
             f"same weights; longitudinal change was used neither in model "
             f"fitting nor in the perturbation nor in the construction of the "
             f"index. In every panel one dot is one participant, the line is "
             f"the ordinary least-squares fit and the band its 95% confidence "
             f"interval. Correlations are Pearson, with Fisher-z intervals; "
             f"all tests two-sided and unpaired, with no correction for "
             f"multiple comparisons (two pre-specified indices over two "
             f"pre-specified covariate sets). Permutation P values come from "
             f"{A_ITEM['n_perm']:,} permutations of the outcome, matched to "
             f"each increment. In b, f and g both axes are residualised on that "
             f"panel's covariates, so the plotted slope is the contribution "
             f"the index makes over and above them; there the partial "
             f"correlation and the nested F test are the same test on the "
             f"same residual degrees of freedom and their P values agree "
             f"exactly. "),
        ("a", f", the mapping the index is built on: the empirical NP at age "
              f"19 against the concurrent internalising total, {sline(MAP)}. "
              f"The weights of the mapping were fitted on the imaging "
              f"sample, not on this sample's later change. "),
        ("b", f", the AMPA index against later symptom change with the four "
              f"baseline symptom items as covariates: {nline(A_ITEM)}. "
              f"Greater predicted restoration corresponds to greater symptom "
              f"reduction. With the baseline empirical NP as covariate "
              f"instead, the same index gives {nline(A_NPC)}; that scatter is "
              f"Fig. 5f of the main figure and is not repeated here. "),
        ("c", f", the model of b as a prediction: its fitted values against "
              f"the empirical change, {mline(A_ITEM, PRED_A)}. These are "
              f"in-sample values, so the correlation shown is that model's "
              f"multiple R and the panel carries no independent test; this is "
              f"the model quoted in the main text. "),
        ("d", f", the AMPA restoration index against the baseline empirical "
              f"NP, {sline(A_NP)} -- the index is not a repackaging of the "
              f"baseline scan. "),
        ("e", f", the AMPA restoration index against the baseline "
              f"internalising total, {sline(A_SY)} -- nor of baseline "
              f"symptoms. The GABA-A index behaves the same way against the "
              f"scan ({sline(G_NP)}) and is weakly related to baseline "
              f"symptoms ({sline(G_SY)}). "),
        ("f", f", the GABA-A index with the baseline symptom items as "
              f"covariates: {nline(G_ITEM)} -- it adds nothing there. "),
        ("g", f", the GABA-A index with the baseline empirical NP as "
              f"covariate: {nline(G_NPC)} -- it reaches the conventional "
              f"threshold on the F test but not on the permutation test. "),
        ("h", f", the same for the model of g, the GABA-A model that reaches "
              f"significance: {mline(G_NPC, PRED_G)} -- also in-sample and "
              f"also without an independent test. The cross-validated "
              f"versions of these models are in Supplementary Fig. S13c, "
              f"where the out-of-sample R2 is 0.111 for the four items plus "
              f"the AMPA index, 0.136 for the empirical NP plus the AMPA "
              f"index and 0.088 for the four items plus the GABA-A index. "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs


# pass 1 -- column geometry, overhangs and the caption height
_f0, _p0, _ = build()
_geom = col_geom(_f0, _p0)
plt.close(_f0)
for _ in range(3):                          # the tick labels shift a little
    _f0, _p0, _ = build(geom=_geom)         # when the axes width changes
    _geom = col_geom(_f0, _p0)
    _o1 = K.overhangs(_f0, _p0)
    _runs0 = caption_runs()
    _l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
                   _f0.canvas.get_renderer())[0] if WITH_CAP else [])
    plt.close(_f0)

_over = {ch: max(_o1[c] for c in row) for row in ROWS for ch in row}
fig, PANELS, BOTTOM = build(_over, geom=_geom)
K.align_left_ink(fig, PANELS, COLS)
K.place_letters(fig, PANELS, rows=ROWS)

runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM

assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
print(f"[{STEM}] axes {PLOT_H:.0f} mm; panels end at {BOTTOM:.1f} mm; "
      f"caption {n_lines} lines -> {CAP_BOTTOM:.1f} mm of {PH:.0f} mm")

# ----------------------------------------------------------------------- export
png, pdf, ppt = (os.path.join(HERE, STEM + ext)
                 for ext in (".png", ".pdf", ".pptx"))
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")
K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
              collect_text_records=collect_text_records)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
print("non-Arial text:", bad[:5], "| files:",
      [os.path.basename(p) for p in (png, pdf, ppt)])
pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
    os.path.join(HERE, "figS14_longscatter_A4_caption_values.csv"),
    index=False)
plt.close(fig)
