"""fig3b_10m_own_hyperparameter_axis.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code loads a CSV of functional connectivity similarity values
    from four runs per subject and, for each combination of reference type
    (voxel-based digital twin brain versus all-voxels model) and build
    (10m_own, 10m_100m_params, 100m, 1b, representing different neuron
    count and hyperparameter voxel-count combinations), extracts the
    corresponding column of similarity values and computes the sample
    size, mean, standard deviation, minimum, and maximum. It then formats
    the mean and standard deviation into a single "mean +/- sd" string and
    the minimum and maximum into a single "min-max" range string. One row
    of the output table corresponds to one build-reference combination,
    reporting how many values went into that summary along with the
    formatted mean/sd and range strings for that group's similarity
    distribution.

INPUT FILES
    revision/10m_voxel_population_simulation/analysis_results/fc_similarity_four_runs_per_subject.csv

OUTPUT FILE
    fig3b_10m_own_hyperparameter_axis.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3b_10m_own_hyperparameter_axis.csv

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
    verbatim archive   : recovered/fig3/fig3b_10m_own_hyperparameter_axis__cell_1dbf78d8.py
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
#      (cells 457de626, 49894910, 706899db, 821bf2cd, 9a17420c, ffbb91c0)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
SUB='/Users/yunman/Desktop/submission/'
D3=FIG+'fig.3/fig3_data/'
FR=pd.read_csv(SUB+'revision/10m_voxel_population_simulation/analysis_results/fc_similarity_four_runs_per_subject.csv')
rows=[]
for ref,tag in [('r_dtb_voxels__','B_model_voxels'),('r_all_voxels__','A_all_voxels')]:
    for k,lab in [('10m_own_params','10m_own (10M neurons, 10M voxel hyper)'),
                  ('10m_100m_params','10m (10M neurons, 100M hyper)'),
                  ('100m','100m (100M neurons, 100M hyper)'),('1b','1b (1B neurons, 100M hyper)')]:
        v=FR[ref+k]
        rows.append(dict(build=lab,reference=tag,n=len(v),mean=round(v.mean(),4),sd=round(v.std(ddof=1),4),
                         min=round(v.min(),4),max=round(v.max(),4)))
OW=pd.DataFrame(rows)

# ---- computation: recovered from execution-log cell 1dbf78d8
def ms(m,s,p=4): return f'{m:.{p}f} ± {s:.{p}f}'
OW2=pd.DataFrame([dict(build=r.build,reference=r.reference,n=r.n,
                       mean_sd=ms(r['mean'],r.sd),range=f'{r["min"]:.4f}–{r["max"]:.4f}')
                  for _,r in OW.iterrows()])
OW2.to_csv(D3+'fig3b_10m_own_hyperparameter_axis.csv',index=False)
