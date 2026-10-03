# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/long85_adjusted_models.csv
# cell id       : cdf07dfd-7770-4717-b207-ae94a144441f
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 649
# executed at   : 2026-09-29 12:36 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/34_long85_adjusted_models.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

SPEC3={'covariates only':COVC,
 'covariates + age-19 symptoms':COVC+['beha19_sum'],
 'covariates + 12 simulated NP edges':COVC+sim,
 'covariates + 12 empirical NP edges':COVC+emp,
 'covariates + summed simulated NP':COVC+['simbase_np_sum'],
 'covariates + summed empirical NP':COVC+['emp_np_sum'],
 'covariates + symptoms + 12 simulated NP edges':COVC+['beha19_sum']+sim,
 'covariates + symptoms + 12 empirical NP edges':COVC+['beha19_sum']+emp,
 'covariates + summed simulated + summed empirical NP':COVC+['simbase_np_sum','emp_np_sum']}
rng=np.random.default_rng(101); MODELS3=[]; PRED3={}
for k,cols in SPEC3.items():
    p,m=loo_pred(MM[cols],y); r,_=stats.pearsonr(p,y); PRED3[k]=p
    X=sm.add_constant(np.asarray(MM[cols],float))
    null=np.array([loo_r_fast(X,rng.permutation(y)) for _ in range(5000)])
    MODELS3.append(dict(model=k,k_pred=len(cols),R2=m.rsquared,adj_R2=m.rsquared_adj,F=m.fvalue,df1=int(m.df_model),
        df2=int(m.df_resid),P_model=m.f_pvalue,loo_r=r,cv_R2=1-np.sum((y-p)**2)/np.sum((y-y.mean())**2),
        perm_P=((null>=r).sum()+1)/5001, null_p95=np.percentile(null,95)))
MOD3=pd.DataFrame(MODELS3); MOD3['q_BH_perm']=multipletests(MOD3.perm_P,method='fdr_bh')[1]
print(MOD3.to_string(index=False,float_format=lambda v:'%.4g'%v))
MOD3.to_csv('long85_adjusted_models.csv',index=False)
