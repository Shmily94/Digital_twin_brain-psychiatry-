# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 9898be5e-14e3-4830-a60d-c39f6d3c2ffa
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 15:04:04 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3b_wholebrain_fc_by_condition.csv
# ===========================================================================

ORD=['SST Stop Success','SST Stop Failure','MID Reward Antici.','MID Pos. Feedback']
MLAB={'3m_268':'3 M / 268','10m_268':'10 M / 268','10m_1000':'10 M / 1000',
      '10m_own':'10 M voxel, 10 M hyper','10m_voxel':'10 M voxel, 100 M hyper',
      '100m_voxel':'100 M voxel','1b_voxel':'1 B voxel','SAR':'SAR','RWW':'rWW'}
piv=B.pivot_table(index='model',columns='condition',values=['r_mean','r_sd'])
rows=[]
for m in ['3m_268','10m_268','10m_1000','10m_own','10m_voxel','100m_voxel','1b_voxel','SAR','RWW']:
    d={'build':MLAB[m],'n':int(B[B.model==m].n.iloc[0])}
    for c in ORD: d[c]=ms(piv.loc[m,('r_mean',c)],piv.loc[m,('r_sd',c)])
    d['mean of 4 conditions']=f"{B[B.model==m].r_mean.mean():.4f}"
    rows.append(d)
WBT=pd.DataFrame(rows)
WBT.to_csv(D3+'fig3b_wholebrain_fc_by_condition.csv',index=False)
pd.set_option('display.width',260)
print(WBT.to_string(index=False))