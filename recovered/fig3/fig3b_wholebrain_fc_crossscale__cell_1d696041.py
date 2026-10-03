# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 1d696041-95de-482e-b3ff-de88ed7fd117
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-21 14:37:40 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3b_wholebrain_fc_crossscale.csv
# ===========================================================================

sar=pd.read_csv(SUB+"revision/text/figures/Model_Benchmark/subject_level_sar_fitting_results.csv")
rww=pd.read_csv(SUB+"revision/text/figures/Model_Benchmark/subject_level_rww_fitting_results.csv")
print("benchmark conditions:", sar.Condition.unique().tolist())
CMAP={'SST_stop_success':'SST Stop Success','SST_stop_failure':'SST Stop Failure',
      'MID_antici_hit':'MID Reward Antici.','MID_feed_hit':'MID Pos. Feedback'}
rows=[]
for nm,d_ in [('SAR',sar),('RWW',rww)]:
    for c_,g in d_.groupby('Condition'):
        rows.append(dict(condition=CMAP[c_], model=nm, r_mean=g.Pearson_r.mean(),
                         r_sd=g.Pearson_r.std(ddof=1), n=len(g)))
bench_fc=pd.DataFrame(rows)
t9b=pd.concat([t9, bench_fc], ignore_index=True)
t9b.to_csv(D3+"fig3b_wholebrain_fc_crossscale.csv", index=False, float_format='%.12g')
print("\n3b with benchmarks:")
print(t9b.pivot(index='condition',columns='model',values='r_mean').round(3).to_string())

a3b = pd.concat([a3, pd.DataFrame([dict(subject_id=r.subject_id, model=m_, family='benchmark',
        empirical_reference='benchmark', mse=getattr(r, f'{m_.lower()}_mse'))
        for r in dv.itertuples() for m_ in ['SAR','RWW']])], ignore_index=True)
a3b.to_csv(D3+"fig3a_mse_per_subject.csv", index=False, float_format='%.12g')
print("\n3a with benchmarks — mean MSE:", a3b.groupby('model',sort=False).mse.mean().round(4).to_dict())
