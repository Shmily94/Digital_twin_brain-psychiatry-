"""Supplementary figure | Whole-brain extent of the virtual perturbations.

Built entirely from the stored n = 288 whole-brain tables -- nothing is
recomputed here:
  SuppTable_WB1_wholebrain_modulation_n288.csv      (extent and magnitude)
  SuppTable_WB_network_pair_summary_n288.csv        (spatial organisation)

  a  magnitude profile: proportion of the 23,436 edges passing FDR and
     exceeding |d_z| = 0.5 and 0.8, per task condition and manipulation
  b  median |d_z| among significant edges
  c  net signed change per network pair, 9 x 9, two tasks x two manipulations

Panel a is deliberately a profile rather than a bar of "% significant": at
n = 288 the FDR proportion mostly reflects power, so the figure shows how
quickly that proportion falls once an effect-size floor is imposed.

    cd revision/text/figures/supp_wholebrain && python wb_supp.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx

D = os.path.join(HERE, 'wb_data')
OUTD = os.path.join(HERE, 'panels')
os.makedirs(OUTD, exist_ok=True)
DPI = 400
apply_np_style()

WB = pd.read_csv(f'{D}/SuppTable_WB1_wholebrain_modulation_n288.csv')
NP_ = pd.read_csv(f'{D}/SuppTable_WB_network_pair_summary_n288.csv')
COND = ['sst_stop_suces', 'sst_stop_failure', 'mid_feed_hit', 'mid_antici_hit']
CLAB = {'sst_stop_suces': 'SST stop-success', 'sst_stop_failure': 'SST stop-failure',
        'mid_feed_hit': 'MID feedback', 'mid_antici_hit': 'MID anticipation'}
CMK = dict(zip(COND, ['o', 's', '^', 'D']))
CONTR = [('AMPA vs baseline', 'AMPA', C('ampa')),
         ('AMPA+GABA-A vs baseline', 'AMPA+GABA-A', C('gaba'))]
manifest = []


def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}',
                         dpi=round(px[0] / (w_mm / 25.4)), source=note))
    plt.close(fig)


# ---- a  magnitude profile ---------------------------------------------------
W, H = 86, 52
fig, ax = plt.subplots(figsize=panel(W, H))
xs = [0, 1, 2]
for contrast, clab, col in CONTR:
    for cond in COND:
        r = WB[(WB.condition == cond) & (WB.contrast == contrast)].iloc[0]
        ax.plot(xs, [r.pct_sig_FDR, r.pct_absdz_gt0p5, r.pct_absdz_gt0p8],
                color=col, lw=LW, marker=CMK[cond], markersize=2.8,
                markerfacecolor=col, markeredgecolor=col, markeredgewidth=LW,
                zorder=3)
ax.set_xticks(xs)
ax.set_xticklabels(['FDR\n$q$ < 0.05', '$|d_z|$ > 0.5', '$|d_z|$ > 0.8'],
                   fontsize=TICK_PT)
ax.set_xlim(-.3, 2.3); ax.set_ylim(0, 100)
ax.set_ylabel('Edges of 23,436 (%)')
h1 = [Line2D([], [], color=col, lw=LW * 1.6) for _, _, col in CONTR]
h2 = [Line2D([], [], color='0.4', lw=0, marker=CMK[c], markersize=2.8,
             markerfacecolor='0.4', markeredgecolor='0.4') for c in COND]
ax.legend(h1 + h2, [l for _, l, _ in CONTR] + [CLAB[c] for c in COND],
          loc='upper right', ncol=2, fontsize=ANNOT_PT, handletextpad=.4,
          columnspacing=1.0, labelspacing=.25, borderaxespad=.2, frameon=False)
panel_title(ax, 'Whole-brain extent shrinks once an effect-size floor is set')
enforce(fig); save(fig, 'figS_wb_a', W, H,
                   'SuppTable_WB1_wholebrain_modulation_n288.csv')

# ---- b  median |dz| among significant edges --------------------------------
W, H = 66, 50
fig, ax = plt.subplots(figsize=panel(W, H))
xw = np.arange(len(COND))
for k, (contrast, clab, col) in enumerate(CONTR):
    v = [WB[(WB.condition == c) & (WB.contrast == contrast)].iloc[0].median_absdz_sig
         for c in COND]
    ax.bar(xw + (k - .5) * .34, v, width=.32, facecolor=col, edgecolor='black',
           linewidth=LW, zorder=2, label=clab)
for y_, lab in [(0.5, 'medium'), (0.8, 'large')]:
    ax.axhline(y_, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.text(len(COND) - .45, y_ + .01, lab, ha='right', va='bottom',
            fontsize=ANNOT_PT, color='0.5')
ax.set_xticks(xw)
ax.set_xticklabels([CLAB[c].replace(' ', '\n') for c in COND], fontsize=TICK_PT)
ax.set_xlim(-.6, len(COND) - .4); ax.set_ylim(0, .95)
ax.set_ylabel('Median $|d_z|$ (significant edges)')
ax.legend(loc='upper left', fontsize=ANNOT_PT, handletextpad=.4, borderaxespad=.2,
          frameon=False)
panel_title(ax, 'Typical effect is small-to-medium')
enforce(fig); save(fig, 'figS_wb_b', W, H,
                   'SuppTable_WB1_wholebrain_modulation_n288.csv')

# ---- c  network-pair net signed change -------------------------------------
NETS = ['DMN', 'FPN', 'Limbic', 'Motor', 'SMF', 'Sub', 'Visual Asso',
        'Visual I', 'Visual II']


def pair_matrix(cond, contrast):
    Mx = np.full((len(NETS), len(NETS)), np.nan)
    sub = NP_[(NP_.condition == cond) & (NP_.contrast == contrast)]
    for _, r in sub.iterrows():
        lab = r.net_pair
        if '(within)' in lab:
            a = b = lab.split(' (')[0]
        else:
            a, b = [s.strip() for s in lab.replace('\u2013', '-').split('-')]
        i, j = NETS.index(a), NETS.index(b)
        Mx[i, j] = Mx[j, i] = r.net_signed_pct
    return Mx


SHOW = [('sst_stop_suces', 'AMPA vs baseline'),
        ('sst_stop_suces', 'AMPA+GABA-A vs baseline'),
        ('mid_feed_hit', 'AMPA vs baseline'),
        ('mid_feed_hit', 'AMPA+GABA-A vs baseline')]
W, H = 180, 58
fig, axes = plt.subplots(1, 4, figsize=panel(W, H), gridspec_kw=dict(wspace=.18))
allm = np.array([pair_matrix(*s) for s in SHOW])
vmax = float(np.nanmax(np.abs(allm)))
for ax, (cond, contrast) in zip(axes, SHOW):
    Mx = pair_matrix(cond, contrast)
    im = ax.imshow(Mx, cmap='coolwarm', vmin=-vmax, vmax=vmax)
    ax.set_xticks(range(len(NETS))); ax.set_yticks(range(len(NETS)))
    ax.set_xticklabels(NETS, fontsize=TICK_PT, rotation=90)
    ax.set_yticklabels(NETS if ax is axes[0] else [''] * len(NETS), fontsize=TICK_PT)
    ax.set_xticks(np.arange(-.5, len(NETS), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(NETS), 1), minor=True)
    ax.grid(which='minor', color='0.85', linewidth=LW)
    ax.tick_params(which='both', length=0)
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_linewidth(LW); sp.set_color('0.40')
    panel_title(ax, f'{CLAB[cond]}\n{contrast.split(" vs")[0]}')
cb = fig.colorbar(im, ax=axes, fraction=.012, pad=.012)
cb.set_label('Net signed change (%)', fontsize=ANNOT_PT, labelpad=1)
cb.ax.tick_params(labelsize=TICK_PT, width=LW, length=1.6)
cb.outline.set_linewidth(LW)
enforce(fig)
for ax in axes:                 # heatmaps: cell grid only, no tick marks
    ax.tick_params(which='both', length=0)
save(fig, 'figS_wb_c', W, H,
                   'SuppTable_WB_network_pair_summary_n288.csv')

mf = pd.DataFrame(manifest)
mf.to_csv(f'{OUTD}/wb_panel_manifest.csv', index=False)
print(mf.to_string(index=False))
print('\nextent and magnitude (n = 288)')
print(WB[WB.contrast != 'AMPA+GABA-A vs AMPA (incremental)'][
    ['condition', 'contrast', 'pct_sig_FDR', 'pct_absdz_gt0p5', 'pct_absdz_gt0p8',
     'median_absdz_sig']].to_string(index=False))
print(f'\nnetwork-pair range across the four shown matrices: '
      f'{np.nanmin(allm):.1f} to {np.nanmax(allm):.1f} %')
