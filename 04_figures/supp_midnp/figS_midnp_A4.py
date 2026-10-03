"""Supplementary Fig. S15 | the Fig. 4 analysis re-run on MID-specific NP
connectivity (the summed six MID edges) instead of the 12-edge NP factor.

Five panels on one A4 page, all recomputed from the Fig. 4 tables read in
place (../fig.4/fig4_data/):

  a  baseline versus AMPA versus GABA-A, within subject (n = 288)
  b  the three clinical groups in each of the three conditions -- does the
     group difference survive the perturbation?
  c  baseline against the AMPA-perturbed level, with the identity line
  d  the same for GABA-A
  e  baseline level of the two response groups DEFINED on MID (both up / any
     down), which is the non-circular half of that split

The conventions are Fig. 4's: one-way ANOVA across the three groups with
Benjamini-Hochberg q over the three pairwise contrasts (b), paired t with
Wilcoxon and Cohen's dz (a), and, for baseline dependence, the slope of the
perturbed level on the baseline level against the identity slope of 1 plus the
variance ratio (c, d) -- never the baseline-versus-change correlation, which is
circular because the change contains the baseline with a negative sign.

    python figS_midnp_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_midnp")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce
from fig_export import collect_text_records
from supp_kit import boxes, fill, pt_edge
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT

D = os.path.join(FIGDIR, "fig.4", "fig4_data")
DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_midnp_A4" if WITH_CAP else "figS_midnp_A4_nocaption"
SUPP_NO = "S15"
apply_np_style()
K.apply_page_style()

# ------------------------------------------------------------------- the data
T = pd.read_csv(os.path.join(D, "fig4_paired_np_mid_n288.csv"))
PAT = pd.read_csv(os.path.join(D, "fig4_mid_pattern_subject_n288.csv"))
T = T.merge(PAT[["ID", "pattern_mid", "pattern_np"]], on="ID", validate="1:1")
assert len(T) == 288 and set(T.pattern_mid) == {"both up", "any down"}

COND = [("mid_baseline", "Baseline", C("baseline")),
        ("mid_ampa", "After AMPA", C("ampa")),
        ("mid_gaba", "After GABA-A", C("gaba"))]
GRP = ["HC", "High-symptom", "Patient"]
GCOL = {"HC": C("hc"), "High-symptom": C("high_symptom"),
        "Patient": C("patient")}
PATS = ["both up", "any down"]
PCOL = {"both up": C("increased"), "any down": C("decreased")}
S = {}                                  # every caption number, dumped to CSV

# ---- a  within-subject effect of each perturbation -------------------------
S["paired"] = []
for k, lab, _ in COND[1:]:
    d = T[k].values - T.mid_baseline.values
    t, p = stats.ttest_rel(T[k].values, T.mid_baseline.values)
    S["paired"].append(dict(
        condition=lab, n=len(d), mean=float(d.mean()), sd=float(d.std(ddof=1)),
        pct_up=100 * float((d > 0).mean()), n_up=int((d > 0).sum()),
        t=float(t), df=len(d) - 1, p=float(p),
        wilcoxon_p=float(stats.wilcoxon(T[k].values,
                                        T.mid_baseline.values).pvalue),
        dz=float(d.mean() / d.std(ddof=1))))

# ---- b  the three clinical groups in each condition ------------------------
S["group"] = []
for k, lab, _ in COND:
    v = [T.loc[T.Group == g, k].values for g in GRP]
    F, p = stats.f_oneway(*v)
    pairs = [("HC", "High-symptom"), ("HC", "Patient"),
             ("High-symptom", "Patient")]
    pw = [float(stats.ttest_ind(T.loc[T.Group == a, k],
                                T.loc[T.Group == b, k],
                                equal_var=True).pvalue) for a, b in pairs]
    q = list(multipletests(pw, method="fdr_bh")[1])
    S["group"].append(dict(
        condition=lab, F=float(F), df=(len(GRP) - 1, len(T) - len(GRP)),
        p_anova=float(p),
        mean={g: float(x.mean()) for g, x in zip(GRP, v)},
        sd={g: float(x.std(ddof=1)) for g, x in zip(GRP, v)},
        n={g: int(len(x)) for g, x in zip(GRP, v)},
        pairs=[f"{a} vs {b}" for a, b in pairs],
        p_pair=pw, q_pair=[float(x) for x in q]))

# ---- c, d  Oldham's test: the mean of the two measurements vs their change
S["oldham"] = []
for k, lab, _ in COND[1:]:
    pre, post = T.mid_baseline.values, T[k].values
    m, d = (pre + post) / 2, post - pre
    r = stats.pearsonr(m, d)
    f = sm.OLS(post, sm.add_constant(pre)).fit()
    lo, hi = f.conf_int()[1]
    t1 = float((f.params[1] - 1) / f.bse[1])
    S["oldham"].append(dict(
        condition=lab, n=len(T), r=float(r.statistic), df=len(T) - 2,
        p=float(r.pvalue),
        var_ratio=float(post.var(ddof=1) / pre.var(ddof=1)),
        sd_baseline=float(pre.std(ddof=1)), sd_post=float(post.std(ddof=1)),
        slope_post_on_pre=float(f.params[1]), slope_ci=(float(lo), float(hi)),
        t_slope_vs_1=t1,
        p_slope_vs_1=float(2 * stats.t.sf(abs(t1), f.df_resid)),
        r_naive_circular=float(stats.pearsonr(pre, d).statistic)))

# ---- e  the MID-defined response groups at baseline ------------------------
bu = T.loc[T.pattern_mid == "both up", "mid_baseline"].values
ad = T.loc[T.pattern_mid == "any down", "mid_baseline"].values
n1, n2 = len(bu), len(ad)
sp = np.sqrt(((n1 - 1) * bu.var(ddof=1) + (n2 - 1) * ad.var(ddof=1))
             / (n1 + n2 - 2))
w = stats.ttest_ind(bu, ad, equal_var=False)
CT = pd.crosstab(T.Group, T.pattern_mid).loc[GRP, PATS]
chi = stats.chi2_contingency(CT.values)
S["pattern"] = dict(
    n={"both up": n1, "any down": n2},
    mean={"both up": float(bu.mean()), "any down": float(ad.mean())},
    sd={"both up": float(bu.std(ddof=1)), "any down": float(ad.std(ddof=1))},
    t=float(w.statistic), df=float(w.df), p=float(w.pvalue),
    g=float((bu.mean() - ad.mean()) / sp),
    mwu_p=float(stats.mannwhitneyu(bu, ad).pvalue),
    counts={g: (int(CT.loc[g, "both up"]), int(CT.loc[g].sum())) for g in GRP},
    pct={g: 100 * float(CT.loc[g, "both up"] / CT.loc[g].sum()) for g in GRP},
    chi2=float(chi.statistic), chi2_df=int(chi.dof), chi2_p=float(chi.pvalue),
    agree_with_np=float((T.pattern_mid == T.pattern_np).mean()))

# --------------------------------------------------------------- the grammar
CAT_PT = LABEL_PT                   # category names are read as axis labels;
                                    # a and b rotate them 45 deg because nine
                                    # of them share row 1
S_PT, S_SC = 3.2, 5.0               # 288 points per box / per scatter
YLAB = "MID summed FC"


def mark(p):
    return ("***" if p < .001 else "**" if p < .01 else "*" if p < .05
            else "n.s.")


def bracket(ax, i, j, y, dy, p):
    ax.plot([i, i, j, j], [y, y + dy, y + dy, y], color="black", lw=LW,
            clip_on=False, zorder=5)
    ax.text((i + j) / 2, y + dy * 1.15, mark(p), ha="center", va="bottom",
            fontsize=ANNOT_PT, clip_on=False, zorder=5)


def p_a(ax):
    vals = [T[k].values for k, _, _ in COND]
    bp = boxes(ax, [0, 1, 2], vals, [c for _, _, c in COND], width=.55,
               jitter=.16, seed=1, s=S_PT)
    for j, (_, _, col) in enumerate(COND):
        bp["boxes"][j].set_facecolor(fill(col))
    lo = min(v.min() for v in vals); hi = max(v.max() for v in vals)
    rng = hi - lo
    for j, r in enumerate(S["paired"]):
        bracket(ax, 0, j + 1, hi + (.04 + .15 * j) * rng, .03 * rng, r["p"])
    ax.set_ylim(lo - .05 * rng, hi + .36 * rng)
    ax.set_xticks(range(3))
    ax.set_xticklabels(["Baseline", "+AMPA", "+GABA-A"], fontsize=CAT_PT,
                       rotation=45, ha="right")
    ax.set_xlim(-.62, 2.62)
    ax.set_ylabel(YLAB)


def p_b(axs):
    lo = min(T[k].min() for k, _, _ in COND)
    hi = max(T[k].max() for k, _, _ in COND)
    rng = hi - lo
    for ax, (k, lab, _), r in zip(axs, COND, S["group"]):
        vals = [T.loc[T.Group == g, k].values for g in GRP]
        boxes(ax, [0, 1, 2], vals, [GCOL[g] for g in GRP], width=.55,
              jitter=.16, seed=2, s=S_PT)
        for lev, ((i, j), q) in enumerate(zip(((0, 1), (1, 2), (0, 2)),
                                              [r["q_pair"][0], r["q_pair"][2],
                                               r["q_pair"][1]])):
            bracket(ax, i, j, hi + (.05 + .16 * lev) * rng, .03 * rng, q)
        ax.set_xticks(range(3))
        ax.set_xticklabels(GRP, fontsize=CAT_PT, rotation=45, ha="right")
        ax.set_xlim(-.62, 2.62)
        ax.set_ylim(lo - .05 * rng, hi + .58 * rng)    # room for 3 brackets;
        ax.text(.02, .99, lab, transform=ax.transAxes, ha="left", va="top",
                fontsize=ANNOT_PT)                     # one scale for the 3
    axs[0].set_ylabel(YLAB)
    for ax in axs[1:]:
        ax.set_yticklabels([])


def _oldham(ax, k, lab, col, r):
    """Oldham's test: the change against the mean of the two measurements.
    Its sign is set by the variance ratio -- it asks whether the spread
    contracted or expanded, which is the non-circular question here."""
    pre, post = T.mid_baseline.values, T[k].values
    x, y = (pre + post) / 2, post - pre
    ax.axhline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.scatter(x, y, s=S_SC, facecolor=col, edgecolor=pt_edge(col),
               linewidth=LW * .4, alpha=.85, zorder=3)
    xs = np.linspace(x.min(), x.max(), 100)
    pr = (sm.OLS(y, sm.add_constant(x)).fit()
          .get_prediction(sm.add_constant(xs)).summary_frame(alpha=.05))
    ax.fill_between(xs, pr.mean_ci_lower, pr.mean_ci_upper, color=fill(col),
                    alpha=.6, lw=0, zorder=2)
    ax.plot(xs, pr["mean"], color=col, lw=LW * 1.8, zorder=4)
    lo, hi = float(y.min()), float(y.max())
    ax.set_ylim(lo - .06 * (hi - lo), hi + .26 * (hi - lo))
    ax.set_xlabel("Mean of baseline and\nperturbed " + YLAB)
    ax.set_ylabel("Change in " + YLAB)
    ax.text(.02, .99, f"{lab}\n$r$ = {r['r']:.2f}".replace("-", "\u2212"),
            transform=ax.transAxes, ha="left", va="top", fontsize=ANNOT_PT,
            linespacing=1.25)


def p_c(ax):
    _oldham(ax, "mid_ampa", "AMPA", C("ampa"), S["oldham"][0])


def p_d(ax):
    _oldham(ax, "mid_gaba", "GABA-A", C("gaba"), S["oldham"][1])


def p_e(ax):
    vals = [T.loc[T.pattern_mid == p, "mid_baseline"].values for p in PATS]
    boxes(ax, [0, 1], vals, [PCOL[p] for p in PATS], width=.55, jitter=.16,
          seed=3, s=S_PT)
    lo = min(v.min() for v in vals); hi = max(v.max() for v in vals)
    rng = hi - lo
    bracket(ax, 0, 1, hi + .05 * rng, .035 * rng, S["pattern"]["p"])
    ax.set_ylim(lo - .05 * rng, hi + .26 * rng)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(PATS, fontsize=CAT_PT)
    ax.set_xlim(-.62, 1.62)
    ax.set_ylabel("Baseline " + YLAB)


# --------------------------------------------------------------- page geometry
GUT = K.LETTER_W + K.LETTER_PADX    # gutter that holds the panel letter
GAP, MB, LETTER_BAND = K.GAP, K.MB, K.LETTER_BAND
GAPX = 8.5                          # visible gap between columns
SUB_GAP = 1.5                       # between b's three sub-axes
LAB_L = 17.0                        # provisional y label + y ticks
LAB_A = 8.5                         # a is tight, so its rotated label
                                    # sits ~2 mm from its tick numbers
H1, H2 = 52.0, 38.0                 # row 1 is taller: b carries three
                                    # brackets per condition
XB1, XB2 = 20.0, 13.0               # rotated 10 pt names in row 1 / two-
                                    # line x labels of the scatters
COL_A = 50.0                        # slot of a; b takes the rest of row 1
LAB_B = 13.0                        # b's y ticks are short, so its label
                                    # block is narrower than the default
W = PW - ML - MR
FN3 = [p_c, p_d, p_e]


def row2_geom(fig, panels):
    """Three equal axes in row 2 whose VISIBLE gaps are GAPX."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    by = {q["ch"]: q for q in panels}
    L, R = [], []
    for ch in "cde":
        ax = by[ch]["axes"][0]
        bb, pos = ax.get_tightbbox(rend), ax.get_position()
        L.append(max(pos.x0 * PW - mm(bb.x0), 0.0))
        R.append(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0))
    w = (W - 2 * GAPX - sum(L) - sum(R) - 3 * GUT) / 3
    geom, x = {}, ML
    for j, ch in enumerate("cde"):
        geom[ch] = (x, x + GUT + L[j], w)
        x += GUT + L[j] + w + R[j] + GAPX
    return geom


