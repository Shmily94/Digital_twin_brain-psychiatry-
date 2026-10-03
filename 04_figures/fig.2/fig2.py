"""Figure 2 | A compact functional-network phenotype of transdiagnostic psychopathology.

ONE FILE PER PANEL.  Every panel is written to ./panels/ as .png (400 dpi),
.pdf (vector) and .pptx (editable text), at its intended printed size, so the
panels can be placed in PowerPoint without any rescaling.

Panels a, b and d are the author's ORIGINAL panels, composited verbatim from
revision/Figure_200726.pptx (slide 1) into fig2_data/original_panels/ and
exported unchanged at >= 300 dpi.

Recomputed because the STRATIFY cohort is now HC + MDD + AUD (225 + 202):
  c  negative profile score (29 edges, incl. cerebellum/brainstem) -- blue family
  e  NP factor (the 12 cortico-subcortical edges) -- group colours, grey/orange
New:
  f  per-edge group difference for the 12 NP-factor edges, laid out horizontally

Naming, per the author: the 29-edge quantity is the "negative profile"; once
cerebellar and brainstem edges are removed the remaining 12 edges are the
"NP factor" -- panels e and f are NP factor, not negative NP.

    cd revision/text/figures/fig.2 && python fig2.py
"""
import os, sys, shutil
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
sys.path.insert(0, os.path.join(HERE, '..'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx
import figA4_kit as PK          # the frozen main-figure type scale, 8/9/10 pt

# Multiple-comparison correction for panel f.  The author's earlier result
# ("7 edges") corresponds to 'none'; MATLAB mafdr corresponds to 'storey'.
FDR_METHOD = 'fdr_bh'    # 'fdr_bh' | 'fdr_by' | 'bonferroni' | 'storey' | 'none'

D = os.path.join(HERE, 'fig2_data')
OPD = os.path.join(D, 'original_panels')
OUTD = os.path.join(HERE, 'panels')
os.makedirs(OUTD, exist_ok=True)
DPI = 400
apply_np_style()

sc = pd.read_csv(f'{D}/fig2c_profile_scores.csv')
e2 = pd.read_csv(f'{D}/fig2e_edge_group_difference.csv')
ORDER = ['HC', 'Patient']
GROUP_COL = {'HC': C('hc'), 'Patient': C('patient')}           # e: group colours
PROFILE_COL = {'HC': C('neg_profile_hc'), 'Patient': C('neg_profile_pt')}  # c: blue
manifest = []


def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    with mpl.rc_context({'savefig.bbox': None}):   # else the raster is cropped
        fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)   # and the text layer
                                                           # sits off-register
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}', dpi=round(px[0] / (w_mm / 25.4)),
                         source=note))
    plt.close(fig)


def export_original(src, stem, w_mm, note):
    """Original panel: copied at native resolution, no re-rendering."""
    im = Image.open(os.path.join(OPD, src))
    h_mm = w_mm * im.height / im.width
    im.save(f'{OUTD}/{stem}.png', dpi=(im.width / (w_mm / 25.4),) * 2)
    manifest.append(dict(panel=stem, printed_w_mm=round(w_mm, 1), printed_h_mm=round(h_mm, 1),
                         png_px=f'{im.width}x{im.height}',
                         dpi=round(im.width / (w_mm / 25.4)), source=note))


def adjust(pvals, method=FDR_METHOD):
    """Return adjusted p/q values for the chosen correction."""
    pv = np.asarray(pvals, float); m = len(pv)
    if method == 'none':
        return pv
    if method == 'bonferroni':
        return np.minimum(pv * m, 1)
    if method == 'storey':
        lam = np.arange(0.05, 0.96, 0.05)
        pi0 = min(np.mean([np.sum(pv > l) / (m * (1 - l)) for l in lam]), 1.0)
        o = np.argsort(pv); q = pi0 * m * pv[o] / np.arange(1, m + 1)
        q = np.minimum.accumulate(q[::-1])[::-1]
        out = np.empty(m); out[o] = np.minimum(q, 1); return out
    o = np.argsort(pv)                       # Benjamini-Hochberg / Yekutieli
    c = 1.0 if method == 'fdr_bh' else np.sum(1.0 / np.arange(1, m + 1))
    q = c * m * pv[o] / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m); out[o] = np.minimum(q, 1); return out


