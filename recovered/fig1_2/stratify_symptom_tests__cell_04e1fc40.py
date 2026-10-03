# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS1_k2/data/stratify_symptom_tests.csv
# cell id     : 04e1fc40-24bc-49e2-bf84-08baad5e4501
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-23 13:55:32 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

def welch(a,b):
    t,p=st.ttest_ind(a,b,equal_var=False)
    na,nb=len(a),len(b); va,vb=a.var(ddof=1),b.var(ddof=1)
    dfw=(va/na+vb/nb)**2/((va/na)**2/(na-1)+(vb/nb)**2/(nb-1))
    sp=np.sqrt(((na-1)*va+(nb-1)*vb)/(na+nb-2)); d=(a.mean()-b.mean())/sp
    g=d*(1-3/(4*(na+nb)-9)); se=np.sqrt((na+nb)/(na*nb)+g**2/(2*(na+nb-2)))
    lev=st.levene(a,b)
    return dict(n1=nb,n2=na,df=round(float(dfw),1),t=float(t),p=float(p),g=float(g),
                ci_lo=float(g-1.96*se),ci_hi=float(g+1.96*se),
                mean1=float(b.mean()),sd1=float(b.std(ddof=1)),mean2=float(a.mean()),sd2=float(a.std(ddof=1)),
                var_ratio=float(va/vb),levene_F=float(lev.statistic),levene_p=float(lev.pvalue),
                test='Welch two-sample t test (unequal variance)')
rows=[]
for lab,vv in [('MDD',sym.loc[sym.diagnosis=='MDD','sym6_sum'].values),
               ('AUD',sym.loc[sym.diagnosis=='AUD','sym6_sum'].values),
               ('Patient',sym.loc[sym.panel_group=='Patient','sym6_sum'].values)]:
    r=welch(vv,H); r.update(panel='e',group=lab,measure='sym6_sum'); rows.append(r)
STW=pd.DataFrame(rows); STW['p_bonf3']=np.minimum(1,STW.p*3)
STW.to_csv(FIG+'supp_stratify/data/stratify_symptom_tests.csv',index=False)
print(STW[['group','n1','n2','df','t','p','p_bonf3','g','ci_lo','ci_hi','var_ratio','levene_F','levene_p']].to_string(index=False))