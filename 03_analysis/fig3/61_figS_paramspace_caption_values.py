"""figS_paramspace_caption_values.csv | Supplementary Fig. S14 (04_figures/supp_paramspace/figS_paramspace_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code characterizes a 2D parameter sweep over AMPA and GABA-A
    conductance values, using firing rate and coherence measures from a
    simulation grid to classify each grid cell into async, sync, or
    excess-rate regimes based on fixed coherence and rate thresholds, then
    tallies how many cells fall into each regime. It also extracts summary
    ranges (firing rate, coherence in low and high bands, per-regime
    firing rate extremes), pulls out values at a designated baseline
    conductance pair, counts region-related columns in the source data,
    and computes median interquartile spreads of per-condition region
    values separately for AMPA values below and above a chosen sweep
    threshold. Each row of the output table is a single named summary
    statistic (the "key") paired with its computed value (the "value"),
    stored as a string, so the CSV is a flat list of caption-ready
    quantities rather than a matrix or time series. The eighteen rows
    correspond to the eighteen distin

INPUT FILES
    coherence_results_tau_gamma.csv

OUTPUT FILE
    figS_paramspace_caption_values.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_paramspace/figS_paramspace_caption_values.csv

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
    verbatim archive   : recovered/fig3/figS_paramspace_caption_values__cell_a4cfb87b.py
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
S = {}
d = pd.read_csv(os.path.join(HERE, "data", "coherence_results_tau_gamma.csv"))
FRp = d.pivot(index="GABA", columns="AMPA", values="Mean_firing_rate")
COp = d.pivot(index="GABA", columns="AMPA", values="Mean_Coherence")
GABA = FRp.index.values
AGRID = FRp.columns.values
AEXT = np.round(np.arange(AGRID[0], 0.00521, 0.0004), 6)
NSWEPT = len(AGRID)
S["n_cells"] = FRp.size
S["ampa_grid"] = f"{AGRID[0]:.4f}-{AGRID[-1]:.4f}"
S["gaba_grid"] = f"{GABA[0]:.4f}-{GABA[-1]:.4f}"
FR = np.full((len(GABA), len(AEXT)), np.nan)
FR[:, :NSWEPT] = FRp.values
CO = np.full((len(GABA), len(AEXT)), np.nan)
CO[:, :NSWEPT] = COp.values
SYNC_CUT, RATE_CUT = 0.20, 50.0
REG = np.where(np.isnan(CO), 3,
               np.where(CO >= SYNC_CUT, 1, np.where(FR >= RATE_CUT, 2, 0)))
for k, key in enumerate(["n_async", "n_sync", "n_excess"]):
    S[key] = int((REG == k).sum())
S["fr_range"] = f"{np.nanmin(FR):.2f}-{np.nanmax(FR):.2f}"
S["co_floor"] = f"{COp.values[COp.values < .08].min():.4f}-{COp.values[COp.values < .08].max():.4f}"
S["co_sync"] = f"{COp.values[COp.values >= .3].min():.3f}-{COp.values[COp.values >= .3].max():.3f}"
S["fr_async_max"] = f"{FR[REG == 0].max():.2f}"
S["fr_excess_min"] = f"{FR[REG == 2].min():.2f}"
S["fr_sync_range"] = f"{FR[REG == 1].min():.2f}-{FR[REG == 1].max():.2f}"
BASE = (0.0008, 0.0015)
SWEEP_A0 = 0.0020
ib = (int(np.where(np.isclose(GABA, BASE[1]))[0][0]),
      int(np.where(np.isclose(AEXT, BASE[0]))[0][0]))
S["baseline_fr"] = f"{FR[ib]:.2f}"
S["baseline_co"] = f"{CO[ib]:.4f}"
S["baseline"] = f"g_AMPA = {BASE[0]:.4f}, g_GABA-A = {BASE[1]:.4f}"
RCOLS = [c for c in d.columns if c.startswith("Region_")]
S["n_regions"] = len(RCOLS)
row = d[np.isclose(d.GABA, BASE[1])].sort_values("AMPA")
vals = [row[row.AMPA == a][RCOLS].values.ravel() for a in AGRID]
S["d_iqr_async"] = "%.4f" % np.median([np.subtract(*np.percentile(v, [75, 25]))
                                       for a, v in zip(AGRID, vals) if a < SWEEP_A0])
S["d_iqr_sync"] = "%.3f" % np.median([np.subtract(*np.percentile(v, [75, 25]))
                                      for a, v in zip(AGRID, vals) if a >= SWEEP_A0])
pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
    os.path.join(HERE, "figS_paramspace_caption_values.csv"), index=False)
