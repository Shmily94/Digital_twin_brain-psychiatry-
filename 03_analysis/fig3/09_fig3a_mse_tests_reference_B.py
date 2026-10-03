"""fig3a_mse_tests_reference_B.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code loads per-subject mean squared error values for different
    model variants, pivots them into a per-subject table, and derives two
    composite family averages: "vox100" as the mean MSE across the 10m,
    100m, and 1b voxel models, and "reg" as the mean MSE across the 3m_268
    and 10m_268 regional models. It then runs six paired comparisons
    between specified model pairs (dropping subjects with missing data in
    either member of the pair), computing a paired t-test on the per-
    subject MSE differences along with the mean MSE of each side, the mean
    difference, a 95 percent confidence interval for that difference, and
    a count of how many subjects favored the lower-MSE model. Each row of
    the output table corresponds to one such named contrast between two
    models or model families, summarizing the paired-difference statistics
    for that specific comparison across the subjects with complete data
    for both models.

INPUT FILES
    fig3a_mse_per_subject.csv

OUTPUT FILE
    fig3a_mse_tests_reference_B.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3a_mse_tests_reference_B.csv

STATISTICAL TESTS
    paired two-sided t test

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 10783ea6-d4d3-4b01-812e-cd27be3faa14
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 15:22:10 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3a_mse_tests_reference_B__cell_10783ea6.py
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

from scipy import stats as st
import numpy as np
import pandas as pd

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 457de626, 49894910, 706899db, bb45f593)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
D3=FIG+'fig.3/fig3_data/'
A=pd.read_csv(D3+'fig3a_mse_per_subject.csv')

# ---- computation: recovered from execution-log cell 10783ea6
MP=A.pivot_table(index='subject_id',columns='model',values='mse')
MP['vox100']=MP[['10m','100m','1b']].mean(axis=1)
MP['reg']=MP[['3m_268','10m_268']].mean(axis=1)
mt=[]
for a_,b_,lab in [('vox100','reg','100M-hyper voxel family vs regional family'),
                  ('vox100','10m_1000','100M-hyper voxel family vs 10M/1000'),
                  ('vox100','10m_own','100M-hyper voxel family vs 10M voxel own hyper'),
                  ('10m','10m_own','10M voxel: 100M hyper vs own 10M hyper'),
                  ('vox100','SAR','100M-hyper voxel family vs SAR'),('vox100','RWW','100M-hyper voxel family vs rWW')]:
    s=MP[[a_,b_]].dropna(); d=s[a_]-s[b_]; t,p=st.ttest_rel(s[a_],s[b_])
    mt.append(dict(contrast=lab,n=len(s),df=len(s)-1,mse_a=f'{s[a_].mean():.4f}',mse_b=f'{s[b_].mean():.4f}',
        diff=f'{d.mean():+.4f}',ci95=f'{d.mean()-st.t.ppf(.975,len(d)-1)*d.std(ddof=1)/np.sqrt(len(d)):.4f} to {d.mean()+st.t.ppf(.975,len(d)-1)*d.std(ddof=1)/np.sqrt(len(d)):.4f}',
        t=round(float(t),3),p=f'{p:.3g}',n_lower=f'{int((d<0).sum())}/{len(d)}'))
T10T=pd.DataFrame(mt)
T10T.to_csv(D3+'fig3a_mse_tests_reference_B.csv',index=False)
