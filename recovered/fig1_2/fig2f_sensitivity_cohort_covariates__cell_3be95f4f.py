# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/fig.2/fig2_data/fig2f_sensitivity_cohort_covariates.csv
# cell id     : 3be95f4f-5095-4838-a544-3174bbfabd61
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-21 13:17:15 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

rows=[]
for name,sub in cohorts.items():
    for adj in (True,False):
        n,nq,np_,which,t = run(sub,adj)
        rows.append(dict(cohort=name, covariates='sex + site + meanFD' if adj else 'none (raw edges)',
                         n=n, n_patients=int((sub.Diseased!='HC').sum()),
                         n_edges_FDR=nq, n_edges_p05=np_,
                         edges_FDR=' '.join(f'E{i}' for i in which)))
sens=pd.DataFrame(rows)
sens.to_csv(OUT+"fig2_data/fig2f_sensitivity_cohort_covariates.csv", index=False)
print(sens.to_string(index=False))
