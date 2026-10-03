#!/usr/bin/env python3
"""long_cv_repeats_n85.csv

Computes
    The per-repeat cross-validated R2 values behind that summary, one column
    per model specification.

Inputs
    - /Users/yunman/Desktop/submission
    - /Users/yunman/Desktop/submission/figures_v2/fig4/predict_fu3_beha_changes/virtual_modu_predict_fu3_beha_changes.mat
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/10m_voxel_population_simulation/np_edges_simulated_baseline_mani.xlsx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/manuscript_numbers_newflow
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/sc-fc_prediction_model
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_longitudinal
    - (path built in the chain) f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat'
    - (path built in the chain) f'{B}/revision/10m_voxel_population_simulation/simulate_FC_edges.csv'
    - (path built in the chain) f'{B}/revision/model_scale_consistent/simulation_results_wide_12subs.csv'
    - (path built in the chain) f'{R3}/new3m_direction_checks.csv'
    - (path built in the chain) f'{R3}/Mani_simulated_3m_NP_12edges_and_factor.mat'
    - (path built in the chain) f'{R3}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat'
    - (path built in the chain) f'{MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv'
    - (path built in the chain) f'{B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv'
    - (path built in the chain) f'{FD3}/fig3a_mse_per_subject.csv'
    - (path built in the chain) f'{SC}/np_location.mat'
    - (path built in the chain) f'{SC}/112288_MID_taskFC.mat'
    - (path built in the chain) f'{NF}/{f}'
    - (path built in the chain) f'{B}/fig.3/fig3_data/fig3g_delta_np_six_models.csv'
    - (path built in the chain) f'{SM}/simulation_results_long_12subs.csv'
    - (path built in the chain) f'{P3S}/sub-000000112288/mid_data_mani_ampa.mat'
    - (path built in the chain) f'{F5}/fig5h_longitudinal_n85.csv'
    - (path built in the chain) f'{F5}/fig5h_added_variable_n85.csv'
    - (path built in the chain) f'{F5}/fig5h_paragraph_scatters_n85.csv'

Output
    04_figures/supp_longitudinal/data/long_cv_repeats_n85.csv

Statistical tests
      - none in this script's own computation: it assembles a source-data /
        audit table, and the tests that use it are named in the scripts of
        the tables downstream
    in the recovered chain that prepares its inputs:
      - one-sample t test
      - Wilcoxon signed-rank test
      - Pearson correlation
      - Spearman correlation
      - Benjamini-Hochberg FDR correction
      - ordinary least squares GLM with covariates
      - nested-model F test for the R2 increment
      - outcome-permutation null
      - leave-one-out cross-validation
      - Fisher z 95% confidence interval
      - partial correlation on residualised variables

Local runnability
    no (local_runnable = no).  Verification: not_run.
    re-run stops with a subject-index KeyError: the recovered chain selects
    subjects by ID from an upstream table whose index no longer matches the
    one it was written against. The statistics are documented but the script
    is not re-runnable against the current upstream files
Recovered from
    execution-log cell 330eedd4-4fd1-4cd7-b987-eaab95c94741
    frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, cell_index 825, 2026-09-22 20:26 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    5233e78b, 39431a70, 1b4a7685, 2cbadd0f, 1deb5307, 6f69dd7b, b74f5fe0,
    ba8e1b25, 1ff04fbb, 694432fe, 91bf4255, 21d0eb4a, 2a21c367, 0f1e9b07,
    5f6051db, c20074f5, 35a51eea, 732cf081, a7bf2f40, b3e94cc7, 3f599fdc,
    27a79d6e, fb0fc018, 802b5c95, a1036f26, 1ee567b6, b440dbfd, 723f178b,
    b30be31c, 330eedd4

Random seed
    fixed in the original run: seed = 7.  Re-running therefore reproduces the
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
    recovered/fig5/long_cv_repeats_n85__cell_330eedd4.py
"""
import os
import sys

OUT_DIR = os.environ.get(
    "RECOVERY_OUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scratch"))
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- cell 5233e78b (cell_index 602)
import scipy.io as sio, pandas as pd, numpy as np, os
from scipy import stats
B='/Users/yunman/Desktop/submission'
MN=f'{B}/revision/model_scale_consistent/manuscript_numbers_newflow'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
FD3=f'{B}/revision/text/figures/fig.3/fig3_data'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
ED=pd.read_csv(f'{B}/revision/10m_voxel_population_simulation/simulate_FC_edges.csv')
CONDMAP={'sst_stop_success':0,'sst_stop_failure':1,'mid_antici_hit':2,'mid_feedback_hit':3}
sub_ids=[str(s) for s in NEW['subject_ids']]
def edges_from_mat(a):
    return np.column_stack([a[i-1,j-1,:,CONDMAP[c]] for i,j,c in zip(ED.roi_i,ED.roi_j,ED.condition)])
MAT={'10m':edges_from_mat(NEW['simu_fc_10m_100m_params']),'100m':edges_from_mat(NEW['simu_fc_100m']),
     '1b':edges_from_mat(NEW['simu_fc_1b']),'10m_own':edges_from_mat(NEW['simu_fc_10m_own_params'])}
