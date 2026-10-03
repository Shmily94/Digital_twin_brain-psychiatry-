"""fig3a_benchmark_reference_check.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code compares two whole-brain models (SAR and rWW) against
    empirical functional connectivity for 12 subjects across 12 task-based
    edges. For each subject and model, it loads a precomputed edge-wise
    prediction error matrix, adds it to a 268-region empirical FC matrix
    (built by indexing task fMRI .mat files per subject and condition
    using node-pair locations) to reconstruct the model's predicted FC,
    then computes two mean squared errors: one between the raw prediction
    error and zero (equivalent to squared error of the model against the
    268-region empirical values), and one between the reconstructed
    predicted FC and a separate empirical FC derived from voxel-population
    simulation data. One row of the output table corresponds to a single
    subject-model pairing (one of 12 subjects times SAR or rWW, yielding
    24 rows), giving that subject's two MSE values for the given model.

INPUT FILES
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv
    {B}/revision/model_scale_consistent/simulation_results_wide_12subs.csv
    {SC}/np_location.mat
    {SC}/{s}_{tk}_taskFC.mat
    {VX}/new10m_simulated_FC_12subs_with_empirical.mat

OUTPUT FILE
    fig3a_benchmark_reference_check.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3a_benchmark_reference_check.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 4cc62de1-2d3e-40af-ab86-d39b0ddc5b5e
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 17:39:04 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3a_benchmark_reference_check__cell_4cc62de1.py
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

import numpy as np
import pandas as pd
import scipy.io as sio

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 04ee0cc9, 1b4a7685, 1ff04fbb, 2cbadd0f, 5233e78b, 899bcd31, 9677e055, ba8e1b25)
B='/Users/yunman/Desktop/submission'
FD3=f'{B}/revision/text/figures/fig.3/fig3_data'
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
sub_ids=[str(s) for s in NEW['subject_ids']]
sw=pd.read_csv(f'{B}/revision/model_scale_consistent/simulation_results_wide_12subs.csv')
sw['sid']=sw.sub_id.astype(str).str.replace('sub-0*','',regex=True)
sw=sw.set_index('sid').loc[sub_ids]
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
sub_ids=[str(s) for s in NEW['subject_ids']]
EMPW=sw[[f'emp_edge{k}' for k in range(1,13)]].values.astype(float)
sid=[s for s in sub_ids]
SC='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/sc-fc_prediction_model'
import scipy.io as sio, h5py
SC='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/sc-fc_prediction_model'
loc=sio.loadmat(f'{SC}/np_location.mat')
L=loc['np_location'].astype(int)
ED=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/edge_definitions.csv')
FLD={'SST_stop_success':('SST','SST_stop_success'),'SST_stop_failure':('SST','SST_stop_failure'),
     'MID_feed_hit':('MID','MID_feed_hit'),'MID_antici_hit':('MID','MID_antici_hit')}
E268=np.zeros((12,12))
for si,s in enumerate(sid):
    cache={}
    for ei,r in ED.iterrows():
        tk,fld=FLD[r.condition]
        if tk not in cache: cache[tk]=sio.loadmat(f'{SC}/{s}_{tk}_taskFC.mat')
        E268[si,ei]=cache[tk][fld][L[ei,0]-1, L[ei,1]-1]
MB='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/Model_Benchmark'

# ---- computation: recovered from execution-log cell 4cc62de1
rows=[]
for bm in ['SAR','rWW']:
    e=pd.read_csv(f'{MB}/np_edges_prediction_error_matrix_'+('sar' if bm=='SAR' else 'rww')+'.csv').set_index('Subject_ID')
    e.index=[str(i) for i in e.index]; e=e.loc[sid].values; pred=e+E268
    for si,s in enumerate(sid):
        rows.append(dict(subject_id=int(s), model=bm,
                         mse_vs_268region_empirical=round(float((e[si]**2).mean()),5),
                         mse_vs_empirical_model_voxels=round(float(((pred[si]-EMPW[si])**2).mean()),5)))
B=pd.DataFrame(rows)
B.to_csv(f'{FD3}/fig3a_benchmark_reference_check.csv', index=False)
