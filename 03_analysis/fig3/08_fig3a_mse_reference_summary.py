"""fig3a_mse_reference_summary.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code builds a small hardcoded summary table comparing two
    families of brain models, voxel-based and regional-based, against
    three different reference standards used in the manuscript. For each
    reference, it records the mean MSE for the voxel family and the
    regional family, determines which family wins (has the lower mean),
    computes the numeric gap between the two means, and notes the single
    best-performing build within the winning family along with its own MSE
    value. One row of the output therefore corresponds to one reference
    condition, showing that reference's name, the two family-level mean
    errors, which family performed better and by how much, and which
    specific build achieved the lowest error under that reference. The
    table is then written out as a CSV file without any additional
    computation, statistical testing, or derivation beyond the values
    already specified in the code.

INPUT FILES
    (no external file path appears in the recovered slice)

OUTPUT FILE
    fig3a_mse_reference_summary.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3a_mse_reference_summary.csv

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
    verbatim archive   : recovered/fig3/fig3a_mse_reference_summary__cell_038cd901.py
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
#      (cells 457de626, 49894910, 706899db)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
D3=FIG+'fig.3/fig3_data/'

# ---- computation: recovered from execution-log cell 038cd901
summ=pd.DataFrame([
 dict(reference='empirical_original_3m (common)',voxel_family_mean=0.1024,regional_family_mean=0.0960,
      winner='regional',gap=0.0065,best_single_build='3m_268 (0.0888)'),
 dict(reference='empirical_model_voxels (common)',voxel_family_mean=0.0581,regional_family_mean=0.0784,
      winner='voxel',gap=0.0204,best_single_build='10m voxel (0.0498)'),
 dict(reference='mixed, as in Table S10',voxel_family_mean=0.0581,regional_family_mean=0.0960,
      winner='voxel',gap=0.0379,best_single_build='10m voxel (0.0498)')])
summ.to_csv(D3+'fig3a_mse_reference_summary.csv',index=False)
