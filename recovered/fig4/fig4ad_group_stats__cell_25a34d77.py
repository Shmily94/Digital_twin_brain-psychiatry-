# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4ad_group_stats.csv
#
# cell id      : 25a34d77-b2b2-48f2-adde-bfe6ba7196f5
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:06:48 UTC
# conda env    : python
# language     : diff
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/10_fig4ad_group_stats.py
##############################################################################
# [edit_file] created /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4.py
+++ /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4.py
+"""Figure 4 | Virtual perturbation of the digital twins (n = 288).
+
+ONE FILE PER PANEL -> ./panels/ as .png (400 dpi), .pdf (vector) and .pptx.
+
+  a  empirical NP by group
+  b  simulated baseline NP by group
+  c  NP after AMPA up-regulation, by group
+  d  NP after GABA-A up-regulation, by group
+  e  distribution of the four conditions across the whole cohort
+  f  per-twin response: delta NP under AMPA vs under GABA-A
+  g  who shows the 'both up' pattern, and what their baseline looks like
+  h  SDQ symptom items compared between the two response patterns
+
+Cohort: the 290-subject modulation sample minus the two twins with head motion
+> 0.5 mm -> n = 288 (HC 69, high-symptom 89, patient 130).  Panels a-d use NP
+residualised on sex, recruitment site and mean head motion, REFIT on these 288
+(the stored *_resid columns of the source table were fitted on 290).  Deltas in
+f-h are raw perturbed - baseline, because residualising the two conditions
+separately does not preserve the within-subject difference.
+
+Colours: ../fig_color/np_dtb_style.py (USER_PALETTE).  HC grey, high-symptom
+#E69F00, patient #D55E00; AMPA #E1D09A, GABA-A #96B9AD; response patterns
+#D9A5B3 (increased) and #8DA0B4 (decreased).
+
+    cd revision/text/figures/fig.4 && python fig4.py
+"""
+import os, sys
+import numpy as np
+import pandas as pd
+import matplotlib.pyplot as plt
+from matplotlib.lines import Line2D
+from matplotlib.patches import Patch
+from scipy import stats
+from scipy.stats import gaussian_kde
+from statsmodels.stats.multitest import multipletests
+import statsmodels.formula.api as smf
+from PIL import Image
+
+HERE = os.path.dirname(os.path.abspath(__file__))
+sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
+from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
+                          LABEL_PT, panel_title, enforce)
+from fig_export import fig_to_pptx
+
+D = os.path.join(HERE, 'fig4_data')
+OUTD = os.path.join(HERE, 'panels')
+os.makedirs(OUTD, exist_ok=True)
+DPI = 400
+apply_np_style()
+
+GRP = ['HC', 'High-symptom', 'Patient']
+GCOL = {'HC': C('hc'), 'High-symptom': C('high_symptom'), 'Patient': C('patient')}
+PAT = ['both up', 'any down']
+PCOL = {'both up': C('increased'), 'any down': C('decreased')}
+COND = [('empirical', 'Empirical', 'black', (0, (2.6, 1.7))),
+        ('simulated', 'Simulated baseline', C('baseline'), '-'),
+        ('ampa', 'After AMPA', C('ampa'), '-'),
+        ('gaba', 'After GABA-A', C('gaba'), '-')]
+manifest = []
+
+T = pd.read_csv(f'{D}/fig4_subject_level_n288.csv')
+S = pd.read_csv(f'{D}/fig4_sdq_items_n287.csv')
+SDQ = [c for c in S.columns if c not in ('ID', 'pattern', 'Group')]
+assert len(T) == 288 and set(T.Group) == set(GRP)
+
+# residuals refit on these 288 (see docstring)
+for c in ['empirical', 'simulated', 'ampa', 'gaba']:
+    T[c + '_r'] = smf.ols(f'{c} ~ C(sex)+C(site)+headmotion', data=T).fit().resid
+
+
+def save(fig, stem, w_mm, h_mm, note):
+    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
+    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
+    fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)
+    px = Image.open(f'{OUTD}/{stem}.png').size
+    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
+                         png_px=f'{px[0]}x{px[1]}',
+                         dpi=round(px[0] / (w_mm / 25.4)), source=note))
+    plt.close(fig)
+
+
+def box_points(ax, groups, values, colours, width=.55, jitter=.14, seed=0, s=3.2):
+    rng = np.random.default_rng(seed)
+    bp = ax.boxplot(values, positions=np.arange(len(groups)), widths=width,
+                    showfliers=False, patch_artist=True)
+    for el in ('boxes', 'whiskers', 'caps', 'medians'):
+        for art in bp[el]:
+            art.set_linewidth(LW); art.set_color('black')
+            if el == 'boxes':
+                art.set_facecolor('white'); art.set_edgecolor('black')
+    for i, v in enumerate(values):
+        ax.scatter(i + rng.uniform(-jitter, jitter, len(v)), v, s=s,
+                   facecolor=colours[i], edgecolor='none', alpha=.75, zorder=3)
+
+
+def star(q):
+    return '***' if q < .001 else '**' if q < .01 else '*' if q < .05 else None
+
+
+# ------------------------------------------------- a-d  group comparisons ----
+ad_stats = []
+PANELS = [('fig4a', 'empirical_r', 'Empirical NP',
+           'Empirical NP is lowest in patients'),
+          ('fig4b', 'simulated_r', 'Simulated NP',
+           'The twins reproduce the patient deficit'),
+          ('fig4c', 'ampa_r', 'NP after AMPA',
+           'AMPA up-regulation removes the group difference'),
+          ('fig4d', 'gaba_r', 'NP after GABA-A',
+           'GABA-A up-regulation removes the group difference')]
+for stem, col, ylab, ttl in PANELS:
+    W, H = 42, 50
+    fig, ax = plt.subplots(figsize=panel(W, H))
+    vals = [T.loc[T.Group == g, col].values for g in GRP]
+    box_points(ax, GRP, vals, [GCOL[g] for g in GRP])
+    F, pF = stats.f_oneway(*vals)
+    pairs = [(0, 1), (0, 2), (1, 2)]
+    ps = [stats.ttest_ind(vals[i], vals[j], equal_var=False).pvalue for i, j in pairs]
+    qs = multipletests(ps, method='fdr_bh')[1]
+    ad_stats.append(dict(panel=stem, measure=col[:-2], F=round(float(F), 3),
+                         p_anova=float(f'{pF:.3g}'),
+                         **{f'{GRP[i]}_vs_{GRP[j]}_p': float(f'{ps[k]:.3g}')
+                            for k, (i, j) in enumerate(pairs)},
+                         **{f'{GRP[i]}_vs_{GRP[j]}_q': float(f'{qs[k]:.3g}')
+                            for k, (i, j) in enumerate(pairs)}))
+    lo = min(v.min() for v in vals); hi = max(v.max() for v in vals)
+    step = (hi - lo) * .12
+    y = hi + step * .6
+    for k, (i, j) in enumerate(pairs):            # brackets only where q < 0.05
+        sg = star(qs[k])
+        if sg is None:
+            continue
+        ax.plot([i, i, j, j], [y, y + step * .25, y + step * .25, y], color='black',
+                lw=LW, clip_on=False)
+        ax.text((i + j) / 2, y + step * .3, sg, ha='center', va='bottom',
+                fontsize=ANNOT_PT)
+        y += step * .95
+    ax.set_ylim(lo - step * .5, max(y, hi + step))
+    ax.set_xticks(range(len(GRP)))
+    ax.set_xticklabels(['HC', 'High-\nsymptom', 'Patient'], fontsize=TICK_PT)
+    ax.set_xlim(-.6, len(GRP) - .4)
+    ax.set_ylabel(ylab)
+    panel_title(ax, ttl)
+    enforce(fig); save(fig, stem, W, H, 'fig4_subject_level_n288.csv')
+pd.DataFrame(ad_stats).to_csv(f'{D}/fig4ad_group_stats.csv', index=False)
+
+# --------------------------------------- e  distribution of the 4 conditions -
+W, H = 86, 48
+fig, ax = plt.subplots(figsize=panel(W, H))
+xs = np.linspace(T[['empirical', 'simulated', 'ampa', 'gaba']].values.min() - .6,
+                 T[['empirical', 'simulated', 'ampa', 'gaba']].values.max() + .6, 400)
+for col, lab, c_, ls in COND:
+    kde = gaussian_kde(T[col].values)
+    ax.plot(xs, kde(xs), color=c_, lw=LW * 1.6, ls=ls, label=lab, zorder=3)
+    ax.plot([T[col].mean()] * 2, [0, kde(T[col].mean())[0]], color=c_, lw=LW,
+            ls=(0, (1.2, 1.2)), zorder=2)
+ax.set_xlabel('NP factor'); ax.set_ylabel('Density')
+ax.set_ylim(0, None)
+ax.legend(loc='upper right', fontsize=ANNOT_PT, handletextpad=.5,
+          labelspacing=.3, borderaxespad=.2)
+panel_title(ax, 'Both perturbations shift the whole cohort upward')
+enforce(fig); save(fig, 'fig4e', W, H, 'fig4_subject_level_n288.csv')
+
+# ------------------------------------- f  per-twin response, AMPA vs GABA-A --
+W, H = 62, 60
+fig, ax = plt.subplots(figsize=panel(W, H))
+ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
+ax.axvline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
+for pat in PAT:
+    sub = T[T.pattern == pat]
+    ax.scatter(sub.d_ampa, sub.d_gaba, s=4.5, facecolor=PCOL[pat], edgecolor='none',
+               alpha=.8, zorder=3, label=f'{pat} (n = {len(sub)})')
+xl = float(np.abs(T.d_ampa).max()) * 1.1
+yl = float(np.abs(T.d_gaba).max()) * 1.1
+ax.set_xlim(-xl, xl); ax.set_ylim(-yl, yl)
+ax.set_xlabel('Δ NP after AMPA'); ax.set_ylabel('Δ NP after GABA-A')
+ax.legend(loc='lower right', fontsize=ANNOT_PT, handletextpad=.3, borderaxespad=.2,
+          markerscale=1.6)
+panel_title(ax, f'{int((T.pattern == "both up").sum())} of 288 twins increase '
+                'under both')
+enforce(fig); save(fig, 'fig4f', W, H, 'fig4_subject_level_n288.csv')
+
+# ---------------------- g  who responds, and where they start ----------------
+W, H = 86, 50
+fig, (ax1, ax2) = plt.subplots(1, 2, figsize=panel(W, H),
+                               gridspec_kw=dict(width_ratios=[1, 1], wspace=.55))
+ct = pd.crosstab(T.Group, T.pattern).loc[GRP, PAT]
+frac = ct.div(ct.sum(1), axis=0) * 100
+bottom = np.zeros(len(GRP))
+for pat in PAT:
+    ax1.bar(np.arange(len(GRP)), frac[pat].values, bottom=bottom, width=.62,
+            facecolor=PCOL[pat], edgecolor='black', linewidth=LW, zorder=2,
+            label=pat)
+    bottom += frac[pat].values
+for i, g in enumerate(GRP):
+    ax1.text(i, 102, f'{ct.loc[g, "both up"]}/{ct.loc[g].sum()}', ha='center',
+             fontsize=ANNOT_PT, color='0.35')
+chi2, pchi, dof, _ = stats.chi2_contingency(ct.values)
+ax1.set_xticks(range(len(GRP)))
+ax1.set_xticklabels(['HC', 'High-\nsymptom', 'Patient'], fontsize=TICK_PT)
+ax1.set_xlim(-.6, len(GRP) - .4); ax1.set_ylim(0, 112)
+ax1.set_yticks([0, 50, 100])
+ax1.set_ylabel('Twins (%)')
+ax1.legend(loc='lower center', fontsize=ANNOT_PT, ncol=1, handletextpad=.4,
+           borderaxespad=.2, frameon=False)
+ax1.text(1, 108, f'χ² = {chi2:.1f}, P = {pchi:.1e}', ha='center',
+         fontsize=ANNOT_PT, color='0.35')
+
+vals = [T.loc[T.pattern == p, 'simulated'].values for p in PAT]
+box_points(ax2, PAT, vals, [PCOL[p] for p in PAT], s=3.0, seed=1)
+tb, pb = stats.ttest_ind(*vals, equal_var=False)
+ax2.set_xticks(range(len(PAT)))
+ax2.set_xticklabels(['both\nup', 'any\ndown'], fontsize=TICK_PT)
+ax2.set_xlim(-.6, len(PAT) - .4)
+ax2.set_ylabel('Simulated baseline NP')
+hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
+ax2.plot([0, 0, 1, 1], [hi + .3, hi + .5, hi + .5, hi + .3], color='black', lw=LW)
+ax2.text(.5, hi + .55, f'P = {pb:.0e}', ha='center', va='bottom', fontsize=ANNOT_PT)
+ax2.set_ylim(lo - .3, hi + 1.4)
+panel_title(ax1, 'Responders are more often patients, and start lower', x=.0)
+enforce(fig); save(fig, 'fig4g', W, H, 'fig4_subject_level_n288.csv')
+
+# ------------------------ h  symptoms between the two response patterns ------
+rows = []
+for it in SDQ:
+    x = S.loc[S.pattern == 'both up', it].astype(float)
+    y = S.loc[S.pattern == 'any down', it].astype(float)
+    u, pu = stats.mannwhitneyu(x, y, alternative='two-sided')
+    n1, n2 = len(x), len(y)
+    sp = np.sqrt(((n1 - 1) * x.var(ddof=1) + (n2 - 1) * y.var(ddof=1)) / (n1 + n2 - 2))
+    gg = (x.mean() - y.mean()) / sp * (1 - 3 / (4 * (n1 + n2) - 9))
+    se = np.sqrt((n1 + n2) / (n1 * n2) + gg ** 2 / (2 * (n1 + n2)))
+    rows.append(dict(item=it, n_both_up=n1, n_any_down=n2,
+                     mean_both_up=round(x.mean(), 3), mean_any_down=round(y.mean(), 3),
+                     hedges_g=round(gg, 3), ci_lo=round(gg - 1.96 * se, 3),
+                     ci_hi=round(gg + 1.96 * se, 3), U=float(u),
+                     p_mw=float(f'{pu:.3g}')))
+H4 = pd.DataFrame(rows)
+H4['q_bh'] = multipletests(H4.p_mw, method='fdr_bh')[1].round(4)
+H4 = H4.sort_values('hedges_g').reset_index(drop=True)
+H4.to_csv(f'{D}/fig4h_sdq_stats.csv', index=False)
+
+W, H = 180, 46
+fig, ax = plt.subplots(figsize=panel(W, H))
+x = np.arange(len(H4))
+sig = (H4.q_bh < .05).values
+cols = [PCOL['both up'] if v > 0 else PCOL['any down'] for v in H4.hedges_g]
+ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
+for i in range(len(H4)):
+    ax.vlines(x[i], H4.ci_lo[i], H4.ci_hi[i], color=cols[i], lw=LW, zorder=2)
+ax.scatter(x[sig], H4.hedges_g[sig], s=10, facecolor=[c for c, m in zip(cols, sig) if m],
+           edgecolor=[c for c, m in zip(cols, sig) if m], linewidth=LW, zorder=3)
+ax.scatter(x[~sig], H4.hedges_g[~sig], s=10, facecolor='white',
+           edgecolor=[c for c, m in zip(cols, ~sig) if m], linewidth=LW, zorder=3)
+ax.set_xticks(x); ax.set_xticklabels(H4.item, fontsize=TICK_PT, rotation=45, ha='right')
+ax.set_xlim(-.7, len(H4) - .3)
+ax.set_ylabel("Hedges' g\n(both up − any down)")
+handles = [Patch(facecolor=PCOL['both up'], edgecolor='none'),
+           Patch(facecolor=PCOL['any down'], edgecolor='none'),
+           Line2D([], [], marker='o', linestyle='none', markersize=3.2,
+                  markerfacecolor='white', markeredgecolor='0.4', markeredgewidth=LW)]
+ax.legend(handles, ['higher in “both up”', 'higher in “any down”',
+                    'n.s. (BH q ≥ 0.05)'], loc='upper left', ncol=3,
+          fontsize=ANNOT_PT, handletextpad=.4, columnspacing=1.0, borderaxespad=.2)
+panel_title(ax, 'No SDQ item separates the two response patterns '
+                f'(smallest q = {H4.q_bh.min():.2f})')
+enforce(fig); save(fig, 'fig4h', W, H, 'fig4_sdq_items_n287.csv')
+
+mf = pd.DataFrame(manifest)
+mf.to_csv(f'{OUTD}/fig4_panel_manifest.csv', index=False)
+print(mf.to_string(index=False))
+print('\na-d group stats')
+print(pd.DataFrame(ad_stats).to_string(index=False))
+print(f'\nf  both up {int((T.pattern == "both up").sum())} / any down '
+      f'{int((T.pattern == "any down").sum())}')
+print(f'g  chi2 = {chi2:.2f}, P = {pchi:.3g}; baseline NP '
+      f'{vals[0].mean():.3f} vs {vals[1].mean():.3f}, t = {tb:.2f}, P = {pb:.3g}')
+print(f'h  smallest q = {H4.q_bh.min():.3f}, items with q<0.05: {int(sig.sum())}')
+
