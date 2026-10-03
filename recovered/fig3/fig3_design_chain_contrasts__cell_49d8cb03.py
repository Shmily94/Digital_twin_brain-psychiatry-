# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 49d8cb03-f5d2-4cc7-969f-4c3dfedc30cc
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 18:01:41 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3_design_chain_contrasts.csv
# ===========================================================================

STEPS=[('1  assimilation scale','10m_own','10m','assimilation 10 M voxel → 100 M'),
       ('2  drop to 1000 regions','10m_own','10m_1000','voxel → 1000 regions'),
       ('3  drop to 268 regions','10m_1000','10m_268','1000 → 268 regions'),
       ('4  cheaper neurons','10m_268','3m_268','10 M → 3 M neurons')]
allrows=[]
for nm,a,bq,fac in STEPS:
    for metric,vals,better in [('assimilated BOLD r',V,'higher'),('NP-edge MSE',M,'lower'),
                               ('whole-brain FC r',WBPS,'higher')]:
        if a not in vals or bq not in vals: continue
        allrows.append(contrast(nm,a,bq,vals,metric,fac,better))
CH2=pd.DataFrame(allrows)
CH2['n']=CH2.metric.map({'assimilated BOLD r':24,'NP-edge MSE':12,'whole-brain FC r':12})
CH2.to_csv(f'{FD3}/fig3_design_chain_contrasts.csv', index=False)
print(CH2[['step','metric','n','mean_from','mean_to','mean_diff','dz','t_p']]
      .to_string(index=False, float_format=lambda x:f'{x:.4g}'))
