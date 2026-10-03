# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4_subject_level_n288.csv
#
# cell id      : 40556d56-3567-4347-9fd1-6bea06be097d
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:04:10 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/09_fig4_subject_level_n288.py
##############################################################################
import os
OUT='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4'
os.makedirs(f'{OUT}/fig4_data',exist_ok=True); os.makedirs(f'{OUT}/panels',exist_ok=True)

# ---- per-subject table: raw + residualised (refit on the n=288 cohort) -------
T=D[['ID','Group','sex','site','headmotion','simulated','ampa','gaba']].copy()
T['empirical']=T.ID.map(e.empirical_np_sum)
assert T.empirical.notna().all()
for c in ['empirical','simulated','ampa','gaba']:
    T[c+'_resid']=smf.ols(f'{c} ~ C(sex)+C(site)+headmotion',data=T).fit().resid
T['d_ampa']=T.ampa-T.simulated; T['d_gaba']=T.gaba-T.simulated
T['pattern']=np.where((T.d_ampa>0)&(T.d_gaba>0),'both up','any down')
T.to_csv(f'{OUT}/fig4_data/fig4_subject_level_n288.csv',index=False,float_format='%.6g')
print(T.groupby(['Group','pattern']).size().unstack().fillna(0).astype(int).to_string())
print('\npattern totals', T.pattern.value_counts().to_dict())
print(T[['empirical','simulated','ampa','gaba']].describe().round(3).to_string())
