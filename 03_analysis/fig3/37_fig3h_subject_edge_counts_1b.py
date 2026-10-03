"""fig3h_subject_edge_counts_1b.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code takes a dataframe called psub, which was built earlier in
    the analysis, and writes it out unchanged to a CSV file named
    fig3h_subject_edge_counts_1b.csv in the specified figures directory.
    No computation, filtering, or transformation happens in this snippet
    itself; it only converts the existing psub structure to a DataFrame
    and saves it, with the row index omitted from the file. One row of the
    output table corresponds to one subject under one modulation
    condition, carrying that subject's summed delta value and an
    associated count of concordant edges as previously computed upstream
    in psub. The code does not compute or reveal what delta_np_sum or
    n_edges_concordant represent beyond the labels already present in the
    data.

INPUT FILES
    (no external file path appears in the recovered slice)

OUTPUT FILE
    fig3h_subject_edge_counts_1b.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3h_subject_edge_counts_1b.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 284588c4-c78f-4686-93d5-c6f98fe25907
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-21 15:34:11 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3h_subject_edge_counts_1b__cell_284588c4.py
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

import numpy as np
import pandas as pd

# NOTE ON PATHS
#   platform artifact 5936b67f resolved to its byte-identical on-disk copy
#     /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/edge_level/np_baseline_and_modulated_per_edge_6models.csv

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 2f52d573, 5eb2d51f, bbc97276)
pe=pd.read_csv("/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/edge_level/np_baseline_and_modulated_per_edge_6models.csv")
s=pe[pe.model=='1b'].groupby(['sub_id','condition']).value.sum().unstack()
long1b = pe[pe.model=='1b'].pivot_table(index=['sub_id','edge'],columns='condition',values='value')
EORD=[f'edge{i}' for i in range(1,13)]
psub=[]
for drug in ['ampa','gaba']:
    dsum=s[drug]-s['baseline']
    for sid in s.index:
        sub=long1b.xs(sid,level='sub_id').loc[EORD]
        de=sub[drug]-sub['baseline']
        psub.append(dict(modulation={'ampa':'AMPA','gaba':'GABA-A'}[drug], sub_id=sid,
                         delta_np_sum=round(float(dsum[sid]),4),
                         n_edges_concordant=int((np.sign(de)==np.sign(dsum[sid])).sum())))
psub=pd.DataFrame(psub)

# ---- computation: recovered from execution-log cell 284588c4
D3='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data'
psub.to_csv(f'{D3}/fig3h_subject_edge_counts_1b.csv', index=False)