def star_of(p):
    return '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else 'n.s.'


# ------------------------------------------------- a, b, d : originals, untouched
export_original('a_original.png', 'fig2a', 120, 'Figure_200726.pptx slide 1, panel a')
export_original('b_pos_original.png', 'fig2b_positive', 55, 'Figure_200726.pptx slide 1, panel b left')
export_original('b_neg_original.png', 'fig2b_negative', 55, 'Figure_200726.pptx slide 1, panel b right')
export_original('d_original.png', 'fig2d', 105, 'Figure_200726.pptx slide 1, panel d')

# --------------------------------- c  negative profile, HC vs patients  (blue)
W, H = 48, 52
fig, ax = plt.subplots(figsize=panel(W, H))
dat = [sc.loc[sc.Group == g, 'Neg_NP'].values for g in ORDER]
pv = ax.violinplot(dat, positions=[0, 1], widths=.62, showextrema=False)
for b, g in zip(pv['bodies'], ORDER):
    b.set_facecolor(PROFILE_COL[g]); b.set_edgecolor(PROFILE_COL[g])
    b.set_alpha(1); b.set_linewidth(LW)
bp = ax.boxplot(dat, positions=[0, 1], widths=.18, showfliers=False, patch_artist=True)
for el in ('boxes', 'whiskers', 'caps', 'medians'):
    for art in bp[el]:
        art.set_linewidth(LW); art.set_color('black')
        if el == 'boxes':
            art.set_facecolor('white'); art.set_edgecolor('black')
t_c, p_c = stats.ttest_ind(*dat); pb_c = min(1, p_c * 2)
ax.plot([0, 0, 1, 1], [4.4, 4.85, 4.85, 4.4], lw=LW, c='k')
ax.text(.5, 4.85, star_of(pb_c), ha='center', va='bottom', fontsize=ANNOT_PT)
ax.set_xticks([0, 1]); ax.set_xticklabels(['HC', 'Patient'])
ax.set_yticks([-6, -3, 0, 3, 6]); ax.set_ylim(-6, 6.4); ax.set_xlim(-.7, 1.7)
ax.set_ylabel('Negative profile score')
panel_title(ax, 'Patients show lower connectivity')
enforce(fig); save(fig, 'fig2c', W, H, 'fig2c_profile_scores.csv')

# ------------------------------------ e  NP factor, HC vs patients (+ density)
W, H = 52, 58
fig, (ax, axk) = plt.subplots(2, 1, figsize=panel(W, H), sharex=False,
                              gridspec_kw=dict(height_ratios=[3.1, 1], hspace=0.55))
rng = np.random.default_rng(1)
npf = [sc.loc[sc.Group == g, 'NP_factor'].values for g in ORDER]
for i, (g, v) in enumerate(zip(ORDER, npf)):
    ax.scatter(i + rng.uniform(-.18, .18, len(v)), v, s=2.4, color=GROUP_COL[g],
               alpha=.65, linewidth=0, zorder=2)
    ax.errorbar(i, v.mean(), yerr=v.std(ddof=1), color='black', lw=LW,
                capsize=1.6, capthick=LW, zorder=4)
ax.plot([0, 1], [npf[0].mean(), npf[1].mean()], color='0.45', lw=LW,
        ls=(0, (2.6, 1.7)), zorder=3)
t_e, p_e = stats.ttest_ind(*npf); pb_e = min(1, p_e * 2)
ax.plot([0, 0, 1, 1], [3.0, 3.35, 3.35, 3.0], lw=LW, c='k')
ax.text(.5, 3.35, star_of(pb_e), ha='center', va='bottom', fontsize=ANNOT_PT)
ax.set_xticks([0, 1])
ax.set_xticklabels([f'HC\nn = {len(npf[0])}', f'Patient\nn = {len(npf[1])}'])
ax.set_ylim(-3.2, 4); ax.set_yticks([-2, 0, 2, 4]); ax.set_xlim(-.6, 1.6)
ax.set_ylabel('NP factor')
panel_title(ax, 'NP factor separates the groups')
xs = np.linspace(-3.2, 4, 240)
for g, v in zip(ORDER, npf):
    k = stats.gaussian_kde(v)(xs)
    axk.fill_between(xs, k, color=GROUP_COL[g], alpha=.55, linewidth=0)
    axk.plot(xs, k, color=GROUP_COL[g], lw=LW)
