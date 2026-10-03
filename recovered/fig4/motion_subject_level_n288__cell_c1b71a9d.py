# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_motion/data/motion_subject_level_n288.csv
#
# cell id      : c1b71a9d-8594-41a2-8c86-0e6441c4a9fa
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 21:48:21 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/38_motion_subject_level_n288.py
##############################################################################
COR=SL4[['ID','Group','headmotion','empirical','simulated','ampa','gaba']].copy()
COR['d_ampa']=COR.ampa-COR.simulated; COR['d_gaba']=COR.gaba-COR.simulated
print('delta columns match the stored ones:',
      np.abs(COR.d_ampa-SL4.d_ampa).max(), np.abs(COR.d_gaba-SL4.d_gaba).max())
ROWS=[('Empirical NP factor','empirical'),('Simulated NP','simulated'),
      ('Manipulated NP (AMPA)','ampa'),('Manipulated NP (GABA-A on high AMPA)','gaba'),
      ('Delta NP (AMPA)','d_ampa'),('Delta NP (GABA-A on high AMPA)','d_gaba')]
rr=[]
for lab,c in ROWS:
    r_,p_=stats.pearsonr(COR.headmotion, COR[c]); rh,ph=stats.spearmanr(COR.headmotion, COR[c])
    lo,hi=np.tanh(np.arctanh(r_)+np.array([-1,1])*1.959964/np.sqrt(len(COR)-3))
    rr.append(dict(Measure=lab, n=len(COR), r=round(float(r_),3),
                   CI95=f'{lo:.3f} to {hi:.3f}', P_raw=float(f'{p_:.3g}'),
                   variance_explained=round(float(r_**2),4),
                   spearman_rho=round(float(rh),3), P_spearman=float(f'{ph:.3g}'),
                   source_column=f'dtb_np_n288_baseline_post.csv[{c}]'))
T=pd.DataFrame(rr)
T['P_FDR']=multipletests(T.P_raw, method='fdr_bh')[1].round(4)
T['P_Bonferroni']=np.minimum(1.0, T.P_raw*len(T)).round(4)
T=T[['Measure','n','r','CI95','P_raw','P_FDR','P_Bonferroni','variance_explained',
     'spearman_rho','P_spearman','source_column']]
OUTM=f"{dirs['motion']}/data"
T.to_csv(f'{OUTM}/TableS25_motion_np_correlations_corrected_n288.csv', index=False)
COR.to_csv(f'{OUTM}/motion_subject_level_n288.csv', index=False)
with pd.ExcelWriter(f'{OUTM}/TableS25_motion_np_correlations_corrected_n288.xlsx') as w:
    T.to_excel(w, sheet_name='Table S25 (corrected)', index=False)
print(T.to_string(index=False))
