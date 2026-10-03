# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/fig.1/fig1_data/fig1_sample_selection.csv
# cell id     : 6cb740f2-6c20-471f-bce9-283abd39f368
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-22 21:09:09 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

F1='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.1'
os.makedirs(f'{F1}/fig1_data',exist_ok=True)
SEL=pd.DataFrame([
 dict(stage=1,cohort='IMAGEN discovery',screened=1050,analysed=1050,excluded=0,reason='',
      source='fig2a_cpm_rho.csv (edge selection cohort)'),
 dict(stage=1,cohort='STRATIFY validation',screened=513,analysed=427,excluded=86,
      reason='eating disorder 79; psychosis 6; ADHD 1',
      source='fig2f_sensitivity_cohort_covariates.csv (513 / 434 / 427)'),
 dict(stage=2,cohort='Cross-scale twins',screened=12,analysed=12,excluded=0,reason='',
      source='fig3a_mse_per_subject.csv'),
 dict(stage=3,cohort='Population twins',screened=290,analysed=288,excluded=2,
      reason='mean framewise displacement > 0.5 mm',
      source='group_empir_simu_manipu_np_Resi3.csv (290) \u2192 fig4_subject_level_n288.csv'),
 dict(stage=4,cohort='Healthy crossover',screened=27,analysed=27,excluded=0,reason='',
      source='summed_MID_FCs_3conditions.csv (27 \u00d7 3 conditions)'),
 dict(stage=4,cohort='Clinical ketamine',screened=41,analysed=36,excluded=5,
      reason='incomplete placebo + ketamine session pair (MDD 3, HC 2)',
      source='age_demographics_placebo_np_n41.csv \u2192 age_demographics_n36.csv'),
 dict(stage=5,cohort='IMAGEN follow-up',screened=288,analysed=85,excluded=203,
      reason='no usable four-year follow-up symptom data',
      source='fig5h_longitudinal_n85.csv'),
])
SEL.to_csv(f'{F1}/fig1_data/fig1_sample_selection.csv',index=False)
mini={}
mini['edges']=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv')
mini['fidelity']=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data/fig3i_assimilated_bold_r.csv')
print(SEL.to_string(index=False)); print(); print('fidelity cols',mini['fidelity'].columns.tolist(), mini['fidelity'].shape)
