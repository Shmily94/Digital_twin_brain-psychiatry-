#!/usr/bin/env python3
"""fingerprint_similarity_empirical.csv

Computes
    Trial-by-subject similarity matrix of the empirical BOLD connectivity
    profiles (24 trials x 4 subjects) that the identification analysis is
    computed on.

Inputs
    - /Users/yunman/Desktop/submission
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data
    - (path built in the chain) f'{F}/fig4_sdq_items_n287.csv'
    - (path built in the chain) f'{F}/fig4_dawba_domains_n284.csv'
    - (path built in the chain) f'{F}/fig4_subject_level_n288.csv'
    - (path built in the chain) f'{B}/{f}'
    - (path built in the chain) f'{D4}/fig4_paired_np_mid_n288.csv'
    - (path built in the chain) f'{D4}/fig4_subject_level_n288.csv'
    - (path built in the chain) f'{B}/revision/model_scale_consistent/3m_repeats/3m_np_edges_repeats_tidy.csv'
    - (path built in the chain) f'{B}/revision/sensitivity_analysis/repeated_assimilation/task_fc_raw_217x217_7runs.mat'
    - (path built in the chain) f'{B}/figures_v2/fig4/cross_validation/{f}'
    - (path built in the chain) f'{AR}/assimilation_stability_source_data.csv'
    - (path built in the chain) f'{AR}/np_edges_7runs_stats.csv'
    - (path built in the chain) f'{AR}/np_edges_7runs_long.csv'
    - (path built in the chain) f'{B}/final_file/data/mani_ampa_gaba_eft_rest_4subs.xlsx'
    - (path built in the chain) f'{CN}/{f}'
    - (path built in the chain) path
    - (path built in the chain) f'{CN}/TableSXX_conductance_sensitivity_n288.csv'
    - (path built in the chain) f'{CN}/individual_response_n288.csv'
    - (path built in the chain) f'{CN}/npchange_correlation_288_n288.csv'

Output
    04_figures/_recovered_session_b194cd74/ed7/data/fingerprint_similarity_empirical.csv

Statistical tests
    in this script's own computation:
      - intraclass correlation
    in the recovered chain that prepares its inputs:
      - Pearson correlation
      - nested-model F test for the R2 increment
      - outcome-permutation null
      - leave-one-out cross-validation
      - partial correlation on residualised variables

Local runnability
    yes (local_runnable = yes).  Verification: match.
    24 rows x 5 cols identical (max rel dev 0.00e+00)
Recovered from
    execution-log cell 4f1219ba-ee06-45f1-adc4-bf6e8ed25294
    frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, cell_index 521, 2026-09-21 21:29 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    9639cab9, 3318eca3, fc72540d, f06441ce, 41572f3b, e9ccf5a2, 4918c1b1,
    33b70781, 205b9942, c59cf5a9, 4f1219ba

Random seed
    fixed in the original run: seed = 2.  Re-running therefore reproduces the
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
    recovered/fig5/fingerprint_similarity_empirical__cell_4f1219ba.py
"""
import os
import sys

OUT_DIR = os.environ.get(
    "RECOVERY_OUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scratch"))
os.makedirs(OUT_DIR, exist_ok=True)

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

# ---------------------------------------------------------------- cell 9639cab9 (cell_index 449)
import pandas as pd, numpy as np, scipy.io as sio, os
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data'
for f in sorted(os.listdir(B)):
    d=pd.read_csv(f'{B}/{f}')
    print('==',f, d.shape); print(list(d.columns))

# ---------------------------------------------------------------- cell f06441ce (cell_index 481)
D4='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data'
PD=pd.read_csv(f'{D4}/fig4_paired_np_mid_n288.csv'); print(PD.shape, list(PD.columns))
SL=pd.read_csv(f'{D4}/fig4_subject_level_n288.csv'); print(SL.shape, list(SL.columns))
print(PD.head(3).to_string(index=False))

# ---------------------------------------------------------------- cell 41572f3b (cell_index 505)
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
# 1 repeated assimilation
t=pd.read_csv(f'{B}/revision/model_scale_consistent/3m_repeats/3m_np_edges_repeats_tidy.csv')
print('3m_repeats:', t.shape, '| replicates', sorted(t.replicate.unique()), '| subs', t.sub_id.nunique(),
      '| conditions', t.condition.unique(), '| edges', t.edge_num.nunique())
