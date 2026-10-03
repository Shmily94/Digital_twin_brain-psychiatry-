# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/supp_longitudinal/data/long_correlations_n85.csv
# cell id       : 330eedd4-4fd1-4cd7-b987-eaab95c94741
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 825
# executed at   : 2026-09-22 20:26 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/52_long_correlations_n85.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
import os
LD='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_longitudinal'
os.makedirs(f'{LD}/panels',exist_ok=True); os.makedirs(f'{LD}/data',exist_ok=True)
CO.to_csv(f'{LD}/data/long_full_model_coefficients_n85.csv', index=False)
INC.to_csv(f'{LD}/data/long_nested_increments_n85.csv', index=False)
CR.to_csv(f'{LD}/data/long_correlations_n85.csv', index=False)
CV.to_csv(f'{LD}/data/long_cv_out_of_sample_n85.csv', index=False)
np.savez(f'{LD}/data/long_permutation_nulls.npz', **{f'{k[0]}|{k[1]}':v for k,v in NULLS.items()})
pd.DataFrame({'ampa_index':ampa85,'gaba_index':gaba85,'empirical_baseline_np_sum':empS,
              'fu3_symptom_change':y85, **{f'baseline_behaviour_{i+1}':beha85[:,i] for i in range(6)},
              'baseline_symptom_sum_4':COV4.sum(1)}).to_csv(f'{LD}/data/long_subject_level_n85.csv', index=False)
pd.DataFrame(CVS).to_csv(f'{LD}/data/long_cv_repeats_n85.csv', index=False)
print('model summary: R2_full', round(float(m_full.rsquared),4), '| F', round(float(m_full.fvalue),3),
      f'({int(m_full.df_model)},{int(m_full.df_resid)})', '| P', f'{m_full.f_pvalue:.3g}')
print('tables written:', sorted(os.listdir(f'{LD}/data')))
