# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4_mid_pattern_subject_n288.csv
#
# cell id      : f88fc48a-773d-46d3-9a3d-f8b0d4b61ca6
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 21:06:01 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/03_fig4_mid_pattern_subject_n288.py
##############################################################################
X=sm.add_constant(M.mid_baseline.values); mod=sm.OLS(M.mid_ampa.values,X).fit()
t=(mod.params[1]-1)/mod.bse[1]; print('AMPA slope t vs 1 = %.2f, P = %.3g' % (t, 2*stats.t.sf(abs(t), len(M)-2)))
rows=[]
for col,nm in [('d_ampa_mid','change after AMPA'),('d_gaba_mid','change after GABA-A'),
               ('mid_baseline','simulated baseline level')]:
    for pat in ['both up','any down']:
        v=M.loc[M.pattern_mid==pat,col]; t_,p_=stats.ttest_1samp(v,0)
        rows.append(dict(cohort='DTB twins n=288', rule='MID-based both-up/any-down', group=pat,
                         measure=nm, n=len(v), mean=round(float(v.mean()),4),
                         sd=round(float(v.std(ddof=1)),4), test='one-sample t vs 0',
                         stat=round(float(t_),3), p=float(f'{p_:.3g}')))
    a=M.loc[M.pattern_mid=='both up',col]; b=M.loc[M.pattern_mid=='any down',col]
    t_,p_=stats.ttest_ind(a,b,equal_var=False); _,pu=stats.mannwhitneyu(a,b)
    sp=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    rows.append(dict(cohort='DTB twins n=288', rule='MID-based both-up/any-down',
                     group='both up vs any down', measure=nm, n=len(M),
                     mean=round(float(a.mean()-b.mean()),4), sd=round(float((a.mean()-b.mean())/sp),3),
                     test=f'Welch t (sd col = Hedges g); Mann-Whitney P = {pu:.3g}',
                     stat=round(float(t_),3), p=float(f'{p_:.3g}')))
for post,nm in [('mid_ampa','AMPA'),('mid_gaba','GABA-A')]:
    mo=sm.OLS(M[post].values,X).fit(); b_,se=mo.params[1],mo.bse[1]; ci=mo.conf_int()[1]
    tt=(b_-1)/se
    rows.append(dict(cohort='DTB twins n=288', rule='non-circular', group=f'MID after {nm}',
                     measure='OLS slope on simulated baseline', n=len(M), mean=round(float(b_),3),
                     sd=f'95% CI {ci[0]:.3f}-{ci[1]:.3f}', test='t vs slope = 1',
                     stat=round(float(tt),3), p=float(f'{2*stats.t.sf(abs(tt),len(M)-2):.3g}')))
    rows.append(dict(cohort='DTB twins n=288', rule='non-circular', group=f'MID after {nm}',
                     measure='var(post) / var(baseline)', n=len(M),
                     mean=round(float(M[post].var(ddof=1)/M.mid_baseline.var(ddof=1)),3),
                     sd=np.nan, test='descriptive', stat=np.nan, p=np.nan))
ctm = pd.crosstab(M.Group, M.pattern_mid).loc[['HC','High-symptom','Patient']]
chi2,pchi,dof,_ = stats.chi2_contingency(ctm.values)
for g in ctm.index:
    rows.append(dict(cohort='DTB twins n=288', rule='MID-based both-up/any-down', group=g,
                     measure='proportion both up', n=int(ctm.loc[g].sum()),
                     mean=round(float(ctm.loc[g,'both up']/ctm.loc[g].sum()*100),1),
                     sd=f"{ctm.loc[g,'both up']}/{ctm.loc[g].sum()}",
                     test=f'chi2({dof}) = {chi2:.2f} across groups', stat=round(float(chi2),3),
                     p=float(f'{pchi:.3g}')))
MS=pd.DataFrame(rows)
OUT='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data'
MS.to_csv(f'{OUT}/fig4_mid_rule_grouping_n288.csv', index=False)
M[['ID','Group','mid_baseline','mid_ampa','mid_gaba','d_ampa_mid','d_gaba_mid','pattern_mid','pattern_np']].to_csv(f'{OUT}/fig4_mid_pattern_subject_n288.csv', index=False)
print(MS[['group','measure','mean','test','p']].to_string(index=False))
