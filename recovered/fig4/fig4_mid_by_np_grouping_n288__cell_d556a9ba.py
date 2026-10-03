# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4_mid_by_np_grouping_n288.csv
#
# cell id      : d556a9ba-afe4-4e91-94c2-17902bc44e68
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 21:09:27 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/02_fig4_mid_by_np_grouping_n288.py
##############################################################################
M['d_ampa_np'] = M.np_ampa - M.np_baseline; M['d_gaba_np'] = M.np_gaba - M.np_baseline
print(M.pattern_np.value_counts().to_dict())
rows=[]
for col,nm in [('mid_baseline','simulated baseline MID FC'),('d_ampa_mid','MID change after AMPA'),
               ('d_gaba_mid','MID change after GABA-A')]:
    for pat in ['both up','any down']:
        v=M.loc[M.pattern_np==pat,col]; t_,p_=stats.ttest_1samp(v,0)
        rows.append(dict(grouping='NP-based both-up / any-down', group=pat, measure=nm, n=len(v),
                         mean=round(float(v.mean()),4), sd=round(float(v.std(ddof=1)),4),
                         test='one-sample t vs 0', stat=round(float(t_),3), p=float(f'{p_:.3g}')))
    a=M.loc[M.pattern_np=='both up',col]; b=M.loc[M.pattern_np=='any down',col]
    t_,p_=stats.ttest_ind(a,b,equal_var=False); _,pu=stats.mannwhitneyu(a,b)
    sp=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    rows.append(dict(grouping='NP-based both-up / any-down', group='both up vs any down', measure=nm,
                     n=len(M), mean=round(float(a.mean()-b.mean()),4),
                     sd=round(float((a.mean()-b.mean())/sp),3),
                     test=f'Welch t (sd col = Hedges g); Mann-Whitney P = {pu:.3g}',
                     stat=round(float(t_),3), p=float(f'{p_:.3g}')))
    print(f'{nm:28s} both up {a.mean():+.3f} (n={len(a)}) vs any down {b.mean():+.3f} (n={len(b)})  '
          f't={t_:+.2f} P={p_:.3g} MW P={pu:.3g} g={(a.mean()-b.mean())/sp:+.2f}')
# how much of the NP grouping is driven by the MID half
print('\nsign agreement between the NP change and the MID change (AMPA): %.1f%%'
      % (100*np.mean(np.sign(M.d_ampa_np)==np.sign(M.d_ampa_mid))))
print('NP grouping vs MID sign, AMPA: both-up twins with MID up = %d/%d'
      % (((M.pattern_np=='both up')&(M.d_ampa_mid>0)).sum(), (M.pattern_np=='both up').sum()))
ct2 = pd.crosstab(M.Group, M.pattern_np).loc[['HC','High-symptom','Patient']]
print('\nNP-rule proportions (unchanged from Fig. 4g):')
print(ct2.assign(pct=(ct2['both up']/ct2.sum(1)*100).round(1)).to_string())
MS2=pd.DataFrame(rows)
MS2.to_csv(f'{OUT}/fig4_mid_by_np_grouping_n288.csv', index=False)
