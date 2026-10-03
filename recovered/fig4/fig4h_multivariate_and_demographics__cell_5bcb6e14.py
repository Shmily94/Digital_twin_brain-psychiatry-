# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4h_multivariate_and_demographics.csv
#
# cell id      : 5bcb6e14-c58d-447d-b78a-f6cdc07704d3
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 20:02:32 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/15_fig4h_multivariate_and_demographics.py
##############################################################################
rows=[
 dict(analysis='PLS-DA (2 comp), SDQ only', block='26 SDQ items', adj='none',
      metric='CV AUC', value=round(cv_auc(B[SDQI].values,M.y.values,2,reps=2,seed=1),3), perm_p=np.nan),
 dict(analysis='PLS-DA (2 comp), SDQ+DAWBA', block='26 SDQ + 6 DAWBA', adj='none',
      metric='CV AUC', value=round(obs_raw,3), perm_p=round(p_raw,3)),
 dict(analysis='PLS-DA (2 comp), SDQ+DAWBA', block='26 SDQ + 6 DAWBA', adj='sex+site+FD',
      metric='CV AUC', value=round(obs_adj,3), perm_p=round(p_adj,3)),
 dict(analysis='CCA r1, behaviour vs brain', block='32 behaviour vs baseline NP, dAMPA, dGABA',
      adj='none', metric='canonical r', value=round(r1,3), perm_p=0.020),
 dict(analysis='CCA r1, behaviour vs brain', block='32 behaviour vs baseline NP, dAMPA, dGABA',
      adj='sex+site+FD', metric='canonical r', value=round(r1a,3), perm_p=0.178),
 dict(analysis='sex vs pattern (chi2)', block='—', adj='none', metric='chi2 (1 df)',
      value=5.53, perm_p=0.0187),
 dict(analysis='sex vs pattern (logistic LR)', block='—', adj='site+FD+group',
      metric='chi2 (1 df)', value=4.76, perm_p=0.0291),
 dict(analysis='site vs pattern (chi2)', block='—', adj='none', metric='chi2 (7 df)',
      value=10.49, perm_p=0.162),
 dict(analysis='site vs pattern (logistic LR)', block='—', adj='sex+FD+group',
      metric='chi2 (7 df)', value=11.28, perm_p=0.127)]
R=pd.DataFrame(rows)
R.to_csv(f'{F}/fig4h_multivariate_and_demographics.csv',index=False)
import shutil
shutil.copy(f'{F}/fig4h_multivariate_and_demographics.csv',
            '/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/workspaces/fe47a03f-2d43-4fe0-a1c3-e0544839d822/')
print(R.to_string(index=False))
