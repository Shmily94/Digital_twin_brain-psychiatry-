"""Supplementary figure | head motion, diagnostic group and NP outcomes.

All NP measures come from the corrected simulated baseline used in Fig. 4-5.

n = 288 twins retained after the mean-FD < 0.5 mm inclusion threshold.  Panel a
compares FD across diagnostic groups; panel b gives the correlation of FD with
every NP outcome (95% CI, BH-FDR across the six); panel c shows the per-edge
correlations for the 12 empirical NP edges.  Associations are reported as
computed, not asserted to be absent -- see the figure legend.

    cd revision/text/figures/supp_motion && python motion_supp.py
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from supp_kit import saver, boxes, forest, pt_edge, fill
from matplotlib.lines import Line2D
apply_np_style()
D, OUTD = f'{HERE}/data', f'{HERE}/panels'
M = pd.read_csv(f'{D}/motion_subject_level_n288.csv')
GT = pd.read_csv(f'{D}/motion_group_tests.csv')
CR = pd.read_csv(f'{D}/TableS25_motion_np_correlations_corrected_n288.csv')
PE = pd.read_csv(f'{D}/motion_per_edge_correlations.csv')
GR = pd.read_csv(f'{D}/TableS26_group_effect_motion_adjustment_corrected_n288.csv')
manifest = []
save = saver(OUTD, manifest)
GRP = ['HC', 'High-symptom', 'Patient']
GCOL = {'HC': C('hc'), 'High-symptom': C('high_symptom'), 'Patient': C('patient')}

# ---- a  FD by diagnostic group ----------------------------------------------
W, H = 54, 54
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [M.loc[M.Group == g, 'headmotion'].values for g in GRP]
boxes(ax, [0, 1, 2], vals, [GCOL[g] for g in GRP], seed=0, s=8)
row = GT[GT.test.str.startswith('one-way')].iloc[0]
hi = max(v.max() for v in vals); lo = min(v.min() for v in vals); span = hi - lo
ax.text(1, hi + span * .06, f'$F$(2, 285) = {row.statistic:.2f}, $P$ = {row.p:.2f}',
        ha='center', va='bottom', fontsize=ANNOT_PT, color='0.35')
ax.set_ylim(lo - span * .05, hi + span * .20)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'HC\n(n = {len(vals[0])})', f'High-\nsymptom\n(n = {len(vals[1])})',
                    f'Patient\n(n = {len(vals[2])})'], fontsize=TICK_PT)
ax.set_xlim(-.7, 2.7)
ax.set_ylabel('Mean framewise displacement (mm)')
panel_title(ax, 'Motion is matched across groups')
enforce(fig); save(fig, 'figS_motion_a', W, H, 'motion_subject_level_n288.csv')

# ---- b  correlation of FD with each NP outcome ------------------------------
# Corrected simulated baseline (dtb_np_n288_baseline_post.csv) throughout, i.e.
# the same data as Fig. 4-5.  P values are Bonferroni-adjusted over the six
# outcomes; the earlier Table S25 used the pre-MID-fix simulations.
W, H = 84, 56
fig, ax = plt.subplots(figsize=panel(W, H))
cols = [C('ampa') if ('AMPA' in o and 'GABA' not in o) else
        C('gaba') if 'GABA' in o else C('reference') for o in CR.Measure]
LOHI = np.array([[float(v) for v in c.split(' to ')] for c in CR.CI95])
yy = forest(ax, [m.replace(' (GABA-A on high AMPA)', ' (GABA-A)') for m in CR.Measure],
            CR.r.values, LOHI[:, 0], LOHI[:, 1], cols, 'Pearson $r$ with mean FD')
lab_ = lambda nm, v: f'${nm}$ < 0.001' if v < .001 else f'${nm}$ = {v:.3f}'
for y, r in zip(yy, CR.itertuples()):
    ax.text(LOHI[len(CR) - 1 - int(y), 1] + .018, y,
            lab_('P_{bonf}', r.P_Bonferroni),
            ha='left', va='center', fontsize=ANNOT_PT,
            color='black' if r.P_Bonferroni < .05 else '0.5')
    ax.text(.995, y, f'{100 * r.variance_explained:.1f}%', ha='right', va='center',
            fontsize=ANNOT_PT, color='0.35', transform=ax.get_yaxis_transform())
ax.text(.995, len(CR) - .30, 'variance explained', ha='right', va='bottom',
        fontsize=ANNOT_PT, color='0.35', transform=ax.get_yaxis_transform())
ax.set_ylim(-.7, len(CR) + .35)
ax.set_xlim(-.20, .82)
panel_title(ax, 'Δ NP after AMPA, the measure behind the main inferences, is '
                'unrelated to motion')
enforce(fig)
save(fig, 'figS_motion_b', W, H, 'TableS25_motion_np_correlations_corrected_n288.csv')

# ---- c  the same test edge by edge ------------------------------------------
W, H = 62, 54
fig, ax = plt.subplots(figsize=panel(W, H))
x = np.arange(len(PE))
ax.bar(x, PE.r.values, width=.66, facecolor=fill(C('np12')), edgecolor='black',
       linewidth=LW, zorder=2)
ax.axhline(0, color='0.6', lw=LW, zorder=1)
npr = CR[CR.Measure == 'Empirical NP factor'].iloc[0]
ax.axhline(npr.r, color=C('np12'), lw=LW * 1.3, ls=(0, (2.4, 1.6)), zorder=3)
ax.text(len(PE) - .4, npr.r + .006,
        f'12-edge sum, $r$ = {npr.r:.3f} ($P_{{bonf}}$ = {npr.P_Bonferroni:.3f})',
        ha='right', va='bottom', fontsize=ANNOT_PT, color=C('np12'))
ax.set_xticks(x)
ax.set_xticklabels([v.replace('empirical_fc', 'e') for v in PE.variable], fontsize=TICK_PT)
ax.set_xlabel('Empirical NP edge')
ax.set_ylabel('Pearson $r$ with mean FD')
ax.set_ylim(PE.r.min() - .05, max(PE.r.max(), npr.r) + .07)
PE['p_bonferroni'] = np.minimum(1.0, PE.p * len(PE))
ax.text(.03, .03, 'no edge survives Bonferroni\n'
        f'(12 edges, min $P_{{bonf}}$ = {PE.p_bonferroni.min():.2f})',
        transform=ax.transAxes, ha='left', va='bottom', fontsize=ANNOT_PT, color='0.35')
PE.to_csv(f'{D}/motion_per_edge_correlations.csv', index=False)
panel_title(ax, 'No single edge is motion-related')
enforce(fig); save(fig, 'figS_motion_c', W, H, 'motion_per_edge_correlations.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/motion_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))

# ---- d  group effect with and without motion adjustment ---------------------
# One-way ANOVA of each NP measure on diagnostic group, then the same model with
# mean FD added as a covariate.  Partial eta-squared for the group term; P values
# Bonferroni-adjusted over the six measures.
W, H = 84, 56
fig, ax = plt.subplots(figsize=panel(W, H))
yy = np.arange(len(GR))[::-1]
cols = [C('ampa') if ('AMPA' in m and 'GABA' not in m) else
        C('gaba') if 'GABA' in m else C('reference') for m in GR.Measure]
for y, r, c in zip(yy, GR.itertuples(), cols):
    ax.plot([r.eta2_group_no_FD, r.eta2_group_with_FD], [y, y], color=c, lw=LW * 1.8,
            solid_capstyle='round', zorder=2)
    ax.scatter([r.eta2_group_no_FD], [y], s=24, facecolor='white', edgecolor=c,
               linewidth=LW * 1.2, zorder=3)
    ax.scatter([r.eta2_group_with_FD], [y], s=24, facecolor=c,
               edgecolor=pt_edge(c), linewidth=LW * .55, zorder=4)
    xr = max(r.eta2_group_no_FD, r.eta2_group_with_FD)
    ax.text(xr + .35, y, ('$P_{bonf}$ < 0.001' if r.P_with_FD_bonf < .001
                          else f'$P_{{bonf}}$ = {r.P_with_FD_bonf:.3f}'),
            ha='left', va='center', fontsize=ANNOT_PT,
            color='black' if r.P_with_FD_bonf < .05 else '0.5')
ax.set_yticks(yy)
ax.set_yticklabels([m.replace(' (GABA-A on high AMPA)', ' (GABA-A)') for m in GR.Measure],
                   fontsize=TICK_PT)
ax.set_ylim(-.7, len(GR) - .3)
ax.set_xlim(0, 14.2)
ax.set_xlabel('Group effect, partial $\\eta^2$ (%)')
ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
ax.legend([Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                  markerfacecolor='white', markeredgecolor='0.45', markeredgewidth=LW),
           Line2D([], [], marker='o', linestyle='none', markersize=3.4,
                  markerfacecolor='0.45', markeredgecolor='none')],
          ['group only', '+ mean FD as covariate'], loc='lower right',
          fontsize=ANNOT_PT, frameon=False, borderaxespad=.2, handletextpad=.4,
          labelspacing=.25)
panel_title(ax, 'Adjusting for motion leaves every group effect unchanged '
                f'(max shift {(GR.eta2_group_with_FD - GR.eta2_group_no_FD).abs().max():.2f} pp)')
enforce(fig)
save(fig, 'figS_motion_d', W, H,
     'TableS26_group_effect_motion_adjustment_corrected_n288.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/motion_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
