"""Comparison of meta-analytic and activation-defined assimilation regions:
spatial overlap and simulation accuracy for each region set.

Sources (revision/sensitivity_analysis/assimilated_region/):
  assimilation_set_comparison_summary.csv   - per-set size, overlap, composition
  region_set_overlap_and_accuracy.csv       - parcel- and voxel-level Dice, simulated set
  activation_vs_meta_accuracy.csv           - whole-connectome accuracy, meta (5 runs) vs act
  baseline_100M_prior_FC_accuracy_by_class.csv - accuracy by assimilation status of the edge
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, '../fig_color')
from np_dtb_style import (apply_np_style, panel, C, panel_title, enforce, LW,
                          LABEL_PT, ANNOT_PT, TICK_PT)
sys.path.insert(0, '../fig_color')
from supp_kit import saver
apply_np_style()
D, P = 'data', 'panels'
manifest = []
save = saver(P, manifest)

CS = pd.read_csv(f'{D}/assimregion_set_summary.csv')
OV = pd.read_csv(f'{D}/assimregion_overlap_simulated_sets.csv')
AC = pd.read_csv(f'{D}/assimregion_simulation_accuracy.csv')
EC = pd.read_csv(f'{D}/assimregion_accuracy_by_edge_class.csv')

# Colour grammar: the meta-analytic (prior) set is the reference condition -> grey;
# every activation-defined alternative is one hue, two tones for the two tasks.
C_PRIOR = C('reference')
C_MID, C_SST = C('model_regional'), C('model_voxel')
SETS = ['prior', 'act_Nmatched', 'act_voxmatched', 'act_thresh', 'act_strict', 'hybrid']
SLAB = {'prior': 'meta-\nanalytic', 'act_Nmatched': 'activation,\nregion-matched',
        'act_voxmatched': 'activation,\nvoxel-matched', 'act_thresh': 'activation,\nT \u2265 5',
        'act_strict': 'activation,\nstrict', 'hybrid': 'activation +\ntask-general'}

# ---------------------------------------------------------------- a  overlap
W, H = 124, 54
fig, ax = plt.subplots(figsize=panel(W, H))
x = np.arange(len(SETS))
for k, (tk, col) in enumerate([('MID', C_MID), ('SST', C_SST)]):
    sub = CS[CS.task == tk].set_index('set').reindex(SETS)
    ax.bar(x + (k - .5) * .38, sub.dice_with_prior, width=.36,
           facecolor=(*plt.matplotlib.colors.to_rgb(col), .35), edgecolor=col,
           linewidth=LW, zorder=2)
    for xi, v, n in zip(x + (k - .5) * .38, sub.dice_with_prior, sub.n_overlap_prior):
        if np.isfinite(v):
            ax.text(xi, v + 2, f'{int(n)}', ha='center', va='bottom',
                    fontsize=TICK_PT, color=col)
ax.set_xticks(x); ax.set_xticklabels([SLAB[s] for s in SETS], fontsize=TICK_PT)
ax.get_xticklabels()[0].set_color(C_PRIOR)
ax.set_ylabel('Overlap with the meta-analytic set\n(Dice, %)')
ax.set_ylim(0, 112)
ax.axhline(100, color='0.85', lw=LW, zorder=0)
ax.legend([Line2D([], [], marker='s', linestyle='none', markersize=3.4,
                  markerfacecolor=c, markeredgecolor=c) for c in (C_MID, C_SST)],
          ['Reward task (MID)', 'Inhibition task (SST)'], loc='upper right',
          fontsize=ANNOT_PT, frameon=False, handletextpad=.4)
panel_title(ax, 'No activation-defined set recovers the meta-analytic regions '
                '(number above bar = shared parcels)')
enforce(fig); save(fig, 'figS_assimreg_a', W, H, 'assimregion_set_summary.csv')

# ------------------------------------------------------- b  composition
W, H = 124, 54
fig, ax = plt.subplots(figsize=panel(W, H))
for k, (tk, col) in enumerate([('MID', C_MID), ('SST', C_SST)]):
    sub = CS[CS.task == tk].set_index('set').reindex(SETS)
    pct = 100 * sub.n_subcortical / sub.n_regions
    ax.bar(x + (k - .5) * .38, pct, width=.36,
           facecolor=(*plt.matplotlib.colors.to_rgb(col), .35), edgecolor=col,
           linewidth=LW, zorder=2)
    for xi, v, n in zip(x + (k - .5) * .38, pct, sub.n_subcortical):
        if np.isfinite(v):
            ax.text(xi, v + 1.2, f'{int(n)}', ha='center', va='bottom',
                    fontsize=TICK_PT, color=col)
ax.set_xticks(x); ax.set_xticklabels([SLAB[s] for s in SETS], fontsize=TICK_PT)
ax.get_xticklabels()[0].set_color(C_PRIOR)
ax.set_ylabel('Subcortical regions in the set (%)')
ax.set_ylim(0, 58)
panel_title(ax, 'Activation-defined selection removes almost all subcortical '
                'territory (number above bar = subcortical parcels)')
enforce(fig); save(fig, 'figS_assimreg_b', W, H, 'assimregion_set_summary.csv')

# ------------------------------------------- c  simulation accuracy
W, H = 84, 54
fig, ax = plt.subplots(figsize=panel(W, H))
xc = np.arange(len(AC))
for i, r in AC.iterrows():
    ax.errorbar(i - .13, r['meta_mean'], yerr=r['meta_sd'], fmt='o', markersize=3.4,
                color=C_PRIOR, markerfacecolor='white', markeredgecolor=C_PRIOR,
                markeredgewidth=LW, elinewidth=LW, capsize=2.0, capthick=LW, zorder=3)
    ax.scatter(i + .13, r['act'], s=22, marker='s', facecolor='white',
               edgecolor=C_MID, linewidth=LW, zorder=3)
    ax.text(i, max(r['meta_mean'], r['act']) + .0022,
            f'$\\Delta$r = {r["delta"]:+.3f} ({r["pct_change"]:+.1f} %)', ha='center',
            va='bottom', fontsize=TICK_PT, color='0.35')
ax.set_xticks(xc)
ax.set_xticklabels([s.replace('-', '\n') for s in AC.condition], fontsize=TICK_PT)
ax.set_ylabel('Whole-connectome accuracy\n(Pearson $r$ vs empirical task FC)')
ax.set_ylim(.696, .724)
ax.set_xlim(-.55, len(AC) - .45)
ax.legend([Line2D([], [], marker='o', linestyle='none', markersize=3.4,
                  markerfacecolor='white', markeredgecolor=C_PRIOR, markeredgewidth=LW),
           Line2D([], [], marker='s', linestyle='none', markersize=3.4,
                  markerfacecolor='white', markeredgecolor=C_MID, markeredgewidth=LW)],
          ['meta-analytic (5 runs, mean \u00b1 s.d.)', 'activation, voxel-matched (1 run)'],
          loc='upper center', fontsize=ANNOT_PT, frameon=False, handletextpad=.4)
panel_title(ax, 'Swapping in activation-defined regions does not improve accuracy')
enforce(fig); save(fig, 'figS_assimreg_c', W, H, 'assimregion_simulation_accuracy.csv')

# ------------------------------- d  why the comparison must be held out
W, H = 74, 52
fig, ax = plt.subplots(figsize=panel(W, H))
EC = EC.set_index('edge_class').loc[['both', 'one', 'neither', 'all']].reset_index()
cols = [C('np12'), C('model_mid'), C('non_np'), C_PRIOR]
ax.bar(np.arange(len(EC)), EC.r_emp_sim, width=.6,
       facecolor=[(*plt.matplotlib.colors.to_rgb(c), .35) for c in cols],
       edgecolor=cols, linewidth=LW, zorder=2)
for i, (v, n) in enumerate(zip(EC.r_emp_sim, EC.n_edges)):
    ax.text(i, v + .02, f'{v:.2f}\nn = {n:,}', ha='center', va='bottom',
            fontsize=TICK_PT, color=cols[i])
ax.set_xticks(range(len(EC)))
ax.set_xticklabels(['both\nendpoints', 'one\nendpoint', 'neither', 'whole\nbrain'],
                   fontsize=TICK_PT)
ax.set_ylabel('Simulated vs empirical FC ($r$)')
ax.set_ylim(0, 1.18)
panel_title(ax, 'Accuracy is set by assimilation status, so any unmatched '
                'comparison is circular')
enforce(fig); save(fig, 'figS_assimreg_d', W, H, 'assimregion_accuracy_by_edge_class.csv')

pd.DataFrame(manifest).to_csv(f'{P}/assimregion_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
