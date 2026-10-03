"""Collect the simulated functional connectivity that Figure 3 actually uses
for the twelve cross-scale participants, in one place.

Three states are collected for each of the seven DTB builds:
  baseline   - unperturbed simulation
  ampa       - AMPA conductance increased
  gaba       - GABA-A conductance increased (applied on top of the AMPA step)

Two kinds of quantity are written:
  (1) the twelve NP-factor edges, per participant, per repeat where repeats
      exist, and the repeat-averaged profile used in the figure;
  (2) whole-brain FC similarity (Pearson r between simulated and empirical
      connectomes over the 217-node / 23,436-edge upper triangle), per
      participant, per task condition, baseline only - no perturbed whole-brain
      matrices exist for most builds.

The source file for every build x state is recorded in source_manifest.csv.
This script does not invent or interpolate any value: where a build has no data
for a state, the cell is left empty and the manifest says so.

Run from the fig.3 directory:  python collect_12subs_fc.py
"""
import os
import numpy as np
import pandas as pd
import scipy.io as sio
import h5py

B = '/Users/yunman/Desktop/submission'
SM = f'{B}/revision/model_scale_consistent'
MN = f'{SM}/manuscript_numbers_newflow'
NR = f'{MN}/3m_model_new_run'
VXR = f'{B}/revision/10m_voxel_population_simulation'
VX = f'{VXR}/analysis_results'
OUT = f'{B}/revision/text/figures/fig.3/fig3_simulated_fc_12subs'
os.makedirs(OUT, exist_ok=True)

EDC = [f'edge{k}' for k in range(1, 13)]
ORDER = ['3m_268', '10m_268', '10m_1000', '10m_own', '10m', '100m', '1b']
BLAB = {'3m_268': '3 M neurons / 268 regions / 3 M-268 hyper-parameters',
        '10m_268': '10 M neurons / 268 regions / 3 M-268 hyper-parameters',
        '10m_1000': '10 M neurons / 1000 regions / 10 M-1000 hyper-parameters',
        '10m_own': '10 M neurons / voxel-wise / 10 M-voxel hyper-parameters',
        '10m': '10 M neurons / voxel-wise / 100 M-voxel hyper-parameters',
        '100m': '100 M neurons / voxel-wise / 100 M-voxel hyper-parameters',
        '1b': '1 B neurons / voxel-wise / 100 M-voxel hyper-parameters'}
CONDMAP = {'sst_stop_success': 0, 'sst_stop_failure': 1,
           'mid_antici_hit': 2, 'mid_feedback_hit': 3}
MAN = []


def matload_v73(path):
    """Read a MATLAB file written in either v7 or v7.3 (HDF5) format."""
    try:
        return {k: v for k, v in sio.loadmat(path, squeeze_me=True).items()
                if not k.startswith('__')}
    except NotImplementedError:
        out = {}
        with h5py.File(path, 'r') as fh:
            for k in fh.keys():
                if k.startswith('#'):
                    continue
                a = np.asarray(fh[k][()])
                # HDF5 stores MATLAB arrays with reversed dimension order
                out[k] = a.T if a.ndim > 1 else a
        return out


def note(build, state, quantity, src, repeats, detail=''):
    MAN.append(dict(build=build, build_description=BLAB.get(build, build),
                    state=state, quantity=quantity, n_repeats=repeats,
                    source_file=src, detail=detail))


# ---------------------------------------------------------------- 12 subjects
NEW = sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat',
                  squeeze_me=True)
sid = [str(s) for s in NEW['subject_ids']]
ED = pd.read_csv(f'{VXR}/simulate_FC_edges.csv')


def edges_from_mat(a):
    return np.column_stack([a[i - 1, j - 1, :, CONDMAP[c]]
                            for i, j, c in zip(ED.roi_i, ED.roi_j, ED.condition)])


# ------------------------------------------------------- baseline, per repeat
NF = pd.read_csv(f'{MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv')
NFB = NF[NF.condition == 'baseline']


def reps_from_nf(scale_key):
    out = []
    for _, sub in NFB[NFB.scale == scale_key].groupby('run_idx'):
        g = sub.groupby('subID')[EDC].mean()
        g.index = [s.replace('sub-', '').lstrip('0') for s in g.index]
        if set(sid) <= set(g.index):
            out.append(np.array([g.loc[s].values for s in sid]))
    return np.stack(out, 1)                                  # subj x rep x edge


