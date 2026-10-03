#!/usr/bin/env python3
"""fig5h_paragraph_scatters_n85.csv

Computes
    Subject-level variables (n = 85) for the four relationships stated in the
    longitudinal paragraph: the AMPA restoration index, the follow-up symptom
    change, the summed baseline empirical NP connectivity, the baseline
    symptom sum, and the index and outcome residualised on baseline empirical
    NP connectivity.

Inputs
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/684a22a0-d6db-4aeb-b5ad-b30777bef882/vd1e0509f_state_similarity_per_subject.csv
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/d5929019-b98a-491a-8698-e51c332ca715/v15ac42f6_six_model_mse_per_subject.csv
    - /Users/yunman/Desktop/submission/
    - /Users/yunman/Desktop/submission/figures_v2/fig4/pharmacological_exper
    - /Users/yunman/Desktop/submission/figures_v2/fig4/predict_fu3_beha_changes/virtual_modu_predict_fu3_beha_changes.mat
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/New_pharma_dataset
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data/fig5_healthy_n27_with_pattern.csv
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data/fig5_mdd_hc_n36.csv
    - (path built in the chain) SUB+"figures_v2/fig2/NP_covari_info_STRATIFY.xlsx"
    - (path built in the chain) SUB+"figures_v2/fig1/pos_neg_np_stratify_resi_without_ed.csv"
    - (path built in the chain) SUB+"Figures/table/stratify_np_fcs12.mat"
    - (path built in the chain) SUB+"revision/text/figures/six_model_run_to_run_sd.csv"
    - (path built in the chain) SUB+"revision/model_scale_consistent/per_subject_modulation_direction_12subs.csv"
    - (path built in the chain) SUB+"revision/model_scale_consistent/manuscript_numbers_newflow/NP_12edges_all_subjects_scales_conditions_newflow.csv"
    - (path built in the chain) SUB+"figures_v2/fig3/manipulated_fcs_4subs/plot_mani_AMPA.csv"
    - (path built in the chain) SUB+"figures_v2/fig3/manipulated_fcs_4subs/plot_mani_gaba.xlsx"
    - (path built in the chain) f'{F}/fig4_sdq_items_n287.csv'
    - (path built in the chain) f'{F}/fig4_dawba_domains_n284.csv'
    - (path built in the chain) f'{F}/fig4_subject_level_n288.csv'
    - (path built in the chain) f'{P2}/ketamine_master_data_for_plots.csv'
    - (path built in the chain) f'{P2}/np_vs_symptomPC1_change_resid_MDD.csv'
    - (path built in the chain) f'{B}/{f}'

Output
    04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_paragraph_scatters_n85.csv; 04_figures/fig.5/fig5_data/fig5h_paragraph_scatters_n85.csv

Statistical tests
    in this script's own computation:
      - Pearson correlation
      - Fisher z 95% confidence interval
      - partial correlation on residualised variables
    in the recovered chain that prepares its inputs:
      - two-sample t test
      - Mann-Whitney U test
      - Spearman correlation
      - ordinary least squares GLM with covariates
      - nested-model F test for the R2 increment
      - outcome-permutation null
      - leave-one-out cross-validation

Local runnability
    partial (local_runnable = partial).  Verification: not_run.
    re-run stops on a name the recovery could not carry over ('nested'): it
    was bound by an interactive step that depends on the platform artifact
    store or on a workspace-only helper, which the recovery does not fabricate
Recovered from
    execution-log cell fbc8f06f-ac73-47ae-8f2b-683d1ce7b349
    frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, cell_index 498, 2026-09-21 21:19 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    b13bdbf2, 94656bfa, b47d163c, 9639cab9, 3318eca3, fc72540d, b032c8db,
    d0efb174, d04f2aa4, ed9bb9dd, bd0dad4d, fbc8f06f

Random seed
    fixed in the original run: seed = 0, seed = 2.  Re-running therefore
    reproduces the permutation / resampling statistics     exactly.  No seed
    was added or changed during recovery.

Notes
    Rebuilt by the statistics-layer recovery (docs/RECOVERY_PROTOCOL.md).  The
    computation is the recovered cell chain unchanged: same tests, same
    covariates, same corrections, same seeds.  Only the header, the explicit
    output path and the suppression of the original session's side outputs were
    added.  Lines marked "[recovery: side output suppressed]" wrote files other
    than this script's one deliverable into the author's working tree; they are
    commented out so that running this script cannot modify anything outside
    OUT_DIR.  The verbatim terminal cell is archived at
    recovered/fig5/fig5h_paragraph_scatters_n85__cell_fbc8f06f.py
"""
import os
import sys

