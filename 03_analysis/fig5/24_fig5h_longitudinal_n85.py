#!/usr/bin/env python3
"""fig5h_longitudinal_n85.csv

Computes
    IMAGEN follow-up cohort (n = 85): the design matrix of the longitudinal
    model - AMPA restoration index plus the four baseline covariates - and the
    four-year follow-up symptom change outcome. Source data for Fig. 5h.

Inputs
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/684a22a0-d6db-4aeb-b5ad-b30777bef882/vd1e0509f_state_similarity_per_subject.csv
    - /Users/yunman/Desktop/submission/figures_v2/fig4/pharmacological_exper
    - /Users/yunman/Desktop/submission/figures_v2/fig4/predict_fu3_beha_changes/virtual_modu_predict_fu3_beha_changes.mat
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/New_pharma_dataset
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/ampa_ketamine_spearman_4outcomes.csv
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5
    - (path built in the chain) f'{P1}/summed_MID_FCs_3conditions.csv'
    - (path built in the chain) f'{P2}/summed_FCs_2conditions_for_plot.csv'
    - (path built in the chain) f'{P2}/ketamine_master_data_for_plots.csv'
    - (path built in the chain) f'{P2}/np_vs_symptomPC1_change_resid_MDD.csv'
    - (path built in the chain) f'{P2}/ketamine_n36_with_covariates.csv'

Output
    04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_longitudinal_n85.csv; 04_figures/fig.5/fig5_data/fig5h_longitudinal_n85.csv

Statistical tests
    in this script's own computation:
      - nested-model F test for the R2 increment
      - principal component analysis
    in the recovered chain that prepares its inputs:
      - k-means clustering

Local runnability
    yes (local_runnable = yes).  Verification: match.
    85 rows x 6 cols identical (max rel dev 0.00e+00)
Recovered from
    execution-log cell 64244dbd-c77a-4853-ad25-1ed508931448
    frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, cell_index 432, 2026-09-21 20:25 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    6c722a4a, 05f06794, 4a491abc, 1c66a2a8, 64244dbd

Random seed
    not applicable - nothing in this script is stochastic.

Notes
    Rebuilt by the statistics-layer recovery (docs/RECOVERY_PROTOCOL.md).  The
    computation is the recovered cell chain unchanged: same tests, same
    covariates, same corrections, same seeds.  Only the header, the explicit
    output path and the suppression of the original session's side outputs were
    added.  Lines marked "[recovery: side output suppressed]" wrote files other
    than this script's one deliverable into the author's working tree; they are
    commented out so that running this script cannot modify anything outside
    OUT_DIR.  The verbatim terminal cell is archived at
    recovered/fig5/fig5h_longitudinal_n85__cell_64244dbd.py
"""
import os
import sys

OUT_DIR = os.environ.get(
    "RECOVERY_OUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scratch"))
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- cell 6c722a4a (cell_index 424)
import pandas as pd
P1='/Users/yunman/Desktop/submission/figures_v2/fig4/pharmacological_exper'
P2='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/New_pharma_dataset'
for f in [f'{P1}/summed_MID_FCs_3conditions.csv', f'{P1}/NP_fcs_only_win_mean.csv',
          f'{P2}/summed_FCs_2conditions_for_plot.csv', f'{P2}/compare_hc_mdd_p2.csv',
          f'{P2}/baseline_np_vs_symptom_change_values.csv']:
    try:
        d=pd.read_csv(f, encoding='utf-8-sig'); print(f.split('/')[-1], d.shape, d.columns.tolist()[:12])
        print(d.head(2).to_string(index=False)[:300]); print()
    except Exception as e: print(f.split('/')[-1],'ERR',e)

# ---------------------------------------------------------------- cell 05f06794 (cell_index 425)
import scipy.io as sio, numpy as np
a=pd.read_csv(f'{P1}/summed_MID_FCs_3conditions.csv')
print(a.Condition.unique(), a.groupby(['Condition']).Score.describe()[['count','mean','std']].round(3).to_string())
print('kmeans groups:', a.groupby(['Kmeans_group','Condition']).size().unstack().to_string())
b=pd.read_csv(f'{P2}/summed_FCs_2conditions_for_plot.csv')
print('\n2cond:', b.shape, 'non-null p2', b['ses-p2'].notna().sum(), 'd2', b['ses-d2'].notna().sum(),
      'paired', (b['ses-p2'].notna()&b['ses-d2'].notna()).sum())
