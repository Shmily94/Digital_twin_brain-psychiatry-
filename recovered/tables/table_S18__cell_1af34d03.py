# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : 1af34d03-f809-4cf4-9cb4-7bfdef3fe897
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:13:01 UTC (epoch-ms 1790676781667)
# conda env        : python
# produced         : Table S18b logistic-regression adjustment of the sex effect for diagnostic group
# ----------------------------------------------------------------------------


import statsmodels.api as sm, statsmodels.formula.api as smf
dd=d.copy(); dd['y']=(dd.grp=='Decreased').astype(int)
m1=smf.logit('y ~ C(sex)', data=dd).fit(disp=0)
m2=smf.logit('y ~ C(sex) + C(Group)', data=dd).fit(disp=0)
print('logistic, sex only:      beta=%.3f z=%.2f P=%.4f'%(m1.params['C(sex)[T.M]'], m1.tvalues['C(sex)[T.M]'], m1.pvalues['C(sex)[T.M]']))
print('logistic, sex + diagnosis: beta=%.3f z=%.2f P=%.4f'%(m2.params['C(sex)[T.M]'], m2.tvalues['C(sex)[T.M]'], m2.pvalues['C(sex)[T.M]']))
print('diagnosis distribution by group:\n', pd.crosstab(dd.grp, dd.Group).to_string())
site_pct=(site_ct.T/site_ct.sum(axis=1)).T*100
print('\nsite % by group:\n', site_pct.round(1).to_string())
