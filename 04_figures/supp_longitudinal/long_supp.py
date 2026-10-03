"""Every statistic in the longitudinal prediction analysis (IMAGEN FU3, n = 85).

a  baseline measured brain -> behaviour mapping
b  where the AMPA and GABA-A restoration indices sit relative to those measures
c  coefficients of the full model
d  incremental variance with permutation nulls
e  out-of-sample accuracy
All tests two-sided; correlations Pearson with Fisher-z 95% CI.
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, '../fig_color')
from np_dtb_style import (apply_np_style, panel, C, panel_title, enforce, LW,
                          LABEL_PT, ANNOT_PT, TICK_PT)
from supp_kit import saver, fill, pt_edge
apply_np_style()
D, P = 'data', 'panels'
manifest = []
save = saver(P, manifest)

CR = pd.read_csv(f'{D}/long_correlations_n85.csv')
CO = pd.read_csv(f'{D}/long_full_model_coefficients_n85.csv')
INC = pd.read_csv(f'{D}/long_nested_increments_n85.csv')
CV = pd.read_csv(f'{D}/long_cv_out_of_sample_n85.csv')
CVR = pd.read_csv(f'{D}/long_cv_repeats_n85.csv')
NUL = np.load(f'{D}/long_permutation_nulls.npz')

C_EMP, C_AMPA, C_GABA = C('np12'), C('ampa'), C('gaba')
ORDER_Y = ['Baseline behaviour 1', 'Baseline behaviour 2', 'Baseline behaviour 3',
           'Baseline behaviour 4', 'Baseline behaviour 5', 'Baseline behaviour 6',
           'Baseline symptom sum (4 model scores)', 'Baseline empirical NP (sum)',
           'FU3 symptom change']
SHORT = {'Baseline symptom sum (4 model scores)': 'Baseline symptom sum',
         'Baseline empirical NP (sum)': 'Baseline empirical NP'}


def forest_r(ax, sub, col, ys):
    for k, yy in enumerate(ys):
        r = sub[sub.y == yy]
        if not len(r):
            continue
        r = r.iloc[0]
        sig = r['q_bh_within_x'] < .05
        ax.plot([r['ci95_lo'], r['ci95_hi']], [k, k], color=col, lw=LW, zorder=2)
        ax.scatter(r['pearson_r'], k, s=20, facecolor=col if sig else 'white',
                   edgecolor=col, linewidth=LW, zorder=3)


# ------------------------------------------- a  baseline brain -> behaviour
W, H = 112, 60
fig, ax = plt.subplots(figsize=panel(W, H))
sub = CR[CR.x == 'Baseline empirical NP (sum)']
ys = [y for y in ORDER_Y if y != 'Baseline empirical NP (sum)']
forest_r(ax, sub, C_EMP, ys)
ax.axvline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_yticks(range(len(ys)))
ax.set_yticklabels([SHORT.get(y, y) for y in ys], fontsize=TICK_PT)
ax.set_xlabel('Pearson $r$ with baseline measured NP  (95% CI)')
ax.set_ylim(-.7, len(ys) - .3); ax.set_xlim(-.62, 1.02)
for k, yy in enumerate(ys):
    r = sub[sub.y == yy].iloc[0]
    ax.text(1.00, k, f"{r['pearson_r']:+.2f}   q = {r['q_bh_within_x']:.3f}", ha='right',
            va='center', fontsize=TICK_PT,
            color=C_EMP if r['q_bh_within_x'] < .05 else '0.45')
panel_title(ax, 'Measured baseline connectivity already maps onto symptoms and '
                'onto later change (n = 85)')
enforce(fig); save(fig, 'figS_long_a', W, H, 'long_correlations_n85.csv')

# ------------------------------------------- b  the two indices
W, H = 96, 60
fig, ax = plt.subplots(figsize=panel(W, H))
ys2 = [y for y in ORDER_Y if y != 'FU3 symptom change'] + ['FU3 symptom change']
for col, xn, dy in [(C_AMPA, 'AMPA index', -.17), (C_GABA, 'GABA-A index', .17)]:
    s2 = CR[CR.x == xn]
    for k, yy in enumerate(ys2):
        r = s2[s2.y == yy]
        if not len(r):
            continue
        r = r.iloc[0]
        ax.plot([r['ci95_lo'], r['ci95_hi']], [k + dy] * 2, color=col, lw=LW, zorder=2)
        ax.scatter(r['pearson_r'], k + dy, s=18,
                   facecolor=col if r['p_pearson'] < .05 else 'white',
                   edgecolor=col, linewidth=LW, zorder=3)
ax.axvline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.axhspan(len(ys2) - 1.5, len(ys2) - .5, color='#F0EDF7', zorder=0)
ax.set_yticks(range(len(ys2)))
ax.set_yticklabels([SHORT.get(y, y) for y in ys2], fontsize=TICK_PT)
ax.set_xlabel('Pearson $r$ with the restoration index  (95% CI)')
ax.set_ylim(-.7, len(ys2) - .3); ax.set_xlim(-.62, .62)
ax.legend([Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                  markerfacecolor=c, markeredgecolor=c) for c in (C_AMPA, C_GABA)],
          ['AMPA index', 'GABA-A index'], loc='lower left', fontsize=ANNOT_PT,
          frameon=False, handletextpad=.4)
panel_title(ax, 'Both indices track later change; neither is explained by '
                'baseline connectivity (filled = P < 0.05, uncorrected)')
enforce(fig); save(fig, 'figS_long_b', W, H, 'long_correlations_n85.csv')

# ------------------------------------------- c  full-model coefficients
W, H = 86, 52
fig, ax = plt.subplots(figsize=panel(W, H))
CO = CO.iloc[::-1].reset_index(drop=True)
for k, r in CO.iterrows():
    col = C_AMPA if 'AMPA' in r['predictor'] else C('reference')
    ax.plot([r['ci95_std_lo'], r['ci95_std_hi']], [k, k], color=col, lw=LW, zorder=2)
    ax.scatter(r['beta_std'], k, s=20, facecolor=col if r['p'] < .05 else 'white',
               edgecolor=col, linewidth=LW, zorder=3)
    ax.text(.62, k, f"P = {r['p']:.3f}", ha='right', va='center', fontsize=TICK_PT,
            color=col if r['p'] < .05 else '0.45')
ax.axvline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_yticks(range(len(CO)))
ax.set_yticklabels([p.replace('AMPA restoration index', 'AMPA restoration\nindex')
                    for p in CO.predictor], fontsize=TICK_PT)
ax.set_xlabel('Standardised $\\beta$  (95% CI)')
ax.set_xlim(-.66, .66); ax.set_ylim(-.7, len(CO) - .3)
panel_title(ax, 'Full model: $R^2$ = 0.233, $F$(5, 79) = 4.80, $P$ = 7.0 '
                '\u00d7 10$^{-4}$')
enforce(fig); save(fig, 'figS_long_c', W, H, 'long_full_model_coefficients_n85.csv')

# ------------------------------------------- d  increments vs permutation null
W, H = 110, 56
fig, ax = plt.subplots(figsize=panel(W, H))
keys = [('AMPA', '4 baseline behaviour scores'), ('GABA-A', '4 baseline behaviour scores'),
        ('AMPA', 'baseline empirical NP'), ('GABA-A', 'baseline empirical NP')]
for k, (inm, cnm) in enumerate(keys):
    null = NUL[f'{inm}|{cnm}']
    col = C_AMPA if inm == 'AMPA' else C_GABA
    vp = ax.violinplot([null], positions=[k], widths=.72, showextrema=False)
    for b in vp['bodies']:
        b.set_facecolor('0.85'); b.set_edgecolor('0.6'); b.set_linewidth(LW); b.set_alpha(.9)
    ax.hlines(np.percentile(null, 95), k - .36, k + .36, color='0.45', lw=LW,
              ls=(0, (2.2, 1.6)), zorder=3)
    r = INC[(INC['index'] == inm) & (INC.covariates == cnm)].iloc[0]
    ax.scatter([k], [r['delta_R2']], s=26, facecolor=col, edgecolor=pt_edge(col),
               linewidth=LW * .6, zorder=4)
    ax.text(k, r['delta_R2'] + .004,
            f"$\\Delta R^2$ = {r['delta_R2']:.3f}\n$P$ = {r['p_change']:.3f}\n"
            f"$P_{{perm}}$ = {r['p_perm_deltaR2']:.3f}", ha='center', va='bottom',
            fontsize=TICK_PT, linespacing=1.2, color=col)
ax.set_xticks(range(len(keys)))
ax.set_xticklabels([f"{i}\nover\n{'4 baseline' if c.startswith('4') else 'baseline NP'}"
                    for i, c in keys], fontsize=TICK_PT)
ax.set_ylabel('Incremental $R^2$')
ax.set_ylim(0, .105)
ax.text(-.45, np.percentile(NUL[f'{keys[0][0]}|{keys[0][1]}'], 95) + .001,
        '95th centile of the null', ha='left', va='bottom', fontsize=ANNOT_PT, color='0.45')
panel_title(ax, 'Incremental variance against its own permutation null '
                '(5,000 permutations of the outcome)')
enforce(fig); save(fig, 'figS_long_d', W, H, 'long_nested_increments_n85.csv')

# ------------------------------------------- e  out-of-sample accuracy
W, H = 86, 52
fig, ax = plt.subplots(figsize=panel(W, H))
mods = list(CVR.columns)
cols = [C('reference'), C_AMPA, C_GABA, C_EMP, C_AMPA]
rng = np.random.default_rng(1)
for k, m_ in enumerate(mods):
    v = CVR[m_].values
    ax.bar(k, v.mean(), width=.6, facecolor=fill(cols[k]), edgecolor=cols[k],
           linewidth=LW, zorder=2)
    ax.scatter(k + rng.uniform(-.13, .13, len(v)), v, s=5, facecolor=cols[k],
               edgecolor='none', alpha=.75, zorder=3)
    ax.text(k, v.max() + .006, f'{v.mean():.3f}', ha='center', va='bottom',
            fontsize=TICK_PT, color=cols[k])
ax.set_xticks(range(len(mods)))
ax.set_xticklabels([m_.replace(' + ', '\n+ ').replace('baseline ', 'baseline\n')
                    for m_ in mods], fontsize=TICK_PT)
ax.set_ylabel('Out-of-sample $R^2$')
ax.set_ylim(0, .175)
panel_title(ax, 'Out-of-sample accuracy, 10-fold cross-validation '
                '(points = 10 repeats)')
enforce(fig); save(fig, 'figS_long_e', W, H, 'long_cv_repeats_n85.csv')

pd.DataFrame(manifest).to_csv(f'{P}/long_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
