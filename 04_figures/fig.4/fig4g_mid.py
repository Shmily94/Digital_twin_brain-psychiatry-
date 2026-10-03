"""Fig. 4 companion | the response-pattern split recomputed on summed MID FC.

The response split is the one used in Fig. 4f-g -- both up / any down defined on
the 12-edge NP sum -- and is left unchanged here.  What changes is the measured
quantity: the in vivo healthy cohort in Fig. 5a-c is scanned on the 6 MID edges
only, so this panel reports the simulated MID sum for the same two groups, which
makes it directly comparable with Fig. 5c.  Drawn with the grammar of fig5.py's
level_panel() so the two panels are visually interchangeable.

    cd revision/text/figures/fig.4 && python fig4g_mid.py
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from fig_export import fig_to_pptx
apply_np_style()
D, OUTD = os.path.join(HERE, 'fig4_data'), os.path.join(HERE, 'panels')

M = pd.read_csv(f'{D}/fig4_mid_pattern_subject_n288.csv')
GRP = 'pattern_np'            # the Fig. 4 grouping, defined on the NP sum
PAT = ['both up', 'any down']
PCOL = {'both up': C('increased'), 'any down': C('decreased')}


def _lum(c):
    r, g, b = mcolors.to_rgb(c); return .2126 * r + .7152 * g + .0722 * b


def _fill(c):
    rgb = np.array(mcolors.to_rgb(c)); f = .35 if _lum(c) > .70 else .45
    return tuple(1 - f * (1 - rgb))


def _pt_edge(c):
    return tuple(np.array(mcolors.to_rgb(c)) * .55) if _lum(c) > .70 else 'none'


W, H = 48, 54
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [M.loc[M[GRP] == p, 'mid_baseline'].values for p in PAT]
bp = ax.boxplot(vals, positions=[0, 1], widths=.62, showfliers=False, patch_artist=True)
for el in ('boxes', 'whiskers', 'caps', 'medians'):
    for art in bp[el]:
        art.set_linewidth(LW); art.set_color('black')
rng = np.random.default_rng(8)
for i, v in enumerate(vals):
    bp['boxes'][i].set_facecolor(_fill(PCOL[PAT[i]])); bp['boxes'][i].set_edgecolor('black')
    ax.scatter(i + rng.uniform(-.15, .15, len(v)), v, s=4.5, facecolor=PCOL[PAT[i]],
               edgecolor=_pt_edge(PCOL[PAT[i]]), linewidth=LW * .5, alpha=.85, zorder=3)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
t_, p_ = stats.ttest_ind(*vals, equal_var=False)
hi = max(v.max() for v in vals); lo = min(v.min() for v in vals); span = hi - lo
ax.plot([0, 0, 1, 1], [hi + span * .08, hi + span * .13, hi + span * .13, hi + span * .08],
        color='black', lw=LW, clip_on=False)
ax.text(.5, hi + span * .145, f'$P$ = {p_:.0e}', ha='center', va='bottom', fontsize=ANNOT_PT)
ax.set_ylim(lo - span * .10, hi + span * .30)
ax.set_xticks([0, 1])
ax.set_xticklabels([f'both up\n(n = {len(vals[0])})', f'any down\n(n = {len(vals[1])})'],
                   fontsize=TICK_PT)
ax.set_xlim(-.75, 1.75)
ax.set_ylabel('Simulated baseline MID FC')
panel_title(ax, 'Digital twins, same split as Fig. 4f')
enforce(fig)
fig.savefig(f'{OUTD}/fig4g_mid.png', dpi=400, bbox_inches='tight')
fig.savefig(f'{OUTD}/fig4g_mid.pdf', bbox_inches='tight')
fig_to_pptx(fig, f'{OUTD}/fig4g_mid.pptx', dpi=400)
px = Image.open(f'{OUTD}/fig4g_mid.png').size
print('fig4g_mid', px, 'dpi', round(px[0] / (W / 25.4)),
      '| both up', len(vals[0]), 'any down', len(vals[1]),
      f'| Welch t = {t_:.2f}, P = {p_:.3g}')