sw=pd.read_csv(f'{B}/revision/model_scale_consistent/simulation_results_wide_12subs.csv')
sw['sid']=sw.sub_id.astype(str).str.replace('sub-0*','',regex=True)
sw=sw.set_index('sid').loc[sub_ids]
CSV={m: sw[[f'{m}_baseline_edge{k}' for k in range(1,13)]].values.astype(float) for m in ['10m','100m','1b']}
print('mat vs wide-CSV baseline edges, same build:')
for m in CSV: print(f'  {m:5s} r = {stats.pearsonr(MAT[m].ravel(),CSV[m].ravel())[0]:.4f}  max|diff| = {np.abs(MAT[m]-CSV[m]).max():.4f}')
fz=lambda a,b: float(np.tanh(np.mean(np.arctanh(np.clip([stats.pearsonr(a[s],b[s])[0] for s in range(12)],-.999,.999)))))
print('\nwithin-subject profile r (Fisher-z), by source:')
print(f"{'pair':14s} {'from .mat':>10s} {'from wide CSV':>14s}")
for x,y in [('10m','100m'),('10m','1b'),('100m','1b')]:
    print(f'{x+" vs "+y:14s} {fz(MAT[x],MAT[y]):10.4f} {fz(CSV[x],CSV[y]):14.4f}')

# ---------------------------------------------------------------- cell 39431a70 (cell_index 607)
R3=f'{B}/revision/model_scale_consistent/manuscript_numbers_newflow/3m_model_new_run'
DC=pd.read_csv(f'{R3}/new3m_direction_checks.csv'); print(DC.to_string(index=False))
mm=sio.loadmat(f'{R3}/Mani_simulated_3m_NP_12edges_and_factor.mat', squeeze_me=True)
print('\nMani mat:', [(k, np.shape(v)) for k,v in mm.items() if not k.startswith('__')])

# ---------------------------------------------------------------- cell 1b4a7685 (cell_index 608)
EMPV=edges_from_mat(NEW['real_fc_dtb_voxels']); EMPA=edges_from_mat(NEW['real_fc_all_voxels'])
EMPW=sw[[f'emp_edge{k}' for k in range(1,13)]].values.astype(float)
for nm,A in [('real_fc_dtb_voxels (mask-matched)',EMPV),('real_fc_all_voxels',EMPA)]:
    print(f'wide-CSV emp_edge vs {nm}: r = {stats.pearsonr(EMPW.ravel(),A.ravel())[0]:.4f}  max|diff| = {np.abs(EMPW-A).max():.4f}')
m3=sio.loadmat(f'{R3}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat', squeeze_me=True)
new3=np.nanmean(np.asarray(m3['NP12edges'],float),axis=1)
mse=lambda s,e: ((s-e)**2).mean(1)
print('\nnew 3M MSE against each candidate reference:')
for nm,A in [('wide-CSV emp_edge',EMPW),('real_fc_dtb_voxels',EMPV),('real_fc_all_voxels',EMPA)]:
    print(f'  vs {nm:22s} {mse(new3,A).mean():.5f}')
print("\nuser's table: 3m_268 NEW vs empirical_original_3m = 0.09411 | vs empirical_model_voxels = 0.06489")

# ---------------------------------------------------------------- cell 2cbadd0f (cell_index 611)
EDC=[f'edge{k}' for k in range(1,13)]
sid=[s for s in sub_ids]
NF=pd.read_csv(f'{MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv')
NFB=NF[NF.condition=='baseline']
def by_sub(df):
    g=df.groupby('subID')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
    return np.array([g.loc[s].values for s in sid])
SRC={}
for sc in ['10m_reg','10m','100m','1b']:
    SRC[sc]=by_sub(NFB[NFB.scale==sc])
REG=pd.read_csv(f'{B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv')
RB=REG[(REG.condition=='baseline')]
g=RB.groupby('subject')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
SRC['regional_csv']=np.array([g.loc[s].values for s in sid])
SRC['3m_new']=new3; SRC['10m_own']=MAT['10m_own']
TARGET={'3m_268':0.06489,'10m_268':0.07180,'10m_1000':0.09747,'10m':0.06841,'100m':0.05571,'1b':0.06159}
print('MSE vs empirical_model_voxels (= emp_edge = real_fc_dtb_voxels), n = 12:')
for nm,A in SRC.items():
    print(f'  {nm:14s} {mse(A,EMPW).mean():.5f}')
print('\nuser new3m_direction_checks.csv targets:', TARGET)

# ---------------------------------------------------------------- cell 1deb5307 (cell_index 612)
def per_repeat_mse(df):
    out=[]
    for r,sub in df.groupby('run_idx'):
        g=sub.groupby('subID')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
        if set(sid)<=set(g.index):
            out.append(mse(np.array([g.loc[s].values for s in sid]), EMPW).mean())
    return float(np.mean(out)), len(out)
