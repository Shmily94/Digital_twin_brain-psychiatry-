"""Supplementary figure: paired placebo-versus-drug comparisons of the summed
NP-related MID connectivity, both panels on ONE A4 page.

Same two plots as panels/figS_midpaired_a and _b (placebo vs ketamine and
placebo vs midazolam, 27 healthy volunteers, within-subject cross-over), laid
out under the frozen rules of figA4_kit: 8 / 9 / 10 / 11 pt type, no
declarative titles, the motion-adjusted P in the heading band and every other
statistic in the rich-text caption, and both variants (with caption and
--no-caption).

  a  Placebo versus ketamine
  b  Placebo versus midazolam

The plotted quantity is the RAW sum of the six NP-related MID edges (fc1-fc6).
The Fig. 5 score is not used here: it is that sum residualised on head motion
and standardised separately WITHIN each condition, so a paired
placebo-versus-drug difference on it is identically zero by construction.
Head motion is not balanced across sessions, so the test carried on each panel
is the motion-adjusted one -- the intercept of (drug - placebo) FC regressed on
(drug - placebo) FD, which adjusts for motion without removing the condition
mean.  The unadjusted and pooled-residual versions are in the source table and
in the caption.

    python figS_midpaired_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_midpaired")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce, panel_title
from fig_export import collect_text_records
from supp_kit import boxes
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT

DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_midpaired_A4" if WITH_CAP else "figS_midpaired_A4_nocaption"
SUPP_NO = "S11"                    # next free number: S1-S8 are in
                                   # FIGURE_LEGENDS.md, S9 stratify, S10 pet,
                                   # S12 oldham
apply_np_style()
K.apply_page_style()

SUB = pd.read_csv(os.path.join(HERE, "data", "midpaired_subject_level_n27.csv"))
ST = pd.read_csv(os.path.join(HERE, "data", "midpaired_placebo_vs_drug_n27.csv"))
N = len(SUB)
C_PL = C("placebo")
DCOL = {"Ketamine": C("ketamine"), "Midazolam": C("midazolam")}
YLAB = "Summed MID FC"             # same wording as Fig. 5 panel a
S_BOX = 16.0                       # same marker area as Fig. 5 panel a

ALL = np.concatenate([SUB[c].values for c in ("Placebo", "Ketamine", "Midazolam")])
YLO, YHI = ALL.min() - .22, ALL.max() + .40      # one scale for both panels
SPEC = [("a", "Ketamine"), ("b", "Midazolam")]
S = {}                                            # every caption number


def row(drug, key):
    m = ST[(ST.comparison == f"Placebo vs {drug}") &
           (ST.measure.astype(str).str.startswith(key))]
    return m.iloc[0]


def fd_test(drug):
    d = SUB[f"FD_{drug}"].values - SUB["FD_Placebo"].values
    t, p = stats.ttest_1samp(d, 0.0)
    return float(d.mean()), float(t), int(len(d) - 1), float(p)


def paired(ax, letter, drug, ylabel=True):
    a, b = SUB["Placebo"].values, SUB[drug].values
    col = DCOL[drug]
    boxes(ax, [0, 1], [a, b], [C_PL, col], width=.46, jitter=.13, seed=3,
          s=S_BOX)
    adj, raw = row(drug, "motion-adjusted (\u0394FC"), row(drug, "raw summed FC")
    pooled = row(drug, "motion-adjusted (pooled")
    fig5 = row(drug, "Fig. 5 score")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Placebo", drug], fontsize=TICK_PT)
    ax.get_xticklabels()[0].set_color(C_PL)
    ax.get_xticklabels()[1].set_color(col)
    if ylabel:
        ax.set_ylabel(YLAB, fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.set_xlim(-.62, 1.62)
    ax.set_ylim(YLO, YHI)
    panel_title(ax, f"Placebo versus {drug.lower()} (n = {N})")
    ax.title.set_fontsize(LABEL_PT)
    ax.text(.98, .985, f"$P$ = {adj.p:.3f}", transform=ax.transAxes,
            ha="right", va="top", fontsize=ANNOT_PT)
    fdm, fdt, fddf, fdp = fd_test(drug)
    S[letter] = dict(
        drug=drug.lower(), n=N,
        pl_mean=float(raw.placebo_mean), dr_mean=float(raw.drug_mean),
        raw_d=float(raw.mean_diff), raw_lo=float(raw.ci95_lo),
        raw_hi=float(raw.ci95_hi), raw_t=float(raw.t), raw_df=int(raw.df),
        raw_p=float(raw.p), wil_p=float(raw.wilcoxon_p), dz=float(raw.cohens_dz),
        n_inc=int(raw.n_increased),
        adj_d=float(adj.mean_diff), adj_lo=float(adj.ci95_lo),
        adj_hi=float(adj.ci95_hi), adj_t=float(adj.t), adj_df=int(adj.df),
        adj_p=float(adj.p),
        po_d=float(pooled.mean_diff), po_t=float(pooled.t),
        po_df=int(pooled.df), po_p=float(pooled.p),
        fig5_p=float(fig5.p),
        fd_d=fdm, fd_t=fdt, fd_df=fddf, fd_p=fdp)


PANEL_FN = {ch: (lambda ax, ch=ch, dr=dr: paired(ax, ch, dr, ylabel=ch == "a"))
            for ch, dr in SPEC}

# --------------------------------------------------------------- page geometry
GUT = K.LETTER_W + K.LETTER_PADX
GAPX = 10.0
LETTER_BAND, MB = K.LETTER_BAND, K.MB
XB = 6.0                           # one-line x tick labels, no x axis label
MAX_H = 62.0
ROWS = [["a", "b"]]
COLS = [["a"], ["b"]]
BLOCK_W = 132.0                    # centred block: a 2-box panel needs no more
X0 = ML + (PW - ML - MR - BLOCK_W) / 2
NCOL = 2
COL_W = (BLOCK_W - (NCOL - 1) * GAPX) / NCOL
LAB_L = 13.0


def col_geom(fig, panels):
    """One x per column so the two frames line up, visible gap = GAPX."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    by = {p["ch"]: p for p in panels}
    L, R = [], []
    for col in COLS:
        ll, rr = [], []
        for ch in col:
            ax = by[ch]["axes"][0]
            bb, pos = ax.get_tightbbox(rend), ax.get_position()
            ll.append(max(pos.x0 * PW - mm(bb.x0), 0.0))
            rr.append(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0))
        L.append(max(ll)); R.append(max(rr))
    w = (BLOCK_W - (NCOL - 1) * GAPX - NCOL * GUT - sum(L) - sum(R)) / NCOL
    geom, x = {}, X0
    for j, col in enumerate(COLS):
        for ch in col:
            geom[ch] = (x, x + GUT + L[j], w)
        x += GUT + L[j] + w + R[j] + GAPX
    return geom


