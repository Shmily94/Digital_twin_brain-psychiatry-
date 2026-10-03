# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_motion/data/motion_correlations.csv
#
# cell id      : b72044c3-67ab-4c45-91dc-304f0d61104b
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 21:45:42 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/35_motion_correlations.py
##############################################################################
MC=pd.read_csv(f"{dirs['motion']}/data/motion_correlations.csv")
m=len(MC)
MC['p_bonferroni']=np.minimum(1.0, MC.p*m).round(4)
MC['p_bonferroni_S25']=np.minimum(1.0, MC.p_S25*m).round(4)
MC['sig_bonferroni']=MC.p_bonferroni<.05
MC['sig_bonferroni_S25']=MC.p_bonferroni_S25<.05
MC['sig_fdr']=MC.q_fdr<.05
MC['sig_fdr_S25']=MC.q_fdr_S25<.05
MC.to_csv(f"{dirs['motion']}/data/motion_correlations.csv", index=False)
print(f'Bonferroni family m = {m}, threshold alpha/m = {0.05/m:.5f}\n')
print(MC[['outcome','r','p','q_fdr','p_bonferroni','sig_bonferroni',
          'r_tableS25','p_S25','q_fdr_S25','p_bonferroni_S25','sig_bonferroni_S25']].to_string(index=False))
print('\nsurvive Bonferroni, corrected dataset:', list(MC.loc[MC.sig_bonferroni,'outcome']))
print('survive Bonferroni, Table S25 dataset:', list(MC.loc[MC.sig_bonferroni_S25,'outcome']))
print('\nagreement between the two datasets under FDR: %d/6 rows; under Bonferroni: %d/6 rows'
      % (int((MC.sig_fdr==MC.sig_fdr_S25).sum()), int((MC.sig_bonferroni==MC.sig_bonferroni_S25).sum())))