print('voxel builds: MSE of repeat-mean  vs  mean of per-repeat MSE')
for sc,tgt in [('10m',0.06841),('100m',0.05571),('1b',0.06159)]:
    d=NFB[NFB.scale==sc]; pr,n=per_repeat_mse(d)
    print(f'  {sc:5s} repeat-mean {mse(SRC[sc],EMPW).mean():.5f} | per-repeat mean {pr:.5f} (n_rep={n}) | user {tgt:.5f}')
# same test for the new 3M (5 repeats in the mat)
NP3=np.asarray(m3['NP12edges'],float)
print(f'  3m_new repeat-mean {mse(new3,EMPW).mean():.5f} | per-repeat mean '
      f'{np.mean([mse(NP3[:,r,:],EMPW).mean() for r in range(5)]):.5f} | user 0.06489')

# ---------------------------------------------------------------- cell 6f69dd7b (cell_index 614)
ORDER=['3m_268','10m_268','10m_1000','10m_own','10m','100m','1b']
def reps_from_nf(sc):
    out=[]
    for r,sub in NFB[NFB.scale==sc].groupby('run_idx'):
        g=sub.groupby('subID')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
        if set(sid)<=set(g.index): out.append(np.array([g.loc[s].values for s in sid]))
    return np.stack(out,1)                                   # subj x rep x edge
RB2=REG[REG.condition=='baseline'].copy(); RB2['rep']=RB2.repeat.astype(str)
r268=[]
for r,sub in RB2.groupby('rep'):
    g=sub.groupby('subject')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
    if set(sid)<=set(g.index): r268.append(np.array([g.loc[s].values for s in sid]))
REPS={'3m_268': NP3, '10m_268': np.stack(r268,1), '10m_1000': reps_from_nf('10m_reg'),
      '10m': reps_from_nf('10m'), '100m': reps_from_nf('100m'), '1b': reps_from_nf('1b')}
PROF={k: np.nanmean(v,1) for k,v in REPS.items()}; PROF['10m_own']=MAT['10m_own']
print('n repeats per build:', {k:v.shape[1] for k,v in REPS.items()}, '| 10m_own: 1 (single run)')
print('MSE vs empirical_model_voxels:', {k: round(float(mse(PROF[k],EMPW).mean()),5) for k in ORDER})

# ---------------------------------------------------------------- cell b74f5fe0 (cell_index 615)
HYP={'3m_268':'3 M','10m_268':'3 M','10m_1000':'10 M / 1000','10m_own':'10 M voxel',
     '10m':'100 M','100m':'100 M','1b':'100 M','SAR':'—','RWW':'—'}
SIMN={'3m_268':'3 M','10m_268':'10 M','10m_1000':'10 M','10m_own':'10 M','10m':'10 M',
      '100m':'100 M','1b':'1 B','SAR':'—','RWW':'—'}
RES={'3m_268':'268 regions','10m_268':'268 regions','10m_1000':'1000 regions',
     '10m_own':'voxel','10m':'voxel','100m':'voxel','1b':'voxel','SAR':'—','RWW':'—'}
FAMILY={**{k:'regional' for k in ['3m_268','10m_268','10m_1000']},
        **{k:'voxel' for k in ['10m_own','10m','100m','1b']},'SAR':'benchmark','RWW':'benchmark'}
a_old=pd.read_csv(f'{FD3}/fig3a_mse_per_subject.csv')
rows=[]
for k in ORDER:
    for s,v in zip(sid, mse(PROF[k],EMPW)):
        rows.append(dict(subject_id=int(s), model=k, mse=round(float(v),5),
                         empirical_reference='empirical_model_voxels'))
for bm in ['SAR','RWW']:
    for _,r in a_old[a_old.model==bm].iterrows():
        rows.append(dict(subject_id=int(r.subject_id), model=bm, mse=float(r.mse),
                         empirical_reference=str(r.empirical_reference)))
A=pd.DataFrame(rows)
A['family']=A.model.map(FAMILY); A['sim_neurons']=A.model.map(SIMN)
A['assimilation_hyperparams']=A.model.map(HYP); A['resolution']=A.model.map(RES)
A['n_repeats_averaged']=A.model.map({**{k:v.shape[1] for k,v in REPS.items()},'10m_own':1,'SAR':np.nan,'RWW':np.nan})
A=A[['subject_id','model','family','sim_neurons','assimilation_hyperparams','resolution',
     'n_repeats_averaged','empirical_reference','mse']]
pass  # [recovery: side output suppressed] A.to_csv(f'{FD3}/fig3a_mse_per_subject.csv', index=False)
# ---- 3c  7x7 similarity, same source rule
fz=lambda a,b: float(np.tanh(np.mean(np.arctanh(np.clip([stats.pearsonr(a[s],b[s])[0] for s in range(12)],-.999,.999)))))
Mx=pd.DataFrame([[1.0 if x==y else fz(PROF[x],PROF[y]) for y in ORDER] for x in ORDER],
                index=ORDER, columns=ORDER)
