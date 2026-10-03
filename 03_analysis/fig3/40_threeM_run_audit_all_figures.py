"""threeM_run_audit_all_figures.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code builds a single audit table that tracks, for each figure or
    panel in a manuscript, which simulation run (OLD vs NEW vs not
    verifiable) actually produced the numbers shown, along with the sample
    size and a short evidence string explaining how that determination was
    made. It does not perform new statistical analysis itself; it
    assembles a hand-compiled record of provenance checks (such as
    comparing values against source .mat or .csv files, checking
    correlations between subsets, or noting missing run markers) into a
    DataFrame and writes it out as a CSV. One row of the output represents
    a single figure or quantity (for example, Fig. 3a's NP-edge MSE, or
    the 288-participant source table), stating its sample size, which run
    version it traces back to, and the evidence text supporting that
    conclusion. The final line simply saves this assembled table to the
    specified path in the fig.3 data directory.

INPUT FILES
    np_edges_3m_full_cohort.csv
    source code reads Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat

OUTPUT FILE
    threeM_run_audit_all_figures.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/threeM_run_audit_all_figures.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 114753da-f981-4fa1-a999-2de0dc0a8e1a
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 16:31:51 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/threeM_run_audit_all_figures__cell_114753da.py
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

# ---- computation: recovered from execution-log cell 114753da
AU=pd.DataFrame([
 dict(figure='Fig. 3a',quantity='NP-edge MSE',n=12,run='NEW',evidence='0.06489 = new3m_direction_checks row "3m_268 NEW / empirical_model_voxels"; n_repeats_averaged = 5'),
 dict(figure='Fig. 3b / Table S9',quantity='whole-brain FC',n=12,run='NEW (fixed this turn)',evidence='recomputed from Baseline_simulated_3m_task_FC.mat; 0.3485 +- 0.0565'),
 dict(figure='Fig. 3c / 3c_ampa / 3c_gaba',quantity='cross-build NP similarity',n=12,run='NEW',evidence='source code reads Baseline_simulated_NP_12edges_and_factor_3m_new_run.mat'),
 dict(figure='Fig. 3d',quantity='run-to-run s.d. of summed NP',n=12,run='NEW',evidence='per-subject values reproduce the new run exactly, max |diff| = 0.00000'),
 dict(figure='Fig. 3g',quantity='delta NP after perturbation',n=12,run='NEW',evidence='source column: "Mani_simulated_3m_NP_12edges_and_factor.mat (new run ...)"'),
 dict(figure='Fig. 3i',quantity='assimilated-region BOLD r',n=12,run='NOT VERIFIABLE',evidence='user-supplied summary table baseline BOLD_r; 5 repeats, r = 0.9132; no run marker in the file'),
 dict(figure='Fig. 4 (all panels)',quantity='simulated / AMPA / GABA-A NP',n=288,run='OLD',evidence='fig4_subject_level_n288.csv "simulated" reproduces the OLD run exactly on the 11 shared participants (r = +1.0000, max |diff| = 0.0000); r vs NEW = -0.43'),
 dict(figure='Fig. 5h + longitudinal supp.',quantity='restoration index (n = 85)',n=85,run='OLD',evidence='derived from the same 288-participant 3M table'),
 dict(figure='Supp. depression-network / whole-brain drug / Oldham / motion',quantity='population perturbation',n=288,run='OLD',evidence='same source'),
 dict(figure='source of the 288 data',quantity='np_edges_3m_full_cohort.csv',n=301,run='OLD',evidence='baseline np_sum reproduces the OLD run exactly (r = +1.000) on the 11 shared participants; no new-run version of the full cohort exists in the tree'),
])
AU.to_csv(D3+'threeM_run_audit_all_figures.csv',index=False)
