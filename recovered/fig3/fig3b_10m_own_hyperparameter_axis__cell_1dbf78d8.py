# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 1dbf78d8-6fdc-4505-97f9-8822a3724f5e
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 15:00:44 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3b_10m_own_hyperparameter_axis.csv
# ===========================================================================

def ms(m,s,p=4): return f'{m:.{p}f} ± {s:.{p}f}'
# 1. hyper-parameter axis table
OW2=pd.DataFrame([dict(build=r.build,reference=r.reference,n=r.n,
                       mean_sd=ms(r['mean'],r.sd),range=f'{r["min"]:.4f}–{r["max"]:.4f}')
                  for _,r in OW.iterrows()])
OW2.to_csv(D3+'fig3b_10m_own_hyperparameter_axis.csv',index=False)
# 2. the paired tests
BW2=pd.DataFrame([dict(reference=r.reference,n=r.n,
        own_hyper_10M=ms(r.own_hyper_mean,r.own_hyper_sd),own_hyper_range=r.own_hyper_range,
        hyper_100M=ms(r.hyper100m_mean,r.hyper100m_sd),difference=f'{r["diff"]:+.4f}',ci95=r.ci,
        t=r.t,df=r.df,p=r.p,dz=r.dz,n_higher=r.n_higher,wilcoxon_p=r.wilcoxon_p,fold=r.fold)
        for _,r in BW.iterrows()])
BW2.to_csv(D3+'fig3b_hyperparameter_axis_tests.csv',index=False)
# 3. benchmark table
BT2=pd.DataFrame([dict(model=r.model,condition=r.condition,n=r.n,
        fc_pearson_r=ms(r.fc_pearson_r_mean,r.fc_pearson_r_sd),
        wholebrain_mse=f'{r.wholebrain_mse_mean:.4f}') for _,r in BT.iterrows()])
BT2.to_csv(D3+'fig3b_benchmark_wholebrain_fc.csv',index=False)
for n,d in [('fig3b_10m_own_hyperparameter_axis',OW2),('fig3b_hyperparameter_axis_tests',BW2),('fig3b_benchmark_wholebrain_fc',BT2)]:
    print('###',n); print(d.to_string(index=False)); print()