# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 3c7e0c72-9ebb-4721-a3d5-f131cda7ec4f
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 17:49:04 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3i_assimilated_bold_r.csv
# ===========================================================================

rows=[]
NREP={'3m_268':5,'10m_268':5,'10m_1000':5,'10m':5,'100m':5,'1b':5,'10m_own':1}
for _,r in T.iterrows():
    for c in BCOL:
        k=XLMAP[c]
        rows.append(dict(subject_id=str(r['被试']).replace('sub-','').lstrip('0'), task=r['任务'], model=k,
                         family=FAMILY[k], sim_neurons=SIMN[k], assimilation_hyperparams=HYP[k],
                         resolution=RES[k], n_repeats_averaged=NREP[k], bold_r=round(float(r[c]),5)))
BR=pd.DataFrame(rows); BR.to_csv(f'{FD3}/fig3i_assimilated_bold_r.csv', index=False)
st=[]
for a,bq in [('1b','100m'),('1b','10m'),('100m','10m'),('3m_268','1b'),('10m','10m_own'),('10m_own','10m_1000')]:
    d=V[a]-V[bq]
    st.append(dict(pair=f'{a} vs {bq}', mean_diff=round(float(d.mean()),5),
                   t_p=float(stats.ttest_rel(V[a],V[bq]).pvalue),
                   wilcoxon_p=float(stats.wilcoxon(V[a],V[bq]).pvalue), n_pairs=len(d)))
pd.DataFrame(st).to_csv(f'{FD3}/fig3i_bold_r_paired_tests.csv', index=False)
print(BR.groupby('model').bold_r.agg(['mean','std']).reindex(ORDER).round(4).to_string())