def build(plot_h, geom=None):
    f = plt.figure(figsize=panel(PW, PH))
    out, y = [], MT
    for r in ROWS:
        top = y + LETTER_BAND
        for j, ch in enumerate(r):
            slot, ax_x, ax_w = (geom[ch] if geom else
                                (X0 + j * (COL_W + GAPX),
                                 X0 + j * (COL_W + GAPX) + LAB_L,
                                 COL_W - LAB_L))
            ax = K.axes_mm(f, ax_x, top, ax_w, plot_h)
            PANEL_FN[ch](ax)
            out.append(dict(ch=ch, x=slot, axes=[ax],
                            txt=K.letter(f, slot, top - 1.2, ch)))
        y = top + plot_h + XB + K.GAP
    enforce(f)
    return f, out, y - K.GAP


# ------------------------------------------------------------------- caption
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Neither ketamine nor midazolam "
             "shifts the summed NP-related MID connectivity in the paired "
             "placebo comparison.")


def pf(p):
    return (f"P = {p:.3g}" if p >= 1e-3 else
            f"P = {p:.2g}" if p >= 1e-4 else f"P = {p:.1e}")


def line(letter, what):
    d = S[letter]
    return (f", {what}. Placebo mean {d['pl_mean']:.3f}, "
            f"{d['drug']} mean {d['dr_mean']:.3f}; unadjusted paired "
            f"difference {d['raw_d']:+.3f} (95% CI {d['raw_lo']:+.3f} to "
            f"{d['raw_hi']:+.3f}), t({d['raw_df']}) = {d['raw_t']:.3f}, "
            f"{pf(d['raw_p'])}, Wilcoxon {pf(d['wil_p'])}, Cohen's dz = "
            f"{d['dz']:+.3f}, {d['n_inc']} of {d['n']} participants higher on "
            f"{d['drug']}. Head motion: mean framewise displacement "
            f"{d['fd_d']:+.3f} mm relative to placebo, t({d['fd_df']}) = "
            f"{d['fd_t']:.3f}, {pf(d['fd_p'])}; the motion-adjusted test "
            f"printed in the panel gives {d['adj_d']:+.3f} "
            f"({d['adj_lo']:+.3f} to {d['adj_hi']:+.3f}), "
            f"t({d['adj_df']}) = {d['adj_t']:.3f}, {pf(d['adj_p'])}, and the "
            f"pooled-residual version {d['po_d']:+.3f}, "
            f"t({d['po_df']}) = {d['po_t']:.3f}, {pf(d['po_p'])}. ")


