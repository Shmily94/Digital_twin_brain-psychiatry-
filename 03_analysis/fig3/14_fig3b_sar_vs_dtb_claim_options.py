"""fig3b_sar_vs_dtb_claim_options.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code builds a single-row status record rather than performing a
    new statistical computation itself; it hardcodes a resolution note
    stating that after re-scoring the 3M/268 build on a corrected task-FC
    pipeline, 3M/268 now exceeds both SAR and rWW across all 12
    participants, with the specific difference values, confidence
    interval, and paired t-test statistics for both comparisons embedded
    directly in the text. The row also records the prior, now-superseded
    SAR versus 3M/268 result (with its own difference and t-statistic) in
    the superseded_claim field for reference. The DataFrame is written out
    as one row to fig3b_sar_vs_dtb_claim_options.csv, with the note field
    explicitly withdrawing earlier options in the file, including a
    Bonferroni correction calculation and a TOST equivalence analysis, on
    the grounds that they assumed the opposite ordering of SAR and 3M/268.

INPUT FILES
    (no external file path appears in the recovered slice)

OUTPUT FILE
    fig3b_sar_vs_dtb_claim_options.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3b_sar_vs_dtb_claim_options.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : ce0ac3a0-7019-4666-b760-e945da67ce43
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 16:06:56 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3b_sar_vs_dtb_claim_options__cell_ce0ac3a0.py
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
#      (cells 457de626, 49894910, 706899db)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
D3=FIG+'fig.3/fig3_data/'

# ---- computation: recovered from execution-log cell ce0ac3a0
pd.DataFrame([dict(status='RESOLVED in v4',note=(
 'The SAR-versus-3M/268 problem no longer exists. With the 3M build re-scored on the corrected '
 'task-FC pipeline, 3M/268 = 0.3485 +- 0.0565 exceeds SAR = 0.2342 +- 0.0317 in 12 of 12 '
 'participants (diff +0.1143, 95% CI +0.0888 to +0.1397, paired t(11) = 9.891, P = 8.24e-07) and '
 'rWW = 0.1486 +- 0.0235 (diff +0.1999, t(11) = 16.143, P = 5.25e-09). The options previously '
 'listed in this file - all of which assumed SAR > 3M/268 - are withdrawn, including the '
 'Bonferroni family-size calculation (576,555 tests) and the TOST equivalence analysis.'),
 superseded_claim='SAR > 3M/268 by +0.0831, t(11) = 12.35, P = 8.67e-08 (computed from the superseded 3M run)')
 ]).to_csv(D3+'fig3b_sar_vs_dtb_claim_options.csv',index=False)
