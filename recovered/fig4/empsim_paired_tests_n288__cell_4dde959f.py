# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_empsim/data/empsim_paired_tests_n288.csv
#
# cell id      : 4dde959f-7678-4a21-8dee-200bbcc14bd8
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-22 20:15:54 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/24_empsim_paired_tests_n288.py
##############################################################################
SD2='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_empsim/data'
sl[['ID','Group','empirical','simulated','empirical_resid','simulated_resid','sex','site','headmotion']]\
  .to_csv(f'{SD2}/empsim_subject_level_n288.csv', index=False)
allr=[]
for pair,lab in [(('empirical','simulated'),'raw'),(('empirical_resid','simulated_resid'),'residualised')]:
    for g in GRPS:
        s_=sl[sl.Group==g]; a,b2=s_[pair[0]].values,s_[pair[1]].values; d=b2-a
        t=stats.ttest_rel(b2,a); w=stats.wilcoxon(b2,a); ci=stats.t.interval(.95,len(d)-1,d.mean(),stats.sem(d))
        allr.append(dict(scores=lab, group=g, n=len(d),
            empirical_mean=round(float(a.mean()),4), empirical_sd=round(float(a.std(ddof=1)),4),
            simulated_mean=round(float(b2.mean()),4), simulated_sd=round(float(b2.std(ddof=1)),4),
            mean_diff_sim_minus_emp=round(float(d.mean()),4), ci95_lo=round(float(ci[0]),4), ci95_hi=round(float(ci[1]),4),
            t=round(float(t.statistic),3), df=len(d)-1, p_paired_t=float(t.pvalue), wilcoxon_p=float(w.pvalue),
            cohens_dz=round(float(d.mean()/d.std(ddof=1)),3), pearson_r_emp_sim=round(float(stats.pearsonr(a,b2)[0]),3)))
pd.DataFrame(allr).to_csv(f'{SD2}/empsim_paired_tests_n288.csv', index=False)
print(pd.DataFrame(allr)[['scores','group','n','t','df','p_paired_t','wilcoxon_p','cohens_dz','pearson_r_emp_sim']]
      .to_string(index=False, float_format=lambda x:f'{x:.4g}'))
