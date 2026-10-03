# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/long85_add_summed_empirical_to_sim12.csv
# cell id       : e44e3f3e-dba6-40b3-9f11-4c6982757fe8
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 711
# executed at   : 2026-09-29 14:15 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/32_long85_add_summed_empirical_to_sim12.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

def williams(r_jk,r_jh,r_kh,n):
    R=1-r_jk**2-r_jh**2-r_kh**2+2*r_jk*r_jh*r_kh
    t=(r_jk-r_jh)*np.sqrt((n-1)*(1+r_kh)/(2*((n-1)/(n-3))*R+((r_jk+r_jh)**2/4)*(1-r_kh)**3))
    return t, 2*stats.t.sf(abs(t),n-3)
r_kh=np.corrcoef(p_f,p_b)[0,1]
tw,pw=williams(r_f,r_b,r_kh,85)
print('pred-pred r=%.3f  Williams t(82)=%.2f P=%.3f'%(r_kh,tw,pw))
rng=np.random.default_rng(1); nperm=5000; c=0
for _ in range(nperm):
    c+= loo_r(FULL,rng.permutation(y))[0]>=r_f
print('LOO perm P full=%.4f'%((c+1)/(nperm+1)))
out=pd.DataFrame([
 dict(model='covariates + 12 simulated edges',k_added=12,dR2=0.3347,F=3.0169,df1=12,df2=63,P=0.0022,R2=0.4176,LOO_r=round(r_b,4)),
 dict(model='covariates + 12 simulated edges + summed empirical NP',k_added=1,dR2=inc['dR2'],F=inc['F'],df1=1,df2=62,P=inc['P'],R2=inc['R2full'],LOO_r=round(r_f,4)),
])
out.to_csv('long85_add_summed_empirical_to_sim12.csv',index=False)
print(out.round(4).to_string(index=False))