pass  # [recovery: side output suppressed] Mx.to_csv(f'{FD3}/fig3c_cross_scale_similarity.csv')
# ---- 3d  run-to-run SD of the NP sum, per subject
drows=[]
for k in ORDER:
    if k=='10m_own':
        drows.append(dict(model=k, subject_id=np.nan, np_sd=np.nan, n_repeats=1)); continue
    npsum=REPS[k].sum(2)                                   # subj x rep
    for s,v in zip(sid, np.nanstd(npsum,axis=1,ddof=1)):
        drows.append(dict(model=k, subject_id=int(s), np_sd=round(float(v),5),
                          n_repeats=REPS[k].shape[1]))
D4=pd.DataFrame(drows); None  # [recovery: side output suppressed]
print(A.groupby('model').mse.mean().round(5).to_string())
print(); print(Mx.round(3).to_string())
print('\nrun-to-run SD of NP sum (mean over 12):')
print(D4.dropna().groupby('model').np_sd.mean().round(4).to_string())

# ---------------------------------------------------------------- cell ba8e1b25 (cell_index 640)
import scipy.io as sio, h5py
SC='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/sc-fc_prediction_model'
loc=sio.loadmat(f'{SC}/np_location.mat'); print({k:(v.shape if hasattr(v,'shape') else v) for k,v in loc.items() if not k.startswith('__')})
m=sio.loadmat(f'{SC}/112288_MID_taskFC.mat'); print({k:(v.shape,str(v.dtype)) for k,v in m.items() if not k.startswith('__')})

# ---------------------------------------------------------------- cell 1ff04fbb (cell_index 644)
ED=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv'); print(ED.to_string(index=False))

# ---------------------------------------------------------------- cell 694432fe (cell_index 652)
NF='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/manuscript_numbers_newflow'
for f in ['mse_vs_1b_three_quantities.csv','delta_consistency_six_models.csv',
          'six_model_modulation_group_effect.csv','nf_claim5_responder_ranking.csv',
          'nf_claim4_response_consistency.csv','baseline_reliability_six_models.csv']:
    try:
        d=pd.read_csv(f'{NF}/{f}')
        print(f'=== {f}  {d.shape}'); print(d.round(4).to_string(index=False)[:1600]); print()
    except Exception as e: print(f,'->',e)

# ---------------------------------------------------------------- cell 91bf4255 (cell_index 684)
import io
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures'
def show(p, n=40, cols=None):
    d=pd.read_csv(p); print(f'--- {p.split("/")[-1]}  {d.shape}')
    dd=d[cols] if cols else d
    print(dd.head(n).to_string(index=False, float_format=lambda x:f'{x:.4g}')[:2500])
for f in ['fig2a_cpm_rho.csv','fig2c_profile_scores.csv','fig2e_edge_group_difference.csv',
          'fig2f_sensitivity_cohort_covariates.csv']:
    show(f'{B}/fig.2/fig2_data/{f}', 12)

# ---------------------------------------------------------------- cell 21d0eb4a (cell_index 688)
F5=f'{B}/fig.5/fig5_data'
show(f'{F5}/fig5_panel_stats.csv', 40)

# ---------------------------------------------------------------- cell 2a21c367 (cell_index 703)
R3=f'{NF}/3m_model_new_run'
m3=sio.loadmat(f'{R3}/Mani_simulated_3m_NP_12edges_and_factor.mat')
print({k:(v.shape,str(v.dtype)) for k,v in m3.items() if not k.startswith('__')})
XP='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/10m_voxel_population_simulation/np_edges_simulated_baseline_mani.xlsx'
xo=pd.ExcelFile(XP); print('\nsheets:', xo.sheet_names)
for sh in xo.sheet_names[:3]:
    d=xo.parse(sh); print(f'--- {sh} {d.shape}', d.columns.tolist()[:10]); print(d.head(3).to_string(index=False)[:400])

# ---------------------------------------------------------------- cell 0f1e9b07 (cell_index 704)
cn=[str(x[0]) for x in m3['condition_names'][0]]; rl=[str(x[0]) for x in m3['repeat_labels'][0]]
s3=[str(x[0]) for x in m3['subjects'][:,0]]
print('conditions:', cn, '| repeats:', rl); print('subjects match fig3 set:', [x.replace('sub-','').lstrip('0') for x in s3]==list(sid))
sp=xo.parse('simulate_np'); sp['sid']=sp.id.astype(str)
print('\nxlsx n=',len(sp),'| overlap with the 12 twins:', len(set(sid)&set(sp.sid)))
print('condition column groups:', [c.split('_edge')[0] for c in sp.columns if c.endswith('edge1')])

# ---------------------------------------------------------------- cell 5f6051db (cell_index 707)
# [recovery] this cell raised in the original session at its line 9; only the
# statements that had already executed are carried over
g6=pd.read_csv(f'{B}/fig.3/fig3_data/fig3g_delta_np_six_models.csv'); print(g6.columns.tolist(), g6.shape)
print(g6.head(3).to_string(index=False))
# reproduce 10m_268 from the regional CSV: conditions baseline / ampa / ampa_gaba
rr=REG[REG.model=='regional'].copy()
rr['s']=rr.subject.str.replace('sub-','').str.lstrip('0')
piv={c: rr[rr.condition==c].groupby('s')[EDC].mean().sum(1) for c in ['baseline','ampa','ampa_gaba','gaba']}
for drug,c in [('ampa','ampa'),('gaba','ampa_gaba')]:
    dd=(piv[c]-piv['baseline']).reindex(sid)

