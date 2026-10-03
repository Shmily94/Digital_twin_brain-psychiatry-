# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4_sdq_composite_stats.csv
#
# cell id      : a9666212-e3ef-41f3-8ac3-b4d157a1e8b1
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:23:19 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/06_fig4_sdq_composite_stats.py
##############################################################################
D4='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data'
X[['ID','G','pattern','ampa_dir','emotional','conduct','hyperactivity','peer',
   'neg_sum','pos_sum','neg_pc1','pos_pc1','sub4_pc1']].rename(columns={'G':'Group'}).to_csv(
   f'{D4}/fig4_sdq_composites_n287.csv',index=False)
pd.concat([R1,R2]).to_csv(f'{D4}/fig4_sdq_composite_stats.csv',index=False)
import shutil
W='/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/workspaces/fe47a03f-2d43-4fe0-a1c3-e0544839d822/'
for f in ['fig4_sdq_composites_n287.csv','fig4_sdq_composite_stats.csv']: shutil.copy(f'{D4}/{f}',W)
# how much of the negative sum do the peer items carry?
print('peer subscale vs neg_sum r = %.2f'%np.corrcoef(X.peer,X.neg_sum)[0,1])
print('Cronbach-ish: neg 20-item PC1 explains %.1f%% of variance'%(vn[0]*100))
print('\ngroup composition of the two AMPA directions:')
print(pd.crosstab(X.G,X.ampa_dir).to_string())