REG = pd.read_csv(f'{SM}/NP_12edges_10m_1000_10m_268_regional_modu.csv')
RB = REG[REG.condition == 'baseline'].copy()
assert set(RB.model) == {'regional'}, 'baseline rows are expected to be 10M/268 only'
r268 = []
for _, sub in RB.groupby(RB.repeat.astype(str)):
    g = sub.groupby('subject')[EDC].mean()
    g.index = [s.replace('sub-', '').lstrip('0') for s in g.index]
    if set(sid) <= set(g.index):
        r268.append(np.array([g.loc[s].values for s in sid]))

NP3_reps = np.asarray(
    matload_v73(f'{NR}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat')
    ['NP12edges'], float)                                      # 12 x 5 x 12

REPS = {'3m_268': NP3_reps,
        '10m_268': np.stack(r268, 1),
        '10m_1000': reps_from_nf('10m_reg'),
        '10m': reps_from_nf('10m'),
        '100m': reps_from_nf('100m'),
        '1b': reps_from_nf('1b')}
note('3m_268', 'baseline', 'NP 12 edges', 'manuscript_numbers_newflow/NP_12edges_and_factor_3m_new_run.mat', 5,
     'corrected 3 M run; task FC computed with the same pipeline as the other builds')
note('10m_268', 'baseline', 'NP 12 edges', 'model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv', 5,
     'model = regional, condition = baseline')
for k, sc in [('10m_1000', '10m_reg'), ('10m', '10m'), ('100m', '100m'), ('1b', '1b')]:
    note(k, 'baseline', 'NP 12 edges',
         f'manuscript_numbers_newflow/NP_12edges_all_subjects_scales_conditions_newflow.csv (scale = {sc})',
         REPS[k].shape[1], '')

BASE = {k: np.nanmean(v, 1) for k, v in REPS.items()}
BASE['10m_own'] = edges_from_mat(NEW['simu_fc_10m_own_params'])
note('10m_own', 'baseline', 'NP 12 edges',
     '10m_voxel_population_simulation/analysis_results/new10m_simulated_FC_12subs_with_empirical.mat '
     '(simu_fc_10m_own_params)', 1, 'single run - no repeats available')

EMP = edges_from_mat(NEW['real_fc_dtb_voxels'])
note('empirical', 'reference B', 'NP 12 edges',
     '10m_voxel_population_simulation/analysis_results/new10m_simulated_FC_12subs_with_empirical.mat '
     '(real_fc_dtb_voxels)', 1,
     '268-parcel empirical FC recomputed from only the voxels the DTB simulates')

# ------------------------------------------------------------- perturbations
m3p = matload_v73(f'{NR}/Mani_simulated_3m_NP_12edges_and_factor.mat')
cn3 = [str(x).strip("[]' ") for x in np.asarray(m3p['condition_names']).ravel()]
NPe = np.asarray(m3p['NP12edges'], float)                 # subj x cond x rep x edge
# The file carries a third condition named manipu_gaba_baseline.  Despite the
# name it is not a baseline: it is GABA-A raised starting FROM baseline, i.e.
# without the preceding AMPA step.  The manuscript does not use that protocol -
# its GABA-A state is always AMPA-raised-then-GABA-raised (manipu_gaba).  The
# GABA-from-baseline condition is therefore excluded here, and both perturbation
# states are referenced to the plain baseline run.
M3STATE = {'ampa': 'manipu', 'gaba': 'manipu_gaba'}
PERT = {('3m_268', s): np.nanmean(NPe[:, cn3.index(c), :, :], 1)
        for s, c in M3STATE.items()}
for s, c in M3STATE.items():
    note('3m_268', s, 'NP 12 edges',
         'manuscript_numbers_newflow/3m_model_new_run/Mani_simulated_3m_NP_12edges_and_factor.mat',
         NPe.shape[2], f'condition_names entry "{c}"; referenced to the plain baseline run')
note('3m_268', 'EXCLUDED', 'NP 12 edges + whole-brain FC',
     'manuscript_numbers_newflow/3m_model_new_run/Mani_simulated_3m_NP_12edges_and_factor.mat '
     'and sub-*_mani_task_FC.mat', NPe.shape[2],
     'condition_names entry "manipu_gaba_baseline" = GABA-A raised from baseline, without the '
     'preceding AMPA step. The manuscript never uses this protocol, so it is not written to any '
     'file here. It is NOT the baseline and must not be used as the perturbation reference.')


