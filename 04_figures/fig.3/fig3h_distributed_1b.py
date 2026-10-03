"""Fig. 3h (alternative form) | The perturbation response is distributed.

Two panels, one per clause of the claim:

  h1  per twin, how many of the 12 NP edges move with the summed factor
      -> "most edges follow the factor"  (chance = 6 of 12)
  h2  cumulative share of the total absolute edge change, edges ranked
      largest-first -> "no single edge drives it"; the dashed diagonal is
      what a perfectly even response across 12 edges would look like.

1 B build, 12 cross-scale twins.  Source: the same per-edge table as fig3h
(np_baseline_and_modulated_per_edge_6models.csv).

    cd revision/text/figures/fig.3 && python fig3h_distributed_1b.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
sys.path.insert(0, os.path.join(HERE, '..'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from fig_export import fig_to_pptx
import figA4_kit as PK          # the frozen main-figure type scale, 8/9/10 pt

D = os.path.join(HERE, 'fig3_data')
OUTD = os.path.join(HERE, 'panels')
apply_np_style()
DPI = 400
DRUGS = [('AMPA', C('ampa'), 'o'), ('GABA-A', C('gaba'), 's')]

cnt = pd.read_csv(f'{D}/fig3h_subject_edge_counts_1b.csv')
cum = pd.read_csv(f'{D}/fig3h_cumulative_share_1b.csv')


def save(fig, stem, w_mm, h_mm):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    with mpl.rc_context({'savefig.bbox': None}):   # else the raster is cropped
        fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)   # and the text layer
                                                           # sits off-register
    px = Image.open(f'{OUTD}/{stem}.png').size
    print(f'{stem}  {w_mm} x {h_mm} mm  {px[0]}x{px[1]} px  '
          f'{round(px[0] / (w_mm / 25.4))} dpi')
    plt.close(fig)


# ---- h1  every twin has more than half its edges moving with the factor ----
W, H = 82, 56            # 8-10 pt type needs the extra 6 mm
fig, ax = plt.subplots(figsize=panel(W, H))
rng = np.random.default_rng(3)
ax.axhspan(0, 6, color='0.94', zorder=0)                 # below chance
ax.axhline(6, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
for i, (lab, col, mk) in enumerate(DRUGS):
    v = cnt[cnt.modulation == lab].n_edges_concordant.values
    ax.scatter(i + rng.uniform(-.13, .13, len(v)), v, s=18, marker=mk,
               facecolor=col, edgecolor=col, linewidth=LW, alpha=.85, zorder=3)
    ax.hlines(v.mean(), i - .26, i + .26, color='black', lw=LW, zorder=4)
    ax.text(i, 12.8, f'{v.mean():.1f}', ha='center', fontsize=PK.ANNOT_PT,
            color='0.35')
ax.text(-.62, 3, 'below chance', rotation=90, va='center', ha='center',
        fontsize=PK.ANNOT_PT, color='0.55')
ax.set_xticks(range(len(DRUGS)))
ax.set_xticklabels([d[0] for d in DRUGS], fontsize=PK.LABEL_PT)  # group names
ax.tick_params(axis='y', labelsize=PK.TICK_PT)
ax.set_xlim(-.75, len(DRUGS) - .25)
ax.set_ylim(0, 13.6); ax.set_yticks([0, 3, 6, 9, 12])
ax.set_ylabel('NP edges moving with\nthe summed factor (of 12)',
              fontsize=PK.LABEL_PT)
# no declarative panel title: the chance level is drawn (dashed line at 6 of
# 12, shaded below) and the claim belongs in the legend
enforce(fig); save(fig, 'fig3h1', W, H)

# ---- h2  no single edge carries the response --------------------------------
W, H = 82, 50
fig, ax = plt.subplots(figsize=panel(W, H))
k = np.arange(1, 13)
# the two extremes the observed curve is read against
ax.plot(k, k / 12, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.text(9.4, 9.4 / 12 - .07, 'even across\nall 12 edges', fontsize=ANNOT_PT,
        color='0.55', ha='center', va='top')
ax.plot(k, np.ones_like(k, dtype=float), color='0.6', lw=LW, ls=(0, (2.6, 1.7)),
        zorder=1)
ax.plot([1, 1], [0, 1], color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.text(4.2, 1.02, 'driven by one edge', fontsize=ANNOT_PT, color='0.55',
        ha='left', va='bottom')
for lab, col, mk in DRUGS:
    sub = cum[cum.modulation == lab]
    for sid, gsub in sub.groupby('sub_id'):
        ax.plot(gsub.n_edges, gsub.cum_share, color=col, lw=LW, alpha=.28, zorder=2)
    m = sub.groupby('n_edges').cum_share.mean()
    ax.plot(k, m.values, color=col, lw=LW * 1.8, marker=mk, markersize=2.6,
            markerfacecolor=col, markeredgecolor=col, zorder=4)
ax.axhline(.5, color='0.6', lw=LW, ls=(0, (1.2, 1.2)), zorder=1)
ax.set_xticks(k); ax.set_xlim(.6, 12.4)
ax.set_ylim(0, 1.13); ax.set_yticks([0, .25, .5, .75, 1])
ax.set_xlabel('Edges, ranked by size of change')
ax.set_ylabel('Cumulative share of the\ntotal absolute change')
handles = [Line2D([], [], marker=mk, color=col, lw=LW * 1.8, markersize=2.6)
           for lab, col, mk in DRUGS]
ax.legend(handles, [d[0] for d in DRUGS], loc='lower right', ncol=1,
          fontsize=ANNOT_PT, handletextpad=.4, borderaxespad=.2)
panel_title(ax, 'The change is spread over the circuit, not one edge')
enforce(fig); save(fig, 'fig3h2', W, H)

print('\nmean cumulative share  (AMPA / GABA-A)')
mm = cum.pivot_table(index='n_edges', columns='modulation', values='cum_share')
print(mm.loc[[1, 2, 3, 6]].round(3).to_string())
print('\nedges concordant per twin:')
print(cnt.groupby('modulation').n_edges_concordant
      .agg(['min', 'median', 'max', 'mean']).round(2).to_string())