# ---------------------------------------------------------------- cell c20074f5 (cell_index 712)
NPe=m3['NP12edges']                                  # 12 x 3 x 5 x 12
i_a, i_g, i_b = cn.index('manipu'), cn.index('manipu_gaba'), cn.index('manipu_gaba_baseline')
sum3=lambda ci: np.nanmean(NPe[:,ci,:,:].sum(2),1)    # 12 subj, repeat-mean of the 12-edge sum
b_run, b_std = sum3(i_b), NP3.sum(2).mean(1)
d3={'ampa_runbase': sum3(i_a)-b_run, 'gaba_runbase': sum3(i_g)-b_run,
    'ampa_stdbase': sum3(i_a)-b_std, 'gaba_stdbase': sum3(i_g)-b_std}
for k,v in d3.items(): print(f'new 3M Δ {k:14s} mean {v.mean():+.4f}  n_up {int((v>0).sum())}/12  t={stats.ttest_1samp(v,0).statistic:.3f} P={stats.ttest_1samp(v,0).pvalue:.4g}')
print('\nold 3M stored: ampa +0.9669 (11/12), gaba +3.1460 (12/12)')
# ---- new build (10m_own) for the same 12 twins
npc=[c for c in sp.columns if c.endswith('_np')]; print('\nxlsx np columns:', npc)
ss=sp.set_index('sid').loc[sid]
print({c: round(float(ss[c].mean()),4) for c in npc})

# ---------------------------------------------------------------- cell 35a51eea (cell_index 713)
own_b, own_a, own_g = ss.baseline_np.values, ss.mani_ampa_np.values, ss.mani_ampa_gaba_np.values
DL={}
for m_ in ['10m_268','10m_1000','10m','100m','1b']:
    for dr in ['ampa','gaba']:
        v=g6[(g6.model==m_)&(g6.drug==dr)].set_index(g6[(g6.model==m_)&(g6.drug==dr)].sub_id.astype(str)).loc[sid].delta.values
        DL[(m_,dr)]=v
DL[('3m_268','ampa')]=d3['ampa_runbase']; DL[('3m_268','gaba')]=d3['gaba_runbase']
DL[('10m_own','ampa')]=own_a-own_b;       DL[('10m_own','gaba')]=own_g-own_b
rows=[]
for (m_,dr),v in DL.items():
    t=stats.ttest_1samp(v,0); w=stats.wilcoxon(v)
    ci=stats.t.interval(.95,11,v.mean(),stats.sem(v))
    rows.append(dict(modulation=dr.upper() if dr=='ampa' else 'GABA-A', model=m_, family=FAMILY[m_], n=12,
        n_increased=int((v>0).sum()), pct_increased=round(100*float((v>0).mean()),1),
        mean_delta=round(float(v.mean()),4), sd_delta=round(float(v.std(ddof=1)),4),
        sem=round(float(stats.sem(v)),4), t=round(float(t.statistic),3), df=11,
        p=float(t.pvalue), cohens_dz=round(float(v.mean()/v.std(ddof=1)),3),
        ci95_lo=round(float(ci[0]),4), ci95_hi=round(float(ci[1]),4), wilcoxon_p=float(w.pvalue)))
G=pd.DataFrame(rows)
from statsmodels.stats.multitest import multipletests
G['q_bh']=multipletests(G.p,method='fdr_bh')[1]
G=G.sort_values(['modulation','model'], key=lambda s: s.map({m:i for i,m in enumerate(ORDER)}) if s.name=='model' else s)
print(G[['modulation','model','n_increased','mean_delta','sd_delta','t','p','cohens_dz','q_bh']]
      .to_string(index=False, float_format=lambda x:f'{x:.4g}'))

# ---------------------------------------------------------------- cell 732cf081 (cell_index 743)
SM='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent'
LG=pd.read_csv(f'{SM}/simulation_results_long_12subs.csv')
print(LG.columns.tolist(), LG.shape)
print(LG.head(3).to_string(index=False)[:400])
if 'scale' in LG.columns: print('\nscales:', LG.scale.unique(), '| conditions:', LG[[c for c in LG.columns if 'cond' in c]].iloc[:,0].unique() if any('cond' in c for c in LG.columns) else '-')

# ---------------------------------------------------------------- cell a7bf2f40 (cell_index 754)
P3S=f'{SM}/orignial_3subs_perturb_100m_whole_brain_fc'
mm=sio.loadmat(f'{P3S}/sub-000000112288/mid_data_mani_ampa.mat')
print({k:(v.shape,str(v.dtype)) for k,v in mm.items() if not k.startswith('__')})

