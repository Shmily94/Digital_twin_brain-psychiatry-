"""Supplementary figure | individual fingerprinting of held-out task trials,
all four panels assembled on ONE A4 page (Supplementary Fig. S16).

Follows the same page kit as the other assembled supplementary figures
(figA4_kit: 8 / 9 / 10 / 11 pt type, measured letter placement, word-wrapped
caption, native-text pptx export).

Panels
  a  pattern correlation of every held-out trial with all four templates,
     empirical BOLD
  b  the same from the digital twins run forward WITHOUT re-assimilation
  c  identification margin per trial (self - best other r), empirical vs twins
  d  identification accuracy against the 25% chance level of a four-way choice

Design: four participants (HC03, HC04, AUD02, MDD02) x 6 held-out emotional-face
trials = 24 trials.  Hyperparameters were fitted on the first half of the task;
the second half is held out, so the comparison tests generalisation, not fit.

    cd revision/text/figures/supp_fingerprint && python figS_finger_A4.py [--no-caption]

Inputs : data/fingerprint_similarity_{empirical,simulated}.csv, data/fingerprint_margins.csv
Outputs: figS_finger_A4.{png,pdf,pptx}, figS_finger_A4_caption_values.csv
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import stats

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_fingerprint")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, C, LW, enforce          # noqa: E402
from supp_kit import fill, pt_edge                               # noqa: E402
from fig_export import collect_text_records                      # noqa: E402
import figA4_kit as K                                            # noqa: E402
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, PW, PH, ML, MR, MT  # noqa: E402

DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_finger_A4" if WITH_CAP else "figS_finger_A4_nocaption"
apply_np_style()
K.apply_page_style()

ME = pd.read_csv(os.path.join(HERE, "data", "fingerprint_similarity_empirical.csv"), index_col=0)
MS = pd.read_csv(os.path.join(HERE, "data", "fingerprint_similarity_simulated.csv"), index_col=0)
MG = pd.read_csv(os.path.join(HERE, "data", "fingerprint_margins.csv"))

# de-identified display labels: participants appear as sub1-sub4, never by the
# acquisition ID, and the two held-out repeats of each condition as 1 and 2
ANON = {"HC03": "sub1", "HC04": "sub2", "AUD02": "sub3", "MDD02": "sub4"}


def relabel(t):
    sub, cond, trial = t.split("_")
    return f"{ANON[sub]} {cond} {'1' if trial.endswith('3') else '2'}"


ME.index = [relabel(t) for t in ME.index]; ME.columns = [ANON[c] for c in ME.columns]
MS.index = [relabel(t) for t in MS.index]; MS.columns = [ANON[c] for c in MS.columns]
MG["trial"] = [relabel(t) for t in MG.trial]
MG["subject"] = [ANON[s] for s in MG.subject]
VMAX = float(max(np.abs(ME.values).max(), np.abs(MS.values).max()))
S = {}                                    # every number quoted in the caption


def identify(M):
    truth = [" ".join(t.split(" ")[:-2]) for t in M.index]
    pick = [M.columns[k] for k in np.argmax(M.values, axis=1)]
    ok = [t == p for t, p in zip(truth, pick)]
    return sum(ok), len(ok), [i for i, o in zip(M.index, ok) if not o]


nE, nT, missE = identify(ME)
nS, _, missS = identify(MS)
mE = (MG.self_r_empirical - MG.best_other_r_empirical).values
mS = (MG.self_r_simulated - MG.best_other_r_simulated).values
tM, pM = stats.ttest_rel(mS, mE)
wM = stats.wilcoxon(mS, mE)
tE, pE = stats.ttest_rel(MG.self_r_empirical, MG.best_other_r_empirical)
tS, pS = stats.ttest_rel(MG.self_r_simulated, MG.best_other_r_simulated)
bE = stats.binomtest(nE, nT, 0.25, alternative="greater").pvalue
bS = stats.binomtest(nS, nT, 0.25, alternative="greater").pvalue
S.update(n_trials=nT, n_subjects=MG.subject.nunique(), chance_pct=25.0,
         emp_correct=nE, emp_pct=100 * nE / nT, emp_missed="; ".join(missE) or "none",
         sim_correct=nS, sim_pct=100 * nS / nT, sim_missed="; ".join(missS) or "none",
         emp_self_r=MG.self_r_empirical.mean(), emp_other_r=MG.best_other_r_empirical.mean(),
         emp_margin=mE.mean(), emp_margin_sd=mE.std(ddof=1),
         sim_self_r=MG.self_r_simulated.mean(), sim_other_r=MG.best_other_r_simulated.mean(),
         sim_margin=mS.mean(), sim_margin_sd=mS.std(ddof=1),
         emp_self_vs_other_t=tE, emp_self_vs_other_p=pE,
         sim_self_vs_other_t=tS, sim_self_vs_other_p=pS,
         margin_sim_minus_emp=(mS - mE).mean(), margin_t=tM, margin_p=pM,
         margin_wilcoxon_p=wM.pvalue, emp_binomial_p=bE, sim_binomial_p=bS,
         vmax=VMAX)

# ------------------------------------------------------------------ layout ---
ROW1_TOP, ROW1_H = MT + K.LETTER_BAND, 104.0
ROW2_H = 56.0
LBLW = 23.0                      # row-label column of panel a
LETTER_OUT = 5.0                 # panel letters sit this far left of the column ink
ROW_EXTRA = 7.0                  # added to the kit's row gap for this figure
GAP_AB = 9.0                     # visible separation between the two heatmaps
COLW1, COLW2 = 60.0, 60.0
X_A, X_B = ML + LBLW + LETTER_OUT, ML + LBLW + LETTER_OUT + COLW1 + GAP_AB
COLW3 = 52.0                     # narrower than the heatmaps; c and d are then
X_C, X_D = ML, ML + 70.0         # shifted so their ink aligns with a and b
fig = K.page()
ax_a = K.axes_mm(fig, X_A, ROW1_TOP, COLW1, ROW1_H)
ax_b = K.axes_mm(fig, X_B, ROW1_TOP, COLW2, ROW1_H)


def _ink_x(ax):
    """(leftmost, rightmost) drawn ink of one panel, in mm from the page left"""
    fig.canvas.draw()
    rnd = fig.canvas.get_renderer()
    bb = ax.get_tightbbox(rnd)
    xs, xe = [bb.x0], [bb.x1]
    for t in ax.texts:
        if t.get_text().strip():
            e = t.get_window_extent(rnd); xs.append(e.x0); xe.append(e.x1)
    k = 25.4 / fig.dpi
    return min(xs) * k, max(xe) * k


def shift_x_mm(ax, dx_mm):
    p = ax.get_position()
    ax.set_position([p.x0 + dx_mm / PW, p.y0, p.width, p.height])


def ink_bottom_mm(axes):
    """lowest drawn ink of a row, in mm from the page top (ticks and labels included)"""
    fig.canvas.draw()
    rnd = fig.canvas.get_renderer()
    ys = []
    for ax in axes:
        ys.append(ax.get_tightbbox(rnd).y0)
        for t in ax.texts:
            if t.get_text().strip():
                ys.append(t.get_window_extent(rnd).y0)
    return PH - min(ys) / fig.dpi * 25.4


def heat(ax, Mx, ytick, head):
    im = ax.imshow(Mx.values, cmap="RdBu_r", vmin=-VMAX, vmax=VMAX, aspect="auto")
    truth = [" ".join(t.split(" ")[:-2]) for t in Mx.index]
    for i, t in enumerate(truth):
        j = list(Mx.columns).index(t)
        ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, fill=False, edgecolor="black",
                               lw=LW * 1.3, zorder=4))
        k = int(np.argmax(Mx.values[i]))
        if k != j:
            ax.add_patch(Rectangle((k - .5, i - .5), 1, 1, fill=False,
                                   edgecolor=C("patient"), lw=LW * 1.7, zorder=5))
    ax.set_xticks(range(Mx.shape[1]))
    ax.set_xticklabels(Mx.columns, fontsize=TICK_PT, rotation=90)
    ax.set_yticks(range(Mx.shape[0]))
    ax.set_yticklabels([])
    if ytick:                       # row labels flush left, off the axes
        for i, lab in enumerate(Mx.index):
            ax.text(-0.335, i, lab, transform=ax.get_yaxis_transform(), ha="left",
                    va="center", fontsize=TICK_PT, clip_on=False)
    ax.set_xlabel("Participant template", fontsize=LABEL_PT)
    ax.tick_params(axis="both", labelsize=TICK_PT)
    ax.set_title(head, fontsize=ANNOT_PT, loc="left", pad=4)
    return im


im_a = heat(ax_a, ME, True, f"Empirical BOLD\n{nE}/{nT} correct = {100 * nE / nT:.1f}%")
GRP = [" ".join(t.split(" ")[:-2]) for t in ME.index]                 # 6 held-out trials per participant
for g in list(dict.fromkeys(GRP))[1:]:                    # hairline between participants
    i0 = min(i for i, t in enumerate(GRP) if t == g)
    for axx in (ax_a, ax_b):
        axx.axhline(i0 - .5, color="white", lw=LW * 1.8, zorder=6)
im_b = heat(ax_b, MS, False,
            f"Digital twins, no re-assimilation\n{nS}/{nT} correct = {100 * nS / nT:.1f}%")
cax = K.axes_mm(fig, X_B + COLW2 + 2.5, ROW1_TOP + ROW1_H * .28, 3.0, ROW1_H * .44)
cb = fig.colorbar(im_b, cax=cax)
cb.set_label("Pattern correlation", fontsize=ANNOT_PT)
cb.ax.tick_params(labelsize=TICK_PT, length=2, width=LW)
cb.outline.set_linewidth(LW)

ROW2_TOP = ink_bottom_mm([ax_a, ax_b, cax]) + K.GAP + K.LETTER_BAND + ROW_EXTRA
ax_c = K.axes_mm(fig, X_C, ROW2_TOP, COLW3, ROW2_H)
ax_d = K.axes_mm(fig, X_D, ROW2_TOP, COLW3, ROW2_H)
COL_INK = (_ink_x(ax_a)[0], _ink_x(ax_b)[0])      # the two column ink boundaries

# ---- c  identification margin ----------------------------------------------
rng = np.random.default_rng(0)
for i, (v, col) in enumerate([(mE, C("reference")), (mS, C("np12"))]):
    bp = ax_c.boxplot([v], positions=[i], widths=.55, showfliers=False, patch_artist=True)
    for el in ("boxes", "whiskers", "caps", "medians"):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color("black")
    bp["boxes"][0].set_facecolor(fill(col)); bp["boxes"][0].set_edgecolor("black")
    ax_c.scatter(i + rng.uniform(-.14, .14, len(v)), v, s=13, facecolor=col,
                 edgecolor=pt_edge(col), linewidth=LW * .55, alpha=.9, zorder=3)
ax_c.axhline(0, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
hi, lo = max(mE.max(), mS.max()), min(mE.min(), mS.min()); span = hi - lo
ax_c.plot([0, 0, 1, 1], [hi + span * .07, hi + span * .12, hi + span * .12,
                         hi + span * .07], color="black", lw=LW)
STAR = "*" if pM < .05 else "n.s."                   # value is given in the caption
ax_c.text(.5, hi + span * .125, STAR, ha="center", va="bottom",
          fontsize=ANNOT_PT + (2 if STAR == "*" else 0))
ax_c.set_ylim(lo - span * .12, hi + span * .34)
ax_c.set_xticks([0, 1]); ax_c.set_xticklabels(["Empirical", "Twins"], fontsize=TICK_PT)
ax_c.set_xlim(-.65, 1.65)
ax_c.set_ylabel("Identification margin\n(self \u2212 best other $r$)", fontsize=LABEL_PT)
ax_c.tick_params(axis="both", labelsize=TICK_PT)

# ---- d  accuracy against chance --------------------------------------------
acc = [100 * nE / nT, 100 * nS / nT]
for i, (v, col) in enumerate(zip(acc, [C("reference"), C("np12")])):
    ax_d.bar(i, v, width=.55, facecolor=fill(col), edgecolor="black", lw=LW, zorder=3)
    ax_d.text(i, v + 2.2, f"{v:.1f}%", ha="center", va="bottom", fontsize=ANNOT_PT)
ax_d.axhline(25.0, color=C("patient"), lw=LW * 1.3, ls=(0, (2.6, 1.7)), zorder=2)
ax_d.text(.5, 27.0, "chance, 25%", ha="center", va="bottom", fontsize=ANNOT_PT,
          color=C("patient"))
ax_d.set_xticks([0, 1]); ax_d.set_xticklabels(["Empirical", "Twins"], fontsize=TICK_PT)
ax_d.set_xlim(-.65, 1.65); ax_d.set_ylim(0, 116)
ax_d.set_yticks([0, 25, 50, 75, 100])
ax_d.set_ylabel("Identification accuracy (%)", fontsize=LABEL_PT)
ax_d.tick_params(axis="both", labelsize=TICK_PT)
ax_d.set_title(f"exact binomial vs chance\n$P$ = {bE:.2g} and {bS:.2g}",
               fontsize=ANNOT_PT, color="0.35", loc="left", pad=4)

# ---- align the lower row on the two column boundaries measured above --------
for ax, target in ((ax_c, COL_INK[0]), (ax_d, COL_INK[1])):
    shift_x_mm(ax, target - _ink_x(ax)[0])
assert _ink_x(ax_c)[1] + 2.0 <= _ink_x(ax_d)[0], \
    f"c and d overlap: {_ink_x(ax_c)[1]:.1f} vs {_ink_x(ax_d)[0]:.1f} mm"

# ------------------------------------------------------------------ letters --
LX = (COL_INK[0] - LETTER_OUT, COL_INK[1] - LETTER_OUT)
PANELS = [dict(ch="a", x=LX[0], axes=[ax_a], txt=K.letter(fig, LX[0], ROW1_TOP, "a")),
          dict(ch="b", x=LX[1], axes=[ax_b], txt=K.letter(fig, LX[1], ROW1_TOP, "b")),
          dict(ch="c", x=LX[0], axes=[ax_c], txt=K.letter(fig, LX[0], ROW2_TOP, "c")),
          dict(ch="d", x=LX[1], axes=[ax_d], txt=K.letter(fig, LX[1], ROW2_TOP, "d"))]
enforce(fig)
K.place_letters(fig, PANELS, rows=[["a", "b"], ["c", "d"]])
BOTTOM = ink_bottom_mm([ax_c, ax_d]) + 1.5


def caption_runs():
    def R(s, bold=False):
        return [(w, bold) for w in s.split(" ")]
    r = []
    r += R("Supplementary Fig. S16 |", True)
    r += R("Digital twin brains preserve participant-specific signatures on held-out "
           f"trials without re-assimilation. Four participants (sub1 and sub2, healthy "
           f"controls; sub3, alcohol use disorder; sub4, major depressive disorder) x 6 "
           f"held-out emotional-face trials (n = {nT} trials; unit of observation, one "
           "held-out trial; the labels sub1-sub4 are local to this figure). Hyperparameters "
           "were estimated from the first half of the task "
           "and the second half was simulated forward without re-assimilation, so every "
           "panel tests generalisation rather than fit.")
    r += R(" a,", True)
    r += R("Pearson correlation between each held-out trial's activation pattern and each "
           f"participant's template, from empirical BOLD; colour scale symmetric at "
           f"+/-{VMAX:.2f}, black outline marks the correct template and an orange outline "
           "the template actually selected when identification failed; no error indicator "
           "and no inferential test (descriptive similarity matrix).")
    r += R(" b,", True)
    r += R("The same matrix from the digital twins.")
    r += R(" c,", True)
    r += R("Identification margin per trial (self minus best-other correlation); boxes show "
           "the median and interquartile range with whiskers at 1.5x IQR and every trial "
           "plotted; empirical "
           f"{mE.mean():.4f} +/- {mE.std(ddof=1):.4f} versus twins {mS.mean():.4f} +/- "
           f"{mS.std(ddof=1):.4f}, two-sided paired t test, t(23) = {tM:.3f}, "
           f"*P = {pM:.4g} (the asterisk in the panel marks this test; "
           f"Wilcoxon signed-rank P = {wM.pvalue:.4g}), no multiple-comparison correction "
           "(one pre-specified contrast). Within each data type the self correlation exceeds "
           f"the best other correlation: empirical {MG.self_r_empirical.mean():.4f} versus "
           f"{MG.best_other_r_empirical.mean():.4f}, t(23) = {tE:.3f}, P = {pE:.3g}; twins "
           f"{MG.self_r_simulated.mean():.4f} versus {MG.best_other_r_simulated.mean():.4f}, "
           f"t(23) = {tS:.3f}, P = {pS:.3g}.")
    r += R(" d,", True)
    r += R(f"Identification accuracy against the 25% chance level of a four-way choice; bars "
           "show the percentage of trials identified correctly, with no error bar because "
           f"the quantity is a count over all {nT} trials: empirical {nE}/{nT} = "
           f"{100 * nE / nT:.1f}% (the single failure is a happy trial of sub3, assigned to "
           f"the sub1 template) and twins {nS}/{nT} "
           f"= {100 * nS / nT:.1f}%; one-sided exact binomial test against 0.25, "
           f"P = {bE:.3g} and P = {bS:.3g}.")
    return r


runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"

png, pdf, ppt = (os.path.join(HERE, STEM + e) for e in (".png", ".pdf", ".pptx"))
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")
K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
              collect_text_records=collect_text_records)
pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
    os.path.join(HERE, "figS_finger_A4_caption_values.csv"), index=False)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
print(f"[{STEM}] panels end at {BOTTOM:.1f} mm, caption {n_lines} lines -> "
      f"{CAP_BOTTOM:.1f} of {PH:.0f} mm | non-Arial: {bad[:3]}")
print(f"empirical {nE}/{nT} ({100 * nE / nT:.1f}%), twins {nS}/{nT} "
      f"({100 * nS / nT:.1f}%); margin t(23) = {tM:.3f}, P = {pM:.4g}")
plt.close(fig)
