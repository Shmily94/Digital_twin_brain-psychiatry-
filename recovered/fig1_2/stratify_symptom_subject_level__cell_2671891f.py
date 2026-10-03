# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS1_k2/data/stratify_symptom_subject_level.csv
# cell id     : 2671891f-151c-446c-86fe-cbbec44af875
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-23 13:44:26 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

HC215=pd.concat([hc_stra,hc_from_f2,hc_from_f3]); assert len(HC215)==215 and HC215.index.is_unique
src215={**{i:'STRATIFY-recruited HC (STRA_self_dawba.mat)' for i in hc_stra.index},
         **{i:'IMAGEN FU2 (STARTIFT_HC_subject_list_fu2.txt)' for i in hc_from_f2.index},
         **{i:'IMAGEN FU3 (STARTIFY_HC_subject_list_fu3.txt)' for i in hc_from_f3.index}}
sym=pd.DataFrame({'ID':list(pm.index)+list(HC215.index),
                  'panel_group':['Patient']*len(pm)+['HC']*len(HC215),
                  'sym6_sum':list(pm.values)+list(HC215.values)}).merge(diag,on='ID',how='left')
sym['symptom_source']=[src215.get(i,'STRATIFY patient self-report (STRA_self_dawba.mat)') for i in sym.ID]
H=sym.loc[sym.panel_group=='HC','sym6_sum'].values
rows=[]
for lab,vv in [('MDD',sym.loc[sym.diagnosis=='MDD','sym6_sum'].values),
               ('AUD',sym.loc[sym.diagnosis=='AUD','sym6_sum'].values),
               ('Patient',sym.loc[sym.panel_group=='Patient','sym6_sum'].values)]:
    r=stud(vv,H); r.update(panel='e',group=lab,measure='sym6_sum'); rows.append(r)
STF=pd.DataFrame(rows); STF['p_bonf3']=np.minimum(1,STF.p*3)
sym.to_csv(FIG+'supp_stratify/data/stratify_symptom_subject_level.csv',index=False)
STF.to_csv(FIG+'supp_stratify/data/stratify_symptom_tests.csv',index=False)
print(STF[['group','n1','n2','df','t','p','p_bonf3','g','ci_lo','ci_hi','mean1','mean2']].to_string(index=False))
print(); print(sym.groupby(['panel_group','symptom_source']).size().to_string())