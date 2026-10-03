# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5g_state_similarity_MDD_n22.csv; 04_figures/fig.5/fig5_data/fig5g_state_similarity_MDD_n22.csv
# cell id       : 64244dbd-c77a-4853-ad25-1ed508931448
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 432
# executed at   : 2026-09-21 20:25 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/18_fig5g_state_similarity_MDD_n22.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
import os, shutil
O5='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5'
os.makedirs(f'{O5}/fig5_data',exist_ok=True); os.makedirs(f'{O5}/panels',exist_ok=True)
w2=w.reset_index().rename(columns={'Kmeans_group':'subgroup'})
w2['subgroup']=w2.subgroup.map({'Group1':'decreasers','Group2':'increasers'})
w2[['Subject','subgroup','Placebo','Ketamine','Midazolam','d_ket','d_mid']].to_csv(
    f'{O5}/fig5_data/fig5_healthy_n27.csv',index=False)
ms[['SubID','group','FC_p2','FC_d2','FC_delta','MADRS_b0','MADRS_d2','symp_b0_pca','symp_delta_pca']].to_csv(
    f'{O5}/fig5_data/fig5_mdd_hc_n36.csv',index=False)
shutil.copy(f'{P2}/np_vs_symptomPC1_change_resid_MDD.csv', f'{O5}/fig5_data/fig5f_np_symptom_resid_MDD_n22.csv')
cv=pd.read_csv(f'{P2}/ketamine_n36_with_covariates.csv')
g5=sim[sim.group=='MDD'][['SubID','pref_p2','pref_d2','crossover']].merge(
    cv[['SubID','age','sex','infusion_1','fd_p2']],on='SubID').merge(
    ms[['SubID','MADRS_delta','HAMD_Bech_delta','HAM17_delta','symp_delta_pca']],on='SubID')
g5.to_csv(f'{O5}/fig5_data/fig5g_state_similarity_MDD_n22.csv',index=False)
h5=pd.DataFrame(np.column_stack([np.asarray(M['X_final']),np.asarray(M['y_final'])]),
    columns=['ampa_restoration_index','x2','x3','x4','x5','fu3_symptom_change'])
h5.to_csv(f'{O5}/fig5_data/fig5h_longitudinal_n85.csv',index=False)
pd.DataFrame([dict(R2_reduced=float(M['R2_reduced']),R2_full=float(M['R2_full']),
  delta_R2=float(M['R2_full'])-float(M['R2_reduced']),F_change=float(M['F_change']),
  p_change=float(M['p_change']),p_perm_R2=float(M['p_perm_R2']),
  beta=float(M['beta_real']),p_perm_beta=float(M['p_perm_beta']),n=int(M['n']),
  n_perm=int(M['Nperm']))]).to_csv(f'{O5}/fig5_data/fig5h_model_stats.csv',index=False)
np.savetxt(f'{O5}/fig5_data/fig5h_R2_permutation_null.csv',np.asarray(M['R2_perm']).ravel(),
           delimiter=',',header='R2_perm',comments='')
print(sorted(os.listdir(f'{O5}/fig5_data')))
print('g5',g5.shape,'h5',h5.shape)