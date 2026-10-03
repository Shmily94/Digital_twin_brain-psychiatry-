"""fig3g_100m_three_subject_verification.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code cross-checks a stored Figure 3g result by independently
    recomputing it from raw per-subject simulation files. For three named
    subjects (mapped to sweep aliases HC01, MDD, AUD) and two drug
    perturbations (ampa, gaba), it loads the perturbed SST and MID task
    condition matrices from the whole-brain 100m-scale simulation output,
    selects the repeats matching the target parameter perturbation,
    averages across those repeats, and sums the twelve edge values defined
    in the edge definitions file to get a perturbed NP sum. It also
    derives a matched 100m baseline NP sum for the same subject from the
    population profile dictionary, and pulls the previously stored delta
    value for that subject and drug from the six-model summary table for
    comparison. One row of the output table corresponds to one subject and
    drug combination, holding the recomputed perturbed sum, the recomputed
    baseline sum, the delta between them, and the originally stored del

INPUT FILES
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv
    {B}/fig.3/fig3_data/fig3g_delta_np_six_models.csv
    {B}/revision/10m_voxel_population_simulation/simulate_FC_edges.csv
    {B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv
    {FD3}/fig3e_ampa_sweep.csv
    {MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv
    {P3S}/{sub}/mid_data_mani_ampa.mat
    {P3S}/{sub}/mid_data_mani_gaba_high.mat
    {P3S}/{sub}/sst_data_mani_ampa.mat
    {P3S}/{sub}/sst_data_mani_gaba_high.mat
    {R3}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat
    {VX}/new10m_simulated_FC_12subs_with_empirical.mat

OUTPUT FILE
    fig3g_100m_three_subject_verification.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3g_100m_three_subject_verification.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : ff182339-08d3-4312-b84b-5193f4aff47f
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 19:53:42 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3g_100m_three_subject_verification__cell_ff182339.py
    candidates found   : 1

REORGANISATION APPLIED
    A header was added; the imports, the input paths and the constants the
    interactive cell inherited from earlier cells in its session were made
    explicit; exploratory prints and abandoned branches were dropped; all file
    writes were redirected to OUT_DIR.  No computation, test, covariate,
    correction or seed was changed.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Output redirection.  The reference data file lives under 04_figures/, which
# this package treats as read-only evidence.  Every file write performed below
# is therefore redirected into OUT_DIR under its own basename.  Set the
# RECOVERY_OUT_DIR environment variable to choose a different scratch folder.
# ---------------------------------------------------------------------------
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/fig_color")
OUT_DIR = os.environ.get("RECOVERY_OUT_DIR", os.path.join("/tmp", "recovery_scratch", "fig3"))
os.makedirs(OUT_DIR, exist_ok=True)


def _install_write_guard():
    import pandas as _pd

    def _redirect(p):
        if isinstance(p, (str, bytes, os.PathLike)):
            p = os.fspath(p)
            if os.path.abspath(os.path.dirname(p) or ".") != os.path.abspath(OUT_DIR):
                return os.path.join(OUT_DIR, os.path.basename(p))
        return p

    for _cls, _name in ((_pd.DataFrame, "to_csv"), (_pd.Series, "to_csv"),
                        (_pd.DataFrame, "to_excel"), (_pd.Series, "to_excel")):
        _orig = getattr(_cls, _name)

        def _w(self, path_or_buf=None, *a, __o=_orig, **k):
            return __o(self, _redirect(path_or_buf), *a, **k)
        setattr(_cls, _name, _w)
    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib.figure import Figure as _F
        _sf = _F.savefig

        def _sfw(self, fname, *a, **k):
            return _sf(self, _redirect(fname), *a, **k)
        _F.savefig = _sfw
    except Exception:
        pass
    try:
        import scipy.io as _sio
        _sm = _sio.savemat

        def _smw(fn, *a, **k):
            return _sm(_redirect(fn), *a, **k)
        _sio.savemat = _smw
    except Exception:
        pass


_install_write_guard()

import h5py
import numpy as np
import pandas as pd
import scipy.io as sio

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 1b4a7685, 1deb5307, 1ff04fbb, 247ecb86, 2cbadd0f, 39431a70, 3f599fdc, 5233e78b, 5f6051db, 6f69dd7b, 732cf081, 91bf4255, a7bf2f40, b3e94cc7, cd18697f)
B='/Users/yunman/Desktop/submission'
FD3=f'{B}/revision/text/figures/fig.3/fig3_data'
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
ED=pd.read_csv(f'{B}/revision/10m_voxel_population_simulation/simulate_FC_edges.csv')
CONDMAP={'sst_stop_success':0,'sst_stop_failure':1,'mid_antici_hit':2,'mid_feedback_hit':3}
def edges_from_mat(a):
    return np.column_stack([a[i-1,j-1,:,CONDMAP[c]] for i,j,c in zip(ED.roi_i,ED.roi_j,ED.condition)])
MAT={'10m':edges_from_mat(NEW['simu_fc_10m_100m_params']),'100m':edges_from_mat(NEW['simu_fc_100m']),
     '1b':edges_from_mat(NEW['simu_fc_1b']),'10m_own':edges_from_mat(NEW['simu_fc_10m_own_params'])}
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
sub_ids=[str(s) for s in NEW['subject_ids']]
B='/Users/yunman/Desktop/submission'
MN=f'{B}/revision/model_scale_consistent/manuscript_numbers_newflow'
R3=f'{B}/revision/model_scale_consistent/manuscript_numbers_newflow/3m_model_new_run'
m3=sio.loadmat(f'{R3}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat', squeeze_me=True)
sid=[s for s in sub_ids]
EDC=[f'edge{k}' for k in range(1,13)]
NF=pd.read_csv(f'{MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv')
NFB=NF[NF.condition=='baseline']
REG=pd.read_csv(f'{B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv')
NP3=np.asarray(m3['NP12edges'],float)
def reps_from_nf(sc):
    out=[]
    for r,sub in NFB[NFB.scale==sc].groupby('run_idx'):
        g=sub.groupby('subID')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
        if set(sid)<=set(g.index): out.append(np.array([g.loc[s].values for s in sid]))
    return np.stack(out,1)
RB2=REG[REG.condition=='baseline'].copy()
RB2['rep']=RB2.repeat.astype(str)
r268=[]
for r,sub in RB2.groupby('rep'):
    g=sub.groupby('subject')[EDC].mean(); g.index=[s.replace('sub-','').lstrip('0') for s in g.index]
    if set(sid)<=set(g.index): r268.append(np.array([g.loc[s].values for s in sid]))
REPS={'3m_268': NP3, '10m_268': np.stack(r268,1), '10m_1000': reps_from_nf('10m_reg'),
      '10m': reps_from_nf('10m'), '100m': reps_from_nf('100m'), '1b': reps_from_nf('1b')}
PROF={k: np.nanmean(v,1) for k,v in REPS.items()}
PROF['10m_own']=MAT['10m_own']
ED=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv')
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures'
g6=pd.read_csv(f'{B}/fig.3/fig3_data/fig3g_delta_np_six_models.csv')
SM='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent'
P3S=f'{SM}/orignial_3subs_perturb_100m_whole_brain_fc'
SUB3={'112288':'sub-000000112288','113174215':'sub-000113174215','182136619':'sub-000182136619'}
SUB3={'112288':'sub-000000112288','113174215':'sub-000113174215','182136619':'sub-000182136619'}
base100={s: PROF['100m'][sid.index(s)] for s in SUB3}
def labs(d,key):
    v=d[key]
    return v if isinstance(v,list) else [str(x[0]) for x in v[0]]
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
def sel_ampa(L,n):
    if n==5: return list(range(5))
    hit=[i for i,l in enumerate(L) if '-0.0044-gaba' in l or '-0.0044-0.0015' in l]
    return hit
def get3(sub,kind):
    out=np.full((5,12),np.nan)
    if kind=='ampa':
        dS,_=matload(f'{P3S}/{sub}/sst_data_mani_ampa.mat'); dM,_=matload(f'{P3S}/{sub}/mid_data_mani_ampa.mat')
        nS=dS['sst_stop_suces'].shape[2]; selS=sel_ampa(labs(dS,'sst_subject'),nS)
        selM=list(range(dM['mid_antici_hit'].shape[2]))[:5]
    else:
        dS,_=matload(f'{P3S}/{sub}/sst_data_mani_gaba_high.mat'); dM,_=matload(f'{P3S}/{sub}/mid_data_mani_gaba_high.mat')
        LS,LM=labs(dS,'sst_subject'),labs(dM,'mid_subject')
        selS=[i for i,l in enumerate(LS) if l.endswith('gaba-0.0040') or '0.0040' in l.split('-')[-1]]
        selM=[i for i,l in enumerate(LM) if l.endswith('gaba-0.0040') or '0.0040' in l.split('-')[-1]]
    FMAP={'SST_stop_success':(dS,'sst_stop_suces',selS),'SST_stop_failure':(dS,'sst_stop_failure',selS),
          'MID_feed_hit':(dM,'mid_feed_hit',selM),'MID_antici_hit':(dM,'mid_antici_hit',selM)}
    for ei,r in ED.iterrows():
        src,fld,sel=FMAP[r.condition]; A=src[fld]
        for k,idx in enumerate(sel[:5]): out[k,ei]=A[r.i_217-1,r.j_217-1,idx]
    return np.nanmean(out,0), len(selS), len(selM)
res={}
for s,folder in SUB3.items():
    for dr in ['ampa','gaba']:
        prof,nS,nM=get3(folder,dr); res[(s,dr)]=prof
        st=float(g6[(g6.model=='100m')&(g6.drug==dr)&(g6.sub_id.astype(str)==s)].delta.iloc[0])
        print(f'{s:11s}{dr:6s}{nS:<5d}{nM:<5d}{prof.sum():10.4f}{base100[s].sum():10.4f}{prof.sum()-base100[s].sum():14.4f}{st:10.4f}')
sw=pd.read_csv(f'{FD3}/fig3e_ampa_sweep.csv').set_index('subject').baseline

# ---- computation: recovered from execution-log cell ff182339
V=[]
for s in SUB3:
    for dr in ['ampa','gaba']:
        st=float(g6[(g6.model=='100m')&(g6.drug==dr)&(g6.sub_id.astype(str)==s)].delta.iloc[0])
        V.append(dict(subject_id=int(s), sweep_alias={'112288':'HC01','113174215':'MDD','182136619':'AUD'}[s],
            drug=dr, perturbed_np_sum_recomputed=round(float(res[(s,dr)].sum()),4),
            baseline_100m_newflow=round(float(base100[s].sum()),4),
            delta_recomputed=round(float(res[(s,dr)].sum()-base100[s].sum()),4),
            delta_stored_fig3g=round(st,4),
            implied_baseline_of_stored=round(float(res[(s,dr)].sum()-st),4),
            baseline_3m_sweep=round(float(sw[{'112288':'HC01','113174215':'MDD','182136619':'AUD'}[s]]),4),
            conductance='ampa 0.0044' if dr=='ampa' else 'ampa 0.0044 + gaba 0.0040',
            n_repeats=5, source=f'orignial_3subs_perturb_100m_whole_brain_fc/{SUB3[s]}'))
VV=pd.DataFrame(V)
VV.to_csv(f'{FD3}/fig3g_100m_three_subject_verification.csv', index=False)
