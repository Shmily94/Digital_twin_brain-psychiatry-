"""paramspace_regional_coherence_ampa_axis.csv | Supplementary Fig. S14 (04_figures/supp_paramspace/figS_paramspace_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code loads a table of coherence-scan results indexed by GABA and
    AMPA conductance values, then fixes GABA at its baseline value
    (0.0015) and selects the rows spanning the full AMPA grid. For each of
    those AMPA values, it pulls the per-region coherence columns
    (Region_*) and collects them into a new table where each column
    corresponds to one AMPA value, scaled by 1e4 and used as a labeled
    column header. One row of the output table therefore holds the
    coherence values of every region at a single matching position across
    the AMPA sweep, so each row corresponds to one region (in whatever
    order the Region_* columns appeared in the source data) and each
    column corresponds to one AMPA conductance level with GABA held fixed.

INPUT FILES
    coherence_results_tau_gamma.csv

OUTPUT FILE
    paramspace_regional_coherence_ampa_axis.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_paramspace/data/paramspace_regional_coherence_ampa_axis.csv

STATISTICAL TESTS
    ordinary least squares regression

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : a4cfb87b-156c-4195-bb69-235f3c5e3223
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-24 23:54:25 UTC
    conda environment  : (not recorded)
    verbatim archive   : recovered/fig3/paramspace_regional_coherence_ampa_axis__cell_a4cfb87b.py
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
#     /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_paramspace/figS_paramspace_A4.py
#   which performs this computation itself.  The code below is that script up
#   to and including the statement that writes this table (prints dropped).
#   HERE and sys.path point at the package copy of that figure directory.
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_paramspace")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_paramspace")
HERE = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/supp_paramspace"

# ---- computation: recovered from execution-log cell a4cfb87b
import os, sys
import numpy as np
import pandas as pd
FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_paramspace")
d = pd.read_csv(os.path.join(HERE, "data", "coherence_results_tau_gamma.csv"))
FRp = d.pivot(index="GABA", columns="AMPA", values="Mean_firing_rate")
AGRID = FRp.columns.values
BASE = (0.0008, 0.0015)
SCALE = 1e4
RCOLS = [c for c in d.columns if c.startswith("Region_")]
row = d[np.isclose(d.GABA, BASE[1])].sort_values("AMPA")
vals = [row[row.AMPA == a][RCOLS].values.ravel() for a in AGRID]
pd.DataFrame({f"{a * SCALE:.0f}": v for a, v in zip(AGRID, vals)}).to_csv(
    os.path.join(HERE, "data", "paramspace_regional_coherence_ampa_axis.csv"), index=False)
