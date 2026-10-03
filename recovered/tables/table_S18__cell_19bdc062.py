# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : 19bdc062-0a71-4065-935d-7be01c40f468
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:12:32 UTC (epoch-ms 1790676752503)
# conda env        : python
# produced         : Table S18 site x response-group and sex x response-group frequency tables, chi-square tests and Fisher exact test
# ----------------------------------------------------------------------------


from scipy import stats as st
d['grp']=d['pattern'].str.strip().str.lower().map({'both up':'Increased','any down':'Decreased'})
print(d.grp.value_counts().to_dict())
site_ct=pd.crosstab(d.grp, d.site); sex_ct=pd.crosstab(d.grp, d.sex)
print('\nsite x group:\n', site_ct.to_string()); print('\nsex x group:\n', sex_ct.to_string())
chi2_s, p_s, dof_s, _ = st.chi2_contingency(site_ct.values)
chi2_x, p_x, dof_x, _ = st.chi2_contingency(sex_ct.values)
print('\nsite: chi2=%.3f df=%d P=%.4f | Fisher(2x8) not applicable; min expected=%.2f'%(chi2_s,dof_s,p_s, st.chi2_contingency(site_ct.values)[3].min()))
print('sex : chi2=%.3f df=%d P=%.4f'%(chi2_x,dof_x,p_x))
odds,pf=st.fisher_exact(sex_ct.values); print('sex Fisher exact: OR=%.3f P=%.4f'%(odds,pf))
