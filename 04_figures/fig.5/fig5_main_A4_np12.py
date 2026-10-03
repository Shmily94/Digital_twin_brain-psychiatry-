"""Figure 5, assembled as ONE Nature-Medicine main figure on A4.

Panels, in reading order, rebuilt from fig5.py's own drawing grammar and
fig5_data/:

  a  fig5b_pattern   change from placebo, both-up vs any-down (Fig. 4 rule)
  b  fig5c_pattern   placebo level of the same two groups
  c  fig5d           ketamine-induced change in NP FC, MDD vs HC
  d  fig5e           placebo NP FC, MDD vs HC
  e  fig5f           NP change vs symptom change (MDD)
  f  fig5g           similarity to the AMPA-perturbed twin vs MADRS change
  g  fig5h3          AMPA restoration index vs follow-up symptom change,
                     both residualised on baseline empirical NP
  h  fig5h           permutation null for R^2, baseline model vs + AMPA index

Frozen layout rules come from figA4_kit (6 mm letter band, 6 mm rows, letters
seated against their own panel's measured content, 8/9/10/11 pt type, legends
above the axes).  Declarative panel titles are dropped and every exact
statistic lives in the caption -- panels carry symbols only.

    python fig5_main_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "fig.5")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce
from fig_export import collect_text_records
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT

D = os.path.join(HERE, "fig5_data")
DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "fig5_main_A4_np12" if WITH_CAP else "fig5_main_A4_np12_nocaption"
apply_np_style()
K.apply_page_style()

HC27 = pd.read_csv(f"{D}/fig5_healthy_n27_with_pattern.csv")
PH36 = pd.read_csv(f"{D}/fig5_mdd_hc_n36.csv")
F22 = pd.read_csv(f"{D}/fig5f_np_symptom_resid_MDD_n22.csv")
G22 = pd.read_csv(f"{D}/fig5g_state_similarity_MDD_n22.csv")
SC = pd.read_csv(f"{D}/fig5h_paragraph_scatters_n85.csv")
SCST = pd.read_csv(f"{D}/fig5h_paragraph_scatter_stats.csv")
RNULL = pd.read_csv(f"{D}/fig5h_R2_permutation_null.csv")
MS = pd.read_csv(f"{D}/fig5h_model_stats.csv").iloc[0]
D4 = os.path.join(FIGDIR, "fig.4", "fig4_data")     # panel c is Fig. 4's companion
MID = pd.read_csv(f"{D4}/fig4_mid_pattern_subject_n288.csv")
NP12 = pd.read_csv(f"{D}/fig5h_np12_loo_n85.csv")
ACC = pd.read_csv(f"{D}/fig5i_np12_loo_accuracy.csv")

PAT = ["both up", "any down"]
PCOL = {"both up": C("increased"), "any down": C("decreased")}
GCOL = {"HC": C("hc"), "MDD": C("mdd")}
S_BOX, S_SCAT = 16.0, 18.0      # defaults; c and the MDD scatters differ
S_DENSE, S_MDD = 4.5, 26.0      # n = 288 twins / n = 22 patients
BLOCK_GAP = 0.35                # a: space between drug blocks, in box units
CAT_PT = LABEL_PT               # group names on x are read as axis labels,
CAT_PAD = 0.45                  # not as scale readings -> label size
PERM_P_F = 0.0068            # permutation P for g, carried over from fig5.py
S = {}                       # every caption number, computed here


# ----------------------------------------------------------- drawing grammar
def _lum(col):
    r, g, b = mcolors.to_rgb(col)
    return .2126 * r + .7152 * g + .0722 * b


def _fill(col):
    rgb = np.array(mcolors.to_rgb(col))
    f = .35 if _lum(col) > .70 else .45
    return tuple(1 - f * (1 - rgb))


def _pt_edge(col):
    return tuple(np.array(mcolors.to_rgb(col)) * .55) if _lum(col) > .70 else "none"


def _dark(c, f=.62):
    """Darker shade of a colour, for text on white."""
    import colorsys
    h, l, sat = colorsys.rgb_to_hls(*mcolors.to_rgb(c))
    return colorsys.hls_to_rgb(h, max(0., l * f), sat)


def mark(p):
    return ("***" if p < .001 else "**" if p < .01 else "*" if p < .05
            else "n.s.")


def ptxt(p):
    return "P < 0.0001" if p < 1e-4 else f"P = {p:.2g}"


def boxes(ax, positions, values, colours, width=.62, jitter=.15, seed=0,
          s=None):
    bp = ax.boxplot(values, positions=positions, widths=width,
                    showfliers=False, patch_artist=True)
    for el in ("boxes", "whiskers", "caps", "medians"):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color("black")
    rng = np.random.default_rng(seed)
    for i, v in enumerate(values):
        bp["boxes"][i].set_facecolor(_fill(colours[i]))
        bp["boxes"][i].set_edgecolor("black")
        ax.scatter(positions[i] + rng.uniform(-jitter, jitter, len(v)), v,
                   s=S_BOX if s is None else s, facecolor=colours[i],
                   edgecolor=_pt_edge(colours[i]), linewidth=LW * .55,
                   alpha=.9, zorder=3)


def bracket(ax, x0, x1, y, p, dy):
    """Bracket with a SYMBOL; the exact test goes in the caption."""
    ax.plot([x0, x0, x1, x1], [y, y + dy, y + dy, y], color="black", lw=LW,
            clip_on=False, zorder=5)
    ax.text((x0 + x1) / 2, y + dy * 1.1, mark(p), ha="center", va="bottom",
            fontsize=ANNOT_PT, clip_on=False, zorder=5)


def effect(ax, txt):
    """The effect size itself, in the heading band, right-aligned.  P values,
    CIs and n stay in the caption."""
    ax.text(.98, .985, txt, transform=ax.transAxes, ha="right", va="top",
            fontsize=ANNOT_PT)


def sub_title(ax, txt, pad=.15):
    """Condition / data source, inside the frame and in the same style as the
    block labels of a -- nothing may sit above the frame (alignment rule)."""
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + (hi - lo) * pad)
    ax.text(.02, .985, txt, transform=ax.transAxes, ha="left", va="top",
            fontsize=ANNOT_PT)   # left, so the effect size can sit right


def _below(ax, mm):
    """mm below the axes, in axes fractions -- panels differ in height."""
    return -mm / (ax.get_position().height * PH)


def change_panel(ax, blocks, ylabel, seed=0, p_between=None, tests=True,
                 s=None, title=None):
    """One block per drug, two contrasted groups inside each block, change from
    the drug-free condition on y.  Asterisks, one-sample test against zero;
    bracket, between-group test."""
    pos, vals, cols, ticks, tlabs, blocklab = [], [], [], [], [], []
    x = 0.0
    for bl, entries in blocks:
        first = x
        for lab, v, col in entries:
            pos.append(x); vals.append(v); cols.append(col)
            ticks.append(x); tlabs.append(lab); x += 1.0
        blocklab.append(((first + x - 1) / 2, bl))
        x += BLOCK_GAP
    boxes(ax, pos, vals, cols, seed=seed, s=s)
    ax.axhline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    span = max(v.max() for v in vals) - min(v.min() for v in vals)
    for i, v in enumerate(vals) if tests else []:
        t_, p_ = stats.ttest_1samp(v, 0)
        if p_ < .05:
            ax.text(pos[i], v.max() + span * .04, mark(p_), ha="center",
                    va="bottom", fontsize=ANNOT_PT)
    tops, k = [], 0
    for bl, entries in (blocks if tests else []):
        v0, v1 = entries[0][1], entries[1][1]
        t_, p_ = stats.ttest_ind(v0, v1, equal_var=False)
        if p_between is not None:
            p_ = p_between
        y = max(v0.max(), v1.max()) + span * .21
        bracket(ax, pos[k], pos[k + 1], y, p_, span * .05)
        tops.append(y + span * .13)
        k += 2
    lo = min(v.min() for v in vals)
    head = span * (.22 if len(blocks) > 1 else .06)   # room for block labels
    ax.set_ylim(lo - span * .07,
                max(tops + [max(v.max() for v in vals)]) + head)
    if title:
        sub_title(ax, title)
    ax.set_xticks(ticks); ax.set_xticklabels(tlabs, fontsize=CAT_PT)
    ax.set_xlim(pos[0] - CAT_PAD, pos[-1] + CAT_PAD)
    if len(blocks) > 1:          # inside the axes: nothing may sit above the
        for xc, bl in blocklab:  # frame, or this row's x axes stop aligning
            ax.text(xc, .985, bl, transform=ax.get_xaxis_transform(),
                    ha="center", va="top", fontsize=ANNOT_PT)
    ax.set_ylabel(ylabel)


def level_panel(ax, labels, values, colours, ylabel, seed=0, p_between=None,
                s=None, sep=1.0, jitter=.15, title=None):
    """The drug-free level of the same two groups."""
    boxes(ax, [0, sep], values, colours, seed=seed, s=s, jitter=jitter)
    ax.axhline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    t_, p_ = stats.ttest_ind(values[0], values[1], equal_var=False)
    if p_between is not None:
        p_ = p_between
    hi = max(v.max() for v in values); lo = min(v.min() for v in values)
    span = hi - lo
    bracket(ax, 0, sep, hi + span * .08, p_, span * .05)
    ax.set_ylim(lo - span * .10, hi + span * .28)
    if title:
        sub_title(ax, title)
    ax.set_xticks([0, sep]); ax.set_xticklabels(labels, fontsize=CAT_PT)
    ax.set_xlim(-CAT_PAD, sep + CAT_PAD)
    ax.set_ylabel(ylabel)


def scatter_fit(ax, x, y, col, spearman=False, s=None, edge=False):
    ax.scatter(x, y, s=S_SCAT if s is None else s, facecolor=col,
               edgecolor=_dark(col) if edge else _pt_edge(col),
               linewidth=LW * (.7 if edge else .55), alpha=.9, zorder=3)
    b = np.polyfit(x, y, 1)
    xx = np.linspace(min(x), max(x), 50)
    ax.plot(xx, np.polyval(b, xx), color="black", lw=LW, zorder=4)
    return stats.spearmanr(x, y) if spearman else stats.pearsonr(x, y)


def resid(v, Z):
    v = np.asarray(v, float)
    A = np.column_stack([np.ones(len(v)), Z])
    return v - A @ np.linalg.lstsq(A, v, rcond=None)[0]


def adj_group_t(df, y):
    """Group coefficient of y on group + age + sex + infusion order + placebo-
    session mean FD -- the model the main text reports for this cohort."""
    import statsmodels.formula.api as smf
    d = df.assign(grp=(df.group == "MDD").astype(int))
    m = smf.ols(f"{y} ~ grp + age + sexM + fd_p2 + drug_first", data=d).fit()
    return (float(m.params["grp"]), float(m.tvalues["grp"]),
            float(m.pvalues["grp"]), int(m.df_resid))


# ------------------------------------------------------------------- panels
# The response split in a is DEFINED by the sign of the plotted change, so no
# test is applied there (it would be circular).  b, c and the clinical panels
# plot a different quantity from the one that defines their grouping.
def p_pat_change(ax):
    blocks, S["pat_change"] = [], {}
    for dkey, dn in [("d_ket", "Ketamine"), ("d_mid", "Midazolam")]:
        entries = []
        for p in PAT:
            v = HC27.loc[HC27.pattern == p, dkey].values
            entries.append((p, v, PCOL[p]))
            S["pat_change"][f"{dn}|{p}"] = dict(n=len(v), mean=float(v.mean()),
                                                sd=float(v.std(ddof=1)))
        blocks.append((dn, entries))
    change_panel(ax, blocks, "$\\Delta$ summed MID FC\n(drug $-$ placebo)",
                 seed=6, tests=False, s=S_BOX)


def p_pat_level(ax):
    vals = [HC27.loc[HC27.pattern == p, "Placebo"].values for p in PAT]
    t_, p_ = stats.ttest_ind(vals[0], vals[1], equal_var=False)
    S["pat_level"] = dict(n=[len(v) for v in vals],
                          mean=[float(v.mean()) for v in vals],
                          t=float(t_), p=float(p_))
    level_panel(ax, PAT, vals, [PCOL[p] for p in PAT],
                "Placebo summed MID FC", seed=7, sep=1.5, title="Placebo")


def p_mid_twin(ax):
    """Fig. 4's companion panel: the twins' simulated baseline MID FC under the
    same both-up / any-down split, so the in vivo panels have a model
    counterpart on the same measure."""
    vals = [MID.loc[MID.pattern_np == p, "mid_baseline"].values for p in PAT]
    t_, p_ = stats.ttest_ind(vals[0], vals[1], equal_var=False)
    S["mid"] = dict(n=[len(v) for v in vals],
                    mean=[float(v.mean()) for v in vals],
                    sd=[float(v.std(ddof=1)) for v in vals],
                    t=float(t_), p=float(p_))
    level_panel(ax, PAT, vals, [PCOL[p] for p in PAT],
                "Simulated baseline MID FC", seed=8, s=S_DENSE, sep=1.5,
                jitter=.24, title="Simulation")


def p_clin_change(ax):
    entries, S["clin_change"] = [], {}
    for g in ["MDD", "HC"]:
        v = PH36.loc[PH36.group == g, "FC_delta"].values
        entries.append((g, v, GCOL[g]))
        t_, p_ = stats.ttest_1samp(v, 0)
        S["clin_change"][g] = dict(n=len(v), mean=float(v.mean()),
                                   t=float(t_), p=float(p_))
    b_, t_, p_, dfr = adj_group_t(PH36, "FC_delta")
    S["clin_change"]["between"] = dict(beta=b_, t=t_, p=p_, df=dfr)
    change_panel(ax, [("Ketamine", entries)],
                 "$\\Delta$ NP FC\n(ketamine $-$ placebo)", seed=3,
                 p_between=p_, title="Ketamine")


def p_clin_level(ax):
    vals = [PH36.loc[PH36.group == g, "FC_p2"].values for g in ["MDD", "HC"]]
    b_, t_, p_, dfr = adj_group_t(PH36, "FC_p2")
    S["clin_level"] = dict(n=[len(v) for v in vals], beta=b_, t=t_, p=p_,
                           df=dfr)
    level_panel(ax, ["MDD", "HC"], vals, [GCOL[g] for g in ["MDD", "HC"]],
                "Placebo NP FC", seed=4, p_between=p_, title="Placebo")


def p_np_symp(ax):
    r, _ = scatter_fit(ax, F22.x_NPchange_resid.values,
                       F22.y_sympPC1change_resid.values, C("mdd"),
                       s=S_MDD, edge=True)
    df_ = len(F22) - 4 - 2          # both axes are residuals on 4 covariates
    t_ = r * np.sqrt(df_ / (1 - r ** 2))
    p_ = float(2 * stats.t.sf(abs(t_), df_))
    S["np_symp"] = dict(n=len(F22), r=float(r), df=df_, p=p_)
    ax.axhline(0, color="0.85", lw=LW, zorder=1)
    ax.axvline(0, color="0.85", lw=LW, zorder=1)
    sub_title(ax, "Ketamine")
    effect(ax, f"$r$ = {r:.2f}".replace("-", "\u2212"))
    ax.set_xlabel("$\\Delta$ NP FC (residual)")
    ax.set_ylabel("$\\Delta$ symptom PC1\n(residual)")


def p_twin_madrs(ax):
    Z = np.column_stack([G22.age.astype(float),
                         (G22.sex.astype(str).str.upper() == "M").astype(float),
                         (G22.infusion_1.astype(str) == "d").astype(float),
                         G22.fd_p2.astype(float)])
    x, y = resid(G22.pref_d2, Z), resid(G22.MADRS_delta, Z)
    rho, p_ = scatter_fit(ax, x, y, C("mdd"), spearman=True, s=S_MDD,
                          edge=True)
    S["twin"] = dict(n=len(G22), rho=float(rho), p=float(p_), p_perm=PERM_P_F)
    ax.axhline(0, color="0.85", lw=LW, zorder=1)   # every residual-vs-residual
    ax.axvline(0, color="0.85", lw=LW, zorder=1)   # panel gets the same zero
    sub_title(ax, "Ketamine")
    effect(ax, f"$\\rho$ = {rho:.2f}".replace("-", "\u2212"))
    ax.set_xlabel("Similarity to AMPA-perturbed\ntwin (residual)")
    ax.set_ylabel("$\\Delta$ MADRS\n(residual)")


def p_index_fu3(ax):
    """h -- leave-one-out prediction from the 12 simulated NP edges."""
    r, p_ = scatter_fit(ax, NP12.predicted_sim.values, NP12.observed.values,
                        C("np12"))
    S["index"] = dict(n=len(NP12), r=float(r), p=float(p_),
                      r2_loo=float(ACC.loc[ACC.model.str.startswith("12 simulated"),
                                           "R2_LOO"].iloc[0]))
    ax.axhline(0, color="0.85", lw=LW, zorder=1)
    sub_title(ax, "Follow-up")
    effect(ax, f"$r$ = {r:.2f}".replace("-", "\u2212"))
    ax.set_xlabel("Predicted $\\Delta$ symptoms\n(leave-one-out)")
    ax.set_ylabel("Observed $\\Delta$ symptoms")


def p_perm_r2(ax):
    """i -- out-of-sample accuracy of five model specifications."""
    x = np.arange(len(ACC))
    base = C("np12")
    for i, row in ACC.iterrows():
        filled = bool(row.simulated)
        ax.bar(i, row.r_LOO, width=.66, zorder=2,
               facecolor=_fill(base) if filled else "white",
               edgecolor=_dark(base, .62) if (filled or row.empirical) else "0.35",
               linewidth=LW)
    thr = float(ACC.null_p95.iloc[0])
    ax.plot([-.6, len(ACC) - .4], [thr] * 2, ls=(0, (2.2, 1.6)), color="0.35",
            lw=LW, zorder=3, solid_capstyle="butt")
    ax.text(len(ACC) - .45, thr, " null 95th", ha="left", va="center",
            fontsize=ANNOT_PT, color="0.35")
    for i, row in ACC.iterrows():
        if row.P < .05:
            ax.text(i, row.r_LOO + .012, mark(row.P), ha="center", va="bottom",
                    fontsize=ANNOT_PT)
    ax.set_xticks(x)
    ax.set_xticklabels(["symptoms", "simulated", "empirical", "sym + sim",
                        "sym + emp"], fontsize=TICK_PT, rotation=45,
                       ha="right", rotation_mode="anchor")
    ax.set_xlim(-.6, len(ACC) - .4)
    ax.set_ylim(0, max(ACC.r_LOO) * 1.22)
    S["perm"] = dict(n=int(ACC.n.iloc[0]), n_perm=int(ACC.n_perm.iloc[0]),
                     thr=thr,
                     r=dict(zip(ACC.model, ACC.r_LOO.round(3))),
                     p=dict(zip(ACC.model, ACC.P.round(4))),
                     p_perm=float(ACC.perm_P.dropna().iloc[0]))
    sub_title(ax, "Follow-up")
    ax.set_ylabel("Leave-one-out $r$\n(predicted vs observed)")


# --------------------------------------------------------------- page geometry
LAB_L = 17.0                       # y label + y ticks
XB_BOX1 = 7.2                      # one line of 10 pt group names
XB_SC2 = 13.0                      # two-line x label
XB_SC1 = 9.5                       # one-line x label
LETTER_BAND, LETTER_PAD, LETTER_PADX = K.LETTER_BAND, K.LETTER_PAD, K.LETTER_PADX
GAP, MB = K.GAP, K.MB
GUT = K.LETTER_W + K.LETTER_PADX   # letter gutter, left of the panel ink
GAPX = 8.5                         # wider than the kit default: row_geom
                                   # spends it on the *visible* gap

COL_A, COL_S = 80.0, 41.5              # row 1: ratios only -- row_geom
                                       # rescales to the measured ink
                                       # ("any down" is 11.9 mm at 8 pt)
COL_T = (PW - ML - MR - 2 * GAPX) / 3  # rows 2-3: three equal columns
MAX_H = 44.0                           # cap: a taller panel than this reads
                                       # as a column, not a panel
ROWS = [[("a", p_pat_change, ML, COL_A, XB_BOX1),
         ("b", p_pat_level, ML + COL_A + GAPX, COL_S, XB_BOX1),
         ("c", p_mid_twin, ML + COL_A + COL_S + 2 * GAPX, COL_S, XB_BOX1)],
        [("d", p_clin_change, ML, COL_T, XB_BOX1),
         ("e", p_clin_level, ML + COL_T + GAPX, COL_T, XB_BOX1),
         ("f", p_np_symp, ML + 2 * (COL_T + GAPX), COL_T, XB_SC1)],
        [("g", p_twin_madrs, ML, COL_T, XB_SC2),
         ("h", p_index_fu3, ML + COL_T + GAPX, COL_T, XB_SC2),
         ("i", p_perm_r2, ML + 2 * (COL_T + GAPX), COL_T, XB_SC2)]]
NROW = len(ROWS)
XB_ROW = [XB_BOX1, XB_BOX1, XB_SC2]   # pitch per row: f's one-line x label
XB_SUM = sum(XB_ROW)                  # is allowed 2.3 mm into the gap


def row_geom(fig, panels):
    """Axes x and width per panel so that the VISIBLE gaps within a row are
    equal (equal column pitch is not enough: the y labels and tick labels of
    the three panels are not equally wide).  Relative panel widths are kept.
    Each panel also gets a GUT gutter at its left so the letter stands clear
    of its own ink, exactly as the kit's place_letters wants it."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    by = {p["ch"]: p for p in panels}
    geom = {}
    meas = []
    for row in ROWS:
        chs = [r[0] for r in row]
        L, R, W = [], [], []
        for ch in chs:
            ax = by[ch]["axes"][0]
            bb, pos = ax.get_tightbbox(rend), ax.get_position()
            L.append(max(pos.x0 * PW - mm(bb.x0), 0.0))
            R.append(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0))
            W.append(pos.width * PW)
        meas.append((chs, L, R, W))
    L1 = max(m[1][0] for m in meas)       # one label column for a, d, g, so
    # rows 2 and 3 are the same three columns, so they are solved TOGETHER on
    # the widest label block of each column: d and g (and e/h, f/i) then get
    # identical frames, and the x axis of g is exactly as long as d's.
    shared = {}
    if len(meas) >= 3:
        _, L2, R2, W2 = meas[1]
        _, L3, R3, W3 = meas[2]
        Lc = [max(a, b) for a, b in zip([L1] + L2[1:], [L1] + L3[1:])]
        RCAP = 2.0                      # mm kept clear; the rest
        Rc = [min(max(a, b), RCAP) for a, b in zip(R2, R3)]
        Wc = W2
        n = len(Wc)
        sc = ((PW - ML - MR - (n - 1) * GAPX - n * GUT - sum(Lc) - sum(Rc))
              / sum(Wc))
        x = ML
        for i in range(n):
            shared[i] = (x, x + GUT + Lc[i], Wc[i] * sc)
            x += GUT + Lc[i] + Wc[i] * sc + Rc[i] + GAPX
    for ri, (chs, L, R, W) in enumerate(meas):
        if ri in (1, 2) and shared:
            for i, ch in enumerate(chs):
                geom[ch] = shared[i]
            continue
        L = [L1] + L[1:]
        s = ((PW - ML - MR - (len(chs) - 1) * GAPX - len(chs) * GUT
              - sum(L) - sum(R)) / sum(W))
        x = ML
        for i, ch in enumerate(chs):
            geom[ch] = (x, x + GUT + L[i], W[i] * s)  # slot, axes x, width
            x += GUT + L[i] + W[i] * s + R[i] + GAPX
    return geom