def reg_edges(model, cond):
    sub = REG[(REG.model == model) & (REG.condition == cond)].copy()
    sub['s'] = sub.subject.str.replace('sub-', '', regex=False).str.lstrip('0')
    return sub.groupby('s')[EDC].mean().reindex(sid).values


for build, model in [('10m_268', 'regional'), ('10m_1000', 'coarse')]:
    PERT[(build, 'ampa')] = reg_edges(model, 'ampa_r')
    PERT[(build, 'gaba')] = reg_edges(model, 'ampa_gaba_r')
    for s, cond in [('ampa', 'ampa_r'), ('gaba', 'ampa_gaba_r')]:
        note(build, s, 'NP 12 edges',
             'model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv',
             1, f'model = {model}, condition = {cond}')

sw = pd.read_csv(f'{SM}/simulation_results_wide_12subs.csv')
sw['s'] = sw.sub_id.astype(str).str.replace('sub-', '', regex=False).str.lstrip('0')
W2 = sw.set_index('s').reindex(sid)
for m_ in ('10m', '1b'):
    for s in ('ampa', 'gaba'):
        PERT[(m_, s)] = W2[[f'{m_}_{s}_edge{i}' for i in range(1, 13)]].values.astype(float)
        note(m_, s, 'NP 12 edges', 'model_scale_consistent/simulation_results_wide_12subs.csv',
             1, f'columns {m_}_{s}_edge1..12')


def matload(p):
    try:
        d = sio.loadmat(p)
        return {k: v for k, v in d.items() if not k.startswith('__')}
    except NotImplementedError:
        f2 = h5py.File(p, 'r')
        out = {}
        for k in f2.keys():
            if k.startswith('#'):
                continue
            a = f2[k]
            if k.endswith('_subject'):
                out[k] = [''.join(chr(c) for c in np.array(f2[r]).ravel())
                          for r in np.array(a).ravel()]
            else:
                out[k] = np.array(a).transpose(2, 1, 0) if a.ndim == 3 else np.array(a)
        return out


P3S = f'{SM}/orignial_3subs_perturb_100m_whole_brain_fc'
SUB3 = {'112288': 'sub-000000112288', '113174215': 'sub-000113174215',
        '182136619': 'sub-000182136619'}
ED2 = pd.read_csv(f'{SM}/edge_definitions.csv')


def labs(d, key):
    v = d[key]
    return v if isinstance(v, list) else [str(x[0]) for x in v[0]]


def get3(folder, kind):
    out = np.full((5, 12), np.nan)
    if kind == 'ampa':
        dS = matload(f'{P3S}/{folder}/sst_data_mani_ampa.mat')
        dM = matload(f'{P3S}/{folder}/mid_data_mani_ampa.mat')
        nS = dS['sst_stop_suces'].shape[2]
        selS = (list(range(5)) if nS == 5 else
                [i for i, l in enumerate(labs(dS, 'sst_subject'))
                 if '-0.0044-gaba' in l or '-0.0044-0.0015' in l])
        selM = list(range(dM['mid_antici_hit'].shape[2]))[:5]
    else:
        dS = matload(f'{P3S}/{folder}/sst_data_mani_gaba_high.mat')
        dM = matload(f'{P3S}/{folder}/mid_data_mani_gaba_high.mat')
        selS = [i for i, l in enumerate(labs(dS, 'sst_subject'))
                if l.endswith('gaba-0.0040') or '0.0040' in l.split('-')[-1]]
        selM = [i for i, l in enumerate(labs(dM, 'mid_subject'))
                if l.endswith('gaba-0.0040') or '0.0040' in l.split('-')[-1]]
    FMAP = {'SST_stop_success': (dS, 'sst_stop_suces', selS),
            'SST_stop_failure': (dS, 'sst_stop_failure', selS),
            'MID_feed_hit': (dM, 'mid_feed_hit', selM),
            'MID_antici_hit': (dM, 'mid_antici_hit', selM)}
    for ei, r in ED2.iterrows():
        src, fld, sel = FMAP[r.condition]
        A = src[fld]
        for k, idx in enumerate(sel[:5]):
            out[k, ei] = A[r.i_217 - 1, r.j_217 - 1, idx]
    return np.nanmean(out, 0)


for s in ('ampa', 'gaba'):
    rows = []
    for sub in sid:
        if sub in SUB3:
            rows.append(get3(SUB3[sub], s))
        else:
            rows.append(W2[[f'100m_{s}_edge{i}' for i in range(1, 13)]].loc[sub].values.astype(float))
    PERT[('100m', s)] = np.vstack(rows)
    note('100m', s, 'NP 12 edges',
         'model_scale_consistent/simulation_results_wide_12subs.csv (9 participants) + '
         'model_scale_consistent/orignial_3subs_perturb_100m_whole_brain_fc/ (112288, 113174215, 182136619)',
         5, 'AMPA step 0.0044; GABA-A step 0.0040 applied on top of AMPA 0.0044')