OUT_DIR = os.environ.get(
    "RECOVERY_OUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scratch"))
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- cell aaadc71b (cell_index 59)
import pandas as pd, numpy as np, scipy.io as sio, os, json
SUB="/Users/yunman/Desktop/submission/"
OUT=SUB+"revision/text/figures/fig.2/"; None  # [recovery: side output suppressed]

cov=pd.read_excel(SUB+"figures_v2/fig2/NP_covari_info_STRATIFY.xlsx")
print("covariates:", cov.shape, cov.columns.tolist()[:12])
st=pd.read_csv(SUB+"figures_v2/fig1/pos_neg_np_stratify_resi_without_ed.csv")
st.columns=[c.strip().lstrip('\ufeff') for c in st.columns]
st=st[st.Diseased.isin(['HC','MDD','AUD'])].copy()
st['Group']=np.where(st.Diseased=='HC','HC','Patient')
print("\nFig2 cohort:", st.Group.value_counts().to_dict(), "| by dx:", st.Diseased.value_counts().to_dict())
m=sio.loadmat(SUB+"Figures/table/stratify_np_fcs12.mat")
edges=pd.DataFrame(m['NP_fcs_no_cere'], columns=[f'edge{i}' for i in range(1,13)])
edges.insert(0,'ID',m['id_sub'][:,0].astype(np.int64))
print("edge table:", edges.shape, "| joinable to cohort:", edges.ID.isin(st.ID).sum())

# ---------------------------------------------------------------- cell fc428740 (cell_index 122)
F3=SUB+"revision/text/figures/fig.3/"; None; D3=F3+"fig3_data/"  # [recovery: side output suppressed]
mse_ps=pd.read_csv('/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/d5929019-b98a-491a-8698-e51c332ca715/v15ac42f6_six_model_mse_per_subject.csv')
sd6=pd.read_csv(SUB+"revision/text/figures/six_model_run_to_run_sd.csv")
mod=pd.read_csv(SUB+"revision/model_scale_consistent/per_subject_modulation_direction_12subs.csv")
nf=pd.read_csv(SUB+"revision/model_scale_consistent/manuscript_numbers_newflow/NP_12edges_all_subjects_scales_conditions_newflow.csv")
print("3a mse_per_subject", mse_ps.shape, mse_ps.columns.tolist())
print("\n3c sd6\n", sd6.to_string(index=False))
print("\n3f mod", mod.shape, mod.columns.tolist(), "| groups:", mod.group.value_counts().to_dict())
print("\n3b newflow", nf.shape, "| scales:", nf.scale.unique().tolist(), "| conditions:", nf.condition.unique().tolist())
print(nf.groupby(['scale','condition']).subID.nunique().unstack(fill_value=0).to_string())

# ---------------------------------------------------------------- cell a7adaae2 (cell_index 143)
amp=pd.read_csv(SUB+"figures_v2/fig3/manipulated_fcs_4subs/plot_mani_AMPA.csv")
gab=pd.read_excel(SUB+"figures_v2/fig3/manipulated_fcs_4subs/plot_mani_gaba.xlsx")
amp.columns=['subject']+[str(c) for c in amp.columns[1:]]
gab.columns=['subject']+[f"{float(c):.4f}" if str(c).replace('.','').isdigit() else str(c) for c in gab.columns[1:]]
amp=amp[amp.subject!='HC02']; gab=gab[gab.subject!='HC02']
pass  # [recovery: side output suppressed] amp.to_csv(D3+"fig3d_ampa_sweep.csv", index=False, float_format='%.12g')
pass  # [recovery: side output suppressed] gab.to_csv(D3+"fig3e_gaba_sweep.csv", index=False, float_format='%.12g')
print("3d", amp.shape, amp.subject.tolist(), "\n cols:", amp.columns.tolist())
print("3e", gab.shape, gab.subject.tolist(), "\n cols:", gab.columns.tolist())

# ---------------------------------------------------------------- cell 83f6587b (cell_index 403)
import pandas as pd, numpy as np
from sklearn.cross_decomposition import PLSRegression, CCA
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as smf
F='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data'
sdq=pd.read_csv(f'{F}/fig4_sdq_items_n287.csv')
daw=pd.read_csv(f'{F}/fig4_dawba_domains_n284.csv')
sub=pd.read_csv(f'{F}/fig4_subject_level_n288.csv')
SDQI=[c for c in sdq.columns if c not in ('ID','pattern','Group')]
DAWI=['adhd','cd','eat','dep','gad','sp']
M=sdq.merge(daw[['ID']+DAWI],on='ID').merge(
    sub[['ID','sex','site','headmotion','d_ampa','d_gaba','simulated','empirical']],on='ID')
