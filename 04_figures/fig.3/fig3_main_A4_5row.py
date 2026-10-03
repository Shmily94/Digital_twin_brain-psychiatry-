"""Figure 3, assembled as ONE Nature-Medicine main figure on an A4 page.

Panel order requested by the author: fig3i, fig3b, fig3a, fig3d, fig3e, fig3f,
fig3g  ->  re-lettered a-g in that reading order.  Declarative panel titles are
dropped; the legend is set below the panels.  Type sizes are the manuscript's
own three-size scheme (8 pt axis labels, 7 pt annotation/legend, 6 pt ticks),
identical in every panel.

Outputs (all at 400 dpi / vector):
  fig3_main_A4.png   fig3_main_A4.pdf   fig3_main_A4.pptx (editable text layer)

    python fig3_main_A4.py
"""
import os, sys, textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "fig.3")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, enforce)
from fig_export import collect_text_records
sys.path.insert(0, FIGDIR)
import figA4_kit as K              # frozen internal-distribution rules

D = os.path.join(HERE, "fig3_data")
DPI = 400
WITH_CAP = "--no-caption" not in sys.argv        # python fig3_main_A4.py --no-caption
STEM = "fig3_main_A4" if WITH_CAP else "fig3_main_A4_nocaption"
apply_np_style()
matplotlib.rcParams["savefig.bbox"] = None          # keep the A4 canvas exact

# Legibility pass: the manuscript's 6/7/8 pt scheme raised two steps to 8/9/10 pt
# (panel letters 11 pt bold, caption 8 pt), keeping ONE size per role.
TICK_PT, ANNOT_PT, LABEL_PT = 8, 9, 10
LETTER_PT, CAP_PT = 11, 8
matplotlib.rcParams.update({
    'axes.labelsize': LABEL_PT, 'axes.titlesize': LABEL_PT,
    'xtick.labelsize': TICK_PT, 'ytick.labelsize': TICK_PT,
    'legend.fontsize': ANNOT_PT, 'font.size': ANNOT_PT,
})
CUR_W, CUR_ROWLAB = 180.0, True      # set by the layout loop before each panel

# ----------------------------------------------------------------- shared keys
BUILDS7 = ['3m_268', '10m_268', '10m_1000', '10m_own', '10m', '100m', '1b']
BENCH = ['SAR', 'RWW']
BLAB = {'3m_268': '3 M\n268', '10m_268': '10 M\n268', '10m_1000': '10 M\n1000',
        '10m_own': '10 M\nvoxel', '10m': '10 M\nvoxel', '100m': '100 M\nvoxel',
        '1b': '1 B\nvoxel', 'SAR': 'SAR', 'RWW': 'rWW'}
BHYP = {'3m_268': '3 M', '10m_268': '3 M', '10m_1000': '10 M\n1000',
        '10m_own': '10 M\nvoxel', '10m': '100 M', '100m': '100 M', '1b': '100 M',
        'SAR': '', 'RWW': ''}
BFAM = {**{k: 'regional' for k in ('3m_268', '10m_268', '10m_1000')},
        **{k: 'voxel' for k in ('10m_own', '10m', '100m', '1b')},
        'SAR': 'benchmark', 'RWW': 'benchmark'}
WBKEY = {'10m': '10m_voxel', '100m': '100m_voxel', '1b': '1b_voxel'}
FAM = {'regional': C('model_regional'), 'voxel': C('model_voxel'),
       'benchmark': C('hc')}
DRUG = {'ampa': C('ampa'), 'gaba': C('gaba')}
DRUG_LAB = {'ampa': 'AMPA', 'gaba': 'GABA-A'}
SUBJ_MK = {'HC01': 'o', 'MDD': 's', 'AUD': '^'}
SUBJ_LS = {'HC01': (0, (2.6, 1.7)), 'MDD': '-', 'AUD': '-'}
SUBJ_OPEN = {'HC01': True, 'MDD': False, 'AUD': False}
COND = ['SST Stop Success', 'SST Stop Failure', 'MID Reward Antici.', 'MID Pos. Feedback']
CMK = {'SST Stop Success': 'o', 'SST Stop Failure': 's',
       'MID Reward Antici.': '^', 'MID Pos. Feedback': 'D'}

