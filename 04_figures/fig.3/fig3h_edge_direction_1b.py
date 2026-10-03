"""Fig. 3h | Which of the 12 NP edges move with the summed NP score (1 B build).

For each of the 12 cross-scale subjects the summed NP score changes in some
direction after a virtual AMPA or GABA-A up-regulation.  An edge is called
CONCORDANT for that subject when its own change has the same sign as the change
in the summed score.  The panel shows, per edge, how many of the 12 subjects are
concordant -- the fig2f form: one row of 12 edges, SST block then MID block.

Chance is 6/12.  The grey band is the central 95% of the binomial null
(n = 12, p = 0.5): counts of 3-9 fall inside it, so only 10+ (or 2-) is a
departure from chance at P < 0.05 uncorrected.  Nothing survives BH correction
over the 24 tests (smallest q = 0.051), which is why the band, not a
significance star, is the honest read-out here.

Source: np_baseline_and_modulated_per_edge_6models.csv (12 subjects x 12 edges
x {baseline, ampa, gaba}); summing its 12 edges reproduces the panel-g deltas
for the 1 B build exactly (max |diff| = 1e-6).

    cd revision/text/figures/fig.3 && python fig3h_edge_direction_1b.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import binom
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from fig_export import fig_to_pptx

D = os.path.join(HERE, 'fig3_data')
OUTD = os.path.join(HERE, 'panels')
apply_np_style()
DPI = 400

t = pd.read_csv(f'{D}/fig3h_edge_direction_1b.csv')
EDGES = [f'E{i}' for i in range(1, 13)]
DRUGS = [('AMPA', C('ampa'), -.16, 'o'), ('GABA-A', C('gaba'), .16, 's')]

W, H = 180, 44
fig, ax = plt.subplots(figsize=panel(W, H))
x = np.arange(len(EDGES))

# central 95% of the binomial null, n = 12, p = 0.5  -> counts 3..9
k = np.arange(13)
lo = int(k[binom.cdf(k, 12, .5) > .025][0])
hi = int(k[binom.sf(k - 1, 12, .5) > .025][-1])
ax.axhspan(lo - .5, hi + .5, color='0.92', zorder=0)
ax.axhline(6, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)

for lab, col, dx, mk in DRUGS:
    sub = t[t.modulation == lab].set_index('edge').loc[EDGES]
    out = (sub.n_concordant < lo) | (sub.n_concordant > hi)
    ax.scatter(x[out.values] + dx, sub.n_concordant[out.values], s=11, marker=mk,
               facecolor=col, edgecolor=col, linewidth=LW, zorder=3)
    ax.scatter(x[~out.values] + dx, sub.n_concordant[~out.values], s=11, marker=mk,
               facecolor='white', edgecolor=col, linewidth=LW, zorder=3)
    ax.vlines(x + dx, 6, sub.n_concordant, color=col, lw=LW, zorder=2)

n_sst = int((t[t.modulation == 'AMPA'].set_index('edge').loc[EDGES].task == 'SST').sum())
ax.axvline(n_sst - .5, color='0.85', lw=LW, zorder=0)
ax.text((n_sst - 1) / 2, 12.4, 'SST', ha='center', fontsize=ANNOT_PT, color='0.35')
ax.text((n_sst + len(EDGES) - 1) / 2, 12.4, 'MID', ha='center', fontsize=ANNOT_PT,
        color='0.35')
ax.set_xticks(x); ax.set_xticklabels(EDGES, fontsize=TICK_PT)
ax.set_xlim(-.7, len(EDGES) - .3)
ax.set_ylim(0, 13.2)
ax.set_yticks([0, 3, 6, 9, 12])
ax.set_ylabel('Subjects moving with\nthe summed NP score')

handles = [Line2D([], [], marker=mk, linestyle='none', markersize=3.2,
                  markerfacecolor='white', markeredgecolor=col, markeredgewidth=LW)
           for lab, col, dx, mk in DRUGS]
handles.append(Patch(facecolor='0.92', edgecolor='none'))
ax.legend(handles, [d[0] for d in DRUGS] + ['95% binomial null'],
          loc='lower right', ncol=3, fontsize=ANNOT_PT, handletextpad=.4,
          columnspacing=1.0, borderaxespad=.2)
panel_title(ax, '1 B build: most NP edges follow the summed score, '
                'none beyond chance after correction')
enforce(fig)
fig.savefig(f'{OUTD}/fig3h.png', dpi=DPI, bbox_inches='tight')
fig.savefig(f'{OUTD}/fig3h.pdf', bbox_inches='tight')
fig_to_pptx(fig, f'{OUTD}/fig3h.pptx', dpi=DPI)
px = Image.open(f'{OUTD}/fig3h.png').size
print(f'fig3h  {W} x {H} mm  {px[0]}x{px[1]} px  {round(px[0] / (W / 25.4))} dpi')
print(f'binomial null band: {lo}..{hi} of 12')
print(t.groupby('modulation').n_concordant.describe()[['mean', 'min', 'max']].round(2).to_string())