M['y']=(M.pattern=='both up').astype(int)
print('n =',len(M), 'both up',int(M.y.sum()),'any down',int((1-M.y).sum()))
# covariate-residualised behaviour block
B=M[SDQI+DAWI].astype(float).copy()
Bres=B.copy()
for c in B.columns:
    Bres[c]=smf.ols(f'v ~ sex + site + headmotion',data=M.assign(v=B[c])).fit().resid
print('blocks:', B.shape, '| SDQ', len(SDQI), '| DAWBA', len(DAWI))

# ---------------------------------------------------------------- cell b971d09f (cell_index 404)
rng=np.random.default_rng(0)
def cv_auc(X,y,ncomp=2,reps=5,seed=0):
    cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=reps,random_state=seed)
    pred=np.zeros(len(y)); cnt=np.zeros(len(y))
    for tr,te in cv.split(X,y):
        sc=StandardScaler().fit(X[tr])
        pls=PLSRegression(n_components=ncomp).fit(sc.transform(X[tr]),y[tr]-y[tr].mean())
        pred[te]+=pls.predict(sc.transform(X[te])).ravel(); cnt[te]+=1
    return roc_auc_score(y,pred/cnt)
def perm_p(X,y,ncomp=2,nperm=500,reps=2,seed=1):
    obs=cv_auc(X,y,ncomp,reps=reps,seed=seed)
    r=np.random.default_rng(seed); null=np.empty(nperm)
    for i in range(nperm):
        null[i]=cv_auc(X,r.permutation(y),ncomp,reps=reps,seed=seed)
    return obs,float((np.sum(null>=obs)+1)/(nperm+1)),null
res={}
for nm,X_ in [('SDQ raw',B[SDQI].values),('SDQ+DAWBA raw',B.values),
              ('SDQ+DAWBA covariate-adj',Bres.values)]:
    for k in (1,2,3):
        res[(nm,k)]=cv_auc(X_,M.y.values,ncomp=k,reps=5,seed=0)
    print(nm, {k:round(res[(nm,k)],3) for k in (1,2,3)})

# ---------------------------------------------------------------- cell 5aa4ffeb (cell_index 406)
from scipy import stats
# ---- CCA: behaviour block vs brain-response block (no dichotomising) -------
Y=M[['simulated','d_ampa','d_gaba']].values
def cca_r1(X,Y,seed=0):
    sx,sy=StandardScaler().fit_transform(X),StandardScaler().fit_transform(Y)
    c=CCA(n_components=1,max_iter=1000).fit(sx,sy)
    u,v=c.transform(sx,sy); return float(np.corrcoef(u[:,0],v[:,0])[0,1])
r1=cca_r1(B.values,Y); rp=np.random.default_rng(2)
null=np.array([cca_r1(B.values,Y[rp.permutation(len(Y))]) for _ in range(500)])
print(f'CCA r1 (32 behaviour vars vs baseline NP, dAMPA, dGABA) = {r1:.3f}, '
      f'permutation P = {(np.sum(null>=r1)+1)/501:.3f} (null mean {null.mean():.3f}, 95th {np.percentile(null,95):.3f})')
# ---- sex / site association with the response pattern ----------------------
print()
for v in ['sex','site']:
    ct=pd.crosstab(M[v],M.pattern)
    chi2,p,dof,_=stats.chi2_contingency(ct)
    print(f'{v}: chi2 = {chi2:.2f}, df = {dof}, P = {p:.3g}')
    print((ct.assign(pct_both_up=(100*ct['both up']/ct.sum(1)).round(1))).to_string())
lg=smf.logit('y ~ C(sex) + C(site) + headmotion + C(Group)',data=M).fit(disp=0)
print('\nlogistic: pattern ~ sex + site + head motion + diagnostic group')
print(lg.summary2().tables[1][['Coef.','Std.Err.','z','P>|z|']].round(3).to_string())

# ---------------------------------------------------------------- cell 6c722a4a (cell_index 424)
import pandas as pd
P1='/Users/yunman/Desktop/submission/figures_v2/fig4/pharmacological_exper'
P2='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/New_pharma_dataset'
for f in [f'{P1}/summed_MID_FCs_3conditions.csv', f'{P1}/NP_fcs_only_win_mean.csv',
          f'{P2}/summed_FCs_2conditions_for_plot.csv', f'{P2}/compare_hc_mdd_p2.csv',
          f'{P2}/baseline_np_vs_symptom_change_values.csv']:
    try:
        d=pd.read_csv(f, encoding='utf-8-sig'); print(f.split('/')[-1], d.shape, d.columns.tolist()[:12])
        print(d.head(2).to_string(index=False)[:300]); print()
    except Exception as e: print(f.split('/')[-1],'ERR',e)

