# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_motion/data/TableS26_group_effect_motion_adjustment_corrected_n288.csv
#
# cell id      : f03a0dec-16d3-4061-a819-100afe256021
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 21:51:38 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/33_TableS26_group_effect_motion_adjustment_corrected_n288.py
##############################################################################
import statsmodels.formula.api as smf, statsmodels.api as sm2
M2=SL4[['ID','Group','sex','site','headmotion','empirical','simulated','ampa','gaba']].copy()
M2['d_ampa']=M2.ampa-M2.simulated; M2['d_gaba']=M2.gaba-M2.simulated
M2['grp']=M2.Group.astype('category'); M2['fd']=M2.headmotion
M2['sx']=M2.sex.astype('category'); M2['st']=M2.site.astype('category')
def peta(formula, term='grp'):
    mod=smf.ols(formula, data=M2).fit(); a=sm2.stats.anova_lm(mod, typ=2)
    ss=a.loc[term,'sum_sq']; ssr=a.loc['Residual','sum_sq']
    return ss/(ss+ssr), float(a.loc[term,'F']), float(a.loc[term,'PR(>F)']), int(a.loc[term,'df']), int(mod.df_resid)
ROWS2=[('Empirical NP factor','empirical'),('Simulated NP','simulated'),
       ('Manipulated NP (AMPA)','ampa'),('Manipulated NP (GABA-A on high AMPA)','gaba'),
       ('Delta NP (AMPA)','d_ampa'),('Delta NP (GABA-A on high AMPA)','d_gaba')]
gr=[]
for lab,c in ROWS2:
    e0,F0,p0,df0,dr0 = peta(f'{c} ~ grp')
    e1,F1,p1,df1,dr1 = peta(f'{c} ~ grp + fd')
    e2,F2,p2,df2,dr2 = peta(f'{c} ~ grp + fd + sx + st')
    gr.append(dict(Measure=lab, n=len(M2),
                   eta2_group_no_FD=round(100*e0,2), F_no_FD=round(F0,3),
                   P_no_FD=float(f'{p0:.3g}'), df_no_FD=f'{df0}, {dr0}',
                   eta2_group_with_FD=round(100*e1,2), F_with_FD=round(F1,3),
                   P_with_FD=float(f'{p1:.3g}'), df_with_FD=f'{df1}, {dr1}',
                   eta2_group_full_cov=round(100*e2,2), P_full_cov=float(f'{p2:.3g}'),
                   df_full_cov=f'{df2}, {dr2}'))
GR=pd.DataFrame(gr)
GR['P_no_FD_bonf']=np.minimum(1,GR.P_no_FD*len(GR)).round(4)
GR['P_with_FD_bonf']=np.minimum(1,GR.P_with_FD*len(GR)).round(4)
GR['P_full_cov_bonf']=np.minimum(1,GR.P_full_cov*len(GR)).round(4)
GR.to_csv(f'{OUTM}/TableS26_group_effect_motion_adjustment_corrected_n288.csv', index=False)
print(GR[['Measure','eta2_group_no_FD','eta2_group_with_FD','P_with_FD','P_with_FD_bonf',
          'eta2_group_full_cov','P_full_cov_bonf']].to_string(index=False))
