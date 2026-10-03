"""Supplementary longitudinal-prediction figure, assembled as ONE A4 page.

Everything the longitudinal analysis (IMAGEN FU3, n = 85) rests on, except the
two panels that are already in the main figure (Fig. 5h, the AMPA restoration
index against later symptom change, and Fig. 5i, the permuted R2 of the full
model).  Rebuilt from the tables of long_supp.py under the frozen rules of
figA4_kit:

  a  Pearson correlations among the baseline measures, the two restoration
     indices and later symptom change
  b  standardised coefficients of the full model
  c  out-of-sample accuracy, 10-fold cross-validation
  d  incremental R2 of each index against its own permutation null

The behavioural measure is the baseline internalising total, i.e. the sum of
items 3-6 of the battery (emp_baseline_beha_sum = sum(beha(:,3:6))), and the
outcome is the same sum at FU3 residualised on baseline; the item-level
correlations of long_correlations_n85.csv are not drawn.  The four items enter
the model separately (b), which is why they appear there and nowhere else.

Panels carry symbols only; every exact statistic lives in the caption, computed
here at render time and dumped to figS_long_A4_caption_values.csv.

    python figS_long_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
STEM = "figS_long_A4" if WITH_CAP else "figS_long_A4_nocaption"
SUPP_NO = "S13"                     # next free number in FIGURE_LEGENDS.md
apply_np_style()
K.apply_page_style()

# ------------------------------------------------------------------- the data
CR = pd.read_csv(os.path.join(D, "long_correlations_n85.csv"))
CO = pd.read_csv(os.path.join(D, "long_full_model_coefficients_n85.csv"))
INC = pd.read_csv(os.path.join(D, "long_nested_increments_n85.csv"))
CV = pd.read_csv(os.path.join(D, "long_cv_out_of_sample_n85.csv"))
CVR = pd.read_csv(os.path.join(D, "long_cv_repeats_n85.csv"))
NUL = np.load(os.path.join(D, "long_permutation_nulls.npz"))
assert set(CR.n) == {85} and len(CO) == 5 and len(INC) == 4

C_EMP, C_AMPA, C_GABA, C_REF = C("np12"), C("ampa"), C("gaba"), C("reference")
NP_X = "Baseline empirical NP (sum)"
TOT = "Baseline symptom sum (4 model scores)"
FU3 = "FU3 symptom change"
YS = [TOT, NP_X, FU3]               # bottom to top in the panel
YLAB = {TOT: "Baseline internalising\ntotal", NP_X: "Baseline measured NP",
        FU3: "Symptom change\nat FU3"}
SERIES = [("Baseline empirical NP (sum)", "Baseline measured NP", C_EMP, .24),
          ("AMPA index", "AMPA index", C_AMPA, 0.0),
          ("GABA-A index", "GABA-A index", C_GABA, -.24)]
S = {}                              # every caption number, dumped to CSV


def rec(x, y):
    """The row of the correlation table, or None for a pair it does not hold
    (a measure against itself)."""
    r = CR[(CR.x == x) & (CR.y == y)]
    return None if not len(r) else r.iloc[0]


# --------------------------------------------------------------- the grammar
CAT_PT = LABEL_PT                   # category names are read as axis labels
MK_S = 16.0                         # forest marker


def mark(p):
    return ("***" if p < .001 else "**" if p < .01 else "*" if p < .05
            else "n.s.")


def p_a(ax):
    """One forest: every pairwise correlation the analysis rests on."""
    ax.axvline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    out = []
    for xname, slab, col, off in SERIES:
        for k, y in enumerate(YS):
            r = rec(xname, y)
            if r is None:
                continue
            ax.plot([r.ci95_lo, r.ci95_hi], [k + off] * 2, color=col, lw=LW,
                    zorder=2)
            ax.scatter(r.pearson_r, k + off, s=MK_S, linewidth=LW, zorder=3,
                       facecolor=col if r.p_pearson < .05 else "white",
                       edgecolor=col)
            out.append(dict(x=slab, y=YLAB[y].replace("\n", " "),
                            r=float(r.pearson_r), lo=float(r.ci95_lo),
                            hi=float(r.ci95_hi), p=float(r.p_pearson),
                            q=float(r.q_bh_within_x)))
    ax.set_yticks(range(len(YS)))
    ax.set_yticklabels([YLAB[y] for y in YS], fontsize=TICK_PT)
    ax.set_ylim(-.62, len(YS) - .38)
    ax.set_xlim(-.62, .70)
    ax.set_xlabel("Pearson $r$ (95% CI)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    h = [Line2D([], [], marker="o", linestyle="none", markersize=3.2,
                markerfacecolor=c, markeredgecolor=c, markeredgewidth=LW)
         for _, _, c, _ in SERIES]
    ax.legend(h, [s for _, s, _, _ in SERIES], loc="upper left",
              fontsize=ANNOT_PT, frameon=False, handletextpad=.4,
              borderaxespad=.2)   # the lower right holds the two negative rows
    S["a"] = out


COLAB = {"AMPA restoration index": "AMPA restoration\nindex"}


def p_b(ax):
    """Standardised coefficients of the full model."""
    co = CO.iloc[::-1].reset_index(drop=True)
    it = {p: f"Internalising item {i + 1}" for i, p in
          enumerate(sorted(p for p in CO.predictor if "AMPA" not in p))}
    ax.axvline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    for k, r in co.iterrows():
        col = C_AMPA if "AMPA" in r.predictor else C_REF
        ax.plot([r.ci95_std_lo, r.ci95_std_hi], [k] * 2, color=col, lw=LW,
                zorder=2)
        ax.scatter(r.beta_std, k, s=MK_S, linewidth=LW, zorder=3,
                   facecolor=col if r.p < .05 else "white", edgecolor=col)
    ax.set_yticks(range(len(co)))
    ax.set_yticklabels([COLAB.get(p, it.get(p, p)) for p in co.predictor],
                       fontsize=TICK_PT)
    ax.set_ylim(-.7, len(co) - .3)
    ax.set_xlim(-.66, .66)
    ax.set_xlabel("Standardised $\\beta$ (95% CI)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    S["b"] = [dict(predictor=it.get(r.predictor, r.predictor),
                   source_name=r.predictor, beta_std=float(r.beta_std),
                   lo=float(r.ci95_std_lo), hi=float(r.ci95_std_hi),
                   t=float(r.t), df=int(r.df_resid), p=float(r.p))
              for _, r in CO.iterrows()]


CVLAB = {"baseline behaviour (4)": "Four items",
         "+ AMPA index": "+ AMPA index",
         "+ GABA-A index": "+ GABA-A index",
         "baseline empirical NP": "Measured NP",
         "baseline NP + AMPA": "Measured NP\n+ AMPA"}


def p_c(ax):
    """Out-of-sample R2, mean over repeats with the repeats overplotted."""
    mods = list(CVR.columns)
    cols = [C_REF, C_AMPA, C_GABA, C_EMP, C_AMPA]
    rng = np.random.default_rng(1)
    for k, m in enumerate(mods):
        v = CVR[m].values
        ax.bar(k, v.mean(), width=.62, facecolor=fill(cols[k]),
               edgecolor=cols[k], linewidth=LW, zorder=2)
        ax.scatter(k + rng.uniform(-.13, .13, len(v)), v, s=4,
                   facecolor=cols[k], edgecolor="none", alpha=.8, zorder=3)
    ax.set_xticks(range(len(mods)))
    ax.set_xticklabels([CVLAB[m] for m in mods], fontsize=TICK_PT,
                       rotation=45, ha="right")   # five model names do not fit
    ax.set_xlim(-.6, len(mods) - .4)              # horizontally in half a row
    ax.set_ylim(0, float(CVR.values.max()) * 1.12)
    ax.set_ylabel("Out-of-sample $R^2$")
    S["c"] = CV.round(4).to_dict("records")


YCAP = 0.10                         # axis cap of d, see the caption
INCK = [("AMPA", "4 baseline behaviour scores"),
        ("GABA-A", "4 baseline behaviour scores"),
        ("AMPA", "baseline empirical NP"),
        ("GABA-A", "baseline empirical NP")]


def p_d(ax):
    """Observed increment against its own permutation null."""
    hi = 0.0
    for k, (inm, cnm) in enumerate(INCK):
        null = NUL[f"{inm}|{cnm}"]
        col = C_AMPA if inm == "AMPA" else C_GABA
        vp = ax.violinplot([null], positions=[k], widths=.72,
                           showextrema=False)
        for b in vp["bodies"]:
            b.set_facecolor("0.85"); b.set_edgecolor("0.6")
            b.set_linewidth(LW); b.set_alpha(.9)
        ax.hlines(float(np.percentile(null, 95)), k - .36, k + .36,
                  color="0.45", lw=LW, ls=(0, (2.2, 1.6)), zorder=3)
        r = INC[(INC["index"] == inm) & (INC.covariates == cnm)].iloc[0]
        ax.scatter([k], [r.delta_R2], s=22, facecolor=col,
                   edgecolor=pt_edge(col), linewidth=LW * .6, zorder=4)
        ax.text(k, r.delta_R2 + .004, mark(float(r.p_perm_deltaR2)),
                ha="center", va="bottom", fontsize=ANNOT_PT, color="black")
        hi = max(hi, float(r.delta_R2))
    ax.set_xticks(range(len(INCK)))
    ax.set_xticklabels([f"{i}\nover\n{'four' if c.startswith('4') else 'measured'}"
                        f"\n{'items' if c.startswith('4') else 'NP'}"
                        for i, c in INCK], fontsize=TICK_PT)   # one word per
                                                   # line: the pitch is 17 mm
    ax.set_xlim(-.6, len(INCK) - .4)
    ax.set_ylim(0, YCAP)           # the nulls' thin upper tails run to 0.167
    ax.set_ylabel("Incremental $R^2$")   # (given in the caption); cutting the
    h = [Line2D([], [], color="0.45", lw=LW, ls=(0, (2.2, 1.6))),   # axis here
         Line2D([], [], marker="o", linestyle="none", markersize=3.2,
                markerfacecolor=C_AMPA, markeredgecolor=pt_edge(C_AMPA),
                markeredgewidth=LW)]                # keeps the observed values
    ax.legend(h, ["95th centile of the null", "Observed"],   # readable
              loc="upper right", fontsize=ANNOT_PT, handletextpad=.5,
              borderaxespad=.2, frameon=True, framealpha=1.0,
              facecolor="white", edgecolor="none")
    S["d"] = INC.round(4).to_dict("records")


# --------------------------------------------------------------- page geometry
GUT = K.LETTER_W + K.LETTER_PADX    # gutter that holds the panel letter
GAP, MB, LETTER_BAND = K.GAP, K.MB, K.LETTER_BAND
GAPX = 8.5                          # visible gap inside a row
LAB = dict(a=34.0, b=30.0, c=16.0, d=16.0)     # y label + y ticks
H1, H2 = 40.0, 40.0                 # axes height per row
XB1, XB2 = 8.5, 17.0                # x label block per row
W = PW - ML - MR
RATIO = dict(ab=0.52, cd=0.46)      # a's and c's labels are the wider ones
ROWS = [(["a", "b"], "ab", H1, XB1), (["c", "d"], "cd", H2, XB2)]
FN = dict(a=p_a, b=p_b, c=p_c, d=p_d)


def two_col(fig, panels, pair, ratio):
    """Solve one row of two panels: the visible gap between their ink is GAPX
    and the two axes split the rest by `ratio`."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    by = {q["ch"]: q for q in panels}
    L, R = [], []
    for ch in pair:
        ax = by[ch]["axes"][0]
        bb, pos = ax.get_tightbbox(rend), ax.get_position()
        L.append(max(pos.x0 * PW - mm(bb.x0), 0.0))
        R.append(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0))
    free = W - GAPX - sum(L) - sum(R) - 2 * GUT
    return (GUT + L[0], free * ratio, GUT + L[1], free * (1 - ratio), R[0])


