"""fig3d_run_to_run_sd_per_subject.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code computes, for each simulation model/scale (3m_268, 10m_268,
    10m_1000, 10m, 100m, 1b), the run-to-run variability of a summed
    12-edge network property (NP) across repeated simulation runs,
    separately for each of 12 subjects. For each model and subject it sums
    the 12 edge values within every repeat run, then takes the standard
    deviation of that summed value across all repeats for that subject,
    yielding one variability estimate per subject per model. The 10m_own
    row is a placeholder with no computed value, included only to preserve
    that model label in the table with np_sd set to missing. One row of
    the output therefore represents a single model-subject pair, giving
    the standard deviation of the summed-edge NP across repeat runs for
    that subject under that model, along with how many repeats contributed
    to the estimate.

INPUT FILES
    {B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv
    {MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv
    {R3}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat
    {VX}/new10m_simulated_FC_12subs_with_empirical.mat

OUTPUT FILE
    fig3d_run_to_run_sd_per_subject.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3d_run_to_run_sd_per_subject.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 2ce942b4-8c5c-419c-a7f3-20d6e843b2ae
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 17:19:32 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3d_run_to_run_sd_per_subject__cell_2ce942b4.py
    candidates found   : 2

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
#      (cells 1b4a7685, 1deb5307, 2cbadd0f, 39431a70, 5233e78b, 6f69dd7b, b74f5fe0)
B='/Users/yunman/Desktop/submission'
FD3=f'{B}/revision/text/figures/fig.3/fig3_data'
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
sub_ids=[str(s) for s in NEW['subject_ids']]
B='/Users/yunman/Desktop/submission'
MN=f'{B}/revision/model_scale_consistent/manuscript_numbers_newflow'
B='/Users/yunman/Desktop/submission'
R3=f'{B}/revision/model_scale_consistent/manuscript_numbers_newflow/3m_model_new_run'
m3=sio.loadmat(f'{R3}/Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat', squeeze_me=True)
sid=[s for s in sub_ids]
EDC=[f'edge{k}' for k in range(1,13)]
NF=pd.read_csv(f'{MN}/NP_12edges_all_subjects_scales_conditions_newflow.csv')
NFB=NF[NF.condition=='baseline']
REG=pd.read_csv(f'{B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv')
NP3=np.asarray(m3['NP12edges'],float)
ORDER=['3m_268','10m_268','10m_1000','10m_own','10m','100m','1b']
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
drows=[]
for k in ORDER:
    if k=='10m_own':
        drows.append(dict(model=k, subject_id=np.nan, np_sd=np.nan, n_repeats=1)); continue
    npsum=REPS[k].sum(2)                                   # subj x rep
    for s,v in zip(sid, np.nanstd(npsum,axis=1,ddof=1)):
        drows.append(dict(model=k, subject_id=int(s), np_sd=round(float(v),5),
                          n_repeats=REPS[k].shape[1]))
D4=pd.DataFrame(drows)

# ---- computation: recovered from execution-log cell 2ce942b4
D4.to_csv(f'{FD3}/fig3d_run_to_run_sd_per_subject.csv', index=False)