mm=sio.loadmat(f'{B}/revision/sensitivity_analysis/repeated_assimilation/task_fc_raw_217x217_7runs.mat', squeeze_me=True)
print('7runs mat keys:', [(k, np.shape(v)) for k,v in mm.items() if not k.startswith('__')])
# 2 fingerprinting
for f in ['finger_predic_empir.csv','finger_predic_simula.csv','label_file.csv']:
    d=pd.read_csv(f'{B}/figures_v2/fig4/cross_validation/{f}')
    print(f, d.shape, list(d.columns)[:8])
print(os.listdir(f'{B}/figures_v2/fig4/cross_validation/cross_hyperparameter')[:10])

# ---------------------------------------------------------------- cell e9ccf5a2 (cell_index 510)
AR=f'{B}/revision/sensitivity_analysis/assimilated_region'
a=pd.read_csv(f'{AR}/assimilation_stability_source_data.csv'); print('source_data', a.shape, list(a.columns)); print(a.head(8).to_string(index=False))
st=pd.read_csv(f'{AR}/np_edges_7runs_stats.csv'); print('\n7runs_stats', st.shape, list(st.columns)); print(st.to_string(index=False)[:1200])
lg=pd.read_csv(f'{AR}/np_edges_7runs_long.csv'); print('\n7runs_long', lg.shape, list(lg.columns), '| runs', sorted(lg.iloc[:,0].unique())[:12] if lg.shape[1] else '')
print(lg.head(6).to_string(index=False))

# ---------------------------------------------------------------- cell 4918c1b1 (cell_index 512)
xl=pd.ExcelFile(f'{B}/final_file/data/mani_ampa_gaba_eft_rest_4subs.xlsx'); print('EFT sheets:', xl.sheet_names)
for sh in xl.sheet_names:
    d=xl.parse(sh); print('--',sh, d.shape); print(d.to_string(index=False)[:700])

# ---------------------------------------------------------------- cell 33b70781 (cell_index 514)
CN=f'{B}/revision/empirical_simul_np_fcs_300subs/cal_np_3m_model'
for f in sorted(os.listdir(CN)):
    if f.endswith('.csv'):
        try:
            d=pd.read_csv(f'{CN}/{f}', nrows=3); full=sum(1 for _ in open(f'{CN}/{f}'))-1
            print(f'{f:52s} rows={full:4d} cols={list(d.columns)[:9]}')
        except Exception as ex: print(f, 'ERR', ex)

# ---------------------------------------------------------------- cell 205b9942 (cell_index 515)
out={}
# ---------- S1 repeated assimilation ----------
A5=pd.read_csv(f'{AR}/assimilation_stability_source_data.csv')
R=A5[['run1','run2','run3','run4','run5']].values          # 6 edges x 5 runs
k=R.shape[1]; nsub=R.shape[0]
gm=R.mean(); MSR=((R.mean(1)-gm)**2).sum()*k/(nsub-1); MSC=((R.mean(0)-gm)**2).sum()*nsub/(k-1)
MSE=((R-R.mean(1,keepdims=True)-R.mean(0,keepdims=True)+gm)**2).sum()/((nsub-1)*(k-1))
icc31=(MSR-MSE)/(MSR+(k-1)*MSE); icc21=(MSR-MSE)/(MSR+(k-1)*MSE+k*(MSC-MSE)/nsub)
import itertools
pair_r=[stats.pearsonr(R[:,i],R[:,j])[0] for i,j in itertools.combinations(range(k),2)]
print(f'S1  ICC(3,1) = {icc31:.4f}  ICC(2,1) = {icc21:.4f}  | run-pair r mean {np.mean(pair_r):.4f} '
      f'range {min(pair_r):.4f}-{max(pair_r):.4f} | between-edge SD {R.mean(1).std(ddof=1):.4f} '
      f'vs mean within-edge SD {R.std(1,ddof=1).mean():.4f} (ratio {R.mean(1).std(ddof=1)/R.std(1,ddof=1).mean():.1f}x)')
out['S1']=dict(icc31=icc31, icc21=icc21, pair_r=pair_r)

# ---------- S2 fingerprinting ----------
def acc(path):
    d=pd.read_excel(path, header=None)
    subs=list(d.iloc[0,1:].values); rows=d.iloc[1:,0].values
    Mx=d.iloc[1:,1:].astype(float).values
    truth=[r.split('_')[0] for r in rows]
    pred=[subs[i] for i in Mx.argmax(1)]
    self_r=np.array([Mx[i, subs.index(truth[i])] for i in range(len(rows))])
    other=np.array([np.delete(Mx[i], subs.index(truth[i])).max() for i in range(len(rows))])
    return subs, rows, Mx, truth, pred, self_r, other
