# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/long85_adjusted_increments.csv
# cell id       : 4c80146c-fc10-451d-b6d0-8b0eb8cc27ce
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 650
# executed at   : 2026-09-29 12:36 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/33_long85_adjusted_increments.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

INC={
 '12 simulated NP edges beyond covariates': nested2([],sim),
 '12 empirical NP edges beyond covariates': nested2([],emp),
 'summed simulated NP beyond covariates': nested2([],['simbase_np_sum']),
 'summed empirical NP beyond covariates': nested2([],['emp_np_sum']),
 '12 simulated beyond the 12 empirical edges': nested2(emp,sim),
 '12 empirical beyond the 12 simulated edges': nested2(sim,emp),
 'summed simulated beyond summed empirical NP': nested2(['emp_np_sum'],['simbase_np_sum']),
 'summed empirical beyond summed simulated NP': nested2(['simbase_np_sum'],['emp_np_sum']),
 '12 simulated edges beyond age-19 symptoms': nested2(['beha19_sum'],sim),
 '12 empirical edges beyond age-19 symptoms': nested2(['beha19_sum'],emp),
}
INC3=pd.DataFrame(INC).T; INC3['q_BH']=multipletests(INC3.P,method='fdr_bh')[1]
INC3['P_bonf']=np.minimum(INC3.P*len(INC3),1)
INC3.index.name='increment'; INC3.to_csv('long85_adjusted_increments.csv')
print(INC3[['dR2','F','df1','df2','P','q_BH','P_bonf']].to_string(float_format=lambda v:'%.4g'%v))
print('\npartial correlations with symptom change, adjusted for covariates:')
def partial(col):
    Z=sm.add_constant(np.asarray(MM[COVC],float))
    rx=y-Z@np.linalg.lstsq(Z,y,rcond=None)[0]; rz=MM[col].values-Z@np.linalg.lstsq(Z,MM[col].values,rcond=None)[0]
    r,p=stats.pearsonr(rx,rz); dfp=len(y)-len(COVC)-2
    lo,hi=np.tanh(np.arctanh(r)+np.array([-1,1])*1.96/np.sqrt(dfp-1))
    return r,p,dfp,lo,hi
for c in ['simbase_np_sum','emp_np_sum','beha19_sum']:
    r,p,dfp,lo,hi=partial(c); print('  %-16s partial r = %+.2f, P = %.4f, df = %d, 95%% CI %.2f to %.2f'%(c,r,p,dfp,lo,hi))