# ---------------------------------------------------------------- cell 3f599fdc (cell_index 762)
def matload(p):
    try:
        d=sio.loadmat(p); return {k:v for k,v in d.items() if not k.startswith('__')}, 'v7'
    except NotImplementedError:
        f2=h5py.File(p,'r'); out={}
        for k in f2.keys():
            if k.startswith('#'): continue
            a=f2[k]
            if k.endswith('_subject'):
                out[k]=[''.join(chr(c) for c in np.array(f2[r]).ravel()) for r in np.array(a).ravel()]
            else:
                out[k]=np.array(a).transpose(2,1,0) if a.ndim==3 else np.array(a)
        return out,'v73'
def labs(d,key):
    v=d[key]
    return v if isinstance(v,list) else [str(x[0]) for x in v[0]]
def get3(sub,kind):
    out=np.full((5,12),np.nan)
    if kind=='ampa':
        dS,_=matload(f'{P3S}/{sub}/sst_data_mani_ampa.mat'); dM,_=matload(f'{P3S}/{sub}/mid_data_mani_ampa.mat')
        selS=[i for i,l in enumerate(labs(dS,'sst_subject')) if '-0.0044-gaba' in l]
        selM=list(range(dM['mid_antici_hit'].shape[2]))
    else:
        dS,_=matload(f'{P3S}/{sub}/sst_data_mani_gaba_high.mat'); dM,_=matload(f'{P3S}/{sub}/mid_data_mani_gaba_high.mat')
        selS=[i for i,l in enumerate(labs(dS,'sst_subject')) if l.endswith('gaba-0.0040')]
        selM=[i for i,l in enumerate(labs(dM,'mid_subject')) if l.endswith('gaba-0.0040')]
    FMAP={'SST_stop_success':(dS,'sst_stop_suces',selS),'SST_stop_failure':(dS,'sst_stop_failure',selS),
          'MID_feed_hit':(dM,'mid_feed_hit',selM),'MID_antici_hit':(dM,'mid_antici_hit',selM)}
    for ei,r in ED.iterrows():
        src,fld,sel=FMAP[r.condition]; A=src[fld]
        for k,idx in enumerate(sel[:5]): out[k,ei]=A[r.i_217-1, r.j_217-1, idx]
    return np.nanmean(out,0), len(selS), len(selM)
res={}
pass  # [recovery: unresolvable interactive debris removed] for s,folder in SUB3.items():
# [recovery: unresolvable interactive debris removed]     for dr in ['ampa','gaba']:
# [recovery: unresolvable interactive debris removed]         prof,nS,nM=get3(folder,dr); res[(s,dr)]=prof
# [recovery: unresolvable interactive debris removed]         print(f'{s:10s} {dr:5s} nSST={nS} nMID={nM} | NP sum {prof.sum():+.4f} | baseline {base100[s].sum():+.4f} | Δ {prof.sum()-base100[s].sum():+.4f}')
print('\nstored fig3g Δ for these three:')
for dr in ['ampa','gaba']:
    pass  # [recovery: unresolvable interactive debris removed] st=g6[(g6.model=='100m')&(g6.drug==dr)].set_index(g6[(g6.model=='100m')&(g6.drug==dr)].sub_id.astype(str)).loc[list(SUB3)].delta
    print(' ',dr, {k:round(v,4) for k,v in st.items()})

# ---------------------------------------------------------------- cell 27a79d6e (cell_index 815)
L85=pd.read_csv(f'{F5}/fig5h_longitudinal_n85.csv'); print(L85.columns.tolist(), L85.shape)
print(L85.head(3).to_string(index=False))

# ---------------------------------------------------------------- cell fb0fc018 (cell_index 816)
AV=pd.read_csv(f'{F5}/fig5h_added_variable_n85.csv'); print('added-variable cols:', AV.columns.tolist(), AV.shape)
PS85=pd.read_csv(f'{F5}/fig5h_paragraph_scatters_n85.csv'); print('paragraph cols:', PS85.columns.tolist(), PS85.shape)
print(PS85.head(2).to_string(index=False))

# ---------------------------------------------------------------- cell 802b5c95 (cell_index 817)
MP='/Users/yunman/Desktop/submission/figures_v2/fig4/predict_fu3_beha_changes/virtual_modu_predict_fu3_beha_changes.mat'
dm,vv=matload(MP); print(vv, {k:(np.shape(v) if not isinstance(v,list) else f'list[{len(v)}]') for k,v in dm.items()})

# ---------------------------------------------------------------- cell a1036f26 (cell_index 818)
Xf, y85 = dm['X_final'], dm['y_final'].ravel()
X1b, empNP85, ampa85, gaba85, beha85 = dm['X1'], dm['C_C_C_empirical_np'], dm['C_Delta_Behav_mod'].ravel(), dm['C_Delta_Behav_mod_gaba'].ravel(), dm['C_C_beha_data']
print('shapes:', Xf.shape, y85.shape, X1b.shape, empNP85.shape, beha85.shape)
print('X_final last column == AMPA index?', np.allclose(Xf[:,-1], ampa85), '| first 4 == X1?', np.allclose(Xf[:,:4], X1b))
print('AMPA index == fig5h csv?', np.allclose(ampa85, L85.ampa_restoration_index.values))
print('y == fu3 change?', np.allclose(y85, L85.fu3_symptom_change.values))
print('empNP sum == paragraph csv?', np.allclose(empNP85.sum(1), PS85.empirical_baseline_np_sum.values))
print('\nbehaviour columns (6), means:', np.round(beha85.mean(0),3), '| X1 cols are which of them?',
      [int(np.argmin([np.abs(np.corrcoef(X1b[:,j],beha85[:,k])[0,1]-1) for k in range(6)])) for j in range(4)])
