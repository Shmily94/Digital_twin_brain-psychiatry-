# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : 693b42e0-fdf9-4ed4-8918-26dba2372a91
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:22:24 UTC (epoch-ms 1790677344126)
# conda env        : python
# produced         : the nine-site x response-group crosstab shipped in Table S18a
# ----------------------------------------------------------------------------


LAB={'LONDON':'London-Invicro','LONDON2':'London-CNS'}
m=S.merge(L[['ID','s2','Group_response2']], on='ID', how='left')
m['site9']=m['s2'].map(lambda x: LAB.get(x, x.capitalize()))
print('Group_response2 in 290 file:', L['Group_response2'].value_counts().to_dict())
print('pattern (288):', m['pattern'].value_counts().to_dict())
print('agreement pattern vs Group_response2 on the 288:'); print(pd.crosstab(m['pattern'], m['Group_response2']))
ORD=['Berlin','Dresden','Dublin','Hamburg','London-Invicro','London-CNS','Mannheim','Nottingham','Paris']
m['grp']=m['pattern'].map({'both up':'Increased','any down':'Decreased'})
ct=pd.crosstab(m['grp'], m['site9']).reindex(index=['Increased','Decreased'], columns=ORD).fillna(0).astype(int)
print('\n', ct.to_string())
chi2,p,dof,exp=stats.chi2_contingency(ct.values)
print('\nsite9 chi2=%.4f df=%d P=%.4f  min expected=%.2f  cells<5=%d'%(chi2,p,dof,exp.min(),(exp<5).sum()))
