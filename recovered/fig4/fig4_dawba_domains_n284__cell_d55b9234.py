# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4_dawba_domains_n284.csv
#
# cell id      : d55b9234-c1ad-4b85-9b1c-6e294ec9c989
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:19:58 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/01_fig4_dawba_domains_n284.py
##############################################################################
D4='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data'
J[['ID','Group','pattern','ampa_dir','adhd','cd','eat','dep','gad','sp','sym6_sum']].to_csv(
    f'{D4}/fig4_dawba_domains_n284.csv',index=False)

blk = '''
# --------------- h (alt)  DAWBA symptom domains between the response groups --
# Six DAWBA band scores (ADHD, conduct, eating, depression, generalised anxiety,
# social phobia) and their sum, for the 284 twins with symptom data.  Same
# split logic and same nominal-P marking as the SDQ panel; BH q across the
# seven measures is kept in the CSV and annotated where it survives.
DW = pd.read_csv(f'{D}/fig4_dawba_domains_n284.csv')
MEAS = ['adhd', 'cd', 'eat', 'dep', 'gad', 'sp', 'sym6_sum']
MLABEL = {'adhd': 'ADHD', 'cd': 'Conduct', 'eat': 'Eating', 'dep': 'Depression',
          'gad': 'Gen. anxiety', 'sp': 'Social phobia', 'sym6_sum': 'Sum of 6'}
for stem, key, up, dn in [('fig4h_dawba', 'ampa_dir', 'AMPA up', 'AMPA down'),
                          ('fig4h_dawba_pattern', 'pattern', 'both up', 'any down')]:
    rows = []
    for m in MEAS:
        xx = DW.loc[DW[key] == up, m].astype(float)
        yy = DW.loc[DW[key] == dn, m].astype(float)
        u, pu = stats.mannwhitneyu(xx, yy, alternative='two-sided')
        n1, n2 = len(xx), len(yy)
        sp_ = np.sqrt(((n1 - 1) * xx.var(ddof=1) + (n2 - 1) * yy.var(ddof=1)) / (n1 + n2 - 2))
        gg = (xx.mean() - yy.mean()) / sp_ * (1 - 3 / (4 * (n1 + n2) - 9))
        se = np.sqrt((n1 + n2) / (n1 * n2) + gg ** 2 / (2 * (n1 + n2)))
        rows.append(dict(measure=m, split=f'{up} vs {dn}', n_up=n1, n_down=n2,
                         mean_up=round(xx.mean(), 3), mean_down=round(yy.mean(), 3),
                         hedges_g=round(gg, 3), ci_lo=round(gg - 1.96 * se, 3),
                         ci_hi=round(gg + 1.96 * se, 3), U=float(u),
                         p_mw=float(f'{pu:.3g}')))
    DT = pd.DataFrame(rows)
    DT['q_bh'] = multipletests(DT.p_mw, method='fdr_bh')[1].round(4)
    DT.to_csv(f'{D}/{stem}_stats.csv', index=False)

    W, H = 86, 50
    fig, ax = plt.subplots(figsize=panel(W, H))
    xx = np.arange(len(DT))
    sg = (DT.p_mw < .05).values
    cols = [PCOL['both up'] if v > 0 else PCOL['any down'] for v in DT.hedges_g]
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.axvline(len(MEAS) - 1.5, color='0.85', lw=LW, zorder=0)
    for i in range(len(DT)):
        ax.vlines(xx[i], DT.ci_lo[i], DT.ci_hi[i], color=cols[i], lw=LW, zorder=2)
    ax.scatter(xx[sg], DT.hedges_g[sg], s=10, facecolor=[c for c, m in zip(cols, sg) if m],
               edgecolor=[c for c, m in zip(cols, sg) if m], linewidth=LW, zorder=3)
    ax.scatter(xx[~sg], DT.hedges_g[~sg], s=10, facecolor='white',
               edgecolor=[c for c, m in zip(cols, ~sg) if m], linewidth=LW, zorder=3)
    for i in np.where(sg)[0]:
        lab = f'P = {DT.p_mw[i]:.3g}'
        if DT.q_bh[i] < .05:
            lab += f', q = {DT.q_bh[i]:.3g}'
        ax.text(xx[i] + .18, DT.ci_lo[i] - .03, lab, ha='left', va='top',
                fontsize=ANNOT_PT, color=cols[i])
    ax.set_xticks(xx)
    ax.set_xticklabels([MLABEL[m] for m in DT.measure], fontsize=TICK_PT,
                       rotation=45, ha='right')
    ax.set_xlim(-.7, len(DT) - .3)
    ax.set_ylim(float(DT.ci_lo.min()) - .30, float(DT.ci_hi.max()) + .16)
    ax.set_ylabel("Hedges' g\\n" + f'({up} − {dn})')
    panel_title(ax, f'{up} (n = {DT.n_up[0]}) vs {dn} (n = {DT.n_down[0]}): '
                    'DAWBA symptom domains')
    enforce(fig); save(fig, stem, W, H, 'fig4_dawba_domains_n284.csv')
    print(f'{stem}: ' + ', '.join(f'{m} (P={q:.3g}, q={qq:.3g}, g={g:.2f})'
          for m, q, qq, g in zip(DT.measure[sg], DT.p_mw[sg], DT.q_bh[sg],
                                 DT.hedges_g[sg])))

'''
s=open(p4).read()
k=s.index("mf = pd.DataFrame(manifest)")
open(p4,'w').write(s[:k]+blk+s[k:])
print('patched')