# ---------------------------------------------------------------- cell 4a491abc (cell_index 429)
sim=pd.read_csv('/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/684a22a0-d6db-4aeb-b5ad-b30777bef882/vd1e0509f_state_similarity_per_subject.csv')
print('state_similarity', sim.shape, sim.columns.tolist())
print(sim.head(3).to_string(index=False))
print('\ngroups:', sim.group.value_counts().to_dict())
ms=pd.read_csv(f'{P2}/ketamine_master_data_for_plots.csv')
print('\nmaster', ms.shape, ms.columns.tolist()[:18], '| groups', ms.group.value_counts().to_dict() if 'group' in ms else '')
r2=pd.read_csv(f'{P2}/np_vs_symptomPC1_change_resid_MDD.csv')
print('\n5f candidate', r2.shape, r2.columns.tolist())

# ---------------------------------------------------------------- cell b13bdbf2 (cell_index 445)
import numpy as np, itertools, matplotlib
def hex2rgb(h): return np.array(matplotlib.colors.to_rgb(h))
def srgb2lin(c): return np.where(c<=.04045, c/12.92, ((c+.055)/1.055)**2.4)
M = np.array([[.4124,.3576,.1805],[.2126,.7152,.0722],[.0193,.1192,.9505]])
WP = np.array([.95047,1.0,1.08883])
def lab(h):
    x = M @ srgb2lin(hex2rgb(h)) / WP
    f = np.where(x>0.008856, np.cbrt(x), 7.787*x+16/116)
    return np.array([116*f[1]-16, 500*(f[0]-f[1]), 200*(f[1]-f[2])])
def de(a,b): return float(np.linalg.norm(lab(a)-lab(b)))
# Brettel-style deuteranopia sim (Machado 2009 matrix, severity 1.0)
DEU = np.array([[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]])
PRO = np.array([[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]])
def sim(h, Mx):
    v = np.clip(Mx @ hex2rgb(h), 0, 1)
    return matplotlib.colors.to_hex(v)

PAL = {'grey_reference':'#7F7F7F','high_symptom':'#E69F00','patient_mdd':'#D55E00',
       'ampa_ketamine':'#E1D09A','gaba_midazolam':'#96B9AD','increased':'#D9A5B3',
       'decreased':'#8DA0B4','neg_profile':'#6BAED6','np12':'#0072B2',
       'pos_profile':'#C878A0','non_np':'#BFBFBF','model_regional':'#8E7CC3',
       'model_voxel':'#4C3F8C'}
rows=[]
for a,b in itertools.combinations(PAL,2):
    rows.append((a,b, de(PAL[a],PAL[b]),
                 de(sim(PAL[a],DEU),sim(PAL[b],DEU)),
                 de(sim(PAL[a],PRO),sim(PAL[b],PRO))))
rows.sort(key=lambda r: min(r[2],r[3],r[4]))
print(f"{'pair':44s} {'dE':>6s} {'dE_deut':>8s} {'dE_prot':>8s}")
for a,b,d,dd,dp in rows[:14]:
    print(f"{a+' / '+b:44s} {d:6.1f} {dd:8.1f} {dp:8.1f}")
print()
# pairs that actually co-occur inside one panel
co = [('grey_reference','ampa_ketamine'),('grey_reference','gaba_midazolam'),
      ('ampa_ketamine','gaba_midazolam'),('increased','decreased'),
      ('grey_reference','patient_mdd'),('grey_reference','high_symptom'),
      ('high_symptom','patient_mdd'),('increased','pos_profile')]
print("co-occurring pairs:")
for a,b in co:
    print(f"  {a+' / '+b:36s} dE={de(PAL[a],PAL[b]):5.1f}  deut={de(sim(PAL[a],DEU),sim(PAL[b],DEU)):5.1f}  prot={de(sim(PAL[a],PRO),sim(PAL[b],PRO)):5.1f}")
print()
print("luminance (L*) of each:", {k: round(lab(v)[0],1) for k,v in PAL.items()})

# ---------------------------------------------------------------- cell 94656bfa (cell_index 446)
GREY = lambda h: float(lab(h)[0])
def audit(pair, ignore=('increased','decreased')):
    """distance of a candidate up/down pair from each other and from the rest of the palette"""
    a, b = pair
    out = {'dE': de(a,b), 'deut': de(sim(a,DEU),sim(b,DEU)), 'prot': de(sim(a,PRO),sim(b,PRO)),
           'dL': abs(GREY(a)-GREY(b))}
    worst = []
    for k, v in PAL.items():
        if k in ignore: continue
        for c in (a, b):
            worst.append((min(de(c,v), de(sim(c,DEU),sim(v,DEU)), de(sim(c,PRO),sim(v,PRO))), k, c))
    worst.sort()
    out['nearest_other'] = worst[:3]
    return out