xo = pd.ExcelFile(f'{VXR}/np_edges_simulated_baseline_mani.xlsx').parse('simulate_np')
xo['s'] = xo.id.astype(str).str.strip("'").str.lstrip('0')
xs = xo.set_index('s').reindex(sid)
PERT[('10m_own', 'ampa')] = xs[[f'mani_ampa_edge{i}' for i in range(1, 13)]].values.astype(float)
PERT[('10m_own', 'gaba')] = xs[[f'mani_ampa_gaba_edge{i}' for i in range(1, 13)]].values.astype(float)
for s in ('ampa', 'gaba'):
    note('10m_own', s, 'NP 12 edges',
         '10m_voxel_population_simulation/np_edges_simulated_baseline_mani.xlsx (sheet simulate_np)',
         1, 'single run')

# ------------------------------------------------------------------- writing
edge_def = pd.read_csv(f'{SM}/edge_definitions.csv')
long_rows = []
for b in ORDER:
    states = [('baseline', BASE[b]), ('ampa', PERT[(b, 'ampa')]),
              ('gaba', PERT[(b, 'gaba')])]
    for state, M in states:
        for i, s in enumerate(sid):
            r = dict(build=b, build_description=BLAB[b], state=state, subject_id=s)
            r.update({f'edge{k + 1}': M[i, k] for k in range(12)})
            r['np_sum'] = np.nansum(M[i])
            r['n_edges_present'] = int(np.isfinite(M[i]).sum())
            long_rows.append(r)
for i, s in enumerate(sid):
    r = dict(build='empirical', build_description='empirical reference B',
             state='empirical', subject_id=s)
    r.update({f'edge{k + 1}': EMP[i, k] for k in range(12)})
    r['np_sum'] = np.nansum(EMP[i])
    r['n_edges_present'] = int(np.isfinite(EMP[i]).sum())
    long_rows.append(r)
NP = pd.DataFrame(long_rows)
NP.to_csv(f'{OUT}/np12_edges_12subs_by_build_and_state.csv', index=False)

rep_rows = []
for b, A in REPS.items():
    for i, s in enumerate(sid):
        for rp in range(A.shape[1]):
            r = dict(build=b, state='baseline', subject_id=s, repeat=rp + 1)
            r.update({f'edge{k + 1}': A[i, rp, k] for k in range(12)})
            r['np_sum'] = np.nansum(A[i, rp])
            rep_rows.append(r)
for i, s in enumerate(sid):
    for rp in range(NPe.shape[2]):
        for st, cname in M3STATE.items():
            ci = cn3.index(cname)
            r = dict(build='3m_268', state=st, subject_id=s, repeat=rp + 1)
            r.update({f'edge{k + 1}': NPe[i, ci, rp, k] for k in range(12)})
            r['np_sum'] = np.nansum(NPe[i, ci, rp])
            rep_rows.append(r)
pd.DataFrame(rep_rows).to_csv(f'{OUT}/np12_edges_12subs_per_repeat.csv', index=False)

edge_def.to_csv(f'{OUT}/np12_edge_definitions.csv', index=False)

# ===================================================== whole-brain FC section
# Similarity is Pearson r between the simulated and the empirical connectome
# over the upper triangle of the 217-node axis (23,436 edges), one value per
# participant per task condition.  The empirical reference is B for all DTB
# builds; SAR and rWW are scored on native Shen-268 regional FC because they
# are not defined at voxel resolution.
CS = f'{SM}/add_new_subjects/empirical_fc_voxel_used_model/simu_real_FC_across_scales_12subs.mat'
MT = matload_v73(CS)


scale_names = [str(x).strip("[]' ") for x in np.asarray(MT['scale_names']).ravel()]
cond_names = [str(x).strip("[]' ") for x in np.asarray(MT['condition_names']).ravel()]
subj_mat = [str(x).strip("[]' ") for x in np.asarray(MT['subject_ids']).ravel()]
FCB = np.asarray(MT['fc_corr_dtb_voxels'], float)            # subj x cond x scale
REAL = np.asarray(MT['real_fc_dtb_voxels'], float)           # 217 x 217 x subj x cond
roi = [int(v) for v in np.asarray(MT['roi_labels']).ravel()]

