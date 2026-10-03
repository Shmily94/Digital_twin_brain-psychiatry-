"""fig3h_edge_direction_1b.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code computes, for each of 12 connectivity edges (E1-E12, split
    into SST and MID tasks) under two neuromodulatory drug conditions
    (AMPA and GABA-A), whether the per-subject change in that edge from
    baseline matches the sign of the per-subject change in the summed
    network property under the same drug, across 12 subjects in model 1b.
    For each drug-edge combination it counts how many of the 12 subjects
    show concordant-sign changes, runs a two-sided exact binomial test
    against a null rate of 0.5, and computes the mean and standard
    deviation of the edge-level change across subjects. One row of the
    output table corresponds to one drug modulation and one edge, giving
    the number of concordant subjects out of 12, the percentage
    concordant, the mean and sd of the delta edge value, the binomial p
    value, and its Benjamini-Hochberg adjusted q value computed jointly
    across all 24 rows.

INPUT FILES
    (no external file path appears in the recovered slice)

OUTPUT FILE
    fig3h_edge_direction_1b.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3h_edge_direction_1b.csv

STATISTICAL TESTS
    Benjamini-Hochberg FDR correction
    exact binomial test against chance

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 284588c4-c78f-4686-93d5-c6f98fe25907
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-21 15:34:11 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3h_edge_direction_1b__cell_284588c4.py
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

from statsmodels.stats.multitest import multipletests
import numpy as np
import pandas as pd

# NOTE ON PATHS
#   platform artifact 5936b67f resolved to its byte-identical on-disk copy
#     /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/edge_level/np_baseline_and_modulated_per_edge_6models.csv

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 2f52d573, 5eb2d51f, bbc97276)
pe=pd.read_csv("/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/edge_level/np_baseline_and_modulated_per_edge_6models.csv")
s=pe[pe.model=='1b'].groupby(['sub_id','condition']).value.sum().unstack()
from scipy.stats import binomtest
long1b = pe[pe.model=='1b'].pivot_table(index=['sub_id','edge'],columns='condition',values='value')
EORD=[f'edge{i}' for i in range(1,13)]
rows=[]
for drug in ['ampa','gaba']:
    dsum = s[drug]-s['baseline']                      # per-subject Delta NP sum
    for e in EORD:
        sub = long1b.xs(e,level='edge')
        de = sub[drug]-sub['baseline']
        conc = np.sign(de)==np.sign(dsum.loc[de.index])
        k=int(conc.sum())
        bt=binomtest(k,12,0.5,alternative='two-sided')
        rows.append(dict(model='1b', modulation={'ampa':'AMPA','gaba':'GABA-A'}[drug],
                         edge='E'+e.replace('edge',''), task='SST' if int(e[4:])<=6 else 'MID',
                         n=12, n_concordant=k, pct=round(100*k/12,1),
                         mean_delta_edge=round(float(de.mean()),4),
                         sd_delta_edge=round(float(de.std(ddof=1)),4),
                         p_binom=float(f'{bt.pvalue:.3g}')))
conc_tab=pd.DataFrame(rows)
conc_tab['q_bh']=multipletests(conc_tab.p_binom,method='fdr_bh')[1].round(4)

# ---- computation: recovered from execution-log cell 284588c4
D3='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data'
conc_tab.to_csv(f'{D3}/fig3h_edge_direction_1b.csv', index=False)