def caption_runs():
    cap = [
        ("", f"Box plots show the median and interquartile range with whiskers "
             f"at 1.5 times the interquartile range; every one of the "
             f"{N} healthy volunteers is plotted as a point, jittered "
             f"horizontally. Both panels share the y axis, and the plotted "
             f"quantity is the RAW sum of the six NP-related MID edges "
             f"(Fisher z). The design is a randomised within-subject "
             f"cross-over with three infusion sessions, so each participant "
             f"contributes a point to placebo and to the drug; the paired "
             f"structure is carried by the test rather than by connecting "
             f"lines. Because head motion is not balanced across sessions, "
             f"the statistic printed in each heading band is the "
             f"motion-adjusted one: the intercept of the paired FC difference "
             f"(drug - placebo) regressed on the paired framewise-displacement "
             f"difference, which adjusts for motion without removing the "
             f"condition mean. All tests are two-sided and uncorrected. "),
        ("a", line("a", "placebo versus ketamine")),
        ("b", line("b", "placebo versus midazolam")),
        ("", f"Neither drug moves the summed NP-related MID connectivity away "
             f"from placebo, whether the comparison is unadjusted "
             f"({pf(S['a']['raw_p'])} and {pf(S['b']['raw_p'])}) or "
             f"motion-adjusted ({pf(S['a']['adj_p'])} and "
             f"{pf(S['b']['adj_p'])}), and the split of participants moving up "
             f"versus down is close to even in both ({S['a']['n_inc']}/{N} and "
             f"{S['b']['n_inc']}/{N} higher on drug). Midazolam is the session "
             f"with the higher head motion ({S['b']['fd_d']:+.3f} mm, "
             f"{pf(S['b']['fd_p'])}), which is why the adjusted test is the one "
             f"reported; ketamine is balanced on motion "
             f"({pf(S['a']['fd_p'])}). The composite score used in Fig. 5 is "
             f"not plotted here: it is this sum residualised on framewise "
             f"displacement and then standardised separately WITHIN each "
             f"condition, so its paired placebo-versus-drug difference is "
             f"identically zero by construction (verified: paired t = 0, "
             f"P = 1 in both comparisons) and a between-condition mean "
             f"contrast on it is not interpretable. Source values, including "
             f"the unadjusted, motion-adjusted and pooled-residual tests for "
             f"both drugs, are in "
             f"midpaired_placebo_vs_drug_n27.csv; the subject-level and "
             f"edgewise inputs are in midpaired_subject_level_n27.csv and "
             f"midpaired_edgewise_source_n27.csv. "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs


# pass 1 -- caption height at a provisional plot height
_f0, _p0, _ = build(40.0)
_runs0 = caption_runs()
_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
plt.close(_f0)

CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
NROW = len(ROWS)
FIXED = MT + NROW * (LETTER_BAND + XB) + (NROW - 1) * K.GAP
PLOT_H = min((PH - MB - CAP_H - FIXED) / NROW, MAX_H)

# pass 2 -- solve the column geometry at the fitted height
_f1, _p1, _ = build(PLOT_H)
_geom = col_geom(_f1, _p1)
plt.close(_f1)
for _ in range(3):                      # tick labels move when the width does
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
    os.path.join(HERE, "figS_midpaired_A4_caption_values.csv"), index=False)
plt.close(fig)