CORD = ['SST_stop_success', 'SST_stop_failure', 'MID_antici_hit', 'MID_feed_hit']
CPRETTY = {'SST_stop_success': 'SST Stop Success', 'SST_stop_failure': 'SST Stop Failure',
           'MID_antici_hit': 'MID Reward Antici.', 'MID_feed_hit': 'MID Pos. Feedback'}
SCMAP = {'3m_268': '3m_268', '10m_268': '10m_268', '10m_1000': '10m_1000',
         '10m': '10m_voxel', '100m': '100m_voxel', '1b': '1b_voxel'}
IU = np.triu_indices(len(roi), 1)


def simfit(simmat, sj, cj):
    a = simmat[:, :, sj, cj][IU] if simmat.ndim == 4 else simmat[:, :, sj][IU]
    b = REAL[:, :, sj, cj][IU]
    m = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(a[m], b[m])[0, 1])


# 3 M/268 whole-brain FC from the corrected run, recomputed here rather than
# taken from the mat file, whose 3m_268 slice is the superseded run.
with h5py.File(f'{NR}/Baseline_simulated_3m_task_FC.mat', 'r') as h3:
    st3 = np.asarray(h3['state_names'])
    sn3 = [[''.join(chr(c) for c in np.asarray(h3[st3[i, j]][()]).ravel())
            for j in range(st3.shape[1])] for i in range(st3.shape[0])]
    TFC = np.asarray(h3['task_fc_Z'])
    ids3 = [''.join(chr(c) for c in np.asarray(h3[h3['subject_ids'][0, j]][()]).ravel())
            for j in range(h3['subject_ids'].shape[1])]
    assert [i.replace('sub-', '').lstrip('0') for i in ids3] == subj_mat, \
        'new-run subject order must match the cross-scale file'
    # MID anticipation averages states 1,3,5; MID feedback states 2,4,6 (task 0);
    # SST success is state 2 and SST failure state 3 on task 1.
    STSEL = {'MID_antici_hit': (0, [1, 3, 5]), 'MID_feed_hit': (0, [2, 4, 6]),
             'SST_stop_success': (1, [2]), 'SST_stop_failure': (1, [3])}
    new3_wb = {}
    for c in CORD:
        tj, states = STSEL[c]
        for sj in range(12):
            acc = []
            for rp in range(TFC.shape[2]):
                mats = [np.asarray(h3[TFC[si, tj, rp, sj]][()]) for si in states]
                acc.append(np.nanmean(np.stack(mats), 0))
            new3_wb[(c, sj)] = np.nanmean(np.stack(acc), 0)

wb_rows = []
for sj, s in enumerate(subj_mat):
    for cj_out, c in enumerate(CORD):
        cj = cond_names.index(c)
        a = new3_wb[(c, sj)][IU]
        b = REAL[:, :, sj, cj][IU]
        m = np.isfinite(a) & np.isfinite(b)
        wb_rows.append(dict(model='3m_268', subject_id=s, condition=CPRETTY[c],
                            r=float(np.corrcoef(a[m], b[m])[0, 1]),
                            empirical_reference='B', n_edges=int(m.sum())))
        for build, key in SCMAP.items():
            if build == '3m_268':
                continue
            wb_rows.append(dict(model=build, subject_id=s, condition=CPRETTY[c],
                                r=float(FCB[sj, cj, scale_names.index(key)]),
                                empirical_reference='B', n_edges=len(IU[0])))
        wb_rows.append(dict(model='10m_own', subject_id=s, condition=CPRETTY[c],
                            r=simfit(NEW['simu_fc_10m_own_params'], sj, cj_out),
                            empirical_reference='B', n_edges=len(IU[0])))

MB = f'{B}/revision/benchmark_predict_baseline_np/Model_Benchmark'
for nm, fn in [('SAR', 'subject_level_sar_fitting_results.csv'),
               ('rWW', 'subject_level_rww_fitting_results.csv')]:
    bm = pd.read_csv(f'{MB}/{fn}')
    ccol = [c for c in bm.columns if 'cond' in c.lower()][0]
    rcol = [c for c in bm.columns if c.lower() in ('fc_pearson_r', 'r', 'pearson_r')][0]
    scol = [c for c in bm.columns if 'sub' in c.lower()][0]
    for _, rw in bm.iterrows():
        wb_rows.append(dict(model=nm,
                            subject_id=str(rw[scol]).replace('sub-', '').lstrip('0'),
                            condition=CPRETTY.get(str(rw[ccol]), str(rw[ccol])),
                            r=float(rw[rcol]),
                            empirical_reference='native Shen-268 regional FC',
                            n_edges=np.nan))
