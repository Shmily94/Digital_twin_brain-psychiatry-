# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 336a609c-71ef-4ba4-891b-3222c790e962
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 16:14:27 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3b_common_reference_tests.csv
# ===========================================================================

r=pair('10 M voxel, 100 M hyper','10 M / 1000','10M voxel (100M hyper)','10M/1000')
print(r)
T=pd.concat([T,pd.DataFrame([r])],ignore_index=True); T.to_csv(D3+'fig3b_common_reference_tests.csv',index=False)
P=pd.read_csv(D3+'fig3_results_paragraph_contrasts.csv')
P=pd.concat([P,pd.DataFrame([dict(panel='3b',quantity='whole-brain FC similarity',
    contrast=r['contrast'],unit='participant',n=r['n'],df=r['df'],estimate='%+.4f'%r['mean_diff'],
    ci=r['ci95'].strip('[]'),stat='t = %.3f'%r['t'],p=r['p'])])],ignore_index=True)
P.to_csv(D3+'fig3_results_paragraph_contrasts.csv',index=False)