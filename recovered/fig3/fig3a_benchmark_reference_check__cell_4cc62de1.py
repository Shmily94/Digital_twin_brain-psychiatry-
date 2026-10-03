# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 4cc62de1-2d3e-40af-ab86-d39b0ddc5b5e
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 17:39:04 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3a_benchmark_reference_check.csv
# ===========================================================================

rows=[]
for bm in ['SAR','rWW']:
    e=pd.read_csv(f'{MB}/np_edges_prediction_error_matrix_'+('sar' if bm=='SAR' else 'rww')+'.csv').set_index('Subject_ID')
    e.index=[str(i) for i in e.index]; e=e.loc[sid].values; pred=e+E268
    for si,s in enumerate(sid):
        rows.append(dict(subject_id=int(s), model=bm,
                         mse_vs_268region_empirical=round(float((e[si]**2).mean()),5),
                         mse_vs_empirical_model_voxels=round(float(((pred[si]-EMPW[si])**2).mean()),5)))
B=pd.DataFrame(rows)
B.to_csv(f'{FD3}/fig3a_benchmark_reference_check.csv', index=False)
print(B.groupby('model')[['mse_vs_268region_empirical','mse_vs_empirical_model_voxels']].mean().round(5).to_string())
print('\nranking if benchmarks are put on the voxel reference:')
r=pd.Series({**{k: float(mse(PROF[k],EMPW).mean()) for k in ORDER},
             'SAR':0.05279,'rWW':0.08236}).sort_values()
print(r.round(5).to_string())
