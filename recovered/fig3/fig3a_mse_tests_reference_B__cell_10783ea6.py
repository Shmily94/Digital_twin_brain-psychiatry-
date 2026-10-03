# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 10783ea6-d4d3-4b01-812e-cd27be3faa14
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 15:22:10 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3a_mse_tests_reference_B.csv
# ===========================================================================

MP=A.pivot_table(index='subject_id',columns='model',values='mse')
M2L={'3m_268':'3 M / 268','10m_268':'10 M / 268','10m_1000':'10 M / 1000','10m_own':'10 M voxel, 10 M hyper',
     '10m':'10 M voxel, 100 M hyper','100m':'100 M voxel','1b':'1 B voxel','SAR':'SAR','RWW':'rWW'}
rows=[]
for k in ['3m_268','10m_268','10m_1000','10m_own','10m','100m','1b','SAR','RWW']:
    s,dr,asc=SRC[M2L[k]]
    rows.append({'simulation scale':s,'data resolution':dr,'assimilation scale':asc,'n':12,
        'empirical reference':('B: 268-parcel FC from the voxels the DTB simulates' if k not in ('SAR','RWW')
                               else 'native Shen-268 regional FC'),
        'NP-edge MSE':ms(MP[k].mean(),MP[k].std(ddof=1)),'median':f'{MP[k].median():.4f}'})
S10B=pd.DataFrame(rows)
MP['vox100']=MP[['10m','100m','1b']].mean(axis=1); MP['reg']=MP[['3m_268','10m_268']].mean(axis=1)
mt=[]
for a_,b_,lab in [('vox100','reg','100M-hyper voxel family vs regional family'),
                  ('vox100','10m_1000','100M-hyper voxel family vs 10M/1000'),
                  ('vox100','10m_own','100M-hyper voxel family vs 10M voxel own hyper'),
                  ('10m','10m_own','10M voxel: 100M hyper vs own 10M hyper'),
                  ('vox100','SAR','100M-hyper voxel family vs SAR'),('vox100','RWW','100M-hyper voxel family vs rWW')]:
    s=MP[[a_,b_]].dropna(); d=s[a_]-s[b_]; t,p=st.ttest_rel(s[a_],s[b_])
    mt.append(dict(contrast=lab,n=len(s),df=len(s)-1,mse_a=f'{s[a_].mean():.4f}',mse_b=f'{s[b_].mean():.4f}',
        diff=f'{d.mean():+.4f}',ci95=f'{d.mean()-st.t.ppf(.975,len(d)-1)*d.std(ddof=1)/np.sqrt(len(d)):.4f} to {d.mean()+st.t.ppf(.975,len(d)-1)*d.std(ddof=1)/np.sqrt(len(d)):.4f}',
        t=round(float(t),3),p=f'{p:.3g}',n_lower=f'{int((d<0).sum())}/{len(d)}'))
T10T=pd.DataFrame(mt)
S10B.to_csv(D3+'fig3a_mse_reference_B.csv',index=False); T10T.to_csv(D3+'fig3a_mse_tests_reference_B.csv',index=False)
print(S10B.drop(columns='empirical reference').to_string(index=False)); print(); print(T10T.to_string(index=False))