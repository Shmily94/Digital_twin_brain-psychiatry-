"""assimregion_np_edges_runwise.csv | Supplementary Fig. S11 (04_figures/supp_assimregion/figS_assimregion_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code sorts a table of per-edge assimilation statistics, named E7,
    by numeric edge index and writes it to a CSV file for a supplementary
    figure on assimilation regions. The actual computation of the
    statistics happens upstream, before this snippet, so this code only
    performs the final ordering and export step. One row of the output
    table corresponds to a single edge under a given condition and pair,
    summarizing repeat and actual measurements along with derived
    comparison metrics for that edge. The sort ensures edges appear in
    ascending numeric order (edge1, edge2, edge3, and so on) rather than
    in string order.

INPUT FILES
    np_edges_7runs_stats.csv

OUTPUT FILE
    assimregion_np_edges_runwise.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_assimregion/data/assimregion_np_edges_runwise.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 0dc263b8-7352-4320-840a-a5d86070b421
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-25 00:15:33 UTC
    conda environment  : (not recorded)
    verbatim archive   : recovered/fig3/assimregion_np_edges_runwise__cell_0dc263b8.py
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

# NOTE ON THE SOURCE
#   The producing cell wrote the figure script
#     /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_assimregion/figS_assimregion_A4.py
#   which performs this computation itself.  The code below is that script up
#   to and including the statement that writes this table (prints dropped).
#   HERE and sys.path point at the package copy of that figure directory.
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_assimregion")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_assimregion")
HERE = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_assimregion"

# ---- computation: recovered from execution-log cell 0dc263b8
import os, sys, itertools
import pandas as pd
FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_assimregion")
SRC = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/sensitivity_analysis/assimilated_region"
E7 = pd.read_csv(os.path.join(SRC, "np_edges_7runs_stats.csv"))
E7 = E7.sort_values("edge", key=lambda s: s.str.replace("edge", "").astype(int)).reset_index(drop=True)
E7.to_csv(os.path.join(HERE, "data", "assimregion_np_edges_runwise.csv"), index=False)
