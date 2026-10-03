"""bold_cc_n288.csv | supplementary BOLD-agreement figure (04_figures/supp_boldcc/figS_boldcc_A4.py); not listed in FIG_SCRIPT_MAP_final.csv

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code selects a subset of columns from an existing dataframe m and
    renames them to lowercase, snake_case labels before saving the result
    as a CSV file. No calculations, aggregations, or transformations of
    values are performed here; the code simply reformats and exports pre-
    existing data. One row of the output table represents a single subject
    or participant, identified by their ID, along with their group
    assignments and four associated measures (assimilated and whole values
    for what appear to be two conditions or tasks, labeled MID and SST).
    The underlying meaning of those measures depends on how they were
    computed earlier in the analysis pipeline, which is not shown in this
    snippet.

INPUT FILES
    /Users/yunman/Desktop/submission/figures_v2/fig3/bold_cc_300subs.csv
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/corr_hd_np/empirical_fc_headmotion_excl_fd05.csv

OUTPUT FILE
    bold_cc_n288.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/supp_boldcc/data/bold_cc_n288.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : a2b350f9-44e8-4d54-85fb-f2fd354b6ec8
    frame              : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
    ran                : 2026-09-27 07:03:44 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/bold_cc_n288__cell_a2b350f9.py
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

# ---- computation: recovered from execution-log cell a2b350f9
import pandas as pd
cc = pd.read_csv('/Users/yunman/Desktop/submission/figures_v2/fig3/bold_cc_300subs.csv')
cc.columns = [c.strip().lstrip('\ufeff') for c in cc.columns]
keep = pd.read_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/corr_hd_np/empirical_fc_headmotion_excl_fd05.csv')
m = cc.merge(keep[['ID', 'Group', 'Group2']], on='ID', how='inner')
m = m[['ID', 'Group', 'Group2', 'MID assimilated', 'MID whole',
       'SST assimilated', 'SST whole']]
m.columns = ['ID', 'group', 'group2', 'mid_assimilated', 'mid_whole',
             'sst_assimilated', 'sst_whole']
m.to_csv('supp_boldcc/data/bold_cc_n288.csv', index=False)
