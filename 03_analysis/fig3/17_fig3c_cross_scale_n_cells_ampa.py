"""fig3c_cross_scale_n_cells_ampa.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code calls a function sp_mat with the argument 'ampa', which
    returns two objects, and takes the second one, NA, as the table to
    save. NA is written directly to CSV as
    fig3c_cross_scale_n_cells_ampa.csv, so the file is simply that
    returned dataframe with no further transformation in this snippet.
    Based on the output columns, NA appears to hold a count of cells
    (n_cells) associated with AMPA-related synapses or recordings,
    organized across a set of network or model scales (for example labels
    like 3m, 10m, 100m, 1b) and some variant conditions at a given scale.
    One row of the output table therefore corresponds to a single
    comparison or condition (indexed by the unlabeled first column) with
    its associated cell counts reported across each of the scale or
    variant columns.

INPUT FILES
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/10m_voxel_population_simulation/np_edges_simulated_baseline_mani.xlsx
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/simulation_results_wide_12subs.csv
    {B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv
    {R3}/Mani_simulated_3m_NP_12edges_and_factor.mat
    {VX}/new10m_simulated_FC_12subs_with_empirical.mat

OUTPUT FILE
    fig3c_cross_scale_n_cells_ampa.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3c_cross_scale_n_cells_ampa.csv

STATISTICAL TESTS
    Spearman rank correlation

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 8ce04524-f306-482a-81ab-a1176ee284c3
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 20:01:32 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3c_cross_scale_n_cells_ampa__cell_8ce04524.py
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

from scipy import stats
import numpy as np
import pandas as pd
import scipy.io as sio

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 073815a6, 0a963d24, 0f1e9b07, 2a21c367, 2cbadd0f, 4e7ec040, 5233e78b, 694432fe, 6f69dd7b, a6def2c4, c20074f5)
B='/Users/yunman/Desktop/submission'
FD3=f'{B}/revision/text/figures/fig.3/fig3_data'
B='/Users/yunman/Desktop/submission'
import scipy.io as sio, pandas as pd, numpy as np, os
B='/Users/yunman/Desktop/submission'
VX=f'{B}/revision/10m_voxel_population_simulation/analysis_results'
NEW=sio.loadmat(f'{VX}/new10m_simulated_FC_12subs_with_empirical.mat', squeeze_me=True)
sub_ids=[str(s) for s in NEW['subject_ids']]
EDC=[f'edge{k}' for k in range(1,13)]
REG=pd.read_csv(f'{B}/revision/model_scale_consistent/NP_12edges_10m_1000_10m_268_regional_modu.csv')
sid=[s for s in sub_ids]
ORDER=['3m_268','10m_268','10m_1000','10m_own','10m','100m','1b']
NF='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/manuscript_numbers_newflow'
R3=f'{NF}/3m_model_new_run'
m3=sio.loadmat(f'{R3}/Mani_simulated_3m_NP_12edges_and_factor.mat')
XP='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/10m_voxel_population_simulation/np_edges_simulated_baseline_mani.xlsx'
xo=pd.ExcelFile(XP)
cn=[str(x[0]) for x in m3['condition_names'][0]]
sp=xo.parse('simulate_np')
sp['sid']=sp.id.astype(str)
NPe=m3['NP12edges']
ss=sp.set_index('sid').loc[sid]
WD=pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/simulation_results_wide_12subs.csv')
WD['s']=WD.sub_id.astype(str)
W2=WD.set_index('s').reindex(sid)
PERT={}
i_a,i_g,i_b=cn.index('manipu'),cn.index('manipu_gaba'),cn.index('manipu_gaba_baseline')
PERT[('3m_268','ampa')]=np.nanmean(NPe[:,i_a,:,:],1)
PERT[('3m_268','gaba')]=np.nanmean(NPe[:,i_g,:,:],1)
def reg_edges(model,cond):
    sub=REG[(REG.model==model)&(REG.condition==cond)].copy()
    sub['s']=sub.subject.str.replace('sub-','').str.lstrip('0')
    g=sub.groupby('s')[EDC].mean().reindex(sid)
    return g.values
PERT[('10m_268','ampa')]=reg_edges('regional','ampa_r')
PERT[('10m_268','gaba')]=reg_edges('regional','ampa_gaba_r')
PERT[('10m_1000','ampa')]=reg_edges('coarse','ampa_r')
PERT[('10m_1000','gaba')]=reg_edges('coarse','ampa_gaba_r')
for m_ in ['10m','100m','1b']:
    for dr in ['ampa','gaba']:
        PERT[(m_,dr)]=W2[[f'{m_}_{dr}_edge{i}' for i in range(1,13)]].values.astype(float)
PERT[('10m_own','ampa')]=ss[[f'mani_ampa_edge{i}' for i in range(1,13)]].values.astype(float)
PERT[('10m_own','gaba')]=ss[[f'mani_ampa_gaba_edge{i}' for i in range(1,13)]].values.astype(float)
def sp_mat(dr):
    M_=np.full((7,7),np.nan); N_=np.zeros((7,7),int)
    for i,x in enumerate(ORDER):
        for j,y in enumerate(ORDER):
            a,b2=PERT[(x,dr)].ravel(),PERT[(y,dr)].ravel()
            ok=np.isfinite(a)&np.isfinite(b2); N_[i,j]=ok.sum()
            M_[i,j]=1.0 if i==j else float(stats.spearmanr(a[ok],b2[ok])[0])
    return pd.DataFrame(M_,index=ORDER,columns=ORDER), pd.DataFrame(N_,index=ORDER,columns=ORDER)

# ---- computation: recovered from execution-log cell 8ce04524
SA,NA=sp_mat('ampa')
NA.to_csv(f'{FD3}/fig3c_cross_scale_n_cells_ampa.csv')
