# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4i_paired_stats.csv
#
# cell id      : 430c5712-5091-41c6-b544-5d65d756d89c
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:30:21 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/17_fig4i_paired_stats.py
##############################################################################
PD.to_csv(f'{D4}/fig4_paired_np_mid_n288.csv',index=False)
blk = '''
# ------------- i  paired tests: baseline vs perturbed, NP and MID sums -------
# Per-twin paired comparison of the simulated baseline against each virtual
# perturbation, for the full 12-edge NP factor and for the 6 MID edges alone
# (NP = SST sum + MID sum, so the MID panel is a subset of the NP panel).
PD = pd.read_csv(f'{D}/fig4_paired_np_mid_n288.csv')
CONDS = [('baseline', 'Baseline', C('baseline')), ('ampa', '+AMPA', C('ampa')),
         ('gaba', '+GABA-A', C('gaba'))]
PMEAS = [('np', 'NP factor (12 edges)'), ('mid', 'MID summed FC (6 edges)')]
W, H = 110, 56
fig, axes = plt.subplots(1, 2, figsize=panel(W, H), gridspec_kw=dict(wspace=.42))
prows = []
rng = np.random.default_rng(4)
for ax, (meas, mlab) in zip(axes, PMEAS):
    vals = [PD[f'{meas}_{k}'].values for k, _, _ in CONDS]
    for j, (k, _, col) in enumerate(CONDS[1:], start=1):   # per-twin pairing
        for y0, y1 in zip(vals[0], vals[j]):
            ax.plot([0, j], [y0, y1], color=col, lw=LW * .6, alpha=.07, zorder=1)
    bp = ax.boxplot(vals, positions=np.arange(3), widths=.5, showfliers=False,
                    patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    for j, (k, _, col) in enumerate(CONDS):
        ax.scatter(j + rng.uniform(-.11, .11, len(vals[j])), vals[j], s=2.6,
                   facecolor=col, edgecolor='none', alpha=.7, zorder=3)
    hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
    step = (hi - lo) * .10
    y = hi + step * .5
    for j, (k, _, col) in enumerate(CONDS[1:], start=1):
        t_, p_ = stats.ttest_rel(vals[j], vals[0])
        dd = vals[j] - vals[0]
        w_, pw = stats.wilcoxon(vals[j], vals[0])
        prows.append(dict(measure=mlab, perturbation=CONDS[j][1].lstrip('+'),
                          n=len(dd), mean_baseline=round(vals[0].mean(), 4),
                          mean_modulated=round(vals[j].mean(), 4),
                          mean_diff=round(dd.mean(), 4), sd_diff=round(dd.std(ddof=1), 4),
                          n_increased=int((dd > 0).sum()),
                          pct_increased=round(100 * (dd > 0).mean(), 1),
                          t=round(float(t_), 3), df=len(dd) - 1,
                          p_paired_t=float(f'{p_:.3g}'), wilcoxon_p=float(f'{pw:.3g}'),
                          cohens_dz=round(float(dd.mean() / dd.std(ddof=1)), 3)))
        ax.plot([0, 0, j, j], [y, y + step * .3, y + step * .3, y], color='black', lw=LW)
        ax.text(j / 2, y + step * .38,
                f'$t$({len(dd)-1}) = {t_:.1f}, $P$ = {p_:.0e}\\n$d_z$ = '
                f'{dd.mean()/dd.std(ddof=1):.2f}, {100*(dd>0).mean():.0f}% up',
                ha='center', va='bottom', fontsize=ANNOT_PT)
        y += step * 1.9
    ax.set_ylim(lo - step * .5, y + step * .3)
    ax.set_xticks(range(3)); ax.set_xticklabels([c[1] for c in CONDS], fontsize=TICK_PT)
    ax.set_xlim(-.6, 2.6)
    ax.set_ylabel(mlab)
    panel_title(ax, 'Both perturbations raise it in almost every twin')
PTT = pd.DataFrame(prows)
PTT.to_csv(f'{D}/fig4i_paired_stats.csv', index=False)
enforce(fig); save(fig, 'fig4i', W, H, 'fig4_paired_np_mid_n288.csv')
print(PTT.to_string(index=False))

'''
s=open(p4).read(); k=s.index("mf = pd.DataFrame(manifest)")
open(p4,'w').write(s[:k]+blk+s[k:]); print('patched')
