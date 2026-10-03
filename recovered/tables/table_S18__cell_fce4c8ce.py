# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : fce4c8ce-79f1-43b2-aef8-069d30cb2b1f
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:22:50 UTC (epoch-ms 1790677370375)
# conda env        : python
# produced         : Table S18a chi-square, the 10,000-iteration permutation test (seed 0) and the London-collapsed comparison
# ----------------------------------------------------------------------------


chi2,p,dof,exp=stats.chi2_contingency(ct.values)
print('site9: chi2=%.2f, df=%d, P=%.4f | expected min %.2f, %d of %d cells <5'%(chi2,dof,p,exp.min(),(exp<5).sum(),exp.size))
rng=np.random.default_rng(0); g=m['grp'].values; s=m['site9'].values; obs=chi2; cnt=0; N=10000
for _ in range(N):
    perm=rng.permutation(g)
    t=pd.crosstab(perm,s).values
    cnt += stats.chi2_contingency(t)[0] >= obs-1e-9
print('permutation P = %.4f (%d/%d)'%((cnt+1)/(N+1),cnt,N))
# 8-site version (London collapsed) for comparison
ct8=pd.crosstab(m['grp'], m['site']).reindex(index=['Increased','Decreased'])
c8,p8,d8,e8=stats.chi2_contingency(ct8.values)
print('site8 (London collapsed): chi2=%.2f, df=%d, P=%.4f'%(c8,d8,p8))
pct=(ct.T/ct.sum(1)).T
print('\npercent:\n', (pct*100).round(1).to_string())