CAND = {
 'current           ': ('#D9A5B3', '#8DA0B4'),
 'Okabe purple/green': ('#CC79A7', '#009E73'),
 'plum two-tone     ': ('#8C4A6B', '#E8C4D2'),
 'plum/steel deeper ': ('#C1607F', '#4F7391'),
 'magenta/teal dark ': ('#A4478A', '#2C7A6B'),
 'rose/slate        ': ('#C2185B', '#5C6BC0'),
 'brown/indigo      ': ('#8B5E3C', '#3F51A3'),
}
for name, p in CAND.items():
    r = audit(p)
    near = ', '.join(f'{k}:{d:.0f}' for d,k,_ in r['nearest_other'])
    print(f"{name}  {p[0]} {p[1]}  dE={r['dE']:5.1f} deut={r['deut']:5.1f} prot={r['prot']:5.1f} dL*={r['dL']:5.1f} | nearest other: {near}")

# ---------------------------------------------------------------- cell b47d163c (cell_index 447)
CO = {'grey_reference':'#7F7F7F','high_symptom':'#E69F00','patient_mdd':'#D55E00',
      'ampa_ketamine':'#E1D09A','gaba_midazolam':'#96B9AD'}   # colours sharing Fig.4 / Fig.5
def score(a,b):
    sep = min(de(a,b), de(sim(a,DEU),sim(b,DEU)), de(sim(a,PRO),sim(b,PRO)))
    worst = min((min(de(c,v), de(sim(c,DEU),sim(v,DEU)), de(sim(c,PRO),sim(v,PRO))), k)
                for k,v in CO.items() for c in (a,b))
    return sep, abs(GREY(a)-GREY(b)), worst
for nm,(a,b) in {
  'plum  dark/pale  ': ('#8C4A6B','#E8C4D2'),
  'plum  dark/chroma': ('#8C4A6B','#DEA9BF'),
  'plum  deeper     ': ('#7A3B5E','#D99BB8'),
  'wine  dark/light ': ('#6E2F4A','#D48FB0'),
  'plum+mid         ': ('#9E5478','#D9A5B3'),
  'indigo dark/light': ('#2F4B7C','#A9C4E8'),
}.items():
    s, dl, (w, wk) = score(a,b)
    print(f"{nm} {a} {b}  min-separation={s:5.1f}  dL*={dl:5.1f}  closest Fig4/5 colour: {wk} ({w:.1f})")
print()
pass  # [recovery: side output suppressed] print('non_np used in fig4/fig5?', __import__('subprocess').run(
# [recovery: side output suppressed]     ["bash","-lc","grep -c \"non_np\" /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4.py /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5.py"],
# [recovery: side output suppressed]     capture_output=True, text=True).stdout.strip())

# ---------------------------------------------------------------- cell 9639cab9 (cell_index 449)
import pandas as pd, numpy as np, scipy.io as sio, os
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data'
for f in sorted(os.listdir(B)):
    d=pd.read_csv(f'{B}/{f}')
    print('==',f, d.shape); print(list(d.columns))

# ---------------------------------------------------------------- cell 3318eca3 (cell_index 450)
p='/Users/yunman/Desktop/submission/figures_v2/fig4/predict_fu3_beha_changes/virtual_modu_predict_fu3_beha_changes.mat'
m=sio.loadmat(p, squeeze_me=True, struct_as_record=False)
for k,v in m.items():
    if k.startswith('__'): continue
    try: print(k, np.shape(v), (str(v)[:120] if np.size(v)<12 else ''))
    except Exception as e: print(k,'?',e)

# ---------------------------------------------------------------- cell b032c8db (cell_index 454)
# [recovery] this cell raised in the original session at its line 34; only the
# statements that had already executed are carried over
from sklearn.model_selection import KFold
pass  # [recovery: unresolvable interactive debris removed] def cv_r2(Xm, yv, repeats=10):
# [recovery: unresolvable interactive debris removed]     out = []
# [recovery: unresolvable interactive debris removed]     for rep in range(repeats):
# [recovery: unresolvable interactive debris removed]         pr = np.empty(len(yv))
# [recovery: unresolvable interactive debris removed]         for tr, te in KFold(10, shuffle=True, random_state=rep).split(Xm):
# [recovery: unresolvable interactive debris removed]             lr = LinearRegression().fit(Xm[tr], yv[tr]); pr[te] = lr.predict(Xm[te])
# [recovery: unresolvable interactive debris removed]         out.append(1 - ((yv - pr) ** 2).sum() / ((yv - yv.mean()) ** 2).sum())
# [recovery: unresolvable interactive debris removed]     return float(np.mean(out)), float(np.std(out))

