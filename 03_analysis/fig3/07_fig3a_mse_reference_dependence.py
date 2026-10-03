"""fig3a_mse_reference_dependence.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code assembles a table comparing model-fit error under two
    different empirical reference choices across six model builds (3m_268,
    10m_268, 10m_1000, 10m, 100m, 1b). For each build, it looks up which
    reference was designated for that build in a separate six-model MSE
    summary file, pulls that designated reference's label and its
    corresponding mean MSE value (the value reported in Table S10), and
    joins these onto the pivoted per-build MSE columns computed under the
    empirical-model-voxels reference and the empirical-original-3m
    reference. One row of the output therefore represents a single build,
    showing its MSE under each of the two reference conditions side by
    side with which reference was actually designated for that build and
    the associated Table S10 MSE value, plus a fixed note explaining that
    the designated reference varies from build to build rather than being
    held constant.

INPUT FILES
    revision/model_scale_consistent/manuscript_numbers_newflow/six_model_mse_12subs.csv

OUTPUT FILE
    fig3a_mse_reference_dependence.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3a_mse_reference_dependence.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 038cd901-1757-432f-bb8d-3abc2bb7a0cf
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 15:13:19 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3a_mse_reference_dependence__cell_038cd901.py
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

import pandas as pd

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 3eeab79b, 457de626, 49894910, 706899db, 821bf2cd, 830cc524)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
SUB='/Users/yunman/Desktop/submission/'
D3=FIG+'fig.3/fig3_data/'
SM=pd.read_csv(SUB+'revision/model_scale_consistent/manuscript_numbers_newflow/six_model_mse_12subs.csv')
piv=SM.pivot_table(index='model',columns='empirical_reference',values='mse_mean')
piv=piv.reindex(['3m_268','10m_268','10m_1000','10m','100m','1b'])
des=SM[SM.is_designated].set_index('model').empirical_reference
piv['designated_reference']=des.reindex(piv.index)
piv['TableS10_value']=[SM[(SM.model==m)&(SM.is_designated)].mse_mean.iloc[0] for m in piv.index]

# ---- computation: recovered from execution-log cell 038cd901
out=piv.reset_index().rename(columns={'model':'build','empirical_model_voxels':'mse_under_empirical_model_voxels',
    'empirical_original_3m':'mse_under_empirical_original_3m'})
out['note']=['Table S10 takes the designated reference for each build; the designation is not constant across builds']*len(out)
out.to_csv(D3+'fig3a_mse_reference_dependence.csv',index=False)