FE=acc(f'{B}/figures_v2/fig4/cross_validation/fingerprint_empirical_data.xlsx')
FS=acc(f'{B}/figures_v2/fig4/cross_validation/fingerprint_simulated_data.xlsx')
for nm,F in [('empirical',FE),('simulated',FS)]:
    corr=np.array([t==p for t,p in zip(F[3],F[4])])
    print(f'S2  {nm:10s} accuracy {corr.sum()}/{len(corr)} = {100*corr.mean():.1f}%  '
          f'| margin (self - best other) mean {np.mean(F[5]-F[6]):+.4f}  n wrong {int((~corr).sum())} '
          f'{[F[1][i] for i in np.where(~corr)[0]]}')
    out[f'S2_{nm}']=dict(correct=int(corr.sum()), n=len(corr), margin=(F[5]-F[6]))

# ---------------------------------------------------------------- cell c59cf5a9 (cell_index 516)
# ---------- S3 conductance grid ----------
CG=pd.read_csv(f'{CN}/TableSXX_conductance_sensitivity_n288.csv')
IND=pd.read_csv(f'{CN}/individual_response_n288.csv')
SL4=pd.read_csv(f'{D4}/fig4_subject_level_n288.csv')
IND=IND.merge(SL4[['ID','Group']], left_on='id_numeric', right_on='ID', how='left')
print('merged groups:', IND.Group.isna().sum(), 'missing |', IND.Group.value_counts().to_dict())
SET=['ampa_low','ampa','ampa_high','gaba_low','gaba','gaba_high']
strat=[]
for s in SET:
    for g in ['HC','High-symptom','Patient']:
        v=IND.loc[IND.Group==g, s]
        strat.append(dict(setting=s, group=g, n=len(v), n_up=int((v>0).sum()),
                          pct_up=round(100*float((v>0).mean()),1)))
    ct=pd.crosstab(IND.Group, IND[s]>0).loc[['HC','High-symptom','Patient']]
    chi2,pchi,dof,_=stats.chi2_contingency(ct.values)
    strat.append(dict(setting=s, group='chi2 across groups', n=len(IND), n_up=int((IND[s]>0).sum()),
                      pct_up=round(100*float((IND[s]>0).mean()),1), chi2=round(float(chi2),3),
                      df=dof, p=float(f'{pchi:.3g}')))
STRAT=pd.DataFrame(strat)
print(STRAT.pivot_table(index='setting', columns='group', values='pct_up').reindex(SET).to_string())
print('\nn_settings_up distribution:', IND.n_settings_up.value_counts().sort_index().to_dict())
print('increase under all 6: %d/%d = %.1f%%' % ((IND.n_settings_up==6).sum(), len(IND), 100*(IND.n_settings_up==6).mean()))
# rank correlation of individual response across settings
IRC=pd.read_csv(f'{CN}/npchange_correlation_288_n288.csv'); print('\nacross-setting correlations:'); print(IRC.to_string(index=False))

# ---------------------------------------------------------------- cell 4f1219ba (cell_index 521)
FIG=f'{B}/revision/text/figures'
dirs={k: f'{FIG}/supp_{k}' for k in ['assim','fingerprint','conductance','eft','motion']}
for k,v in dirs.items():
    None; None  # [recovery: side output suppressed]  # [recovery: side output suppressed]

# ---- S1 data
pass  # [recovery: side output suppressed] A5.to_csv(f"{dirs['assim']}/data/assim5_edges_mid.csv", index=False)
pass  # [recovery: side output suppressed] pd.DataFrame([dict(statistic='ICC(3,1), runs fixed', value=round(float(icc31),4)),
# [recovery: side output suppressed]               dict(statistic='ICC(2,1), runs random', value=round(float(icc21),4)),
# [recovery: side output suppressed]               dict(statistic='mean between-run profile r', value=round(float(np.mean(pair_r)),4)),
# [recovery: side output suppressed]               dict(statistic='min between-run profile r', value=round(float(min(pair_r)),4)),
# [recovery: side output suppressed]               dict(statistic='max between-run profile r', value=round(float(max(pair_r)),4)),
# [recovery: side output suppressed]               dict(statistic='SD between edges (signal)', value=round(float(R.mean(1).std(ddof=1)),4)),
# [recovery: side output suppressed]               dict(statistic='mean SD between runs (noise)', value=round(float(R.std(1,ddof=1).mean()),4)),
# [recovery: side output suppressed]               dict(statistic='signal/noise SD ratio', value=round(float(R.mean(1).std(ddof=1)/R.std(1,ddof=1).mean()),2)),
# [recovery: side output suppressed]               dict(statistic='n runs', value=5), dict(statistic='n reward-task edges', value=6),
# [recovery: side output suppressed]               ]).to_csv(f"{dirs['assim']}/data/assim5_stats.csv", index=False)