a3 = pd.read_csv(f'{D}/fig3a_mse_per_subject.csv')
wb = pd.read_csv(f'{D}/fig3b_wholebrain_fc_crossscale.csv')
c3 = pd.read_csv(f'{D}/fig3d_run_to_run_sd.csv')
d3 = pd.read_csv(f'{D}/fig3e_ampa_sweep.csv')
e3 = pd.read_csv(f'{D}/fig3f_gaba_sweep.csv')
gg = pd.read_csv(f'{D}/fig3g_delta_np_seven_models.csv')
bi = pd.read_csv(f'{D}/fig3i_assimilated_bold_r.csv')


def hyper_row(ax, keys, y):
    tr = ax.get_xaxis_transform()
    if CUR_ROWLAB:
        # x in AXES fractions (tr blends data-x with axes-y, so it cannot be
        # used here): -LAB_L/(CUR_W-LAB_L) is exactly the panel's left edge.
        ax.text(-LAB_L / (CUR_W - LAB_L), y, 'assimilated\nhyper-parameters',
                transform=ax.transAxes, ha='left', va='top', fontsize=TICK_PT,
                color='0.35', clip_on=False)
    for i, k in enumerate(keys):
        if BHYP[k]:
            ax.text(i, y, BHYP[k], transform=tr, ha='center', va='top',
                    fontsize=ANNOT_PT, color='0.35', clip_on=False)


def block_bands(ax, keys, y, n_bench=0):
    n_reg = sum(1 for k in keys if BFAM[k] == 'regional')
    n_dtb = sum(1 for k in keys if BFAM[k] != 'benchmark')
    ax.axvline(n_reg - .5, color='0.85', lw=LW, zorder=0)
    if n_bench:
        ax.axvline(n_dtb - .5, color='0.85', lw=LW, zorder=0)
    ax.text((n_reg - 1) / 2, y, 'regional models', ha='center', fontsize=ANNOT_PT,
            color=FAM['regional'])
    ax.text((n_reg + n_dtb - 1) / 2, y, 'voxel models', ha='center',
            fontsize=ANNOT_PT, color=FAM['voxel'])
    if n_bench:
        ax.text(n_dtb + (n_bench - 1) / 2, y, 'benchmarks', ha='center',
                fontsize=ANNOT_PT, color='0.35')


