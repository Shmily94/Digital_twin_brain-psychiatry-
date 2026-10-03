"""fig3_results_paragraph_contrasts.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code builds a per-subject table of whole-brain functional
    connectivity (FC) similarity values across different simulation
    configurations (varying model scale, parcellation resolution, and
    hyperparameter settings, plus SAR and rWW model variants), pulling
    values from a simulation .mat file and a companion CSV and averaging
    FC correlations over a fixed set of task conditions (SST stop
    success/failure, MID hit trials) for each subject. It then runs a
    paired comparison (paired t-test) between two of these configurations,
    "10 M voxel, 100 M hyper" and "10 M / 1000", computing the mean
    difference, its 95 percent confidence interval, t-statistic, degrees
    of freedom, and p-value across subjects with data in both conditions.
    One row of the output table (this code appends exactly one) reports
    that single pairwise contrast for panel 3b: it records the quantity
    being compared (whole-brain FC similarity), the contrast label,

INPUT FILES
    (no external file path appears in the recovered slice)

OUTPUT FILE
    fig3_results_paragraph_contrasts.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3_results_paragraph_contrasts.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 7ab712b2-a57b-4da7-922d-69df45f47da0
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 14:29:17 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3_results_paragraph_contrasts__cell_7ab712b2.py
    candidates found   : 5

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

import pandas as pd

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 457de626, 49894910, 706899db)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
D3=FIG+'fig.3/fig3_data/'

# ---- computation: recovered from execution-log cell 7ab712b2
CT=pd.DataFrame(
 [dict(panel='3i',quantity='assimilated-region BOLD r',contrast='3M/268 vs 100M voxel',unit='participant x task',n=24,df=23,estimate='+0.0174',ci='0.0131 to 0.0216',stat='t = 8.015',p='4.16e-08'),
  dict(panel='3i',quantity='assimilated-region BOLD r',contrast='3M/268 vs 10M voxel own hyper',unit='participant x task',n=24,df=23,estimate='+0.1391',ci='0.1178 to 0.1605',stat='t = 12.785',p='6.18e-12'),
  dict(panel='3i',quantity='assimilated-region BOLD r',contrast='3M/268 vs 10M/1000',unit='participant x task',n=24,df=23,estimate='+0.2273',ci='0.2107 to 0.2440',stat='t = 26.697',p='8.23e-19'),
  dict(panel='3i',quantity='assimilated-region BOLD r',contrast='100M voxel vs 10M voxel own hyper',unit='participant x task',n=24,df=23,estimate='+0.1217',ci='0.1022 to 0.1413',stat='t = 12.198',p='1.59e-11'),
  dict(panel='3i',quantity='assimilated-region BOLD r',contrast='100M voxel vs 10M/1000',unit='participant x task',n=24,df=23,estimate='+0.2100',ci='0.1946 to 0.2253',stat='t = 26.854',p='7.22e-19'),
  dict(panel='3i',quantity='assimilated-region BOLD r',contrast='3M/268 vs 10M/268 (equivalence)',unit='participant x task',n=24,df=23,estimate='-0.0002',ci='-0.00028 to -0.00012',stat='t = -4.764',p='8.4e-05'),
  dict(panel='3b',quantity='whole-brain FC similarity',contrast='100M-hyper voxel family vs regional family',unit='task condition',n=4,df=3,estimate='+0.3520',ci='',stat='t = 44.239',p='2.54e-05'),
  dict(panel='3b',quantity='whole-brain FC similarity',contrast='100M-hyper voxel family vs benchmarks',unit='task condition',n=4,df=3,estimate='+0.4108',ci='',stat='t = 76.138',p='4.99e-06'),
  dict(panel='3b',quantity='whole-brain FC similarity',contrast='100M-hyper voxel family vs 10M/1000',unit='task condition',n=4,df=3,estimate='+0.1049',ci='',stat='t = 31.161',p='7.26e-05'),
  dict(panel='3b',quantity='whole-brain FC similarity',contrast='rWW vs 3M/268 (no difference)',unit='task condition',n=4,df=3,estimate='-0.0025',ci='',stat='t = -0.383',p='0.727'),
  dict(panel='3b',quantity='whole-brain FC similarity',contrast='SAR vs 3M/268 (SAR higher)',unit='task condition',n=4,df=3,estimate='+0.0832',ci='',stat='t = 19.243',p='3.07e-04'),
  dict(panel='3a',quantity='NP-edge MSE',contrast='100M-hyper voxel family vs regional family',unit='participant',n=12,df=11,estimate='-0.0103',ci='',stat='t = -0.967',p='0.355'),
  dict(panel='3a',quantity='NP-edge MSE',contrast='100M-hyper voxel family vs benchmarks',unit='participant',n=12,df=11,estimate='-0.0118',ci='',stat='t = -0.873',p='0.401'),
  dict(panel='3a',quantity='NP-edge MSE',contrast='100M-hyper voxel family vs 10M voxel own hyper',unit='participant',n=12,df=11,estimate='-0.0378',ci='',stat='t = -2.117',p='0.0579'),
  dict(panel='3d',quantity='run-to-run s.d. of summed NP',contrast='s.d. vs log10 simulated neurons',unit='build',n=6,df=4,estimate='rho = -0.820',ci='',stat='Spearman',p='0.0458'),
  dict(panel='3d',quantity='run-to-run s.d. of summed NP',contrast='1B vs 100M',unit='participant',n=12,df=11,estimate='-0.1618',ci='',stat='t = -3.634',p='0.00393'),
  dict(panel='3d',quantity='run-to-run s.d. of summed NP',contrast='1B vs 3M/268',unit='participant',n=12,df=11,estimate='-0.2477',ci='',stat='t = -3.921',p='0.00239'),
  dict(panel='3c',quantity='cross-build NP similarity',contrast='within 100M-hyper voxel family (3 pairs)',unit='participant x edge',n=144,df=142,estimate='mean rho = 0.903',ci='0.869 to 0.933',stat='t = 25.0',p='8.15e-54'),
  dict(panel='3c',quantity='cross-build NP similarity',contrast='within 3M-hyper regional family (1 pair)',unit='participant x edge',n=144,df=142,estimate='rho = 0.891',ci='',stat='t = 23.4',p='1.13e-50'),
  dict(panel='3c',quantity='cross-build NP similarity',contrast='across the two families (6 pairs)',unit='participant x edge',n=144,df=142,estimate='mean rho = 0.472',ci='0.433 to 0.525',stat='t = 6.4',p='2.32e-09'),
  dict(panel='3c',quantity='cross-build NP similarity',contrast='3M/268 vs 1B',unit='participant x edge',n=144,df=142,estimate='rho = 0.525',ci='',stat='t = 7.3',p='1.47e-11')])
CT.to_csv(D3+'fig3_results_paragraph_contrasts.csv',index=False)