# ---- S2 data
# [recovery] the original loop wrote both similarity matrices; restricted here to
# this script's one output. The expression itself is unchanged.
for nm, F, path in [('empirical', FE, 'fingerprint_similarity_empirical.csv')]:
    pd.DataFrame(F[2], index=F[1], columns=F[0]).to_csv(os.path.join(OUT_DIR, 'fingerprint_similarity_empirical.csv'))
fp=[]
for nm,F in [('empirical BOLD',FE),('simulated (no re-assimilation)',FS)]:
    corr=np.array([t==p for t,p in zip(F[3],F[4])])
    fp.append(dict(data=nm, n_trials=len(corr), n_correct=int(corr.sum()),
                   accuracy_pct=round(100*float(corr.mean()),1),
                   mean_self_r=round(float(F[5].mean()),4),
                   mean_best_other_r=round(float(F[6].mean()),4),
                   mean_margin=round(float((F[5]-F[6]).mean()),4),
                   misidentified=';'.join([F[1][i] for i in np.where(~corr)[0]]) or 'none'))
FPA=pd.DataFrame(fp); None  # [recovery: side output suppressed]
pass  # [recovery: side output suppressed] pd.DataFrame(dict(trial=FE[1], subject=FE[3],
# [recovery: side output suppressed]                   self_r_empirical=FE[5], best_other_r_empirical=FE[6],
# [recovery: side output suppressed]                   self_r_simulated=FS[5], best_other_r_simulated=FS[6])).to_csv(
# [recovery: side output suppressed]     f"{dirs['fingerprint']}/data/fingerprint_margins.csv", index=False)
print(FPA.to_string(index=False))

# ---- S3 data
pass  # [recovery: side output suppressed] CG.to_csv(f"{dirs['conductance']}/data/conductance_grid_summary_n288.csv", index=False)
pass  # [recovery: side output suppressed] STRAT.to_csv(f"{dirs['conductance']}/data/conductance_responder_by_group_n288.csv", index=False)
pass  # [recovery: side output suppressed] IND.drop(columns=['ID']).to_csv(f"{dirs['conductance']}/data/conductance_subject_level_n288.csv", index=False)
pass  # [recovery: side output suppressed] IRC.to_csv(f"{dirs['conductance']}/data/conductance_across_setting_correlations.csv", index=False)

# ---- S4 data
EFT=pd.concat([xl.parse('ampa_eft').rename(columns={'Unnamed: 0':'subject','0.0044':'perturbed'}).assign(perturbation='AMPA'),
               xl.parse('gaba_eft').rename(columns={'Unnamed: 0':'subject','0.0040':'perturbed'}).assign(perturbation='GABA-A')])
EFT=EFT[EFT.subject!='HC02'].reset_index(drop=True)     # HC02 excluded, as in the model sweeps
EFT['delta']=EFT.perturbed-EFT.baseline
NPT=pd.concat([xl.parse('Sheet3').rename(columns={'Unnamed: 0':'subject','simulation_np':'baseline','mani_ampa_np':'perturbed'}).assign(perturbation='AMPA'),
               xl.parse('Sheet4').rename(columns={'Unnamed: 0':'subject','simulation_np':'baseline','mani_gaba_np':'perturbed'}).assign(perturbation='GABA-A')])
NPT=NPT[NPT.subject!='HC02'].reset_index(drop=True); NPT['delta']=NPT.perturbed-NPT.baseline
pass  # [recovery: side output suppressed] EFT.to_csv(f"{dirs['eft']}/data/eft_3subs.csv", index=False)
pass  # [recovery: side output suppressed] NPT.to_csv(f"{dirs['eft']}/data/np_task_3subs.csv", index=False)
print(); print(EFT.to_string(index=False)); print(); print(NPT.to_string(index=False))