def box_strip(ax, values, colour, width=.52, jitter=.13, seed=0):
    rng = np.random.default_rng(seed)
    bp = ax.boxplot(values, positions=np.arange(len(values)), widths=width,
                    showfliers=False, patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    for i, v in enumerate(values):
        ax.scatter(i + rng.uniform(-jitter, jitter, len(v)), v, s=4.5,
                   facecolor=colour[i], edgecolor='none', alpha=.8, zorder=3)


def build_ticks(ax, keys, hyp_y):
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels([BLAB[k] for k in keys], fontsize=TICK_PT)
    for t, k in zip(ax.get_xticklabels(), keys):
        t.set_color(FAM[BFAM[k]] if BFAM[k] != 'benchmark' else '0.35')
    hyper_row(ax, keys, hyp_y)


# ------------------------------------------------------------------- panels a-g
def panel_a(ax):                       # was fig3i - assimilated-region BOLD r
    MK = {'MID': 'o', 'SST': 's'}
    rng = np.random.default_rng(5)
    for i, m in enumerate(BUILDS7):
        col = FAM[BFAM[m]]
        sub = bi[bi.model == m]
        for tk in ('MID', 'SST'):
            v = sub[sub.task == tk].bold_r.values
            dx = -.16 if tk == 'MID' else .16
            ax.scatter(i + dx + rng.uniform(-.05, .05, len(v)), v, s=9, marker=MK[tk],
                       facecolor='white', edgecolor=col, linewidth=LW, zorder=3)
            ax.hlines(v.mean(), i + dx - .13, i + dx + .13, color=col,
                      lw=LW * 1.6, zorder=4)
    ax.set_ylabel('Assimilated-region\nBOLD $r$')
    ax.set_ylim(.55, 1.0)
    ax.set_yticks([.6, .7, .8, .9, 1.0])
    build_ticks(ax, BUILDS7, HYP_Y)
    block_bands(ax, BUILDS7, .965)
    hM = [Line2D([], [], marker=MK[t], linestyle='none', markersize=3,
                 markerfacecolor='white', markeredgecolor='0.35', markeredgewidth=LW)
          for t in ('MID', 'SST')]
    ax.legend(hM, ['MID', 'SST'], loc='lower center', bbox_to_anchor=(.5, 1.0),
              ncol=2, fontsize=ANNOT_PT, handletextpad=.3, columnspacing=1.2,
              borderpad=0, frameon=False)


def panel_b(ax):                       # was fig3b - whole-brain FC similarity
    WBM = [WBKEY.get(m, m) for m in BUILDS7] + BENCH
    WKEY = BUILDS7 + BENCH
    xw = np.arange(len(WBM))
    dx = np.linspace(-.20, .20, len(COND))
    for k, cond in enumerate(COND):
        sub = wb[wb.condition == cond].set_index('model').loc[WBM]
        for i, m in enumerate(WBM):
            col = FAM[BFAM[WKEY[i]]]
            ax.errorbar(xw[i] + dx[k], sub.r_mean.iloc[i], yerr=sub.r_sd.iloc[i],
                        fmt=CMK[cond], color=col, markersize=2.6, lw=0,
                        elinewidth=LW, capsize=1.6, capthick=LW,
                        markerfacecolor='white', markeredgecolor=col,
                        markeredgewidth=LW, zorder=3)
    ax.set_ylabel('Whole-brain FC\nsimilarity ($r$)')
    ax.set_ylim(0, .82)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    build_ticks(ax, WKEY, HYP_Y)
    block_bands(ax, WKEY, .78, n_bench=len(BENCH))


def panel_c(ax):                       # was fig3a - simulation error
    AMOD = BUILDS7 + BENCH
    vals = [a3.loc[a3.model == m, 'mse'].values for m in AMOD]
    box_strip(ax, vals, [FAM[BFAM[m]] for m in AMOD])
    top = max(a3.mse) * 1.30
    ax.set_ylabel('Simulation error\n(MSE)')
    ax.set_ylim(0, top)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    build_ticks(ax, AMOD, HYP_Y)
    block_bands(ax, AMOD, top * .90, n_bench=len(BENCH))


def panel_d(ax):                       # was fig3d - run-to-run variability
    BUILDS_REP = [m for m in BUILDS7 if m != '10m_own']
    c = c3.set_index('model').loc[BUILDS_REP].reset_index()
    x = np.arange(len(c))
    dcol = [FAM[BFAM[m]] for m in c.model]
    ax.bar(x, c.run_sd_mean.fillna(0), width=.58,
           facecolor=[(*matplotlib.colors.to_rgb(k), .35) for k in dcol],
           edgecolor=dcol, linewidth=LW, zorder=2)
    for xi, m, sd, col in zip(x, c.run_sd_mean, c.run_sd_sd, dcol):
        if np.isfinite(m):
            ax.errorbar(xi, m, yerr=sd, fmt='none', ecolor=col, elinewidth=LW,
                        capsize=1.8, capthick=LW, zorder=3)
    top = float((c.run_sd_mean + c.run_sd_sd).max()) * 1.22
    ax.set_ylabel('Run-to-run s.d.\nof summed NP')
    ax.set_ylim(0, top)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    build_ticks(ax, list(c.model), HYP_Y)
    block_bands(ax, list(c.model), top * .93)


def _sweep(ax, df_, xlab, dkey):
    levels = list(df_.columns[1:])
    xs = np.arange(len(levels))
    ylo, yhi = -2.0, 2.0
    for _, row in df_.iterrows():
        s = row['subject']
        ax.plot(xs, row[levels].astype(float).values, color=DRUG[dkey],
                marker=SUBJ_MK[s], markersize=2.8, lw=LW, ls=SUBJ_LS[s],
                markerfacecolor='white' if SUBJ_OPEN[s] else DRUG[dkey],
                markeredgecolor=DRUG[dkey], markeredgewidth=LW,
                label=s, clip_on=False, zorder=3)
    ax.set_xticks(xs)
    ax.set_xticklabels(['baseline'] + [f'{float(v):g}' for v in levels[1:]],
                       rotation=90, ha='center', va='top', fontsize=TICK_PT)
    ax.set_xlabel(xlab); ax.set_ylabel('NP factor')
    ax.set_xlim(-.4, len(levels) - .6)
    ax.set_ylim(ylo, yhi)
    ax.set_yticks(np.arange(ylo, yhi + .01, 1.0))
    ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.0), ncol=3,
              fontsize=ANNOT_PT, handletextpad=.4, columnspacing=1.0,
              borderpad=0, frameon=False)


def panel_e(ax):
    _sweep(ax, d3, 'AMPA conductance', 'ampa')