pass  # [recovery: unresolvable interactive debris removed] def nested(idx_col, name):
# [recovery: unresolvable interactive debris removed]     Xfull = np.column_stack([idx_col, X1])
# [recovery: unresolvable interactive debris removed]     R2r, _ = r2(X1, y); R2f, bf = r2(Xfull, y)
# [recovery: unresolvable interactive debris removed]     n, p1, p2 = len(y), X1.shape[1], Xfull.shape[1]
# [recovery: unresolvable interactive debris removed]     F = ((R2f - R2r) / (p2 - p1)) / ((1 - R2f) / (n - p2 - 1))
# [recovery: unresolvable interactive debris removed]     p = 1 - stats.f.cdf(F, p2 - p1, n - p2 - 1)
# [recovery: unresolvable interactive debris removed]     rng = np.random.default_rng(0); null = np.empty(5000)
# [recovery: unresolvable interactive debris removed]     for i in range(5000):
# [recovery: unresolvable interactive debris removed]         yp = rng.permutation(y)
# [recovery: unresolvable interactive debris removed]         null[i] = r2(Xfull, yp)[0] - r2(X1, yp)[0]
# [recovery: unresolvable interactive debris removed]     q2r, s_r = cv_r2(X1, y); q2f, s_f = cv_r2(Xfull, y)
# [recovery: unresolvable interactive debris removed]     t = np.sqrt(F)
# [recovery: unresolvable interactive debris removed]     return dict(predictor=name, R2_reduced=R2r, R2_full=R2f, delta_R2=R2f - R2r,
# [recovery: unresolvable interactive debris removed]                 F_change=F, df1=p2 - p1, df2=n - p2 - 1, p_change=p,
# [recovery: unresolvable interactive debris removed]                 beta=bf[1], partial_r=np.sign(bf[1]) * t / np.sqrt(t**2 + n - p2 - 1),
# [recovery: unresolvable interactive debris removed]                 p_perm_deltaR2=float((null >= R2f - R2r).mean()),
# [recovery: unresolvable interactive debris removed]                 perm_null_p95=float(np.percentile(null, 95)),
# [recovery: unresolvable interactive debris removed]                 cvR2_reduced=q2r, cvR2_full=q2f, cvR2_full_sd=s_f), null

pass  # [recovery: unresolvable interactive debris removed] ampa_row, ampa_null = nested(Xf[:, 0], 'AMPA restoration index')
gaba_row, gaba_null = nested(gab, 'GABA-A restoration index')
T = pd.DataFrame([ampa_row, gaba_row])
print(T.round(4).to_string(index=False))

# ---------------------------------------------------------------- cell d0efb174 (cell_index 455)
def resid(v, Z):
    Zd = np.column_stack([np.ones(len(v)), Z]); b, *_ = np.linalg.lstsq(Zd, v, rcond=None)
    return v - Zd @ b
pass  # [recovery: unresolvable interactive debris removed] xr, yr = resid(Xf[:, 0], X1), resid(y, X1)
rp, pp = stats.pearsonr(xr, yr)
print('partial r (AMPA) =', round(float(rp),4), 'P =', f'{pp:.4g}')
pass  # [recovery: unresolvable interactive debris removed] print('AMPA vs GABA index r =', round(float(stats.pearsonr(Xf[:,0], gab)[0]),3))
import os; os.makedirs('/tmp/cvd', exist_ok=True)
None; None  # [recovery: side output suppressed]  # [recovery: side output suppressed]
pass  # [recovery: side output suppressed] pd.DataFrame(dict(ampa_index_resid=xr, fu3_change_resid=yr)).to_csv('/tmp/cvd/h1.csv', index=False)
pass  # [recovery: side output suppressed] T.to_csv('/tmp/cvd/h_models.csv', index=False)
# final colour-pair pick: need both tones dark enough for 11-pt points on white
for nm, (a,b) in {'plum dark/pale':('#8C4A6B','#E8C4D2'), 'plum dark/mid':('#7A3B5E','#C2849B'),
                  'plum dark/mid2':('#8C4A6B','#CE9BAF'), 'plum vs dusk':('#7A3B5E','#B07A93')}.items():
    s, dl, (w, wk) = score(a,b)
    print(f'{nm:16s} {a} {b}  sep(min over vision types)={s:5.1f}  dL*={dl:5.1f}  L*=({GREY(a):.0f},{GREY(b):.0f})  closest Fig4/5: {wk} {w:.0f}')

