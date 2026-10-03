# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS1_k2/data/stratify_subject_level_n434.csv
# cell id     : ce74bfcc-9a4f-4961-a8dc-5475eaf1d40a
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-22 20:51:51 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

SD='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_stratify'
rows=[]
for pan,meas,pairs in [('a','Neg_NP',[('MDD',mdd),('AUD',aud)]),('b','Pos_NP',[('Patient',pat)]),
                       ('c','Pos_NP',[('MDD',mdd),('AUD',aud)]),('d','NP factor',[('MDD',mdd),('AUD',aud)])]:
    for nm,g in pairs:
        t=stats.ttest_ind(hc[meas],g[meas],equal_var=True); n1,n2=len(hc),len(g)
        sp=np.sqrt(((n1-1)*hc[meas].var(ddof=1)+(n2-1)*g[meas].var(ddof=1))/(n1+n2-2))
        dd=hc[meas].mean()-g[meas].mean(); se=sp*np.sqrt(1/n1+1/n2); ci=stats.t.interval(.95,n1+n2-2,dd,se)
        rows.append(dict(panel=pan,measure=meas,group=nm,n_hc=n1,n_group=n2,
            hc_mean=round(hc[meas].mean(),4),group_mean=round(g[meas].mean(),4),
            diff_hc_minus_group=round(dd,4),ci95_lo=round(ci[0],4),ci95_hi=round(ci[1],4),
            hedges_g=round(dd/sp*(1-3/(4*(n1+n2)-9)),4),t=round(t.statistic,4),df=n1+n2-2,
            p_uncorrected=float(t.pvalue),p_bonf3=min(float(t.pvalue)*3,1.0),
            test='two-sided independent-samples Student t (equal variance)',
            correction='Bonferroni, 3 tests'))
GT=pd.DataFrame(rows); GT.to_csv(f'{SD}/data/stratify_group_tests.csv',index=False)
SL=ST[['ID','Group','Diseased','Pos_NP','Neg_NP','NP factor']].copy()
SL['panel_group']=np.where(SL.Group=='HC','HC',np.where(SL.Diseased.isin(['MDD','AUD']),SL.Diseased,'Other patient'))
SL2=pd.concat([SL,SL[SL.Group=='Patient'].assign(panel_group='Patient')],ignore_index=True)
SL2.to_csv(f'{SD}/data/stratify_subject_level_n434.csv',index=False)
print(GT[['panel','group','t','df','p_bonf3','hedges_g']].to_string(index=False,float_format=lambda x:f'{x:.4g}'))
print('\npanel_group counts:',SL2.panel_group.value_counts().to_dict())