WB = pd.DataFrame(wb_rows)
WB.to_csv(f'{OUT}/wholebrain_fc_similarity_12subs.csv', index=False)
note('3m_268', 'baseline', 'whole-brain FC matrices + similarity',
     'manuscript_numbers_newflow/3m_model_new_run/Baseline_simulated_3m_task_FC.mat', 5,
     'recomputed here; the 3m_268 slice of simu_real_FC_across_scales_12subs.mat is the superseded run')
for b in ['10m_268', '10m_1000', '10m', '100m', '1b']:
    note(b, 'baseline', 'whole-brain FC similarity',
         'model_scale_consistent/add_new_subjects/empirical_fc_voxel_used_model/'
         'simu_real_FC_across_scales_12subs.mat (fc_corr_dtb_voxels)', np.nan,
         f'scale_names entry "{SCMAP[b]}"; similarity only, no simulated matrices in this file')
note('10m_own', 'baseline', 'whole-brain FC matrices + similarity',
     '10m_voxel_population_simulation/analysis_results/new10m_simulated_FC_12subs_with_empirical.mat', 1, '')
note('SAR / rWW', 'baseline', 'whole-brain FC similarity',
     'benchmark_predict_baseline_np/Model_Benchmark/subject_level_{sar,rww}_fitting_results.csv',
     np.nan, 'native Shen-268 regional FC; coupling parameter grid-searched on this same metric')

# ------------------------------------ whole-brain matrices, repeat-averaged
ARR = {'empirical_reference_B': REAL.astype(np.float32)}
for c in CORD:
    ARR[f'3m_268_baseline__{c}'] = np.stack(
        [new3_wb[(c, sj)] for sj in range(12)], -1).astype(np.float32)
for key, nm in [('simu_fc_10m_own_params', '10m_own'), ('simu_fc_10m_100m_params', '10m'),
                ('simu_fc_100m', '100m'), ('simu_fc_1b', '1b')]:
    if key in NEW:
        ARR[f'{nm}_baseline'] = np.asarray(NEW[key], np.float32)

# 3 M perturbed whole-brain matrices, one file per participant
for sj, s in enumerate(subj_mat):
    p = f'{NR}/sub-{int(s):012d}_mani_task_FC.mat'
    if not os.path.exists(p):
        continue
    with h5py.File(p, 'r') as hp:
        T = np.asarray(hp['task_fc_Z'])
        cnames = [''.join(chr(c) for c in np.asarray(hp[r][()]).ravel())
                  for r in np.asarray(hp['condition_names']).ravel()]
        for ci, cname in enumerate(cnames):
            if cname == 'manipu_gaba_baseline':
                continue          # unused perturbation setting, see note above
            for c in CORD:
                tj, states = STSEL[c]
                acc = []
                for rp in range(T.shape[2]):
                    # some state x repeat cells are empty placeholders, not matrices
                    mats = [a for a in (np.asarray(hp[T[si, tj, rp, ci]][()])
                                        for si in states)
                            if a.shape == (len(roi), len(roi))]
                    if mats:
                        acc.append(np.nanmean(np.stack(mats), 0))
                ARR.setdefault(f'3m_268_{cname}__{c}', np.full((len(roi), len(roi), 12),
                                                               np.nan, np.float32))
                if acc:
                    ARR[f'3m_268_{cname}__{c}'][:, :, sj] = np.nanmean(np.stack(acc), 0)
    note('3m_268', 'ampa / gaba / gaba_reference', 'whole-brain FC matrices',
         f'manuscript_numbers_newflow/3m_model_new_run/sub-*_mani_task_FC.mat', T.shape[2],
         'per-participant files; repeat-averaged here') if sj == 0 else None

ARR['roi_labels_217'] = np.asarray(roi, np.int32)
ARR['subject_ids'] = np.asarray(subj_mat)
ARR['conditions'] = np.asarray(CORD)
np.savez_compressed(f'{OUT}/wholebrain_fc_matrices_12subs.npz', **ARR)

pd.DataFrame(MAN).to_csv(f'{OUT}/source_manifest.csv', index=False)
print('subjects:', len(sid), '| NP rows:', len(NP), '| repeat rows:', len(rep_rows),
      '| whole-brain rows:', len(WB), '| npz arrays:', len(ARR))
