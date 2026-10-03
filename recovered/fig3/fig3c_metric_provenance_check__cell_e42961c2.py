# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : e42961c2-2a6a-4710-b411-85df8fbcc0bd
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 17:10:37 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3c_metric_provenance_check.csv
# ===========================================================================

rows=[]
for x,y in [('10m','100m'),('10m','1b'),('100m','1b')]:
    for src,dat in [('new .mat (simu_fc_*)',MAT),('archive simulation_results_wide_12subs.csv',CSV)]:
        for nlab,mask in [('all 12',np.ones(12,bool)),('9 with complete archive data',ok)]:
            if src.startswith('archive') and nlab=='all 12': continue
            r=[stats.pearsonr(dat[x][s],dat[y][s])[0] for s in np.where(mask)[0]]
            rows.append(dict(pair=f'{x} vs {y}', simulated_source=src, subjects=nlab, n=len(r),
                             fisher_z_mean=round(float(np.tanh(np.mean(np.arctanh(np.clip(r,-.999,.999))))),4),
                             plain_mean=round(float(np.mean(r)),4),
                             value_in_fc_similarity_six_models_new3m=
                             {'10m vs 100m':0.6497,'10m vs 1b':0.7273,'100m vs 1b':0.8909}[f'{x} vs {y}']))
CMP=pd.DataFrame(rows)
CMP.to_csv(f'{FD3}/fig3c_metric_provenance_check.csv', index=False)
print(CMP.to_string(index=False))
print('\nper-build agreement between the two simulated sources (same 12 subjects):')
for m in ['10m']:
    print(f'  {m}: r = {stats.pearsonr(MAT[m].ravel(),CSV[m].ravel())[0]:.3f}, max|diff| = {np.abs(MAT[m]-CSV[m]).max():.3f}')
print('  100m / 1b: archive table has 36 NaN cells each (subjects 112288, 113174215, 182136619)')
