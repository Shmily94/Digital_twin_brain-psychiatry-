# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : ba4d43f8-e8fe-4c0c-baa4-d54a309c2b1a
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 09:06:59 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3a_mse_per_subject.csv
# ===========================================================================

rows=[]
HYP={'3m_268':'3 M','10m_268':'3 M','10m_1000':'10 M / 1000','10m_own':'10 M voxel',
     '10m':'100 M','100m':'100 M','1b':'100 M','SAR':'—','RWW':'—'}
SIMN={'3m_268':'3 M','10m_268':'10 M','10m_1000':'10 M','10m_own':'10 M','10m':'10 M',
      '100m':'100 M','1b':'1 B','SAR':'—','RWW':'—'}
RES={'3m_268':'268 regions','10m_268':'268 regions','10m_1000':'1000 regions',
     '10m_own':'voxel','10m':'voxel','100m':'voxel','1b':'voxel','SAR':'—','RWW':'—'}
FAMILY={'3m_268':'regional','10m_268':'regional','10m_1000':'regional',
        '10m_own':'voxel','10m':'voxel','100m':'voxel','1b':'voxel',
        'SAR':'benchmark','RWW':'benchmark'}
# 1. carry over the builds that are unchanged
for mdl in ['10m_268','10m_1000','10m','100m','1b','SAR','RWW']:
    for _,r in a3[a3.model==mdl].iterrows():
        rows.append(dict(subject_id=r.subject_id, model=mdl, mse=r.mse,
                         empirical_reference=r.empirical_reference))
# 2. new 3M run, mean of 5 repeats, vs the same regional empirical reference
for s,v in zip(sid3, mse(new3m_mean, EMP_R)):
    rows.append(dict(subject_id=int(s), model='3m_268', mse=round(float(v),5),
                     empirical_reference='emp_edge1-12 (simulation_results_wide_12subs.csv)'))
# 3. new 10M-voxel build with its own hyperparameters
for s,v in zip(sub_ids, mse(SIM['10m_own_params'], EMP_V)):
    rows.append(dict(subject_id=int(s), model='10m_own', mse=round(float(v),5),
                     empirical_reference='real_fc_dtb_voxels (mask-matched)'))
A=pd.DataFrame(rows)
A['family']=A.model.map(FAMILY); A['sim_neurons']=A.model.map(SIMN)
A['assimilation_hyperparams']=A.model.map(HYP); A['resolution']=A.model.map(RES)
A=A[['subject_id','model','family','sim_neurons','assimilation_hyperparams','resolution',
     'empirical_reference','mse']]
A.to_csv(f'{FD3}/fig3a_mse_per_subject.csv', index=False)
print(A.groupby(['model','family','sim_neurons','assimilation_hyperparams']).mse
      .agg(['mean','std','count']).round(4).to_string())
