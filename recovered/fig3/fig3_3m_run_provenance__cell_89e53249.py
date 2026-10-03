# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 89e53249-e679-4b45-98f8-256ddea81e98
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 16:00:12 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3_3m_run_provenance.csv
# ===========================================================================

newFC=np.column_stack([res[c] for c in CORD]).mean(axis=1)   # new-run 3M, per participant, ref B
old=PB['3 M / 268'].values
rows=[dict(panel='Fig. 3a / Table S10 (NP-edge MSE)',quantity='3M/268 MSE, reference B',
      old_run='0.0851 (six_model_mse_12subs.csv)',new_run='0.0649',used_in_figure='NEW run',verdict='CORRECT'),
 dict(panel='Fig. 3b / Table S9 (whole-brain FC)',quantity='3M/268 whole-brain r, reference B',
      old_run=f'{old.mean():.4f} ± {old.std(ddof=1):.4f}',new_run=f'{newFC.mean():.4f} ± {newFC.std(ddof=1):.4f}',
      used_in_figure='OLD run',verdict='MISMATCH')]
print(pd.DataFrame(rows).to_string(index=False))
print('\n--- what changes if the whole-brain panel is switched to the new 3M run')
d=old-newFC; t,p=st.ttest_rel(old,newFC)
print('  3M/268 whole-brain r: %.4f (old) -> %.4f (new), diff %+.4f, t(11) = %.2f, P = %.3g'%(old.mean(),newFC.mean(),-d.mean(),t,p))
for other,lab in [('10 M / 268','10M/268'),('SAR','SAR'),('rWW','rWW')]:
    s=pd.DataFrame({'a':PB[other].values,'b':newFC}).dropna(); dd=s.a-s.b; tt,pp=st.ttest_rel(s.a,s.b)
    print(f'  {lab:8s} vs NEW 3M/268: diff {dd.mean():+.4f}, t(11) = {tt:.3f}, P = {pp:.3g}   (vs OLD 3M/268 was '
          f'{PB[other].mean()-old.mean():+.4f})')
CK=pd.DataFrame(rows); CK.to_csv(D3+'fig3_3m_run_provenance.csv',index=False)