def build(shift=None, geom=None):
    shift = shift or {}
    f, out = plt.figure(figsize=panel(PW, PH)), []
    # row 1 -- a, then b's three sub-axes
    top = MT + LETTER_BAND
    ax_a = K.axes_mm(f, ML + GUT + LAB_A, top + shift.get("a", 0.0),
                     COL_A - GUT - LAB_A, H1)
    p_a(ax_a)
    out.append(dict(ch="a", x=ML, axes=[ax_a],
                    txt=K.letter(f, ML, top - 1.2, "a")))
    xb = ML + COL_A + GAPX
    wb = (W - COL_A - GAPX - GUT - LAB_B - 2 * SUB_GAP) / 3
    axs = [K.axes_mm(f, xb + GUT + LAB_B + i * (wb + SUB_GAP),
                     top + shift.get("b", 0.0), wb, H1) for i in range(3)]
    p_b(axs)
    out.append(dict(ch="b", x=xb, axes=axs,
                    txt=K.letter(f, xb, top - 1.2, "b")))
    # row 2 -- c, d, e
    top2 = (top + max(shift.get(c, 0.0) for c in "ab") + H1 + XB1 + GAP
            + LETTER_BAND)
    for j, (ch, fn) in enumerate(zip("cde", FN3)):
        slot, ax_x, ax_w = (geom[ch] if geom else
                            (ML + j * (W / 3), ML + j * (W / 3) + LAB_L,
                             W / 3 - LAB_L - GAPX))
        ax = K.axes_mm(f, ax_x, top2 + shift.get(ch, 0.0), ax_w, H2)
        fn(ax)
        out.append(dict(ch=ch, x=slot, axes=[ax],
                        txt=K.letter(f, slot, top2 - 1.2, ch)))
    enforce(f)
    return f, out, top2 + max(shift.get(c, 0.0) for c in "cde") + H2 + XB2


