#!/usr/bin/env python3
"""fig5i_np12_loo_accuracy.csv

Computes
    Leave-one-out prediction accuracy of the five model specifications of Fig.
    5i (symptoms only, 12 simulated edges, 12 empirical edges, and the two
    combined models): LOO r, LOO R2, the parametric and permutation P values
    and the null 95th percentile (2,000 outcome permutations).

Inputs
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/restoration_index_clinical_weights/
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/240926Supplementary Information-liyi.docx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/250926NatMed_Manuscript_Claude_tracked-gunter.docx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures
    - (path built in the chain) base+f
    - (path built in the chain) bp+'np85_full_table_corrected_groups.csv'
    - (path built in the chain) bp+'np85_full_table_datadictionary.csv'
    - (path built in the chain) base+'clinicalW_mapping_edge_weights.csv'

Output
    04_figures/fig.5/fig5_data/fig5i_np12_loo_accuracy.csv

Statistical tests
      - none in this script's own computation: it assembles a source-data /
        audit table, and the tests that use it are named in the scripts of
        the tables downstream
    in the recovered chain that prepares its inputs:
      - Pearson correlation
      - ordinary least squares GLM with covariates
      - outcome-permutation null
      - leave-one-out cross-validation

Local runnability
    partial (local_runnable = partial).  Verification: not_run.
    re-run stops at a helper module that lived only in the original session
    workspace ('docxedit'); it is not part of the package and has no offline
    equivalent
Recovered from
    execution-log cell 76935dae-cb54-4fc2-b7fc-ad874e070d6a
    frame b194cd74-5255-435a-9c1e-206638f9adae, cell_index 144, 2026-09-26 21:40 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    d33b3ce6, 297defc1, 734cfe01, 5e8b6c30, 876400dd, cc69d8f7, e1375717,
    76935dae

Random seed
    fixed in the original run: seed = 0.  Re-running therefore reproduces the
    permutation / resampling statistics     exactly.  No seed was added or
    changed during recovery.

Notes
    Rebuilt by the statistics-layer recovery (docs/RECOVERY_PROTOCOL.md).  The
    computation is the recovered cell chain unchanged: same tests, same
    covariates, same corrections, same seeds.  Only the header, the explicit
    output path and the suppression of the original session's side outputs were
    added.  Lines marked "[recovery: side output suppressed]" wrote files other
    than this script's one deliverable into the author's working tree; they are
    commented out so that running this script cannot modify anything outside
    OUT_DIR.  The verbatim terminal cell is archived at
    recovered/fig5/fig5i_np12_loo_accuracy__cell_76935dae.py
"""
import os
import sys

OUT_DIR = os.environ.get(
    "RECOVERY_OUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scratch"))
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- cell d33b3ce6 (cell_index 96)
import pandas as pd, os
base='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/restoration_index_clinical_weights/'
pd.set_option('display.width',250,'display.max_columns',60)
for f in ['np85_12edge_direct_crossvalidation.csv','np85_12edge_model_comparison_tests.csv','np85_simulated_NP_direct_prediction.csv','np85_index_vs_simulated_baseline_adjustment.csv']:
    print('#####',f); print(pd.read_csv(base+f).to_string(max_colwidth=46),'\n')

# ---------------------------------------------------------------- cell 297defc1 (cell_index 97)
import os, sys, re, zipfile, shutil, datetime, importlib
sys.path.append(os.getcwd())
from xml.etree import ElementTree as ET
import docxedit; importlib.reload(docxedit)
from docxedit import TrackedDoc, accept_all, q
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
TR='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/250926NatMed_Manuscript_Claude_tracked-gunter.docx'
SI='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/240926Supplementary Information-liyi.docx'
dest='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
out_ms='250926NatMed_Manuscript_round2_tracked.docx'; out_si='240926Supplementary_Information_round2_tracked.docx'
def dump(path,out):
    z=zipfile.ZipFile(path); root=ET.fromstring(z.read('word/document.xml'))
    lines=[]
    for i,pn in enumerate(root.find(W+'body').iter(W+'p')):
        txt=''.join((t.text or '') for t in pn.iter(W+'t'))
        dele=''.join((t.text or '') for t in pn.iter(W+'delText'))
        lines.append(f"[{i}]() {txt}"+(f"   <<DEL:{dele}>>" if dele else ""))
    open(out,'w').write('\n'.join(lines)); return len(lines)
