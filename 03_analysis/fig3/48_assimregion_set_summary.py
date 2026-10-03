"""assimregion_set_summary.csv | Supplementary Fig. S11 (04_figures/supp_assimregion/figS_assimregion_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code does not compute anything itself; it simply copies an
    already-computed summary table
    (assimilation_set_comparison_summary.csv) from the sensitivity
    analysis directory into the figure data directory under a new
    filename, assimregion_set_summary.csv, with no changes to the values,
    columns, or row order. The actual computation of the metrics in that
    table happens elsewhere, upstream of this snippet. One row of the
    output table corresponds to one task and assimilated-region set
    combination, giving that set's region composition and its size,
    spatial overlap, connectivity, and holdout characteristics as
    previously calculated. Since the code is a straight file copy, the 13
    rows in the shipped file directly mirror the 13 rows of the source
    comparison summary.

INPUT FILES
    {AR}/assimilation_set_comparison_summary.csv

OUTPUT FILE
    assimregion_set_summary.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_assimregion/data/assimregion_set_summary.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 70b24b7e-48f9-4b00-9392-31414c49feae
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 20:08:10 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/assimregion_set_summary__cell_70b24b7e.py
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
#      (cells 1da5a5c6, 6e8ac2d7)
AR='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/sensitivity_analysis/assimilated_region'
CS=pd.read_csv(f'{AR}/assimilation_set_comparison_summary.csv')

# ---- computation: recovered from execution-log cell 70b24b7e
SD='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_assimregion/data'
CS.to_csv(f'{SD}/assimregion_set_summary.csv', index=False)