def build(shift=None, geom=None):
    shift = shift or {}
    out, f, top = [], plt.figure(figsize=panel(PW, PH)), MT + LETTER_BAND
    for chs, key, h, xb in ROWS:
        l0, w0, l1, w1, r0 = (geom[key] if geom else
                              (GUT + LAB[chs[0]],
                               W * RATIO[key] - GUT - LAB[chs[0]],
                               GUT + LAB[chs[1]],
                               W * (1 - RATIO[key]) - GAPX - GUT
                               - LAB[chs[1]], 0.0))
        x0, x1 = ML, ML + l0 + w0 + r0 + GAPX
        for ch, x, l, w in ((chs[0], x0, l0, w0), (chs[1], x1, l1, w1)):
            ax = K.axes_mm(f, x + l, top + shift.get(ch, 0.0), w, h)
            FN[ch](ax)
            out.append(dict(ch=ch, x=x, axes=[ax],
                            txt=K.letter(f, x, top - 1.2, ch)))
        top += max(shift.get(c, 0.0) for c in chs) + h + xb + GAP + LETTER_BAND
    enforce(f)
    return f, out, top - GAP - LETTER_BAND


# ------------------------------------------------------------------- caption
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | The longitudinal prediction in "
             f"full: what the restoration index adds over baseline behaviour "
             f"and baseline connectivity.")