b=TrackedDoc(TR); accept_all(b.root); b.save('ms_base_accepted.docx'); dump('ms_base_accepted.docx','ms_base_paras.txt')
L=open('ms_base_paras.txt').read().split('\n')
for pat in [r'restoration', r'Stage 5', r'perturbation-derived index']:
    print('#####',pat)
    for i,l in enumerate(L):
        if re.search(pat,l): print(f'  [{i}]', l[:160])

# ---------------------------------------------------------------- cell 734cfe01 (cell_index 119)
bp='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/'
T=pd.read_csv(bp+'np85_full_table_corrected_groups.csv')
print(T.shape); print(T.columns.tolist())
print(pd.read_csv(bp+'np85_full_table_datadictionary.csv').to_string(max_colwidth=70)[:2500])

# ---------------------------------------------------------------- cell 5e8b6c30 (cell_index 120)
Wt=pd.read_csv(base+'clinicalW_mapping_edge_weights.csv'); print(Wt.to_string(max_colwidth=30))
print(T[['beha_change_raw','restoration_index__ampa','restoration_index_ampa_PUBLISHED']].describe().round(3).to_string())

# ---------------------------------------------------------------- cell 876400dd (cell_index 121)
import numpy as np, statsmodels.api as sm
w=Wt.sort_values('edge')['weight'].values
sim=T[[f'simbase_edge{i}' for i in range(1,13)]].values
amp=T[[f'mod_ampa_edge{i}' for i in range(1,13)]].values
gab=T[[f'mod_gaba_edge{i}' for i in range(1,13)]].values
y=T['beha_change_raw'].values
f_sim, f_amp, f_gab = sim@w, amp@w, gab@w
RI_a, RI_g = -( (amp-sim)@w ), -( (gab-sim)@w )
print('RI check vs table:', np.corrcoef(RI_a, T['restoration_index__ampa'])[0,1].round(4), np.corrcoef(RI_g, T['restoration_index__gaba'])[0,1].round(4))
def dR2(y, Xcov, xadd):
    X0=sm.add_constant(np.column_stack(Xcov)) if len(Xcov) else np.ones((len(y),1))
    X1=np.column_stack([X0, xadd])
    m0,m1=sm.OLS(y,X0).fit(), sm.OLS(y,X1).fit()
    d=m1.rsquared-m0.rsquared; F=(d/1)/((1-m1.rsquared)/m1.df_resid)
    from scipy import stats
    return d, F, 1-stats.f.cdf(F,1,m1.df_resid), int(m1.df_resid)
emp_sum=T['emp_np_sum'].values; sym=T['beha19_sum'].values
rows=[]
for nm,RI in [('AMPA',RI_a),('GABA-A',RI_g)]:
    fx = f_amp if nm=='AMPA' else f_gab
    rows.append((nm,'zero-order',*dR2(y,[],RI)))
    rows.append((nm,'12-edge sum baseline',*dR2(y,[sim.sum(1)],RI)))
    rows.append((nm,'weighted read-out f(NP_sim)',*dR2(y,[f_sim],RI)))
    rows.append((nm,'all 12 simbase edges',*dR2(y,[sim],RI)))
    rows.append((nm,'f(NP_sim)+symptoms+empNP',*dR2(y,[f_sim,sym,emp_sum],RI)))
res=pd.DataFrame(rows,columns=['index','covariates','dR2','F','P','df2'])
print(res.round(4).to_string())
print('\ndispersion: sd f_sim %.2f | AMPA post %.2f (%.0f%% ↓) r_pre_post %.3f | shared var with baseline %.3f'%(
  f_sim.std(ddof=1), f_amp.std(ddof=1), 100*(1-f_amp.std(ddof=1)/f_sim.std(ddof=1)), np.corrcoef(f_sim,f_amp)[0,1], np.corrcoef(RI_a,f_sim)[0,1]**2))
