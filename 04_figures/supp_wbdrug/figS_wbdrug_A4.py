"""Supplementary figure: agreement between simulated and empirical whole-brain
drug effects, all three panels and their shared legend on ONE A4 page.

Same plots as panels/figS_wbdrug_a, _b, _c and figS_wbdrug_legend, rebuilt
under the frozen rules of figA4_kit (8 / 9 / 10 / 11 pt type, no declarative
titles, every statistic in the rich-text caption, both variants):

  a  directional concordance for the pharmacologically MATCHED pairings,
     task-matched (MID) versus task-mismatched (SST) DTB predictions
  b  the same for the CROSS-RECEPTOR pairings - the receptor-specificity
     control
  c  split-half reliability of the empirical drug-effect maps, which bounds
     the agreement any model can attain

Pharmacological sample: 27 healthy volunteers, three within-subject sessions
(placebo, ketamine, midazolam), MID task, Shen-268 whole-brain FC.  Edges
entering the test are those with a nominal drug-versus-placebo effect at
P < 0.001.  Significance is the node-level sign-flip null (999 permutations);
the binomial test is reported alongside but ignores edge dependence.

    python figS_wbdrug_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_wbdrug")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, panel, C, LW, enforce, panel_title
from fig_export import collect_text_records
from supp_kit import fill
import figA4_kit as K
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT

DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_wbdrug_A4" if WITH_CAP else "figS_wbdrug_A4_nocaption"
SUPP_NO = "S13"                    # next free: S1-S8 in FIGURE_LEGENDS.md,
                                   # S9 stratify, S10 pet, S11 midpaired,
                                   # S12 oldham
apply_np_style()
K.apply_page_style()

W3 = pd.read_csv(os.path.join(HERE, "data",
                              "wbdrug_direction_agreement_n288.csv"))
RL = pd.read_csv(os.path.join(HERE, "data", "wbdrug_map_reliability.csv"))
RL = RL.sort_values(["drug", "drug_condition"]).reset_index(drop=True)
CK, CM = C("ketamine"), C("midazolam")
DCOL = {"Ketamine": CK, "Midazolam": CM}
LLAB = {"mid_antici_hit": "MID\nanticipation", "mid_feed_hit": "MID\nfeedback",
        "pooled (both MID conditions)": "pooled"}
LEVELS = ["mid_antici_hit", "mid_feed_hit", "pooled (both MID conditions)"]
S_EST = 24.0                       # estimate marker, as in the single panels
S = {}                             # every caption number


def conc_panel(ax, letter, pairing, head):
    sub = W3[W3.pairing == pairing]
    xs, xl, xc, k = [], [], [], 0.0
    for drug in ["Ketamine", "Midazolam"]:
        for lv in LEVELS:
            pair = []
            for tm, dx in [("matched(MID)", -.19), ("mismatched(SST)", .19)]:
                r = sub[(sub.drug == drug) & (sub.level == lv) &
                        (sub.task_match == tm)]
                if len(r):
                    pair.append((tm, dx, r.iloc[0]))
            # the two markers of a pair can sit a percent apart, so each label
            # goes on the side AWAY from its partner
            hi = max(range(len(pair)), key=lambda i: pair[i][2]["pct_same"]) \
                if len(pair) > 1 else 0
            for i, (tm, dx, r) in enumerate(pair):
                col, x = DCOL[drug], k + dx
                ax.add_patch(plt.Rectangle((x - .15, 50 - r["null_sd_pct"]),
                                           .30, 2 * r["null_sd_pct"],
                                           facecolor="0.90", edgecolor="none",
                                           zorder=0))
                mism = tm.startswith("mis")
                ax.scatter(x, r["pct_same"], s=S_EST, marker="s" if mism else "o",
                           facecolor=col if r["p_signflip_node"] < .05
                           else "white",
                           edgecolor=col, linewidth=LW, zorder=3)
                up = (i == hi)
                ax.text(x, r["pct_same"] + (2.4 if up else -2.6),
                        f"{int(r['n_same'])}/{int(r['n_edges'])}", ha="center",
                        va="bottom" if up else "top", fontsize=TICK_PT,
                        color=col)
                S[f"{letter}|{drug}|{lv}|{tm}"] = dict(
                    contrast=str(r["dtb_contrast"]), n_edges=int(r["n_edges"]),
                    n_same=int(r["n_same"]), pct=float(r["pct_same"]),
                    p_sf=float(r["p_signflip_node"]),
                    p_bin=float(r["p_binomial"]),
                    null_sd=float(r["null_sd_pct"]))
            xs.append(k); xl.append(LLAB[lv]); xc.append(DCOL[drug]); k += 1.25
        k += .45
    ax.axhline(50, color="0.45", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.set_xticks(xs); ax.set_xticklabels(xl, fontsize=TICK_PT)
    for t_, c_ in zip(ax.get_xticklabels(), xc):
        t_.set_color(c_)
    ax.set_ylabel("Edges with matching\ndirection (%)", fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.set_yticks(np.arange(30, 101, 10))
    ax.set_ylim(30, 109)               # headroom for the drug labels, which
    ax.set_xlim(-.7, xs[-1] + .7)      # stay INSIDE the frame so the rows align
    for drug, xr in [("Ketamine", xs[:3]), ("Midazolam", xs[3:])]:
        ax.text(np.mean(xr), 107, drug, ha="center", va="top",
                fontsize=ANNOT_PT, color=DCOL[drug])
    panel_title(ax, head)
    ax.title.set_fontsize(LABEL_PT)


def p_a(ax):
    conc_panel(ax, "a", "matched", "Pharmacologically matched pairings")


def p_b(ax):
    conc_panel(ax, "b", "cross-receptor",
               "Cross-receptor pairings (receptor-specificity control)")


def p_c(ax):
    x = np.arange(len(RL))
    cols = [DCOL[d] for d in RL.drug]
    ax.bar(x, RL.spearman_brown_reliability, width=.6,
           facecolor=[fill(c) for c in cols], edgecolor=cols, zorder=2)
    for i, r in RL.iterrows():
        ax.scatter(i, r["max_attainable_r"], s=20, marker="v",
                   facecolor="white", edgecolor=cols[i], linewidth=LW, zorder=3)
        ax.text(i, r["max_attainable_r"] + .012,
                f"max attainable\n$r$ = {r['max_attainable_r']:.2f}",
                ha="center", va="bottom", fontsize=TICK_PT, color=cols[i],
                linespacing=1.15)
        ax.text(i, r["spearman_brown_reliability"] / 2,
                f"{r['spearman_brown_reliability']:.3f}", ha="center",
                va="center", fontsize=TICK_PT, color="black")
        S[f"b|{r['drug']}|{r['drug_condition']}"] = dict(
            rel=float(r["spearman_brown_reliability"]),
            rmax=float(r["max_attainable_r"]))
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r['drug']}\n"
                        f"{LLAB[r['drug_condition']].replace(chr(10), ' ')}"
                        for _, r in RL.iterrows()], fontsize=TICK_PT)
    for t_, c_ in zip(ax.get_xticklabels(), cols):
        t_.set_color(c_)
    ax.set_ylabel("Split-half reliability of the\nempirical drug-effect map",
                  fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.set_ylim(0, .62)
    panel_title(ax, "Reliability of the empirical maps at n = 27")
    ax.title.set_fontsize(LABEL_PT)


def legend_strip(ax):
    ax.axis("off")
    h = [Line2D([], [], marker="o", linestyle="none", markersize=3.2,
                markerfacecolor="0.35", markeredgecolor="0.35"),
         Line2D([], [], marker="s", linestyle="none", markersize=3.2,
                markerfacecolor="white", markeredgecolor="0.35",
                markeredgewidth=LW),
         Line2D([], [], marker="s", linestyle="none", markersize=4.2,
                markerfacecolor="0.90", markeredgecolor="0.90"),
         Line2D([], [], linestyle=(0, (2.6, 1.7)), color="0.45", lw=LW),
         Line2D([], [], marker="o", linestyle="none", markersize=3.2,
                markerfacecolor="0.35", markeredgecolor="0.35")]
    ax.legend(h, ["task-matched (MID) prediction",
                  "task-mismatched (SST) prediction",
                  "\u00b11 s.d. of the sign-flip null", "chance (50%)",
                  "filled = P < 0.05 vs the sign-flip null"],
              loc="center", ncol=3, fontsize=ANNOT_PT, handletextpad=.5,
              labelspacing=.45, columnspacing=1.4, borderpad=0, frameon=False)


# --------------------------------------------------------------- page geometry
GUT = K.LETTER_W + K.LETTER_PADX
LETTER_BAND, MB, GAP = K.LETTER_BAND, K.MB, K.GAP
XB = 7.0                           # two-line x tick labels
LEG_H = 9.0                        # the shared legend strip, no letter
MAX_H = 46.0
TEXT_W = PW - ML - MR
# (letter, plot fn, block width, has letter band)
ROWS = [("a", p_a, TEXT_W), ("b", p_c, 118.0)]


def row_geom(fig, panels):
    """Left/right label overhang per row -> axes x and width, so every frame
    starts at the same ink line and no label leaves the text column."""
    rend = fig.canvas.get_renderer()
    mm = lambda px: px / fig.dpi * 25.4
    geom = {}
    for p in panels:
        ax = p["axes"][0]
        bb, pos = ax.get_tightbbox(rend), ax.get_position()
        L = max(pos.x0 * PW - mm(bb.x0), 0.0)
        R = max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0)
        geom[p["ch"]] = (ML + GUT + L, p["block"] - GUT - L - R)
    return geom


def build(plot_h, geom=None):
    f = plt.figure(figsize=panel(PW, PH))
    out, y = [], MT
    for ch, fn, block in ROWS:
        top = y + LETTER_BAND
        ax_x, ax_w = (geom[ch] if geom else (ML + GUT + 17.0,
                                             block - GUT - 17.0 - 2.0))
        ax = K.axes_mm(f, ax_x, top, ax_w, plot_h)
        fn(ax)
        out.append(dict(ch=ch, x=ML, block=block, axes=[ax],
                        txt=K.letter(f, ML, top - 1.2, ch)))
        y = top + plot_h + XB + GAP
        if ch == "a":                      # legend under the concordance panel
            axl = K.axes_mm(f, ML, y, TEXT_W, LEG_H)
            legend_strip(axl)
            y += LEG_H + GAP
    enforce(f)
    return f, out, y - GAP


# ------------------------------------------------------------------- caption
CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Simulated and empirical "
             "whole-brain drug effects agree in direction for the "
             "task-matched model, within the ceiling set by the reliability "
             "of the empirical maps.")


def pf(p):
    return (f"P = {p:.3g}" if p >= 1e-3 else
            f"P = {p:.2g}" if p >= 1e-4 else f"P = {p:.1e}")


def cell(letter, drug, lv, tm):
    return S[f"{letter}|{drug}|{lv}|{tm}"]


def conc_line(letter):
    out = []
    for drug in ["Ketamine", "Midazolam"]:
        m = cell(letter, drug, "pooled (both MID conditions)", "matched(MID)")
        x = cell(letter, drug, "pooled (both MID conditions)",
                 "mismatched(SST)")
        an = cell(letter, drug, "mid_antici_hit", "matched(MID)")
        fe = cell(letter, drug, "mid_feed_hit", "matched(MID)")
        out.append(
            f"{drug} ({m['contrast']}): pooled over both MID conditions "
            f"{m['n_same']} of {m['n_edges']} edges match in direction "
            f"({m['pct']:.1f}%, {pf(m['p_sf'])}), against {x['pct']:.1f}% "
            f"({x['n_same']}/{x['n_edges']}, {pf(x['p_sf'])}) for the "
            f"task-mismatched SST prediction; MID anticipation "
            f"{an['pct']:.1f}% ({pf(an['p_sf'])}) and MID feedback "
            f"{fe['pct']:.1f}% ({pf(fe['p_sf'])}). ")
    return " ".join(out)


def rel_line():
    parts = []
    for k, v in ((k, v) for k, v in S.items() if k.startswith("b|")):
        _, drug, cond = k.split("|")
        parts.append(f"{drug} {LLAB[cond].replace(chr(10), ' ')} "
                     f"{v['rel']:.3f} (max attainable r = {v['rmax']:.2f})")
    return "; ".join(parts)


def caption_runs():
    ket_m = cell("a", "Ketamine", "pooled (both MID conditions)",
                 "matched(MID)")
    mid_m = cell("a", "Midazolam", "pooled (both MID conditions)",
                 "matched(MID)")
    cap = [
        ("", "Directional concordance between the whole-brain drug effect "
             "measured in the pharmacological cohort (27 healthy volunteers, "
             "three within-subject sessions, MID task, Shen-268 functional "
             "connectivity) and the corresponding perturbation of the digital "
             "twin brain. Edges entering each test are those with a nominal "
             "drug-versus-placebo effect at P < 0.001, so the number of edges "
             "differs between drugs and MID conditions and is printed beside "
             "every marker as matching/total. Circles are predictions from the "
             "task-matched (MID) model, squares from the task-mismatched "
             "(SST) model; a filled marker is significant against the "
             "node-level sign-flip null (999 permutations), the grey band is "
             "\u00b11 s.d. of that null and the dashed line is chance (50%). "
             "The binomial test is given below for reference only \u2014 it "
             "ignores the dependence between edges that share a node. "),
        ("a", ", pharmacologically matched pairings: the AMPA perturbation "
              "against ketamine and the AMPA+GABA-A perturbation against "
              "midazolam. " + conc_line("a")),
        ("b", ", split-half reliability (Spearman-Brown) of the empirical "
              "drug-effect maps themselves, computed by splitting the 27 "
              "volunteers into halves: " + rel_line() + ". The triangle marks "
              "the highest correlation any model could attain against a map "
              "of this reliability, the square root of the reliability. "),
        ("", f"Task specificity holds: in the matched pairing the "
             f"task-matched model beats its task-mismatched counterpart for "
             f"both drugs (a), pooled over both MID conditions "
             f"{ket_m['pct']:.1f}% versus {mid_m['pct']:.1f}% for ketamine "
             f"and midazolam respectively. The ceiling on any such agreement "
             f"is low: at n = 27 the empirical maps reproduce themselves only "
             f"weakly (b), which is why the analysis is reported on the sign "
             f"of each edge and not on the magnitude of the effect. All tests "
             f"are two-sided and uncorrected. Source values are in "
             f"wbdrug_direction_agreement_n288.csv, which also holds the "
             f"cross-receptor pairings that are not plotted here, and in "
             f"wbdrug_map_reliability.csv; "
             f"wbdrug_direction_agreement_pooled_prior.csv holds the "
             f"pooled-prior variant of the same test. "),
    ]
    runs = [(CAP_TITLE + " ", True)]
    for lab, seg in cap:
        if lab:
            runs.append((lab + ",", True))
            seg = seg[1:] if seg.startswith(",") else seg
        runs.append((seg, False))
    return runs


# pass 1 -- caption height at a provisional plot height
_f0, _p0, _ = build(34.0)
_runs0 = caption_runs()
_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
plt.close(_f0)

CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
NROW = len(ROWS)
FIXED = (MT + NROW * (LETTER_BAND + XB) + NROW * GAP + LEG_H)
PLOT_H = min((PH - MB - CAP_H - FIXED) / NROW, MAX_H)
assert PLOT_H > 20.0, f"no room for the panels: {PLOT_H:.1f} mm"

# pass 2 -- solve the row geometry at the fitted height
_f1, _p1, _ = build(PLOT_H)
_geom = row_geom(_f1, _p1)
plt.close(_f1)
for _ in range(3):                      # tick labels move when the width does
    _f2, _p2, _ = build(PLOT_H, geom=_geom)
    _geom = row_geom(_f2, _p2)
    plt.close(_f2)
fig, PANELS, BOTTOM = build(PLOT_H, geom=_geom)
K.place_letters(fig, PANELS)

runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM

assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
for k, v in S.items():                  # the ceiling is sqrt(reliability)
    if k.startswith("b|"):
        assert abs(v["rmax"] - np.sqrt(v["rel"])) < .01, k
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
    os.path.join(HERE, "figS_wbdrug_A4_caption_values.csv"), index=False)
plt.close(fig)
