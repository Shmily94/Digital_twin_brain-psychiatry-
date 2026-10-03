"""assim5_stats.csv | Supplementary Fig. S10 (04_figures/supp_assim/figS_assim_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code assesses the reliability of an assimilation-region
    connectivity profile across five repeated runs on the same set of
    reward-task edges. It computes ICC(3,1) and ICC(2,1) reliability
    coefficients, pairwise Pearson correlations between runs (summarized
    as mean, min, and max), and a signal versus noise comparison using the
    standard deviation across edges of the per-edge run averages against
    the average within-edge standard deviation across runs, plus the
    resulting signal to noise ratio. It also records the number of runs
    and the number of edges used in the analysis. One row of the output
    table holds the name of one such statistic in the statistic column and
    its computed numeric value, rounded to four or two decimal places, in
    the value column.

INPUT FILES
    {AR}/assimilation_stability_source_data.csv

OUTPUT FILE
    assim5_stats.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_assim/data/assim5_stats.csv

STATISTICAL TESTS
    Pearson correlation
    intraclass correlation (ICC)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 4f1219ba-ee06-45f1-adc4-bf6e8ed25294
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-21 21:29:24 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/assim5_stats__cell_4f1219ba.py
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

from scipy import stats
import numpy as np
import pandas as pd

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 205b9942, 408324e5, 41572f3b, e9ccf5a2)
def icc21(X,Y):
    n=len(X); M=np.column_stack([X,Y]); gm=M.mean()
    msb=2*((M.mean(1)-gm)**2).sum()/(n-1)
    msw=((M-M.mean(1,keepdims=True))**2).sum()/n
    mss=n*((M.mean(0)-gm)**2).sum()/1
    mse=((M-M.mean(1,keepdims=True)-M.mean(0)+gm)**2).sum()/(n-1)
    icc=(msb-mse)/(msb+(2-1)*mse+2*(mss-mse)/n)
    F=msb/mse; f1,f2=n-1,n-1
    lo=(F/stats.f.ppf(.975,f1,f2)-1)/(F/stats.f.ppf(.975,f1,f2)+1)
    hi=(F/stats.f.ppf(.025,f1,f2)-1)/(F/stats.f.ppf(.025,f1,f2)+1)
    return icc,lo,hi,F
B='/Users/yunman/Desktop/submission'
AR=f'{B}/revision/sensitivity_analysis/assimilated_region'
A5=pd.read_csv(f'{AR}/assimilation_stability_source_data.csv')
R=A5[['run1','run2','run3','run4','run5']].values
A5=pd.read_csv(f'{AR}/assimilation_stability_source_data.csv')
R=A5[['run1','run2','run3','run4','run5']].values
k=R.shape[1]
nsub=R.shape[0]
gm=R.mean()
MSR=((R.mean(1)-gm)**2).sum()*k/(nsub-1)
MSE=((R-R.mean(1,keepdims=True)-R.mean(0,keepdims=True)+gm)**2).sum()/((nsub-1)*(k-1))
icc31=(MSR-MSE)/(MSR+(k-1)*MSE)
A5=pd.read_csv(f'{AR}/assimilation_stability_source_data.csv')
R=A5[['run1','run2','run3','run4','run5']].values
k=R.shape[1]
import itertools
pair_r=[stats.pearsonr(R[:,i],R[:,j])[0] for i,j in itertools.combinations(range(k),2)]

# ---- computation: recovered from execution-log cell 4f1219ba
FIG=f'{B}/revision/text/figures'
dirs={k: f'{FIG}/supp_{k}' for k in ['assim','fingerprint','conductance','eft','motion']}
pd.DataFrame([dict(statistic='ICC(3,1), runs fixed', value=round(float(icc31),4)),
              dict(statistic='ICC(2,1), runs random', value=round(float(icc21),4)),
              dict(statistic='mean between-run profile r', value=round(float(np.mean(pair_r)),4)),
              dict(statistic='min between-run profile r', value=round(float(min(pair_r)),4)),
              dict(statistic='max between-run profile r', value=round(float(max(pair_r)),4)),
              dict(statistic='SD between edges (signal)', value=round(float(R.mean(1).std(ddof=1)),4)),
              dict(statistic='mean SD between runs (noise)', value=round(float(R.std(1,ddof=1).mean()),4)),
              dict(statistic='signal/noise SD ratio', value=round(float(R.mean(1).std(ddof=1)/R.std(1,ddof=1).mean()),2)),
              dict(statistic='n runs', value=5), dict(statistic='n reward-task edges', value=6),
              ]).to_csv(f"{dirs['assim']}/data/assim5_stats.csv", index=False)