def panel_f(ax):
    _sweep(ax, e3, 'GABA-A conductance', 'gaba')


def panel_g(ax):                       # was fig3g - delta NP across builds
    rng = np.random.default_rng(2)
    off = {'ampa': -.18, 'gaba': .18}
    for drug in ['ampa', 'gaba']:
        for i, m_ in enumerate(BUILDS7):
            v = gg[(gg.drug == drug) & (gg.model == m_)].delta.values
            ax.scatter(i + off[drug] + rng.uniform(-.06, .06, len(v)), v, s=13,
                       facecolor=DRUG[drug], edgecolor='none', alpha=.85, zorder=3)
            ax.hlines(v.mean(), i + off[drug] - .13, i + off[drug] + .13,
                      color='black', lw=LW, zorder=4)
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.set_ylabel('$\\Delta$ NP (perturbed\n$-$ baseline)')
    ax.set_xlim(-.55, len(BUILDS7) - .45)
    ymax = float(gg.delta.max())
    ax.set_ylim(float(gg.delta.min()) - .3, ymax * 1.28)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    build_ticks(ax, BUILDS7, HYP_Y)
    block_bands(ax, BUILDS7, ymax * 1.12)
    handles = [Line2D([], [], marker='o', linestyle='none', markersize=4,
                      markerfacecolor=DRUG[d], markeredgecolor='none')
               for d in ['ampa', 'gaba']]
    ax.legend(handles, [DRUG_LAB[d] for d in ['ampa', 'gaba']], loc='lower center',
              bbox_to_anchor=(.5, 1.0), ncol=2, fontsize=ANNOT_PT,
              handletextpad=.4, columnspacing=1.2, borderpad=0, frameon=False)


# --------------------------------------------------------------- page geometry
# Internal distribution is the frozen kit ruleset (figA4_kit): 6 mm letter band,
# 6 mm between rows, letters seated 0.9 mm above / 1.0 mm left of their OWN
# panel's measured content.  The axes height is then solved so the page is
# filled exactly and never overrun.
PW, PH = K.PW, K.PH
ML, MR, MT, MB = K.ML, K.MR, K.MT, K.MB
LAB_L = 18.0                       # width reserved for y label + y ticks
XBLOCK = 16.5                      # space under the axes for the two tick rows
XBLOCK_SWEEP = 17.5                # vertical ticks + x label
LETTER_BAND, LETTER_PAD, LETTER_PADX = K.LETTER_BAND, K.LETTER_PAD, K.LETTER_PADX
GAP = K.GAP
HYP_MM = 7.6                       # hyper-parameter row, mm below the axes
HYP_Y = -HYP_MM / 22.0             # rescaled once PLOT_H is solved

ROWS = [[("a", panel_a, ML, PW - ML - MR, XBLOCK)],
        [("b", panel_b, ML, PW - ML - MR, XBLOCK)],
        [("c", panel_c, ML, PW - ML - MR, XBLOCK)],
        [("d", panel_d, ML, 100.0, XBLOCK),
         ("e", panel_e, ML + 108.0, 72.0, XBLOCK_SWEEP)],
        [("f", panel_f, ML, 72.0, XBLOCK_SWEEP),
         ("g", panel_g, ML + 80.0, 100.0, XBLOCK)]]
NROW = len(ROWS)
XB_SUM = sum(max(r[4] for r in row) for row in ROWS)


def build(plot_h, shift=None):
    """Lay the rows out at axes height `plot_h`; `shift` pushes single panels
    down by mm so the CONTENT tops within a row sit on one line."""
    global CUR_W, CUR_ROWLAB
    shift = shift or {}
    f = plt.figure(figsize=panel(PW, PH))
    out, y = [], MT
    for row in ROWS:
        top = y + LETTER_BAND
        for ch, fn, x_mm, w_mm, xblock in row:
            ax = f.add_axes([(x_mm + LAB_L) / PW,
                             1 - (top + shift.get(ch, 0.0) + plot_h) / PH,
                             (w_mm - LAB_L) / PW, plot_h / PH])
            CUR_W, CUR_ROWLAB = w_mm, ch in ("a", "b", "c")
            fn(ax)
            out.append(dict(ch=ch, x=x_mm, axes=[ax],
                            txt=K.letter(f, x_mm, top - 1.2, ch)))
        y = (top + max(shift.get(r[0], 0.0) for r in row) + plot_h
             + max(r[4] for r in row) + GAP)
    enforce(f)
    return f, out, y - GAP