axk.set_xlim(-3.2, 4); axk.set_yticks([]); axk.set_xlabel('NP factor')
axk.spines['left'].set_visible(False)
enforce(fig); save(fig, 'fig2e', W, H, 'fig2c_profile_scores.csv')

# ------------------------- f  per-edge group difference, horizontal row (NEW)
# All 12 edges are NP-factor edges, so they all carry the NP-factor colour;
# fill state carries significance (solid = FDR q < 0.05, open = n.s.).
W, H = 180, 46           # 8 pt ticks and a 10 pt y label need the extra 6 mm
COL_F = C('patient')
fig, ax = plt.subplots(figsize=panel(W, H))
x = np.arange(len(e2))
q_f = adjust(e2.p.values)
sig = q_f < .05
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.vlines(x, e2.ci_lo, e2.ci_hi, color=COL_F, lw=LW, zorder=2)
ax.scatter(x[sig], e2.d[sig], s=16, facecolor=COL_F, edgecolor=COL_F,
           linewidth=LW, zorder=3)
ax.scatter(x[~sig], e2.d[~sig], s=16, facecolor='white', edgecolor=COL_F,
           linewidth=LW, zorder=3)
n_sst = int((e2.task == 'SST').sum())
ax.set_ylim(-.45, .78)
ax.axvline(n_sst - .5, color='0.85', lw=LW, zorder=0)
ax.text((n_sst - 1) / 2, .70, 'SST', ha='center', va='center',
        fontsize=PK.ANNOT_PT, color='0.35')
ax.text((n_sst + len(e2) - 1) / 2, .70, 'MID', ha='center', va='center',
        fontsize=PK.ANNOT_PT, color='0.35')
ax.set_xticks(x)
ax.set_xticklabels([r.edge.replace('Edge ', 'E') for r in e2.itertuples()],
                   fontsize=PK.TICK_PT)
ax.tick_params(axis='both', labelsize=PK.TICK_PT)
ax.set_xlim(-.7, len(e2) - .3)
ax.set_ylabel("Cohen's $d$\n(HC \u2212 patient)", fontsize=PK.LABEL_PT)
ax.legend(loc='lower right', ncol=2, fontsize=ANNOT_PT, handletextpad=.4,
          columnspacing=1.0, borderaxespad=.2)
LAB = {'fdr_bh': 'FDR q < 0.05', 'fdr_by': 'FDR (BY) q < 0.05',
       'bonferroni': 'Bonferroni P < 0.05', 'storey': 'Storey q < 0.05',
       'none': 'uncorrected P < 0.05'}[FDR_METHOD]
handles = [Line2D([], [], marker='o', linestyle='none', markersize=4.0,
                  markerfacecolor=COL_F, markeredgecolor=COL_F, markeredgewidth=LW),
           Line2D([], [], marker='o', linestyle='none', markersize=4.0,
                  markerfacecolor='white', markeredgecolor=COL_F, markeredgewidth=LW)]
ax.legend(handles, [LAB, 'n.s.'], loc='lower right', ncol=2,
          fontsize=PK.ANNOT_PT, handletextpad=.4, columnspacing=1.0,
          borderaxespad=.2)
# no declarative panel title: the count of surviving edges belongs to the
# Figure 2 legend (house rule), not on the panel
enforce(fig); save(fig, 'fig2f', W, H, 'fig2e_edge_group_difference.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
print(f'\nc negative profile : t = {t_c:.3f}, p = {p_c:.3g}, p_Bonf = {pb_c:.3g}')
print(f'e NP factor        : t = {t_e:.3f}, p = {p_e:.3g}, p_Bonf = {pb_e:.3g}')
print(f'  n_HC = {len(npf[0])}, n_patient = {len(npf[1])}')
print(f'f correction = {FDR_METHOD}: {int(sig.sum())}/12 edges q<0.05: '
      f'{", ".join(e2.edge[sig])}')
