# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS15_covariate_adjusted_models.csv
# cell id     : 7cb0f84d-b703-4c6e-9dd7-cb2240f1a89e
# frame id    : b194cd74-5255-435a-9c1e-206638f9adae
# executed    : 2026-09-29 12:26:42 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================


SPEC2={'covariates only':COVC,'+ summed simulated':COVC+['simbase_np_sum'],'+ summed empirical':COVC+['emp_np_sum'],
       '+ 12 simulated edges':COVC+sim,'+ 12 empirical edges':COVC+emp,
       '+ symptoms':COVC+['beha19_sum'],'+ symptoms + 12 simulated':COVC+['beha19_sum']+sim,
       '+ symptoms + 12 empirical':COVC+['beha19_sum']+emp}
rng=np.random.default_rng(23); OUT=[]
for k,cols in SPEC2.items():
    p,m=loo_pred(MM[cols],y); r=np.corrcoef(p,y)[0,1]
    X=sm.add_constant(np.asarray(MM[cols],float))
    null=np.array([loo_r_fast(X,rng.permutation(y)) for _ in range(2000)])
    OUT.append(dict(model=k,R2=m.rsquared,adjR2=m.rsquared_adj,loo_r=r,
                    cvR2=1-np.sum((y-p)**2)/np.sum((y-y.mean())**2), perm_P=((null>=r).sum()+1)/2001))
A=pd.DataFrame(OUT); A['q_BH']=multipletests(A.perm_P,method='fdr_bh')[1]
print(A.to_string(index=False,float_format=lambda v:'%.4g'%v))
A.to_csv('figS15_covariate_adjusted_models.csv',index=False); Z2.round(6).to_csv('figS15_covariate_adjusted_increments.csv')