# ---------------------------------------------------------------- cell d04f2aa4 (cell_index 459)
D5='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data'
pass  # [recovery: side output suppressed] pd.DataFrame(dict(ampa_index_resid=xr, fu3_change_resid=yr)).to_csv(f'{D5}/fig5h_added_variable_n85.csv', index=False)
pass  # [recovery: side output suppressed] T.to_csv(f'{D5}/fig5h_nested_models.csv', index=False)
pass  # [recovery: side output suppressed] pd.DataFrame(dict(deltaR2_null_ampa=ampa_null, deltaR2_null_gaba=gaba_null)).to_csv(f'{D5}/fig5h_deltaR2_null.csv', index=False)
print(T[['predictor','delta_R2','F_change','p_change','p_perm_deltaR2','partial_r','cvR2_reduced','cvR2_full']].round(4).to_string(index=False))

# ---------------------------------------------------------------- cell ed9bb9dd (cell_index 479)
Hp=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data/fig5_healthy_n27_with_pattern.csv')
import statsmodels.api as sm
# 1. how much of the b_pattern contrast is forced by the definition
ad = Hp[Hp.pattern=='any down']
print('any down (19): d_ket>0 in %d, <=0 in %d | d_mid>0 in %d, <=0 in %d'
      % ((ad.d_ket>0).sum(), (ad.d_ket<=0).sum(), (ad.d_mid>0).sum(), (ad.d_mid<=0).sum()))
print('both up (8): d_ket>0 in %d/8, d_mid>0 in %d/8  (forced by definition)'
      % ((Hp.pattern=='both up').sum() and (Hp[Hp.pattern=='both up'].d_ket>0).sum(),
         (Hp[Hp.pattern=='both up'].d_mid>0).sum()))

# 2. cross-drug consistency of the individual response (non-circular version)
r_raw, p_raw = stats.pearsonr(Hp.d_ket, Hp.d_mid)
def partial(x, y, z):
    rx = x - sm.add_constant(z) @ np.linalg.lstsq(sm.add_constant(z), x, rcond=None)[0]
    ry = y - sm.add_constant(z) @ np.linalg.lstsq(sm.add_constant(z), y, rcond=None)[0]
    r = np.corrcoef(rx, ry)[0,1]; n = len(x); k = np.atleast_2d(z).shape[1] if z.ndim>1 else 1
    t = r*np.sqrt((n-2-k)/(1-r**2)); return r, float(2*(1-stats.t.cdf(abs(t), n-2-k)))
r_pc, p_pc = partial(Hp.Ketamine.values, Hp.Midazolam.values, Hp.Placebo.values.reshape(-1,1))
print('\nDelta_ket vs Delta_mid: raw r = %.3f, P = %.4g' % (r_raw, p_raw))
print('Ketamine vs Midazolam partial on Placebo: r = %.3f, P = %.4g' % (r_pc, p_pc))
rs, ps = stats.spearmanr(Hp.Ketamine, Hp.Midazolam); print('Ketamine vs Midazolam raw Spearman rho = %.3f, P = %.4g' % (rs, ps))

# 3. non-circular test of the baseline claim: post-on-pre slope vs 1, variance ratio
print()
for post in ['Ketamine','Midazolam']:
    X = sm.add_constant(Hp.Placebo.values); mod = sm.OLS(Hp[post].values, X).fit()
    b, se = mod.params[1], mod.bse[1]; t = (b-1)/se; df = len(Hp)-2
    ci = mod.conf_int()[1]
    vr = Hp[post].var(ddof=1)/Hp.Placebo.var(ddof=1)
    rn, pn = stats.pearsonr(Hp.Placebo, Hp[post]-Hp.Placebo)
    print(f'{post:10s} slope on placebo = {b:.3f} (95% CI {ci[0]:.3f}-{ci[1]:.3f}), '
          f't vs 1 = {t:+.2f}, P = {2*(1-stats.t.cdf(abs(t),df)):.4g} | var ratio = {vr:.2f} | '
          f'naive baseline-vs-change r = {rn:+.3f}')

# 4. MDD/HC cohort: grouping is external, so report baseline, post-drug and interaction
PH=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data/fig5_mdd_hc_n36.csv')
print()
for col, nm in [('FC_p2','placebo (p2)'), ('FC_d2','ketamine (d2)'), ('FC_delta','change d2-p2')]:
    a = PH.loc[PH.group=='HC', col]; b = PH.loc[PH.group=='MDD', col]
    t_, p_ = stats.ttest_ind(a,b,equal_var=False); _, pu = stats.mannwhitneyu(a,b)
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    print(f'{nm:14s} HC {a.mean():+.3f} vs MDD {b.mean():+.3f}  Welch t = {t_:+.3f}, P = {p_:.4g}, '
          f'MW P = {pu:.4g}, g = {(a.mean()-b.mean())/sp:+.2f}')