print('baseline symptom sum == paragraph csv?', np.allclose(beha85.sum(1), PS85.baseline_symptom_sum.values))

# ---------------------------------------------------------------- cell 1ee567b6 (cell_index 820)
import statsmodels.api as sm
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import LinearRegression
BEH=[f'baseline behaviour {i+1}' for i in range(6)]
MODEL_BEH=[2,3,4,5]
empS=empNP85.sum(1)
def ols(X,y):
    Xc=sm.add_constant(X); return sm.OLS(y,Xc).fit()
# ---- 1  full model coefficients
names=['AMPA restoration index']+[BEH[i] for i in MODEL_BEH]
Xfull=np.column_stack([ampa85]+[beha85[:,i] for i in MODEL_BEH])
m_full, m_red = ols(Xfull,y85), ols(np.column_stack([beha85[:,i] for i in MODEL_BEH]),y85)
z=lambda v:(v-v.mean())/v.std(ddof=1)
m_std=ols(np.column_stack([z(c) for c in Xfull.T]), z(y85))
CO=[]
for j,nm in enumerate(names):
    ci=m_full.conf_int()[j+1]
    CO.append(dict(predictor=nm, beta=round(float(m_full.params[j+1]),4), se=round(float(m_full.bse[j+1]),4),
                   ci95_lo=round(float(ci[0]),4), ci95_hi=round(float(ci[1]),4),
                   t=round(float(m_full.tvalues[j+1]),3), df_resid=int(m_full.df_resid),
                   p=float(m_full.pvalues[j+1]), beta_std=round(float(m_std.params[j+1]),4),
                   ci95_std_lo=round(float(m_std.conf_int()[j+1][0]),4), ci95_std_hi=round(float(m_std.conf_int()[j+1][1]),4)))
CO=pd.DataFrame(CO)
print(f'full model R2={m_full.rsquared:.4f}  F({int(m_full.df_model)},{int(m_full.df_resid)})={m_full.fvalue:.3f}  P={m_full.f_pvalue:.3g}')
print(f'reduced (4 baseline) R2={m_red.rsquared:.4f}')
print(CO[['predictor','beta','se','ci95_lo','ci95_hi','t','p','beta_std']].to_string(index=False, float_format=lambda x:f'{x:.4g}'))

# ---------------------------------------------------------------- cell b440dbfd (cell_index 821)
rng=np.random.default_rng(7); NP_=5000
def increment(idx, cov, covname, idxname):
    Xr=cov; Xf_=np.column_stack([idx,cov])
    mr,mf=ols(Xr,y85),ols(Xf_,y85)
    d=mf.rsquared-mr.rsquared
    F=(d/1)/((1-mf.rsquared)/mf.df_resid); pF=1-stats.f.cdf(F,1,mf.df_resid)
    null=np.empty(NP_)
    for b in range(NP_):
        yp=rng.permutation(y85)
        null[b]=ols(Xf_,yp).rsquared-ols(Xr,yp).rsquared
    # partial correlation of idx with y given cov
    rx=sm.OLS(idx,sm.add_constant(cov)).fit().resid; ry=sm.OLS(y85,sm.add_constant(cov)).fit().resid
    pr=stats.pearsonr(rx,ry)
    return dict(index=idxname, covariates=covname, n=85, R2_reduced=round(float(mr.rsquared),4),
                R2_full=round(float(mf.rsquared),4), delta_R2=round(float(d),4), F_change=round(float(F),3),
                df1=1, df2=int(mf.df_resid), p_change=float(pF), p_perm_deltaR2=float((null>=d).mean()),
                null_p95=round(float(np.percentile(null,95)),4), partial_r=round(float(pr[0]),3),
                p_partial=float(pr[1])), null
COV4=np.column_stack([beha85[:,i] for i in MODEL_BEH]); COV1=empS[:,None]
INC=[];NULLS={}
for idx,inm in [(ampa85,'AMPA'),(gaba85,'GABA-A')]:
    for cov,cnm in [(COV4,'4 baseline behaviour scores'),(COV1,'baseline empirical NP')]:
        r_,n_=increment(idx,cov,cnm,inm); INC.append(r_); NULLS[(inm,cnm)]=n_
INC=pd.DataFrame(INC)
print(INC[['index','covariates','R2_reduced','R2_full','delta_R2','F_change','df2','p_change','p_perm_deltaR2','partial_r','p_partial']]
      .to_string(index=False, float_format=lambda x:f'{x:.4g}'))

# ---------------------------------------------------------------- cell 723f178b (cell_index 822)
VARS=[('Baseline empirical NP (sum)',empS)]+[(f'Baseline behaviour {i+1}',beha85[:,i]) for i in range(6)]+\
     [('Baseline symptom sum (4 model scores)',COV4.sum(1)),('FU3 symptom change',y85)]
