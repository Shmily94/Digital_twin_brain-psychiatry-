# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/inclusion_comparison_stratify.csv
# cell id     : cdaf9702-be32-4d18-a33f-f8e815701be5
# frame id    : b194cd74-5255-435a-9c1e-206638f9adae
# executed    : 2026-09-29 11:18:35 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================


ST['included']=ST['ID'].isin(S288['ID'])
print(ST.groupby(['panel_group','included'])['sym6_sum'].agg(['count','mean','std']).round(2).to_string())
out=[]
for lbl,sub in [('All STRATIFY',ST),('HC',ST[ST.panel_group=='HC']),('Patients',ST[ST.panel_group=='Patient'])]:
    a=sub.loc[sub.included,'sym6_sum'].dropna(); b=sub.loc[~sub.included,'sym6_sum'].dropna()
    t,p=stats.ttest_ind(a,b,equal_var=False); u,pu=stats.mannwhitneyu(a,b)
    dof=(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))**2/((a.var(ddof=1)/len(a))**2/(len(a)-1)+(b.var(ddof=1)/len(b))**2/(len(b)-1))
    sp=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2)); g=(a.mean()-b.mean())/sp
    out.append(dict(stratum=lbl,n_inc=len(a),n_exc=len(b),m_inc=a.mean(),sd_inc=a.std(ddof=1),m_exc=b.mean(),sd_exc=b.std(ddof=1),t=t,df=dof,P=p,U=u,P_MW=pu,g=g))
    print('\n%-14s inc %d (%.2f ± %.2f) vs exc %d (%.2f ± %.2f) | Welch t(%.1f) = %.2f, P = %.3f | U = %.0f, P = %.3f | g = %.2f'%(lbl,len(a),a.mean(),a.std(ddof=1),len(b),b.mean(),b.std(ddof=1),dof,t,p,u,pu,g))
ct=pd.crosstab(ST['panel_group'],ST['included']); c2,p2,_,_=stats.chi2_contingency(ct.values)
print('\ngroup composition included vs not:\n', ct.to_string(), '\nchi2(1) = %.2f, P = %.3f'%(c2,p2))
ctd=pd.crosstab(ST.loc[ST.panel_group=='Patient','diagnosis'],ST.loc[ST.panel_group=='Patient','included'])
c3,p3,_,_=stats.chi2_contingency(ctd.values); print('\ndiagnosis within patients:\n',ctd.to_string(),'\nchi2(1) = %.2f, P = %.3f'%(c3,p3))
pd.DataFrame(out).to_csv('inclusion_comparison_stratify.csv',index=False)
