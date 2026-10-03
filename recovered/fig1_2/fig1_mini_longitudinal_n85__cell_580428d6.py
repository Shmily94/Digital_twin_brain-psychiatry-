# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/fig.1/fig1_data/fig1_mini_longitudinal_n85.csv
# cell id     : 580428d6-95dc-4aad-9790-2ae4bfe22707
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-22 21:09:19 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

MD1=f'{F1}/fig1_data'
fid=mini['fidelity'].groupby('model').bold_r.mean().sort_values(ascending=False)
fid.rename('bold_r_mean').to_csv(f'{MD1}/fig1_mini_fidelity.csv')
S4[['ID','Group','simulated','ampa','gaba']].to_csv(f'{MD1}/fig1_mini_perturbation_n288.csv',index=False)
R27.reset_index().to_csv(f'{MD1}/fig1_mini_healthy_n27.csv',index=False)
M36[['SubID','group','FC_p2','FC_d2']].to_csv(f'{MD1}/fig1_mini_clinical_n36.csv',index=False)
L85.to_csv(f'{MD1}/fig1_mini_longitudinal_n85.csv',index=False)
mini['edges'].to_csv(f'{MD1}/fig1_mini_np12_edges.csv',index=False)
print(fid.round(4).to_string())
print('\nL85 corr(ampa index, fu3 change) =', round(stats.pearsonr(L85.ampa_restoration_index,L85.fu3_symptom_change)[0],4))