rows=[]
for inm,idx in [('AMPA index',ampa85),('GABA-A index',gaba85),('Baseline empirical NP (sum)',empS)]:
    for vn,v in VARS:
        if vn==inm: continue
        r=stats.pearsonr(idx,v); rho=stats.spearmanr(idx,v)
        lo,hi=np.tanh(np.arctanh(r[0])+np.array([-1,1])*1.96/np.sqrt(82))
        rows.append(dict(x=inm, y=vn, n=85, pearson_r=round(float(r[0]),3), ci95_lo=round(float(lo),3),
                         ci95_hi=round(float(hi),3), p_pearson=float(r[1]), spearman_rho=round(float(rho[0]),3),
                         p_spearman=float(rho[1])))
CR=pd.DataFrame(rows)
CR['q_bh_within_x']=CR.groupby('x').p_pearson.transform(lambda s: multipletests(s,method='fdr_bh')[1])
print(CR[CR.x=='AMPA index'][['y','pearson_r','ci95_lo','ci95_hi','p_pearson','q_bh_within_x']].to_string(index=False, float_format=lambda x:f'{x:.4g}'))
print()
print(CR[CR.x=='Baseline empirical NP (sum)'][['y','pearson_r','p_pearson','q_bh_within_x']].to_string(index=False, float_format=lambda x:f'{x:.4g}'))

# ---------------------------------------------------------------- cell b30be31c (cell_index 824)
def cvr2_pooled(X,y,n_repeats=10,n_splits=10,seed=0):
    out=[]
    for rep in range(n_repeats):
        kf=KFold(n_splits=n_splits,shuffle=True,random_state=seed+rep); pred=np.empty_like(y,dtype=float)
        for tr,te in kf.split(X): pred[te]=LinearRegression().fit(X[tr],y[tr]).predict(X[te])
        out.append(1-((y-pred)**2).sum()/((y-y.mean())**2).sum())
    return np.array(out)
from sklearn.model_selection import KFold
CVS={'baseline behaviour (4)':cvr2_pooled(COV4,y85),
     '+ AMPA index':cvr2_pooled(np.column_stack([COV4,ampa85]),y85),
     '+ GABA-A index':cvr2_pooled(np.column_stack([COV4,gaba85]),y85),
     'baseline empirical NP':cvr2_pooled(COV1,y85),
     'baseline NP + AMPA':cvr2_pooled(np.column_stack([COV1,ampa85]),y85)}
CV=pd.DataFrame([dict(model=k, n=85, cv_R2_mean=round(float(v.mean()),4), cv_R2_sd=round(float(v.std(ddof=1)),4),
                      cv_R2_min=round(float(v.min()),4), cv_R2_max=round(float(v.max()),4),
                      n_repeats=len(v), scheme='10-fold, pooled out-of-fold predictions, 10 repeats') for k,v in CVS.items()])
print(CV.to_string(index=False))
print('\nstored fig5h_nested_models.csv: cvR2_reduced 0.08602, cvR2_full(AMPA) 0.1107, cvR2_full(GABA) 0.08805')

# ---------------------------------------------------------------- cell 330eedd4 (cell_index 825)
import os
LD='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_longitudinal'
None; None  # [recovery: side output suppressed]  # [recovery: side output suppressed]
pass  # [recovery: side output suppressed] CO.to_csv(f'{LD}/data/long_full_model_coefficients_n85.csv', index=False)
pass  # [recovery: side output suppressed] INC.to_csv(f'{LD}/data/long_nested_increments_n85.csv', index=False)
pass  # [recovery: side output suppressed] CR.to_csv(f'{LD}/data/long_correlations_n85.csv', index=False)
pass  # [recovery: side output suppressed] CV.to_csv(f'{LD}/data/long_cv_out_of_sample_n85.csv', index=False)
pass  # [recovery: side output suppressed] np.savez(f'{LD}/data/long_permutation_nulls.npz', **{f'{k[0]}|{k[1]}':v for k,v in NULLS.items()})
pass  # [recovery: side output suppressed] pd.DataFrame({'ampa_index':ampa85,'gaba_index':gaba85,'empirical_baseline_np_sum':empS,
# [recovery: side output suppressed]               'fu3_symptom_change':y85, **{f'baseline_behaviour_{i+1}':beha85[:,i] for i in range(6)},
# [recovery: side output suppressed]               'baseline_symptom_sum_4':COV4.sum(1)}).to_csv(f'{LD}/data/long_subject_level_n85.csv', index=False)
pd.DataFrame(CVS).to_csv(os.path.join(OUT_DIR, 'long_cv_repeats_n85.csv'), index=False)
print('model summary: R2_full', round(float(m_full.rsquared),4), '| F', round(float(m_full.fvalue),3),
      f'({int(m_full.df_model)},{int(m_full.df_resid)})', '| P', f'{m_full.f_pvalue:.3g}')
print('tables written:', sorted(os.listdir(f'{LD}/data')))