def pf(p):
    return (f"P = {p:.3g}" if p >= 1e-3 else
            f"P = {p:.2g}" if p >= 1e-4 else f"P = {p:.1e}")


def caption_runs():
    A = {(r["x"], r["y"]): r for r in S["a"]}
    co = {r["predictor"]: r for r in S["b"]}
    cv = {r["model"]: r for r in S["c"]}
    inc = {(r["index"], r["covariates"]): r for r in S["d"]}
    amp = co["AMPA restoration index"]
    # the full model's own F test, from its R2 and the residual df of the
    # nested table -- never typed in, so a re-render cannot go stale
    k_full, r2_full = len(S["b"]), float(INC.R2_full.iloc[0])
    df2_full = int(INC.df2.iloc[0])
    F_full = (r2_full / k_full) / ((1 - r2_full) / df2_full)
    p_full = float(stats.f.sf(F_full, k_full, df2_full))
    S["full_model"] = dict(k=k_full, r2=round(r2_full, 4), df2=df2_full,
                           F=round(F_full, 3), p=float(f"{p_full:.3g}"))
    beh = [co[k] for k in co if k != "AMPA restoration index"]
    sig_beh = [r for r in beh if r["p"] < .05]
    n = int(CR.n.iloc[0])
    EMP, AM, GA = "Baseline measured NP", "AMPA index", "GABA-A index"
    TOTL, FUL = "Baseline internalising total", "Symptom change at FU3"

    def rl(x, y):
        r = A[(x, y)]
        return (f"r = {r['r']:+.2f} (95% CI {r['lo']:+.2f} to {r['hi']:+.2f}, "
                f"{pf(r['p'])})")
    cap = [
        ("", f"The follow-up sample is the n = {n} IMAGEN participants with a "
             f"digital twin at baseline (age 19) and a symptom assessment at "
             f"FU3 (age 23). The behavioural measure is the baseline "
             f"internalising total, the sum of items 3-6 of the battery, and "
             f"the outcome is that same sum at FU3 residualised on its "
             f"baseline value; item-level correlations are tabulated in "
             f"long_correlations_n85.csv and are not drawn here. The "
             f"restoration index is the similarity of a participant's "
             f"perturbed twin to the healthy pattern, computed separately for "
             f"the AMPA and the GABA-A perturbation, with the same weights "
             f"for both. Correlations are Pearson with Fisher-z 95% "
             f"confidence intervals; all tests two-sided; filled symbols mark "
             f"an uncorrected P < 0.05 in a and b. This figure holds the "
             f"analyses behind Fig. 5h and 5i without repeating them: the "
             f"index-versus-outcome scatter and the permuted R2 of the full "
             f"model are in the main figure. "),
        ("a", f", every pairwise correlation the prediction rests on. "
              f"Measured baseline connectivity already carries signal: it "
              f"tracks the baseline internalising total "
              f"({rl(EMP, TOTL)}, Benjamini-Hochberg "
              f"q = {A[(EMP, TOTL)]['q']:.3f} across the panel's targets) and "
              f"later symptom change ({rl(EMP, FUL)}, "
              f"q = {A[(EMP, FUL)]['q']:.3f}), which is the baseline any "
              f"claim for the twins has to beat. Both indices track later "
              f"change (AMPA {rl(AM, FUL)}; GABA-A {rl(GA, FUL)}) and "
              f"neither is explained by the baseline scan (AMPA "
              f"{rl(AM, EMP)}; GABA-A {rl(GA, EMP)}), so an index is not a "
              f"proxy for measured connectivity. Against the baseline "
              f"internalising total the AMPA index is flat "
              f"({rl(AM, TOTL)}) and the GABA-A index is weakly negative "
              f"({rl(GA, TOTL)}). "),
        ("b", f", the full model of FU3 symptom change on the AMPA "
              f"restoration index and the four internalising items: R2 = "
              f"{r2_full:.3f}, F({k_full}, {df2_full}) = {F_full:.2f}, "
              f"{pf(p_full)}. The index "
              f"carries an independent contribution (standardised beta = "
              f"{amp['beta_std']:+.3f}, 95% CI {amp['lo']:+.3f} to "
              f"{amp['hi']:+.3f}, t({amp['df']}) = {amp['t']:.2f}, "
              f"{pf(amp['p'])}), as does one item "
              f"({sig_beh[0]['predictor'].lower()}, beta = "
              f"{sig_beh[0]['beta_std']:+.3f}, {pf(sig_beh[0]['p'])}); the "
              f"other three do not (P "
              f"{min(r['p'] for r in beh if r['p'] >= .05):.2f}-"
              f"{max(r['p'] for r in beh):.2f}). The items enter separately "
              f"here rather than as their sum, which is why they are listed "
              f"individually; the item numbering follows the order of the "
              f"battery and the per-column domain mapping is not verified in "
              f"the source data. "),
        ("c", f", out-of-sample accuracy, 10-fold cross-validation with "
              f"pooled out-of-fold predictions and "
              f"{int(cv['+ AMPA index']['n_repeats'])} repeats (bars, mean "
              f"over repeats; points, the individual repeats). Adding the "
              f"AMPA index raises cross-validated R2 from "
              f"{cv['baseline behaviour (4)']['cv_R2_mean']:.3f} +/- "
              f"{cv['baseline behaviour (4)']['cv_R2_sd']:.3f} to "
              f"{cv['+ AMPA index']['cv_R2_mean']:.3f} +/- "
              f"{cv['+ AMPA index']['cv_R2_sd']:.3f} over the four items, and "
              f"from {cv['baseline empirical NP']['cv_R2_mean']:.3f} +/- "
              f"{cv['baseline empirical NP']['cv_R2_sd']:.3f} to "
              f"{cv['baseline NP + AMPA']['cv_R2_mean']:.3f} +/- "
              f"{cv['baseline NP + AMPA']['cv_R2_sd']:.3f} over measured "
              f"baseline connectivity; the GABA-A index adds nothing "
              f"({cv['+ GABA-A index']['cv_R2_mean']:.3f} +/- "
              f"{cv['+ GABA-A index']['cv_R2_sd']:.3f}). These are "
              f"out-of-sample values and carry no test. "),
        ("d", f", incremental R2 of each index over each covariate set, "
              f"against its own permutation null (grey violin, 5,000 "
              f"permutations of the outcome; dashed line, the null's 95th "
              f"centile). Over the four items the AMPA index adds "
              f"{inc[('AMPA', '4 baseline behaviour scores')]['delta_R2']:.3f} "
              f"(F(1, {int(inc[('AMPA', '4 baseline behaviour scores')]['df2'])}) = "
              f"{inc[('AMPA', '4 baseline behaviour scores')]['F_change']:.2f}, "
              f"{pf(inc[('AMPA', '4 baseline behaviour scores')]['p_change'])}, "
              f"permutation P = "
              f"{inc[('AMPA', '4 baseline behaviour scores')]['p_perm_deltaR2']:.3f}) "
              f"and over measured baseline connectivity "
              f"{inc[('AMPA', 'baseline empirical NP')]['delta_R2']:.3f} "
              f"(F(1, {int(inc[('AMPA', 'baseline empirical NP')]['df2'])}) = "
              f"{inc[('AMPA', 'baseline empirical NP')]['F_change']:.2f}, "
              f"{pf(inc[('AMPA', 'baseline empirical NP')]['p_change'])}, "
              f"permutation P = "
              f"{inc[('AMPA', 'baseline empirical NP')]['p_perm_deltaR2']:.3f}). "
              f"The GABA-A index adds "
              f"{inc[('GABA-A', '4 baseline behaviour scores')]['delta_R2']:.3f} "
              f"({pf(inc[('GABA-A', '4 baseline behaviour scores')]['p_change'])}, "
              f"permutation P = "
              f"{inc[('GABA-A', '4 baseline behaviour scores')]['p_perm_deltaR2']:.3f}) "
              f"and {inc[('GABA-A', 'baseline empirical NP')]['delta_R2']:.3f} "
              f"({pf(inc[('GABA-A', 'baseline empirical NP')]['p_change'])}, "
              f"permutation P = "
              f"{inc[('GABA-A', 'baseline empirical NP')]['p_perm_deltaR2']:.3f}), "
              f"i.e. it reaches the conventional threshold over the measured "
              f"scan but not over behaviour and not on the permutation test. "
              f"The y axis is cut at {YCAP:.2f} so that the observed values "
              f"stay readable; the nulls are thin above that and reach "
              f"{min(float(NUL[f'{i}|{c}'].max()) for i, c in INCK):.3f}-"
              f"{max(float(NUL[f'{i}|{c}'].max()) for i, c in INCK):.3f} at "
              f"their maxima, with 99th centiles of "
              f"{min(float(np.percentile(NUL[f'{i}|{c}'], 99)) for i, c in INCK):.3f}-"
              f"{max(float(np.percentile(NUL[f'{i}|{c}'], 99)) for i, c in INCK):.3f}. "
              f"Symbols give the permutation P; *P < 0.05, **P < 0.01, "
              f"***P < 0.001; n.s., not significant. The increments are a few "
              f"per cent of variance in a sample of {n}, and the nulls are "
              f"shown so that they can be read against what chance produces "
              f"here. "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs


# pass 1 -- row geometry, content overhang per panel, caption height
_f0, _p0, _ = build()
_geom = {k: two_col(_f0, _p0, chs, RATIO[k]) for chs, k, _, _ in ROWS}
plt.close(_f0)
for _ in range(3):                          # the tick labels shift a little
    _f0, _p0, _ = build(geom=_geom)         # when the axes width changes
    _geom = {k: two_col(_f0, _p0, chs, RATIO[k]) for chs, k, _, _ in ROWS}
    _over = K.overhangs(_f0, _p0)
    _runs0 = caption_runs()
    _l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
                   _f0.canvas.get_renderer())[0] if WITH_CAP else [])
    plt.close(_f0)

fig, PANELS, BOTTOM = build(_over, geom=_geom)
K.align_left_ink(fig, PANELS, [["a", "c"], ["b", "d"]])
K.place_letters(fig, PANELS, rows=[["a", "b"], ["c", "d"]])

runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM

assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
print(f"[{STEM}] rows {H1:.0f}/{H2:.0f} mm; panels end at {BOTTOM:.1f} mm; "
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
    os.path.join(HERE, "figS_long_A4_caption_values.csv"), index=False)
plt.close(fig)
