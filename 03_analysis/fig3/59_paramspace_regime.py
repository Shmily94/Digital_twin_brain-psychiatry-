"""paramspace_regime.csv | Supplementary Fig. S14 (04_figures/supp_paramspace/figS_paramspace_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code classifies each point in a 2D parameter sweep over AMPA and
    GABA conductance values into a discrete network regime based on
    simulated coherence and firing rate. For each combination it labels
    the regime as 3 if no coherence value was recorded, 1 if the mean
    coherence meets or exceeds the synchrony cutoff of 0.20, 2 if it falls
    below that cutoff but the mean firing rate reaches or exceeds 50 Hz,
    and 0 otherwise. The result is a grid with GABA values as rows and
    AMPA values as columns, where one row corresponds to a fixed GABA
    conductance and gives the regime code across the swept range of AMPA
    conductance values. The output is restricted to only the AMPA values
    that were actually simulated, excluding the extended padding columns.

INPUT FILES
    coherence_results_tau_gamma.csv

OUTPUT FILE
    paramspace_regime.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_paramspace/data/paramspace_regime.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : a4cfb87b-156c-4195-bb69-235f3c5e3223
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-24 23:54:25 UTC
    conda environment  : (not recorded)
    verbatim archive   : recovered/fig3/paramspace_regime__cell_a4cfb87b.py
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
COp = d.pivot(index="GABA", columns="AMPA", values="Mean_Coherence")
GABA = FRp.index.values
AGRID = FRp.columns.values
AEXT = np.round(np.arange(AGRID[0], 0.00521, 0.0004), 6)
NSWEPT = len(AGRID)
FR = np.full((len(GABA), len(AEXT)), np.nan)
FR[:, :NSWEPT] = FRp.values
CO = np.full((len(GABA), len(AEXT)), np.nan)
CO[:, :NSWEPT] = COp.values
SYNC_CUT, RATE_CUT = 0.20, 50.0
REG = np.where(np.isnan(CO), 3,
               np.where(CO >= SYNC_CUT, 1, np.where(FR >= RATE_CUT, 2, 0)))
pd.DataFrame(REG[:, :NSWEPT], index=GABA, columns=AGRID).to_csv(
    os.path.join(HERE, "data", "paramspace_regime.csv"))