print('GABA post sd %.2f (ratio %.2f) shared var %.3f'%(f_gab.std(ddof=1), f_gab.std(ddof=1)/f_sim.std(ddof=1), np.corrcoef(RI_g,f_sim)[0,1]**2))
from scipy import stats as st
print('AMPA post-perturbation state vs outcome r=%.3f P=%.3f'%st.pearsonr(f_amp,y))

# ---------------------------------------------------------------- cell cc69d8f7 (cell_index 137)
def loo_pred(X, y):
    X=np.asarray(X,float); n=len(y); pred=np.empty(n)
    X1=np.column_stack([np.ones(n),X])
    for i in range(n):
        m=np.ones(n,bool); m[i]=False
        beta,*_=np.linalg.lstsq(X1[m],y[m],rcond=None)
        pred[i]=X1[i]@beta
    return pred
Xsim=T[[f'simbase_edge{i}' for i in range(1,13)]].values
Xemp=T[[f'emp_edge{i}' for i in range(1,13)]].values
sym=T[['beha19_sum']].values
specs={'age-19 symptoms only':sym,'12 simulated NP edges':Xsim,'12 empirical NP edges':Xemp,
       'symptoms + 12 simulated edges':np.column_stack([sym,Xsim]),'symptoms + 12 empirical edges':np.column_stack([sym,Xemp])}
rows=[]
preds={}
for k,X in specs.items():
    p=loo_pred(X,y); preds[k]=p
    r,pv=st.pearsonr(p,y); r2=1-((y-p)**2).sum()/((y-y.mean())**2).sum()
    rows.append((k,X.shape[1],round(r,4),round(pv,5),round(r2,4)))
print(pd.DataFrame(rows,columns=['model','k','r_LOO','P','R2_LOO']).to_string(index=False))

# ---------------------------------------------------------------- cell e1375717 (cell_index 138)
def loo_fast(X,y):
    X1=np.column_stack([np.ones(len(y)),np.asarray(X,float)])
    H=X1@np.linalg.pinv(X1); h=np.diag(H); e=y-H@y
    return y-e/(1-h), H, h
p_fast,Hs,hs=loo_fast(Xsim,y)
print('hat vs loop match:', np.allclose(p_fast,preds['12 simulated NP edges']))
rng=np.random.default_rng(0); null=np.empty(2000)
for b in range(2000):
    yp=rng.permutation(y); e=yp-Hs@yp; pr=yp-e/(1-hs); null[b]=np.corrcoef(pr,yp)[0,1]
obs=st.pearsonr(p_fast,y)[0]
print('obs r %.4f | null p95 %.3f | perm P %.4f'%(obs, np.percentile(null,95), (null>=obs).mean()))

# ---------------------------------------------------------------- cell 76935dae (cell_index 144)
FIGDIR='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures'; HERE5=os.path.join(FIGDIR,'fig.5'); D5=os.path.join(HERE5,'fig5_data')
np12=pd.DataFrame({'observed':y,'predicted_sim':preds['12 simulated NP edges'],'predicted_emp':preds['12 empirical NP edges']})
pass  # [recovery: side output suppressed] np12.to_csv(os.path.join(D5,'fig5h_np12_loo_n85.csv'),index=False)
acc=pd.DataFrame(rows,columns=['model','k','r_LOO','P','R2_LOO'])
acc['short']=['symptoms','simulated\nedges','empirical\nedges','symptoms +\nsimulated','symptoms +\nempirical']
acc['simulated']=[0,1,0,1,0]; acc['empirical']=[0,0,1,0,1]
acc['null_p95']=0.19; acc['perm_P']=[np.nan,0.0095,np.nan,np.nan,np.nan]; acc['n']=85; acc['n_perm']=2000
acc.to_csv(os.path.join(OUT_DIR, 'fig5i_np12_loo_accuracy.csv'), index=False)
print(acc.to_string(index=False))