# ------------------------------------------------------------------- caption
CAP_TITLE = "Fig. 3 | Multiscale validation of the digital twin brain."
CAP = [
    ("", "Seven DTB builds are compared throughout; they differ in the number of simulated "
         "neurons, the neuron count of the assimilated hyper-parameter set and the spatial "
         "resolution of the simulation target, so every panel carries a second tick row naming "
         "the hyper-parameter set (the two 10 M voxel builds are identical on the other two "
         "axes). Colour encodes model family (regional versus voxel) only; benchmarks (SAR, rWW) "
         "are grey. "),
    ("a", ", Pearson correlation between simulated and measured BOLD within the assimilated "
          "regions (MID, 51 Shen labels; SST, 47), averaged over assimilated voxels; one subject "
          "× task session, 24 points per build, bar, group mean; two-sided paired t tests, "
          "n = 24, uncorrected. "),
    ("b", ", whole-brain FC similarity, mean ± s.d. across the 12 twins of the correlation "
          "between simulated and measured FC (23,436 edges among 217 nodes), per task condition "
          "(marker shape); n = 12 per point; descriptive. "),
    ("c", ", simulation error of the 12-edge NP profile against one empirical reference (FC "
          "recomputed from the simulated voxels); median, 25th–75th percentiles, 1.5 × IQR "
          "whiskers, all 12 twins overplotted; paired t tests, df = 11, uncorrected. Benchmarks "
          "are scored against the Shen-268 task FC their coupling was fitted to and are not on "
          "the DTB scale. "),
    ("d", ", run-to-run variability: mean across twins of the within-subject s.d. of summed NP "
          "over 5 repeats; error bars, s.d. across twins; the single-run 10 M voxel "
          "own-hyper-parameter build is omitted; descriptive. "),
    ("e, f", ", NP factor versus AMPA (e; 9 settings, 0.0020–0.0052) and GABA-A (f; 5 settings, "
             "0.0020–0.0040) conductance in three twins (HC01, MDD, AUD), each twin's own "
             "baseline marked; descriptive only, no test at n = 3. "),
    ("g", ", change in summed NP after AMPA and after GABA-A perturbation in all seven builds; "
          "points, twins; bar, group mean; n = 12 per build × perturbation; two-sided one-sample "
          "t tests against zero, df = 11, Benjamini–Hochberg FDR across the 14 tests. Only the "
          "two 268-region builds survive correction, and only under GABA-A; GABA-A is applied on "
          "top of AMPA."),
]


def rich_lines(fig, runs, width_mm, size_pt, renderer):
    """Greedy word wrap over (text, bold) runs; returns lines of placed segments."""
    words = []
    for txt, bold in runs:
        for w in txt.split(" "):
            if w:
                words.append((w, bold))
    def wpx(s, bold):
        t = fig.text(0, 0, s, fontsize=size_pt,
                     fontweight="bold" if bold else "normal")
        w = t.get_window_extent(renderer=renderer).width
        t.remove()
        return w / fig.dpi * 25.4
    space = wpx(" ", False)
    lines, cur, cw = [], [], 0.0
    for w, bold in words:
        ww = wpx(w, bold)
        if cur and cw + space + ww > width_mm:
            lines.append(cur); cur, cw = [], 0.0
        cur.append((w, bold, ww))
        cw += ww + (space if len(cur) > 1 else 0)
    if cur:
        lines.append(cur)
    return lines, space


runs = [(CAP_TITLE + " ", True)]
for lab, seg in CAP:
    if lab:
        runs.append((lab + ",", True))
        seg = seg[1:] if seg.startswith(",") else seg
    runs.append((seg, False))
CAP_W = PW - ML - MR
LH = K.CAP_LH

# pass 1 -- measure each panel's content overhang and the caption height
_f0, _p0, _ = build(22.0)
_over = K.overhangs(_f0, _p0)
_l0 = (rich_lines(_f0, runs, CAP_W, CAP_PT, _f0.canvas.get_renderer())[0]
       if WITH_CAP else [])
plt.close(_f0)

CAP_H = (K.CAP_GAP + len(_l0) * LH + 1.0) if WITH_CAP else 0.0
FIXED = (MT + NROW * LETTER_BAND + XB_SUM + (NROW - 1) * GAP
         + sum(max(_over[r[0]] for r in row) for row in ROWS))