# ------------------------------------------------------------------- caption
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Robustness of the "
             f"baseline-dependent, bidirectional response when the network "
             f"phenotype is restricted to MID-specific NP connectivity.")


def pf(p):
    return (f"P = {p:.3g}" if p >= 1e-3 else
            f"P = {p:.2g}" if p >= 1e-4 else f"P = {p:.1e}")


def caption_runs():
    pa, pg = S["paired"]
    gb, ga, gg = S["group"]
    da, dg = S["oldham"]
    pt = S["pattern"]

    def gline(d):
        return (f"F({d['df'][0]}, {d['df'][1]}) = {d['F']:.2f}, "
                f"{pf(d['p_anova'])}")

    def oline(d):
        return (f"r = {d['r']:+.3f} (n = {d['n']}, df = {d['df']}, "
                f"{pf(d['p'])}); variance ratio {d['var_ratio']:.3f} "
                f"(s.d. {d['sd_baseline']:.3f} to {d['sd_post']:.3f}), and "
                f"the slope of the perturbed level on the baseline level is "
                f"{d['slope_post_on_pre']:.3f} (95% CI "
                f"{d['slope_ci'][0]:.3f} to {d['slope_ci'][1]:.3f}, below the "
                f"identity slope of 1: t = {d['t_slope_vs_1']:.2f}, "
                f"{pf(d['p_slope_vs_1'])})")
    cap = [
        ("", f"The virtual AMPA and GABA-A perturbations were re-analysed in "
             f"the population-scale simulations with the network phenotype "
             f"restricted to the NP-related MID-specific connectivity, i.e. "
             f"the summed six MID edges, in place of the 12-edge NP factor of "
             f"Fig. 4. Unit of observation is one digital twin; n = "
             f"{len(T)} (HC {gb['n']['HC']}, high-symptom "
             f"{gb['n']['High-symptom']}, patients {gb['n']['Patient']}). The "
             f"GABA-A perturbation is applied on top of AMPA, as everywhere "
             f"else in this work. Box plots show the median, 25th-75th "
             f"percentiles and 1.5 x IQR whiskers with every twin "
             f"overplotted; *P < 0.05, **P < 0.01, ***P < 0.001; n.s., not "
             f"significant. All tests two-sided. "),
        ("a", f", within-subject effect of each perturbation on the same "
              f"measure. AMPA raises it by {pa['mean']:+.3f} +/- "
              f"{pa['sd']:.3f} ({pa['n_up']}/{pa['n']} twins, "
              f"{pa['pct_up']:.1f}%, increase; paired t({pa['df']}) = "
              f"{pa['t']:.2f}, {pf(pa['p'])}, Wilcoxon "
              f"{pf(pa['wilcoxon_p'])}, Cohen's dz = {pa['dz']:.3f}) and "
              f"GABA-A by {pg['mean']:+.3f} +/- {pg['sd']:.3f} "
              f"({pg['n_up']}/{pg['n']}, {pg['pct_up']:.1f}%; "
              f"t({pg['df']}) = {pg['t']:.2f}, {pf(pg['p'])}, Wilcoxon "
              f"{pf(pg['wilcoxon_p'])}, dz = {pg['dz']:.3f}). The "
              f"bidirectional response of Fig. 4 is therefore reproduced on "
              f"the MID-specific measure. "),
        ("b", f", the three clinical groups in each condition (one-way ANOVA; "
              f"the symbol is that F test, pairwise contrasts "
              f"Benjamini-Hochberg-corrected over the three within a "
              f"condition). At baseline the groups differ, {gline(gb)} "
              f"(means HC {gb['mean']['HC']:+.3f}, high-symptom "
              f"{gb['mean']['High-symptom']:+.3f}, patients "
              f"{gb['mean']['Patient']:+.3f}; q = "
              f"{gb['q_pair'][0]:.3g} / {gb['q_pair'][1]:.3g} / "
              f"{gb['q_pair'][2]:.3g} for HC vs high-symptom / HC vs "
              f"patients / high-symptom vs patients). After AMPA the "
              f"difference is much reduced but not abolished, {gline(ga)} "
              f"(q = {ga['q_pair'][0]:.3g} / {ga['q_pair'][1]:.3g} / "
              f"{ga['q_pair'][2]:.3g}; only high-symptom versus patients "
              f"survives correction), and after GABA-A it is absent, "
              f"{gline(gg)} (q = {gg['q_pair'][0]:.3g} / "
              f"{gg['q_pair'][1]:.3g} / {gg['q_pair'][2]:.3g}). On the "
              f"12-edge NP factor the contrast was already absent after AMPA "
              f"(Fig. 4c), so on MID-specific connectivity the convergence "
              f"is partial under AMPA and complete under GABA-A. The three "
              f"sub-panels share one y scale. "),
        ("c", f", Oldham's test for the AMPA perturbation: the change "
              f"against the mean of the baseline and perturbed level, which "
              f"is the non-circular way to ask whether the response depends "
              f"on where a twin starts. {oline(da)}. The negative "
              f"correlation and the variance ratio below 1 are the same "
              f"fact: the spread contracts, so twins low at baseline gain "
              f"more and the group converges towards a common level. "),
        ("d", f", the same for GABA-A: {oline(dg)} -- here the correlation "
              f"is positive and the variance ratio above 1, i.e. the spread "
              f"expands, so the perturbation moves twins apart rather than "
              f"together. Oldham's test is used instead of the "
              f"baseline-versus-change correlation because the change "
              f"contains the baseline with a negative sign; that circular "
              f"quantity is r = {da['r_naive_circular']:.3f} for AMPA and "
              f"{dg['r_naive_circular']:.3f} for GABA-A and is reported only "
              f"so that it is not mistaken for the test. "),
        ("e", f", the baseline level of the two response groups defined on "
              f"the MID measure itself (both up, n = {pt['n']['both up']}; "
              f"any down, n = {pt['n']['any down']}; "
              f"{100 * pt['agree_with_np']:.1f}% of twins fall in the same "
              f"group as under the NP-factor rule). Twins that respond in "
              f"both conditions start lower: {pt['mean']['both up']:+.3f} "
              f"+/- {pt['sd']['both up']:.3f} versus "
              f"{pt['mean']['any down']:+.3f} +/- "
              f"{pt['sd']['any down']:.3f} (Welch t = {pt['t']:.2f}, "
              f"df = {pt['df']:.1f}, {pf(pt['p'])}, Hedges' g = "
              f"{pt['g']:.2f}, Mann-Whitney {pf(pt['mwu_p'])}). The grouping "
              f"is defined by the sign of the change, so the change itself "
              f"is not tested between these groups -- the baseline is, and "
              f"it is the quantity the split was not built on. The share of "
              f"both-up twins also differs across the clinical groups (HC "
              f"{pt['counts']['HC'][0]}/{pt['counts']['HC'][1]} = "
              f"{pt['pct']['HC']:.1f}%, high-symptom "
              f"{pt['counts']['High-symptom'][0]}/"
              f"{pt['counts']['High-symptom'][1]} = "
              f"{pt['pct']['High-symptom']:.1f}%, patients "
              f"{pt['counts']['Patient'][0]}/{pt['counts']['Patient'][1]} = "
              f"{pt['pct']['Patient']:.1f}%; chi2({pt['chi2_df']}) = "
              f"{pt['chi2']:.2f}, {pf(pt['chi2_p'])}). "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs


# pass 1 -- row-2 geometry, overhangs and the caption height
_f0, _p0, _ = build()
_geom = row2_geom(_f0, _p0)
plt.close(_f0)
for _ in range(3):                          # the tick labels shift a little
    _f0, _p0, _ = build(geom=_geom)         # when the axes width changes
    _geom = row2_geom(_f0, _p0)
    _o1 = K.overhangs(_f0, _p0)
    _runs0 = caption_runs()
    _l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
                   _f0.canvas.get_renderer())[0] if WITH_CAP else [])
    plt.close(_f0)

_over = {ch: max(_o1[c] for c in row) for row in ("ab", "cde") for ch in row}
fig, PANELS, BOTTOM = build(_over, geom=_geom)
K.align_left_ink(fig, PANELS, [["a", "c"]])
K.place_letters(fig, PANELS, rows=[["a", "b"], ["c", "d", "e"]])

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
    os.path.join(HERE, "figS_midnp_A4_caption_values.csv"), index=False)
plt.close(fig)
