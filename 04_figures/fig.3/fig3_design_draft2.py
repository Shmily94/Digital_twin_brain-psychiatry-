"""DRAFT v2 - two replacements for the hard-to-read contrast panel.
A : the four steps drawn AS ARROWS ON THE DESIGN MAP (one panel, no statistics axis)
B : map + a slope chart on the natural BOLD r scale (two panels)
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
sys.path.insert(0, '../fig_color')
from np_dtb_style import apply_np_style, panel, C, panel_title, enforce, LW, \
    LABEL_PT, ANNOT_PT, TICK_PT
apply_np_style()
D = 'fig3_data'
ch = pd.read_csv(f'{D}/fig3_design_chain_contrasts.csv')
bold = pd.read_csv(f'{D}/fig3i_assimilated_bold_r.csv').groupby('model').bold_r.mean()
FAM = {'regional': C('model_regional'), 'voxel': C('model_voxel')}
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
    'f', ['#FFFFFF', C('model_mid')])
SPACE = [('3m_268', 0, 0, '3 M', 'regional'), ('10m_268', 0, 0, '10 M', 'regional'),
         ('10m_1000', 1, 1, '10 M', 'regional'), ('10m_own', 2, 2, '10 M', 'voxel'),
         ('10m', 2, 3, '10 M', 'voxel'), ('100m', 2, 3, '100 M', 'voxel'),
         ('1b', 2, 3, '1 B', 'voxel')]
XL = ['268 regions', '1000 regions', 'voxel']
YL = ['3 M', '10 M / 1000', '10 M voxel', '100 M']
POS = {}


def draw_map(ax, arrows=False):
    for y in (0, 3):
        ax.axhspan(y - .42, y + .42, color='#F0EDF7', zorder=0)
    seen = {}
    for b, x, y, n, fam in SPACE:
        k = (x, y); i = seen.get(k, 0); seen[k] = i + 1
        tot = sum(1 for s in SPACE if (s[1], s[2]) == k)
        dx = (i - (tot - 1) / 2) * .30
        POS[b] = (x + dx, y)
        r = bold[b]
        ax.scatter(x + dx, y, s=175, facecolor=cmap((r - .6) / .4),
                   edgecolor=FAM[fam], linewidth=LW * 1.6, zorder=3)
        ax.text(x + dx, y - .30, n, ha='center', va='top', fontsize=TICK_PT,
                color=FAM[fam])
        ax.text(x + dx, y, f'{r:.2f}', ha='center', va='center', fontsize=TICK_PT,
                color='white' if r > .85 else 'black', zorder=4)
    ax.set_xticks(range(3)); ax.set_xticklabels(XL, fontsize=TICK_PT)
    ax.set_yticks(range(4)); ax.set_yticklabels(YL, fontsize=TICK_PT)
    ax.set_xlabel('Simulation target', fontsize=LABEL_PT)
    ax.set_ylabel('Assimilated hyper-parameters', fontsize=LABEL_PT)
    ax.set_xlim(-.7, 2.95); ax.set_ylim(-.8, 3.7)
    for y, lab in ((0, 'works'), (3, 'works')):
        ax.text(2.92, y, lab, ha='right', va='center', fontsize=ANNOT_PT, color='0.35')


STEPS = [('1', '10m_own', '10m',      'assimilate at 100 M', '+0.12'),
         ('2', '10m_own', '10m_1000', 'coarsen to 1000',     '\u22120.09'),
         ('3', '10m_1000', '10m_268', 'coarsen to 268',      '+0.23'),
         ('4', '10m_268', '3m_268',   'fewer neurons',       '\u00b10.00')]

# ---------------- A : arrows on the map -------------------------------------
figA, ax = plt.subplots(figsize=panel(104, 64))
draw_map(ax)
RAD = {'1': .0, '2': -.32, '3': -.28, '4': -.55}
for n, a, b, lab, dlt in STEPS:
    (x0, y0), (x1, y1) = POS[a], POS[b]
    col = '#333333' if dlt.startswith('+') else ('#999999' if dlt.startswith('\u00b1') else '#B05A7A')
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), connectionstyle=f'arc3,rad={RAD[n]}',
                                 arrowstyle='-|>', mutation_scale=7, lw=LW * 1.5,
                                 color=col, shrinkA=9, shrinkB=9, zorder=5))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = (.30, 0) if n == '1' else (-.05, .22) if n == '2' else (0, .26) if n == '3' else (0, -.42)
    ax.text(mx + ox, my + oy, f'{n}  {lab}\n\u0394 BOLD r {dlt}', ha='center', va='center',
            fontsize=TICK_PT, color=col, zorder=6,
            bbox=dict(fc='white', ec='none', alpha=.82, pad=.8))
panel_title(ax, 'The narrative as a path through the design space')
enforce(figA)
figA.savefig('panels/fig3_design_draftA.png', dpi=400, bbox_inches='tight')

# ---------------- B : map + slope chart -------------------------------------
figB, axs = plt.subplots(1, 2, figsize=panel(180, 64),
                         gridspec_kw=dict(width_ratios=[1.1, 1]))
draw_map(axs[0])
panel_title(axs[0], 'Only two corners of the design space assimilate well')
ax = axs[1]
for i, (n, a, b, lab, dlt) in enumerate(STEPS):
    ya, yb = bold[a], bold[b]
    col = '#333333' if yb > ya + .005 else ('#999999' if abs(yb - ya) <= .005 else '#B05A7A')
    ax.plot([i - .17, i + .17], [ya, yb], color=col, lw=LW * 1.8, zorder=2)
    ax.scatter([i - .17, i + .17], [ya, yb], s=26, facecolor='white',
               edgecolor=col, linewidth=LW * 1.4, zorder=3)
    ax.text(i - .17, ya - .018, f'{ya:.2f}', ha='center', va='top', fontsize=TICK_PT, color=col)
    ax.text(i + .17, yb + .014, f'{yb:.2f}', ha='center', va='bottom', fontsize=TICK_PT, color=col)
    p = ch[(ch.step.str.startswith(n)) & (ch.metric == 'assimilated BOLD r')].t_p.iloc[0]
    ax.text(i, .625, f'P = {p:.0e}' if p < .001 else f'P = {p:.2f}', ha='center',
            va='bottom', fontsize=TICK_PT, color='0.35')
ax.set_xticks(range(4))
ax.set_xticklabels([f'{n}\n{lab}' for n, _, _, lab, _ in STEPS], fontsize=TICK_PT)
ax.set_ylabel('Assimilated BOLD $r$', fontsize=LABEL_PT)
ax.set_ylim(.60, .98); ax.set_xlim(-.5, 3.5)
panel_title(ax, 'One design factor changed per step (left dot = before, right = after)')
enforce(figB)
figB.tight_layout()
figB.savefig('panels/fig3_design_draftB.png', dpi=400, bbox_inches='tight')
print('written A and B')