PLOT_H = (PH - MB - CAP_H - FIXED) / NROW    # fill the page, never overrun it
HYP_Y = -HYP_MM / PLOT_H       # keep the second tick row a fixed mm below

# pass 2 -- push each panel down by its own overhang so the rows read flush
fig, PANELS, BOTTOM = build(PLOT_H, _over)
K.place_letters(fig, PANELS)

renderer = fig.canvas.get_renderer()
cap_objs, cap_rect = [], None
lines, space = (rich_lines(fig, runs, CAP_W, CAP_PT, renderer) if WITH_CAP
                else ([], 0))
cap_top = BOTTOM + K.CAP_GAP
for i, line in enumerate(lines):
    x = ML
    yy = cap_top + i * LH
    for word, bold, ww in line:
        t = fig.text(x / PW, 1 - (yy + LH * 0.78) / PH, word, fontsize=CAP_PT,
                     fontweight="bold" if bold else "normal", va="baseline",
                     ha="left")
        cap_objs.append(t)
        x += ww + space
CAP_BOTTOM = cap_top + len(lines) * LH
if WITH_CAP:
    cap_rect = (ML, cap_top - 0.5, CAP_W, CAP_BOTTOM - cap_top + 2)

assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
print(f"[{STEM}] axes height {PLOT_H:.1f} mm; panels end at {BOTTOM:.1f} mm; "
      f"caption {len(lines)} lines -> {CAP_BOTTOM:.1f} mm of {PH:.0f} mm")

# ----------------------------------------------------------------------- export
png = os.path.join(HERE, STEM + ".png")
pdf = os.path.join(HERE, STEM + ".pdf")
ppt = os.path.join(HERE, STEM + ".pptx")
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")


def export_pptx(fig, path, caption_objs, caption_runs, cap_rect, dpi=DPI):
    """Raster graphics layer + one native text box per label, caption as ONE box."""
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
    from matplotlib import colors as mcolors

    recs = [r for r in collect_text_records(fig) if r["obj"] not in caption_objs]
    fw, fh = [float(v) for v in fig.get_size_inches()]
    fdpi = float(fig.dpi)
    vis = [(t, t.get_visible()) for t in fig.findobj(matplotlib.text.Text)]
    for t, _ in vis:
        t.set_visible(False)
    bg = os.path.splitext(path)[0] + "_bg.png"
    fig.savefig(bg, dpi=dpi, bbox_inches=None, facecolor=fig.get_facecolor())
    for t, v in vis:
        t.set_visible(v)

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(fw), Inches(fh)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(bg, 0, 0, width=Inches(fw), height=Inches(fh))
    align = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
    pad = 1.25
    for r in recs:
        w, h = r["w"] * pad / fdpi, r["h"] * pad / fdpi
        left, top = r["cx"] / fdpi - w / 2.0, (fh - r["cy"] / fdpi) - h / 2.0
        box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = align.get(r["ha"], PP_ALIGN.CENTER)
        run = p.add_run()
        run.text = r["text"].replace("$", "").replace("\\Delta", "Δ").replace("\\", "")
        f = run.font
        f.name = "Arial"; f.size = Pt(r["size"])
        f.bold = r["weight"] in ("bold", "semibold", "heavy", "black")
        f.italic = r["style"] in ("italic", "oblique")
        f.color.rgb = RGBColor(*[int(round(255 * c)) for c in mcolors.to_rgb(r["color"])])
        if r["rot"]:
            box.rotation = (-r["rot"]) % 360.0
    # caption: a single editable, word-wrapped text box
    if cap_rect is None:
        prs.save(path); os.remove(bg); return path
    x_mm, y_mm, w_mm, h_mm = cap_rect
    box = slide.shapes.add_textbox(Inches(x_mm / 25.4), Inches(y_mm / 25.4),
                                   Inches(w_mm / 25.4), Inches(h_mm / 25.4))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    for text, bold in caption_runs:
        run = p.add_run()
        run.text = text
        run.font.name = "Arial"; run.font.size = Pt(CAP_PT); run.font.bold = bold
    prs.save(path)
    os.remove(bg)
    return path


export_pptx(fig, ppt, set(cap_objs), runs, cap_rect)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
print("non-Arial text:", bad[:5], "| files:", [os.path.basename(p) for p in (png, pdf, ppt)])
plt.close(fig)
