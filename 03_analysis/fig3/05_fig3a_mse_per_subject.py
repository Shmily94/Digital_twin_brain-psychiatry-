"""fig3a_mse_per_subject.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code selects a fixed set of columns from an existing dataframe A
    and writes them out as a CSV table, without performing any new
    computation itself, so the actual mean squared error values and their
    averaging over repeats must have been produced earlier in the
    pipeline. One row of the output represents a single subject's result
    for one model within a given family, summarizing the simulated neuron
    configuration, the hyperparameters used for assimilation, the temporal
    or spatial resolution, and how many repeated runs were averaged to
    obtain that subject's mse value. Each row also names the empirical
    reference dataset the simulation was compared against, tying that
    subject's error score to a specific ground truth source. The added
    reference_note column is not present in the selected slice from A, so
    its contents are not determined by this snippet and are not described
    here.

INPUT FILES
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/simulation_results_wide_12subs.csv
    {MN}/NP_12edges_and_factor_3m_new_run.mat
    {VXR}/simulate_FC_edges.csv
    {VX}/new10m_simulated_FC_12subs_with_empirical.mat

OUTPUT FILE
    fig3a_mse_per_subject.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3a_mse_per_subject.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    no -- a name inherited from the session could not be recovered; see the NOT RECOVERED block

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : ba4d43f8-e8fe-4c0c-baa4-d54a309c2b1a
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 09:06:59 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3a_mse_per_subject__cell_ba4d43f8.py
    candidates found   : 7

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

import numpy as np
import pandas as pd
import scipy.io as sio

# -------------------------------------------------------------------------
# NOT RECOVERED.  This script needs the name(s)
#     host
# which the interactive session inherited from a cell that is not present in
# the execution log (or, for `host`, from the platform session object).  The
# script therefore cannot run as shipped.  They are used below as:
#     mse_ps=pd.read_csv(host.artifact_path("15ac42f6-64b1-4ee2-8157-d067bc1
# Supply them before running.  Nothing has been invented in their place.
# -------------------------------------------------------------------------

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 04e0caaa, 20964bbd, 226818d6, 3e0eda7f, 534f5996, 5a581de6, 70999d82, ad178fc1, e93d4d44, fc428740, fd08edb0)
mse_ps=pd.read_csv(host.artifact_path("15ac42f6-64b1-4ee2-8157-d067bc1cf5e9"))
MODELS=['3m_268','10m_268','10m_1000','10m','100m','1b']
FAM={'3m_268':'regional','10m_268':'regional','10m_1000':'regional','10m':'voxel','100m':'voxel','1b':'voxel'}
REF={'regional':'regional','voxel':'voxel'}
rows=[]
for m_ in MODELS:
    col=f"{m_}|{REF[FAM[m_]]}"
    for sid,v in zip(mse_ps.subject_id, mse_ps[col]):
        rows.append(dict(subject_id=sid, model=m_, family=FAM[m_],
                         empirical_reference='empirical_original_3m' if FAM[m_]=='regional' else 'empirical_model_voxels',
                         mse=v))
a3=pd.DataFrame(rows)
MN='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/manuscript_numbers_newflow'
FD3='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data'
VX='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/10m_voxel_population_simulation/analysis_results'
VXR='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/10m_voxel_population_simulation'
sw=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/simulation_results_wide_12subs.csv')
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True, struct_as_record=False)
ED=pd.read_csv(f'{VXR}/simulate_FC_edges.csv')
CONDMAP={'sst_stop_success':0,'sst_stop_failure':1,'mid_antici_hit':2,'mid_feedback_hit':3}
sub_ids=[str(s) for s in NEW['subject_ids']]
def edges_from_mat(arr):
    """arr: 217x217x12x4 -> (12 subjects, 12 edges)"""
    out=np.empty((len(sub_ids), len(ED)))
    for e,(i,j,cond) in enumerate(zip(ED.roi_i, ED.roi_j, ED.condition)):
        out[:, e]=arr[i-1, j-1, :, CONDMAP[cond]]
    return out
EMP_V=edges_from_mat(NEW['real_fc_dtb_voxels'])
CONDMAP={'sst_stop_success':0,'sst_stop_failure':1,'mid_antici_hit':2,'mid_feedback_hit':3}
sub_ids=[str(s) for s in NEW['subject_ids']]
def edges_from_mat(arr):
    """arr: 217x217x12x4 -> (12 subjects, 12 edges)"""
    out=np.empty((len(sub_ids), len(ED)))
    for e,(i,j,cond) in enumerate(zip(ED.roi_i, ED.roi_j, ED.condition)):
        out[:, e]=arr[i-1, j-1, :, CONDMAP[cond]]
    return out
SIM={k: edges_from_mat(NEW[f'simu_fc_{k}']) for k in
     ['10m_own_params','10m_100m_params','100m','1b']}
mse=lambda s,e: ((s-e)**2).mean(1)
sub_ids=[str(s) for s in NEW['subject_ids']]
m3=sio.loadmat(f'{MN}/NP_12edges_and_factor_3m_new_run.mat', squeeze_me=True)
subs3=[str(s) for s in m3['subjects']]
m3=sio.loadmat(f'{MN}/NP_12edges_and_factor_3m_new_run.mat', squeeze_me=True)
NEW3M=np.asarray(m3['NP12edges'], float)
emp_map={r.sid: r[[f'emp_edge{k}' for k in range(1,13)]].values.astype(float) for _,r in sw.iterrows()}
sid3=[s.replace('sub-','').lstrip('0') for s in subs3]
EMP_R=np.array([emp_map[s] for s in sid3])
new3m_mean=np.nanmean(NEW3M, axis=1)
sid3=[s.replace('sub-','').lstrip('0') for s in subs3]

# ---- computation: recovered from execution-log cell ba4d43f8
rows=[]
HYP={'3m_268':'3 M','10m_268':'3 M','10m_1000':'10 M / 1000','10m_own':'10 M voxel',
     '10m':'100 M','100m':'100 M','1b':'100 M','SAR':'—','RWW':'—'}
SIMN={'3m_268':'3 M','10m_268':'10 M','10m_1000':'10 M','10m_own':'10 M','10m':'10 M',
      '100m':'100 M','1b':'1 B','SAR':'—','RWW':'—'}
RES={'3m_268':'268 regions','10m_268':'268 regions','10m_1000':'1000 regions',
     '10m_own':'voxel','10m':'voxel','100m':'voxel','1b':'voxel','SAR':'—','RWW':'—'}
FAMILY={'3m_268':'regional','10m_268':'regional','10m_1000':'regional',
        '10m_own':'voxel','10m':'voxel','100m':'voxel','1b':'voxel',
        'SAR':'benchmark','RWW':'benchmark'}
for mdl in ['10m_268','10m_1000','10m','100m','1b','SAR','RWW']:
    for _,r in a3[a3.model==mdl].iterrows():
        rows.append(dict(subject_id=r.subject_id, model=mdl, mse=r.mse,
                         empirical_reference=r.empirical_reference))
for s,v in zip(sid3, mse(new3m_mean, EMP_R)):
    rows.append(dict(subject_id=int(s), model='3m_268', mse=round(float(v),5),
                     empirical_reference='emp_edge1-12 (simulation_results_wide_12subs.csv)'))
for s,v in zip(sub_ids, mse(SIM['10m_own_params'], EMP_V)):
    rows.append(dict(subject_id=int(s), model='10m_own', mse=round(float(v),5),
                     empirical_reference='real_fc_dtb_voxels (mask-matched)'))
A=pd.DataFrame(rows)
A['family']=A.model.map(FAMILY)
A['sim_neurons']=A.model.map(SIMN)
A['assimilation_hyperparams']=A.model.map(HYP)
A['resolution']=A.model.map(RES)
A=A[['subject_id','model','family','sim_neurons','assimilation_hyperparams','resolution',
     'empirical_reference','mse']]
A.to_csv(f'{FD3}/fig3a_mse_per_subject.csv', index=False)
