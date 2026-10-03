"""assim5_edges_mid.csv | Supplementary Fig. S10 (04_figures/supp_assim/figS_assim_A4.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code does not compute anything new; it reads an existing source
    data file, assimilation_stability_source_data.csv, containing results
    from a five-run assimilation stability check, and simply copies it
    unchanged into the supplementary figure data folder under the name
    assim5_edges_mid.csv. The underlying values, such as per-run
    measurements and their summary statistics, must have been produced by
    an earlier analysis step not shown here. One row of the output table
    corresponds to a single edge (a pair of regions in the 217-space
    parcellation), reporting that edge's value across the five runs along
    with the mean, standard deviation, and range of those five values. The
    script's role is purely to relocate the already-computed per-edge
    stability table to the location used for assembling the manuscript's
    figures.

INPUT FILES
    {AR}/assimilation_stability_source_data.csv

OUTPUT FILE
    assim5_edges_mid.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_assim/data/assim5_edges_mid.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 4f1219ba-ee06-45f1-adc4-bf6e8ed25294
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-21 21:29:24 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/assim5_edges_mid__cell_4f1219ba.py
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
#      (cells 205b9942, 41572f3b, e9ccf5a2)
B='/Users/yunman/Desktop/submission'
AR=f'{B}/revision/sensitivity_analysis/assimilated_region'
A5=pd.read_csv(f'{AR}/assimilation_stability_source_data.csv')

# ---- computation: recovered from execution-log cell 4f1219ba
FIG=f'{B}/revision/text/figures'
dirs={k: f'{FIG}/supp_{k}' for k in ['assim','fingerprint','conductance','eft','motion']}
A5.to_csv(f"{dirs['assim']}/data/assim5_edges_mid.csv", index=False)