def build(plot_h, shift=None, geom=None):
    """Lay the rows out at axes height `plot_h`; `shift` pushes single panels
    down by mm so the CONTENT tops within a row sit on one line, and `geom`
    (from row_geom) equalises the visible gaps."""
    shift = shift or {}
    f = plt.figure(figsize=panel(PW, PH))
    out, y = [], MT
    for ri, row in enumerate(ROWS):
        top = y + LETTER_BAND
        for ch, fn, x_mm, w_mm, xblock in row:
            slot, ax_x, ax_w = (geom[ch] if geom else
                                (x_mm, x_mm + LAB_L, w_mm - LAB_L))
            ax = K.axes_mm(f, ax_x, top + shift.get(ch, 0.0), ax_w, plot_h)
            fn(ax)
            out.append(dict(ch=ch, x=slot, axes=[ax],
                            txt=K.letter(f, slot, top - 1.2, ch)))
        y = (top + max(shift.get(r[0], 0.0) for r in row) + plot_h
             + XB_ROW[ri] + GAP)
    enforce(f)
    return f, out, y - GAP


# ------------------------------------------------------------------- caption
CAP_TITLE = "Fig. 5 | In vivo pharmacology and longitudinal association."


def caption_runs():
    pc, pl, md = S["pat_change"], S["pat_level"], S["mid"]
    cc, cl = S["clin_change"], S["clin_level"]
    ns, tw, ix, pm = S["np_symp"], S["twin"], S["index"], S["perm"]
    k = [pc["Ketamine|both up"], pc["Ketamine|any down"]]
    m = [pc["Midazolam|both up"], pc["Midazolam|any down"]]
    cap = [
        ("", "Two cohorts test the perturbation account in vivo, one panel gives "
             "its model counterpart, and a third cohort tests it prospectively. "
             "Healthy volunteers (n = 27) received placebo, ketamine and "
             "midazolam; the clinical cohort (n = 36) received placebo and "
             "ketamine; the digital twins in c are the Fig. 4 cohort (n = 288); "
             "the longitudinal cohort is the IMAGEN follow-up (n = 85). Box "
             "plots show the median, 25th-75th percentiles and 1.5 x IQR "
             "whiskers with every participant overplotted; dashed line, no "
             "change. An asterisk above a single box (d) is a two-sided "
             "one-sample t test against zero; brackets are the between-group "
             "test named below. *P < 0.05, **P < 0.01, ***P < 0.001. The "
             "heading inside each panel names the condition or data source it "
             "shows. b, c and e make one statement in two independent drug "
             "datasets and in the model: the group whose connectivity rises "
             "under the drug is the group that starts from the lower drug-free "
             "level. In f, g and h both axes are residuals, so the grey cross "
             "marks zero on each and the coefficient in the heading band is "
             "the effect size itself (both axes being residuals, it is a "
             "partial coefficient); its P, confidence interval and n are given "
             "below. "),
        ("a", f", change in summed MID FC from placebo in the healthy cohort, "
              f"split by the Fig. 4 response rule (both up n = {k[0]['n']}, any "
              f"down n = {k[1]['n']}). Ketamine: {k[0]['mean']:+.2f} +/- "
              f"{k[0]['sd']:.2f} in both-up versus {k[1]['mean']:+.2f} +/- "
              f"{k[1]['sd']:.2f} in any-down; midazolam: {m[0]['mean']:+.2f} +/- "
              f"{m[0]['sd']:.2f} versus {m[1]['mean']:+.2f} +/- {m[1]['sd']:.2f} "
              f"(mean +/- s.d.). This panel is descriptive and carries no test: "
              f"the two groups are defined by the sign of the very quantity "
              f"plotted here, so any test of it would be circular. "),
        ("b", f", drug-free (placebo) level of the same two groups: "
              f"{pl['mean'][0]:+.2f} versus {pl['mean'][1]:+.2f}, two-sided "
              f"Welch t = {pl['t']:.2f}, {ptxt(pl['p'])}. The grouping is "
              f"defined on the drug-induced change and the plotted quantity is "
              f"the drug-free level, so this contrast is not circular. "),
        ("c", f", the same comparison in the digital twins of the Fig. 4 cohort: "
              f"simulated baseline MID FC under the both-up / any-down split "
              f"defined on the NP sum (both up n = {md['n'][0]}, any down "
              f"n = {md['n'][1]}): {md['mean'][0]:+.2f} +/- {md['sd'][0]:.2f} "
              f"versus {md['mean'][1]:+.2f} +/- {md['sd'][1]:.2f}, Welch "
              f"t = {md['t']:.2f}, {ptxt(md['p'])} -- the model reproduces the "
              f"direction seen in b on the same measure. "),
        ("d", f", ketamine-induced change in NP FC in the clinical cohort "
              f"(MDD n = {cc['MDD']['n']}, HC n = {cc['HC']['n']}): "
              f"{cc['MDD']['mean']:+.2f} versus {cc['HC']['mean']:+.2f}. The "
              f"bracket is the group coefficient of an OLS model adjusted for "
              f"age, sex, infusion order and placebo-session mean framewise "
              f"displacement (beta = {cc['between']['beta']:.2f}, "
              f"t = {cc['between']['t']:.2f}, df = {cc['between']['df']}, "
              f"{ptxt(cc['between']['p'])}), not a raw two-sample test. "),
        ("e", f", placebo NP FC in the same cohort, same adjusted model "
              f"(beta = {cl['beta']:.2f}, t = {cl['t']:.2f}, df = {cl['df']}, "
              f"{ptxt(cl['p'])}). "),
        ("f", f", change in NP FC against change in the symptom PC1 in the "
              f"patients (n = {ns['n']}); both axes are residuals on baseline "
              f"severity, age, infusion order and placebo-session mean framewise "
              f"displacement, so the residual df is {ns['df']}: partial "
              f"r = {ns['r']:.2f}, {ptxt(ns['p'])}. "),
        ("g", f", similarity of the ketamine state to the AMPA-perturbed digital "
              f"twin against MADRS change (n = {tw['n']}), both residualised on "
              f"age, sex, infusion order and placebo-session mean framewise "
              f"displacement: Spearman rho = {tw['rho']:.2f}, {ptxt(tw['p'])}; "
              f"permutation P = {tw['p_perm']:.4f}. "),
        ("h", f", leave-one-out predicted against observed four-year symptom "
              f"change from the 12 NP edges of each participant's unperturbed "
              f"digital twin (n = {ix['n']}): r = {ix['r']:.2f}, "
              f"{ptxt(ix['p'])}; cross-validated R^2 = {ix['r2_loo']:.3f}. "
              f"Negative values on both axes are improvement; the line is a "
              f"least-squares fit shown to indicate direction, not an "
              f"additional test. "),
        ("i", f", leave-one-out correlation between predicted and observed "
              f"symptom change for five model specifications in the same "
              f"n = {pm['n']}: age-19 symptoms alone "
              f"r = {pm['r']['age-19 symptoms only']:.2f}, the 12 simulated "
              f"edges r = {pm['r']['12 simulated NP edges']:.2f}, the 12 "
              f"empirical edges r = {pm['r']['12 empirical NP edges']:.2f}, and "
              f"symptoms combined with each edge set "
              f"r = {pm['r']['symptoms + 12 simulated edges']:.2f} and "
              f"r = {pm['r']['symptoms + 12 empirical edges']:.2f}. Filled bars, "
              f"simulated network; open bars, empirical network. The dashed line "
              f"is the 95th percentile ({pm['thr']:.2f}) of a permutation null "
              f"for the 12-edge simulated model in which the outcome was "
              f"shuffled and the whole leave-one-out procedure repeated "
              f"{pm['n_perm']:,} times (observed P = {pm['p_perm']:.4f}). "
              f"*P < 0.05, **P < 0.01, ***P < 0.001 on the leave-one-out "
              f"correlation itself."),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs


# pass 1 -- content overhang per panel and the caption height
_f0, _p0, _ = build(30.0)
_over = K.overhangs(_f0, _p0)
_runs0 = caption_runs()
_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
plt.close(_f0)

CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
FIXED = (MT + NROW * LETTER_BAND + XB_SUM + (NROW - 1) * GAP
         + sum(max(_over[r[0]] for r in row) for row in ROWS))
PLOT_H = min((PH - MB - CAP_H - FIXED) / NROW, MAX_H)   # fill, never overrun

# pass 2 -- re-measure the overhang AT the solved height (anything positioned
# in axes fractions changes with it), then push each panel down by its own
_f1, _p1, _ = build(PLOT_H)
_geom = row_geom(_f1, _p1)
plt.close(_f1)
for _ in range(4):                           # iterate: the tick labels shift a
    _f2, _p2, _ = build(PLOT_H, geom=_geom)  # little when the axes width does
    _geom = row_geom(_f2, _p2)
    _o1 = K.overhangs(_f2, _p2)
    plt.close(_f2)
# one shift per ROW (its largest overhang), not per panel: that keeps the x and
# y axes of a row on one line as well as the letters.  It costs nothing here
# because no panel puts anything above its own frame.
_over = {ch: max(_o1[r[0]] for r in row) for row in ROWS for ch, *_ in row}
fig, PANELS, BOTTOM = build(PLOT_H, _over, geom=_geom)
K.align_left_ink(fig, PANELS, [["a", "d", "g"]])
# align_left_ink levels each panel's whole ink block (label + tick labels); the
# tick labels of a, d and g differ in width, so the LABELS themselves still sat
# on three different lines.  Level the label text as well -- measured on the
# label's own bbox, because a rotated text's anchor is not its edge.
fig.canvas.draw()
_r = fig.canvas.get_renderer()
_mm = lambda px: px / fig.dpi * 25.4
_cols = [("a", "d", "g"), ("e", "h")]
_ax_of = {p["ch"]: p["axes"][0] for p in PANELS}
_lx = lambda a: _mm(a.yaxis.label.get_window_extent(renderer=_r).x0)
for _grp in _cols:                   # one line per column of panels
    _line = min(_lx(_ax_of[ch]) for ch in _grp)
    for ch in _grp:
        _ax = _ax_of[ch]
        for _ in range(4):
            _d = _lx(_ax) - _line
            if abs(_d) < .05:
                break
            _lab, _pos = _ax.yaxis.label, _ax.get_position()
            _px, _py = _lab.get_position()
            _ax.yaxis.set_label_coords(
                (_px - _d / 25.4 * fig.dpi - _pos.x0 * fig.bbox.width)
                / (_pos.width * fig.bbox.width), _py)
            fig.canvas.draw()
print("row-2 gaps (mm): "
      + f"d->e {_geom['e'][0] - (_geom['d'][1] + _geom['d'][2]):.1f}, "
      + f"e->f {_geom['f'][0] - (_geom['e'][1] + _geom['e'][2]):.1f}")
print("frame width (mm): " + ", ".join(
    f"{p['ch']} {p['axes'][0].get_position().width * PW:.2f}"
    for p in PANELS if p["ch"] in ("d", "e", "f", "g", "h", "i")))
print("y-label left edge (mm): " + ", ".join(
    f"{ch} {_lx(_ax_of[ch]):.2f}" for _grp in _cols for ch in _grp))
K.place_letters(fig, PANELS, rows=[[ch for ch, *_ in row] for row in ROWS])

runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM

assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
print(f"[{STEM}] axes height {PLOT_H:.1f} mm; panels end at {BOTTOM:.1f} mm; "
      f"caption {n_lines} lines -> {CAP_BOTTOM:.1f} mm of {PH:.0f} mm")

# ----------------------------------------------------------------------- export
png, pdf, ppt = (os.path.join(HERE, STEM + ext) for ext in (".png", ".pdf", ".pptx"))
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")
K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
              collect_text_records=collect_text_records)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
print("non-Arial text:", bad[:5], "| files:",
      [os.path.basename(p) for p in (png, pdf, ppt)])
pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
    os.path.join(HERE, "fig5_main_A4_np12_caption_values.csv"), index=False)
plt.close(fig)