g=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/ampa_ketamine_spearman_4outcomes.csv')
print('\n5g:', g.shape); print(g.to_string(index=False))
M=sio.loadmat('/Users/yunman/Desktop/submission/figures_v2/fig4/predict_fu3_beha_changes/virtual_modu_predict_fu3_beha_changes.mat')
print('\n5h mat vars:', {k:np.asarray(v).shape for k,v in M.items() if not k.startswith('__')})

# ---------------------------------------------------------------- cell 4a491abc (cell_index 429)
sim=pd.read_csv('/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/684a22a0-d6db-4aeb-b5ad-b30777bef882/vd1e0509f_state_similarity_per_subject.csv')
print('state_similarity', sim.shape, sim.columns.tolist())
print(sim.head(3).to_string(index=False))
print('\ngroups:', sim.group.value_counts().to_dict())
ms=pd.read_csv(f'{P2}/ketamine_master_data_for_plots.csv')
print('\nmaster', ms.shape, ms.columns.tolist()[:18], '| groups', ms.group.value_counts().to_dict() if 'group' in ms else '')
r2=pd.read_csv(f'{P2}/np_vs_symptomPC1_change_resid_MDD.csv')
print('\n5f candidate', r2.shape, r2.columns.tolist())

# ---------------------------------------------------------------- cell 1c66a2a8 (cell_index 431)
ph=pd.read_csv(f'{P1}/summed_MID_FCs_3conditions.csv')
print(pd.crosstab(ph.Kmeans_group, ph.Direction))
w=ph.pivot(index='Subject',columns='Condition',values='Score').join(ph.groupby('Subject').Kmeans_group.first())
w['d_ket']=w.Ketamine-w.Placebo; w['d_mid']=w.Midazolam-w.Placebo
print('\nby kmeans group:'); print(w.groupby('Kmeans_group')[['Placebo','Ketamine','Midazolam','d_ket','d_mid']].mean().round(3).to_string())
print(w.groupby('Kmeans_group').size().to_dict())
ms['d']=ms.FC_d2-ms.FC_p2
print('\nMDD/HC pharma:'); print(ms.groupby('group')[['FC_p2','FC_d2','d']].agg(['mean','std','count']).round(3).to_string())

# ---------------------------------------------------------------- cell 64244dbd (cell_index 432)
# [recovery] this cell raised in the original session at its line 19; only the
# statements that had already executed are carried over
import os, shutil
O5='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5'
None; None  # [recovery: side output suppressed]  # [recovery: side output suppressed]
w2=w.reset_index().rename(columns={'Kmeans_group':'subgroup'})
w2['subgroup']=w2.subgroup.map({'Group1':'decreasers','Group2':'increasers'})
pass  # [recovery: side output suppressed] w2[['Subject','subgroup','Placebo','Ketamine','Midazolam','d_ket','d_mid']].to_csv(
# [recovery: side output suppressed]     f'{O5}/fig5_data/fig5_healthy_n27.csv',index=False)
pass  # [recovery: side output suppressed] ms[['SubID','group','FC_p2','FC_d2','FC_delta','MADRS_b0','MADRS_d2','symp_b0_pca','symp_delta_pca']].to_csv(
# [recovery: side output suppressed]     f'{O5}/fig5_data/fig5_mdd_hc_n36.csv',index=False)
pass  # [recovery: side output suppressed] shutil.copy(f'{P2}/np_vs_symptomPC1_change_resid_MDD.csv', f'{O5}/fig5_data/fig5f_np_symptom_resid_MDD_n22.csv')
cv=pd.read_csv(f'{P2}/ketamine_n36_with_covariates.csv')
g5=sim[sim.group=='MDD'][['SubID','pref_p2','pref_d2','crossover']].merge(
    cv[['SubID','age','sex','infusion_1','fd_p2']],on='SubID').merge(
    ms[['SubID','MADRS_delta','HAMD_Bech_delta','HAM17_delta','symp_delta_pca']],on='SubID')
pass  # [recovery: side output suppressed] g5.to_csv(f'{O5}/fig5_data/fig5g_state_similarity_MDD_n22.csv',index=False)
h5=pd.DataFrame(np.column_stack([np.asarray(M['X_final']),np.asarray(M['y_final'])]),
    columns=['ampa_restoration_index','x2','x3','x4','x5','fu3_symptom_change'])
h5.to_csv(os.path.join(OUT_DIR, 'fig5h_longitudinal_n85.csv'), index=False)
