"""DRAFT (unpolished) - two candidate ways to carry the design-space argument.
Left  : the design space itself, assimilation configuration x simulation target.
Right : the four one-factor-at-a-time contrasts that the narrative walks through.
Run after fig3.py has written fig3_data/.  Nothing here is final styling.
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
sys.path.insert(0, '../fig_color')
from np_dtb_style import apply_np_style, panel, C, panel_title, enforce, LW, \
    LABEL_PT, ANNOT_PT, TICK_PT
apply_np_style()
D = 'fig3_data'
ch = pd.read_csv(f'{D}/fig3_design_chain_contrasts.csv')
bi = pd.read_csv(f'{D}/fig3i_assimilated_bold_r.csv')
bold = bi.groupby('model').bold_r.mean()

FAM = {'regional': C('model_regional'), 'voxel': C('model_voxel')}
# (build, x = simulation target, y = assimilation config, simulated neurons, family)
SPACE = [('3m_268',   0, 0, '3 M',   'regional'),
         ('10m_268',  0, 0, '10 M',  'regional'),
         ('10m_1000', 1, 1, '10 M',  'regional'),
         ('10m_own',  2, 2, '10 M',  'voxel'),
         ('10m',      2, 3, '10 M',  'voxel'),
         ('100m',     2, 3, '100 M', 'voxel'),
         ('1b',       2, 3, '1 B',   'voxel')]
XL = ['268 regions', '1000 regions', 'voxel']
YL = ['3 M', '10 M / 1000', '10 M voxel', '100 M']

fig, axs = plt.subplots(1, 2, figsize=panel(180, 62),
                        gridspec_kw=dict(width_ratios=[1.05, 1]))

# ---- left: design space -----------------------------------------------------
ax = axs[0]
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list(
    'f', ['#FFFFFF', C('model_mid')])
for y in (0, 3):                       # the two working assimilation configs
    ax.axhspan(y - .42, y + .42, color='#F0EDF7', zorder=0)
seen = {}
for b, x, y, n, fam in SPACE:
    k = (x, y); i = seen.get(k, 0); seen[k] = i + 1
    tot = sum(1 for s in SPACE if (s[1], s[2]) == k)
    dx = (i - (tot - 1) / 2) * .30
    r = bold[b]
    ax.scatter(x + dx, y, s=170, marker='o', facecolor=cmap((r - .6) / .4),
               edgecolor=FAM[fam], linewidth=LW * 1.6, zorder=3)
    ax.text(x + dx, y - .30, n, ha='center', va='top', fontsize=TICK_PT,
            color=FAM[fam])
    ax.text(x + dx, y, f'{r:.2f}', ha='center', va='center', fontsize=TICK_PT,
            color='white' if r > .85 else 'black', zorder=4)
ax.set_xticks(range(3)); ax.set_xticklabels(XL, fontsize=TICK_PT)
ax.set_yticks(range(4)); ax.set_yticklabels(YL, fontsize=TICK_PT)
ax.set_xlabel('Simulation target', fontsize=LABEL_PT)
ax.set_ylabel('Assimilated hyper-parameters', fontsize=LABEL_PT)
ax.set_xlim(-.6, 2.75); ax.set_ylim(-.75, 3.6)
ax.text(2.7, 0, 'works', ha='right', va='center', fontsize=ANNOT_PT, color='0.35')
ax.text(2.7, 3, 'works', ha='right', va='center', fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Only two corners of the design space assimilate well '
                '(number in marker = BOLD r; label below = simulated neurons)')

# ---- right: the four contrasts ---------------------------------------------
ax = axs[1]
MET = {'assimilated BOLD r': ('o', C('model_voxel')),
       'NP-edge MSE': ('s', C('model_regional')),
       'whole-brain FC r': ('^', C('np12'))}
steps = list(dict.fromkeys(ch.step))
for i, st in enumerate(steps):
    sub = ch[ch.step == st]
    for j, (_, r) in enumerate(sub.iterrows()):
        mk, col = MET[r.metric]
        # sign-align: positive dz always means "the change helped"
        dz = r.dz if r.direction != 'lower' else -r.dz
        yy = len(steps) - 1 - i + (j - (len(sub) - 1) / 2) * .24
        ax.scatter(dz, yy, s=22, marker=mk, facecolor='white', edgecolor=col,
                   linewidth=LW * 1.4, zorder=3)
        ax.text(dz, yy + .10, f'P = {r.t_p:.0e}' if r.t_p < .001 else f'P = {r.t_p:.2f}',
                ha='center', va='bottom', fontsize=TICK_PT, color=col)
ax.axvline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_yticks(range(len(steps))[::-1])
ax.set_yticklabels([s[3:] for s in steps], fontsize=TICK_PT)
ax.set_xlabel('Paired effect $d_z$  (positive = the change improved the model)',
              fontsize=LABEL_PT)
ax.set_xlim(-3.5, 13)
h = [plt.Line2D([], [], marker=m, linestyle='none', markersize=3.4,
                markerfacecolor='white', markeredgecolor=c, markeredgewidth=LW)
     for m, c in MET.values()]
ax.legend(h, list(MET), loc='lower right', fontsize=ANNOT_PT, frameon=False,
          handletextpad=.3)
panel_title(ax, 'Every step in the narrative, one design factor at a time')
for a in axs:
    enforce(fig)
fig.tight_layout()
fig.savefig('panels/fig3_design_draft.png', dpi=400, bbox_inches='tight')
print('written panels/fig3_design_draft.png')
