"""fig3b_benchmark_wholebrain_fc.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code compares two whole-brain computational models, SAR and rWW,
    against subject-level fitting results for four task conditions (SST
    stop success, SST stop failure, MID anticipation hit, MID feedback
    hit), plus an average across those four conditions. For each model and
    condition it pivots the per-subject results to compute the mean and
    standard deviation of the FC Pearson correlation across subjects,
    along with the mean whole-brain MSE, then formats the correlation as a
    mean plus or minus standard deviation string and the MSE as a single
    rounded value. One row of the output table therefore represents one
    model-condition pairing (for example, SAR under MID_feed_hit, or rWW
    averaged across all four conditions), reporting the number of subjects
    used and the summarized fit-quality statistics for that pairing.

INPUT FILES
    revision/text/figures/Model_Benchmark/subject_level_rww_fitting_results.csv
    subject_level_sar_fitting_results.csv

OUTPUT FILE
    fig3b_benchmark_wholebrain_fc.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3b_benchmark_wholebrain_fc.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 1dbf78d8-6fdc-4505-97f9-8822a3724f5e
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 15:00:44 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3b_benchmark_wholebrain_fc__cell_1dbf78d8.py
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

import pandas as pd

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 1d696041, 457de626, 459ce015, 49894910, 706899db, aaadc71b, c1dd2f51, cbbdccb4)
SUB="/Users/yunman/Desktop/submission/"
rww=pd.read_csv(SUB+"revision/text/figures/Model_Benchmark/subject_level_rww_fitting_results.csv")
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
D3=FIG+'fig.3/fig3_data/'
MB=SUB+'revision/benchmark_predict_baseline_np/Model_Benchmark/'
sar=pd.read_csv(MB+'subject_level_sar_fitting_results.csv')
rows=[]
for nm,d in [('SAR',sar),('rWW',rww)]:
    pc=d.pivot_table(index='Subject_ID',columns='Condition',values='Pearson_r')
    ms=d.pivot_table(index='Subject_ID',columns='Condition',values='MSE')
    for c in ['SST_stop_success','SST_stop_failure','MID_antici_hit','MID_feed_hit']:
        rows.append(dict(model=nm,condition=c,n=len(pc),fc_pearson_r_mean=round(pc[c].mean(),4),
                         fc_pearson_r_sd=round(pc[c].std(ddof=1),4),wholebrain_mse_mean=round(ms[c].mean(),4)))
    rows.append(dict(model=nm,condition='mean of 4 conditions',n=len(pc),
                     fc_pearson_r_mean=round(pc.mean(axis=1).mean(),4),
                     fc_pearson_r_sd=round(pc.mean(axis=1).std(ddof=1),4),
                     wholebrain_mse_mean=round(ms.mean(axis=1).mean(),4)))
BT=pd.DataFrame(rows)

# ---- computation: recovered from execution-log cell 1dbf78d8
def ms(m,s,p=4): return f'{m:.{p}f} ± {s:.{p}f}'
BT2=pd.DataFrame([dict(model=r.model,condition=r.condition,n=r.n,
        fc_pearson_r=ms(r.fc_pearson_r_mean,r.fc_pearson_r_sd),
        wholebrain_mse=f'{r.wholebrain_mse_mean:.4f}') for _,r in BT.iterrows()])
BT2.to_csv(D3+'fig3b_benchmark_wholebrain_fc.csv',index=False)