# ---------------------------------------------------------------- cell bd0dad4d (cell_index 489)
emp = np.asarray(m['C_C_C_empirical_np'], float)      # 85 x 12 baseline empirical NP edges
None                                        # AMPA restoration index  # [recovery: unresolvable interactive debris removed]
emp_sum = emp.sum(1)
print('--- verifying the pasted paragraph ---')
r0, p0 = stats.pearsonr(idx, y); print(f'index vs FU3 change, unadjusted: r = {r0:.3f}, P = {p0:.4g}')
None; None  # [recovery: unresolvable interactive debris removed]  # [recovery: unresolvable interactive debris removed]
F = (R2f/p2)/((1-R2f)/(n-p2-1)); print(f'full model: R2 = {R2f:.4f}, F({p2},{n-p2-1}) = {F:.3f}, P = {stats.f.sf(F,p2,n-p2-1):.4g}')
pass  # [recovery: unresolvable interactive debris removed] for nm, red in [('baseline symptoms (4 cols)', X1), ('baseline empirical NP (summed)', emp_sum.reshape(-1,1)),
# [recovery: unresolvable interactive debris removed]                 ('baseline empirical NP (12 cols)', emp)]:
# [recovery: unresolvable interactive debris removed]     for pred, pn in [(idx,'AMPA'), (gab,'GABA-A')]:
# [recovery: unresolvable interactive debris removed]         Xr = red; Xfu = np.column_stack([pred, red])
# [recovery: unresolvable interactive debris removed]         R2r,_ = r2(Xr,y); R2fu,_ = r2(Xfu,y); p1_, p2_ = Xr.shape[1], Xfu.shape[1]
# [recovery: unresolvable interactive debris removed]         Fc = ((R2fu-R2r)/(p2_-p1_))/((1-R2fu)/(n-p2_-1)); pc = stats.f.sf(Fc, p2_-p1_, n-p2_-1)
# [recovery: unresolvable interactive debris removed]         print(f'  {pn:6s} added to {nm:32s} dR2 = {R2fu-R2r:.4f}, F(1,{n-p2_-1}) = {Fc:.3f}, P = {pc:.4g}')
print()
r1,pp1 = stats.pearsonr(idx, emp_sum); print(f'index vs baseline empirical NP (summed): r = {r1:.3f}, P = {pp1:.4g}')
None; None  # [recovery: unresolvable interactive debris removed]  # [recovery: unresolvable interactive debris removed]

# ---------------------------------------------------------------- cell fbc8f06f (cell_index 498)
Z1 = emp_sum.reshape(-1,1)
xr2, yr2 = resid(idx, Z1), resid(y, Z1)
rp2, pp2_ = stats.pearsonr(xr2, yr2)
print('added-variable over empirical baseline NP: partial r = %.4f, P = %.4g (nested F P = 0.0259)' % (rp2, pp2_))
pass  # [recovery: unresolvable interactive debris removed] SC = pd.DataFrame(dict(
# [recovery: unresolvable interactive debris removed]     ampa_index=idx, fu3_symptom_change=y,
# [recovery: unresolvable interactive debris removed]     empirical_baseline_np_sum=emp_sum, baseline_symptom_sum=X1.sum(1),
# [recovery: unresolvable interactive debris removed]     index_resid_on_empNP=xr2, fu3change_resid_on_empNP=yr2))
SC.to_csv(os.path.join(OUT_DIR, 'fig5h_paragraph_scatters_n85.csv'), index=False)
rows=[]
for xn, yn, lab, kind in [
    ('index_resid_on_empNP','fu3change_resid_on_empNP','AMPA index vs FU3 symptom change, adjusted for baseline empirical NP','partial Pearson r'),
    ('ampa_index','fu3_symptom_change','AMPA index vs FU3 symptom change, unadjusted','Pearson r'),
    ('ampa_index','empirical_baseline_np_sum','AMPA index vs baseline empirical NP connectivity','Pearson r'),
    ('ampa_index','baseline_symptom_sum','AMPA index vs baseline symptoms','Pearson r')]:
    r_, p_ = stats.pearsonr(SC[xn], SC[yn])
    lo, hi = np.tanh(np.arctanh(r_) + np.array([-1,1])*1.959964/np.sqrt(len(SC)-3))
    rows.append(dict(relationship=lab, n=len(SC), test=kind, r=round(float(r_),3),
                     ci_low=round(float(lo),3), ci_high=round(float(hi),3),
                     p=float(f'{p_:.3g}')))
ST=pd.DataFrame(rows); None  # [recovery: side output suppressed]
print(ST.to_string(index=False))
