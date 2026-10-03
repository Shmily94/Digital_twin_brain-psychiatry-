"""Supplementary figure | two-dimensional AMPA / GABA-A parameter sweep.

DRAFT.  Source data: revision/gui_baseline_identify/coherence_results_tau_gamma.csv
(copied into data/), a single sweep of the regional DTB over
g_AMPA = 0.0004-0.0040 S cm-2 (10 levels) x g_GABA-A = 0.0005-0.0040 S cm-2
(8 levels), I_ext = 0, one simulation per grid cell (80 cells).  The file carries
mean population firing rate, mean coherence and the coherence of each of the 217
regions; it does NOT carry a BOLD-stability measure.

Regimes are read off the data, not thresholded by hand: coherence is bimodal
(46 cells at the 0.063-0.065 floor, 34 cells at 0.34-0.76, nothing in between)
and the floor cells split by rate with equally clean gaps (38 cells <= 3.4 Hz,
8 cells >= 69.7 Hz, while every synchronised cell lies between 5.3 and 39.9 Hz).

    cd revision/text/figures/supp_paramspace && python paramspace_supp.py
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
apply_np_style()
D, OUTD = f'{HERE}/data', f'{HERE}/panels'

d = pd.read_csv(f'{D}/coherence_results_tau_gamma.csv')
FR = d.pivot(index='GABA', columns='AMPA', values='Mean_firing_rate')
CO = d.pivot(index='GABA', columns='AMPA', values='Mean_Coherence')
A, G = FR.columns.values, FR.index.values

# ---- regimes from the empirical gaps ---------------------------------------
SYNC_CUT, RATE_CUT = 0.20, 50.0          # both fall inside an empty interval
REG = np.where(CO.values >= SYNC_CUT, 1,
               np.where(FR.values >= RATE_CUT, 2, 0))       # 0 async 1 sync 2 saturated
assert not ((CO.values > 0.08) & (CO.values < 0.30)).any()
assert not ((REG == 0) & (FR.values > 4)).any()

GREY = ['#E2E2E2', '#8C8C8C', '#F4F4F4']
LAB = ['Asynchronous', 'Synchronised', 'Excessive firing (excluded)']


def grid(ax, M, cmap, norm, title, cbar_label, ticks=None):
    im = ax.imshow(M, origin='lower', aspect='auto', cmap=cmap, norm=norm)
    ax.set_xticks(range(len(A)))
    ax.set_xticklabels([f'{v*1e4:.0f}' for v in A], fontsize=TICK_PT)
    ax.set_yticks(range(len(G)))
    ax.set_yticklabels([f'{v*1e4:.0f}' for v in G], fontsize=TICK_PT)
    ax.set_xlabel('$g_{\\rm AMPA}$ ($10^{-4}$ S cm$^{-2}$)', fontsize=LABEL_PT)
    ax.set_ylabel('$g_{\\rm GABA}$-A ($10^{-4}$ S cm$^{-2}$)', fontsize=LABEL_PT)
    panel_title(ax, title)
    if cbar_label is not None:
        cb = plt.colorbar(im, ax=ax, fraction=.055, pad=.03, ticks=ticks)
        cb.set_label(cbar_label, fontsize=LABEL_PT)
        cb.ax.tick_params(labelsize=TICK_PT, length=1.6, width=LW)
        cb.outline.set_linewidth(LW)
    return im


fig, axes = plt.subplots(1, 3, figsize=panel(180, 52))
grid(axes[0], FR.values, 'Greys', LogNorm(vmin=FR.values.min(), vmax=FR.values.max()),
     'Mean firing rate', 'Firing rate (Hz)', ticks=[1, 3, 10, 30, 100])
grid(axes[1], CO.values, 'Greys', None, 'Mean coherence', 'Coherence')
grid(axes[2], REG, ListedColormap(GREY), BoundaryNorm([-.5, .5, 1.5, 2.5], 3),
     'Dynamical regime', None)
for j in range(len(A)):                       # hatch the excluded cells
    for i in range(len(G)):
        if REG[i, j] == 2:
            axes[2].add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False,
                                            hatch='////', edgecolor='0.45',
                                            linewidth=0))
axes[2].legend(handles=[Patch(facecolor=GREY[0], edgecolor='none', label=LAB[0]),
                        Patch(facecolor=GREY[1], edgecolor='none', label=LAB[1]),
                        Patch(facecolor=GREY[2], edgecolor='0.45', hatch='////',
                              label=LAB[2])],
               fontsize=ANNOT_PT, frameon=False, loc='upper left',
               bbox_to_anchor=(0, -.30), handlelength=1.4, labelspacing=.35)
for ax in axes:
    for s in ax.spines.values():
        s.set_linewidth(LW)
    ax.tick_params(length=1.8, width=LW)
fig.subplots_adjust(left=.055, right=.985, bottom=.30, top=.90, wspace=.42)
fig.savefig(f'{OUTD}/figS_paramspace_draft.png', dpi=300)
print('regime counts async/sync/excluded:', [(REG == k).sum() for k in (0, 1, 2)])
print('firing rate range %.2f-%.2f Hz; coherence %.4f-%.4f'
      % (FR.values.min(), FR.values.max(), CO.values.min(), CO.values.max()))
print('non-Arial:', enforce(fig)[:3])
