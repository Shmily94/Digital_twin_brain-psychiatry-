# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4h_sdq_stats.csv
#
# cell id      : 37142daa-f186-4e77-98d3-783912832160
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:16:39 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/16_fig4h_sdq_stats.py
##############################################################################
new_h = '''# ------------------------ h  symptoms between the response groups ------------
# Two ways of splitting the cohort are drawn: the joint pattern (both
# perturbations up vs at least one down) and the AMPA direction alone.
# Significance is the nominal Mann-Whitney P (no multiplicity correction, at
# the author's request); BH q is kept in the accompanying CSV.
S = S.merge(T[['ID', 'd_ampa']], on='ID')
SPLITS = [('fig4h', 'pattern', 'both up', 'any down', 'both up', 'any down'),
          ('fig4h_ampa', 'ampa_dir', 'AMPA up', 'AMPA down', 'AMPA up', 'AMPA down')]
S['ampa_dir'] = np.where(S.d_ampa > 0, 'AMPA up', 'AMPA down')
for stem, key, up, dn, lab_up, lab_dn in SPLITS:
    rows = []
    for it in SDQ:
        x = S.loc[S[key] == up, it].astype(float)
        y = S.loc[S[key] == dn, it].astype(float)
        u, pu = stats.mannwhitneyu(x, y, alternative='two-sided')
        n1, n2 = len(x), len(y)
        sp = np.sqrt(((n1 - 1) * x.var(ddof=1) + (n2 - 1) * y.var(ddof=1)) / (n1 + n2 - 2))
        gg = (x.mean() - y.mean()) / sp * (1 - 3 / (4 * (n1 + n2) - 9))
        se = np.sqrt((n1 + n2) / (n1 * n2) + gg ** 2 / (2 * (n1 + n2)))
        rows.append(dict(item=it, split=f'{lab_up} vs {lab_dn}', n_up=n1, n_down=n2,
                         mean_up=round(x.mean(), 3), mean_down=round(y.mean(), 3),
                         hedges_g=round(gg, 3), ci_lo=round(gg - 1.96 * se, 3),
                         ci_hi=round(gg + 1.96 * se, 3), U=float(u),
                         p_mw=float(f'{pu:.3g}')))
    H4 = pd.DataFrame(rows)
    H4['q_bh'] = multipletests(H4.p_mw, method='fdr_bh')[1].round(4)
    H4 = H4.sort_values('hedges_g').reset_index(drop=True)
    H4.to_csv(f'{D}/{stem}_sdq_stats.csv', index=False)

    W, H = 180, 46
    fig, ax = plt.subplots(figsize=panel(W, H))
    x = np.arange(len(H4))
    sig = (H4.p_mw < .05).values          # nominal P, no multiplicity correction
    cols = [PCOL['both up'] if v > 0 else PCOL['any down'] for v in H4.hedges_g]
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    for i in range(len(H4)):
        ax.vlines(x[i], H4.ci_lo[i], H4.ci_hi[i], color=cols[i], lw=LW, zorder=2)
    ax.scatter(x[sig], H4.hedges_g[sig], s=10,
               facecolor=[c for c, m in zip(cols, sig) if m],
               edgecolor=[c for c, m in zip(cols, sig) if m], linewidth=LW, zorder=3)
    ax.scatter(x[~sig], H4.hedges_g[~sig], s=10, facecolor='white',
               edgecolor=[c for c, m in zip(cols, ~sig) if m], linewidth=LW, zorder=3)
    for i in np.where(sig)[0]:            # name the items that reach P < 0.05
        ax.text(x[i], H4.ci_lo[i] - .04, f'P = {H4.p_mw[i]:.3g}', ha='center',
                va='top', fontsize=ANNOT_PT, color=cols[i])
    ax.set_xticks(x)
    ax.set_xticklabels(H4.item, fontsize=TICK_PT, rotation=45, ha='right')
    ax.set_xlim(-.7, len(H4) - .3)
    ax.set_ylabel("Hedges' g\\n" + f'({lab_up} − {lab_dn})')
    handles = [Patch(facecolor=PCOL['both up'], edgecolor='none'),
               Patch(facecolor=PCOL['any down'], edgecolor='none'),
               Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                      markerfacecolor='white', markeredgecolor='0.4',
                      markeredgewidth=LW)]
    ax.legend(handles, [f'higher in "{lab_up}"', f'higher in "{lab_dn}"', 'P \\u2265 0.05'],
              loc='upper left', ncol=3, fontsize=ANNOT_PT, handletextpad=.4,
              columnspacing=1.0, borderaxespad=.2)
    _s = H4.item[sig].tolist()
    panel_title(ax, f'{lab_up} (n = {H4.n_up[0]}) vs {lab_dn} (n = {H4.n_down[0]}): '
                    f'{len(_s)} SDQ items differ ({", ".join(_s)}; P < 0.05, uncorrected)')
    enforce(fig); save(fig, stem, W, H, 'fig4_sdq_items_n287.csv')
    print(f'{stem}: ' + ', '.join(f'{i} (P={q:.3g}, g={g:.2f})'
          for i, q, g in zip(H4.item[sig], H4.p_mw[sig], H4.hedges_g[sig])))

'''
s2 = s[:i] + new_h + s[j:]
# the old trailing print for h is gone; drop the stale reference if present
s2 = s2.replace("print('h  items with P<0.05: ' + ', '.join(f'{i} (P={q:.3g}, g={g:.2f})'\n      for i, q, g in zip(H4.item[sig], H4.p_mw[sig], H4.hedges_g[sig])))\n", "")
open(p4,'w').write(s2)
print(len(s2))
