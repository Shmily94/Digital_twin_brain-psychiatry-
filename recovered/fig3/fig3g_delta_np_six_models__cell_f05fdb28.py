# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : f05fdb28-ecb6-44a6-b124-4323104531dc
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-21 14:02:47 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3g_delta_np_six_models.csv
#                   (written under its pre-rename name fig3f_delta_np_six_models.csv)
# ===========================================================================

base_map={'10m_1000':'10m_reg','10m':'10m','100m':'100m','1b':'1b'}
prof={}
for mdl,sc_ in base_map.items():
    A=base[base.scale==sc_].copy(); A['sid']=[int(s.split('-')[1]) for s in A.subID]
    prof[mdl]=A.set_index('sid')[ecols]
prof['3m_268']=w12.set_index('id_numeric')[[f'baseline_edge{i}' for i in range(1,13)]].rename(
    columns={f'baseline_edge{i}':f'edge{i}' for i in range(1,13)})
ORDER5=['3m_268','10m_1000','10m','100m','1b']
m5=pd.DataFrame(index=ORDER5,columns=ORDER5,dtype=float)
for i_ in ORDER5:
    for j_ in ORDER5:
        ids=prof[i_].index.intersection(prof[j_].index)
        m5.loc[i_,j_]=stats.pearsonr(prof[i_].loc[ids].values.ravel(), prof[j_].loc[ids].values.ravel())[0]
m5.to_csv(D3+"fig3b_cross_scale_similarity.csv", float_format='%.12g')
print("3b 5x5 (per-edge baseline profile, n = 144 subject x edge):"); print(m5.round(3).to_string())
print("\n10m_268 baseline rows in coarse file:", int(((modu.condition=='baseline')&(modu.model=='coarse')).sum()),
      "| 10m_268 in newflow:", int((nf.scale=='10m_268').sum()))

f6=six.melt(id_vars=['model','style','sub_id'], value_vars=['d_ampa','d_gaba'],
            var_name='drug', value_name='delta')
f6['drug']=f6.drug.str.replace('d_','',regex=False)
f6.to_csv(D3+"fig3f_delta_np_six_models.csv", index=False, float_format='%.12g')
print("\n3f six-model delta mean (summed NP over 12 edges):")
print(f6.groupby(['drug','model']).delta.agg(['mean','std']).round(3).to_string())
