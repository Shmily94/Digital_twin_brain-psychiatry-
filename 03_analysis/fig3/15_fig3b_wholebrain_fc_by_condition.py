"""fig3b_wholebrain_fc_by_condition.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code builds a comparison table of whole-brain functional
    connectivity (FC) similarity between simulated and empirical data
    across nine model variants: six DTB simulation configurations spanning
    different simulation scales, data resolutions, and assimilation scales
    (from 3 million to 1 billion units, at parcel or voxel resolution),
    plus two alternative fitting models (SAR and rWW). For each of the
    four task conditions (SST Stop Success, SST Stop Failure, MID Reward
    Anticipation, MID Positive Feedback), it computes the mean and
    standard deviation across 12 subjects of the correlation between
    simulated and empirical FC, formatted as a mean-plus-or-minus-std
    string, and also computes an overall four-condition mean and std per
    model variant. One row of the output table therefore corresponds to a
    single model configuration (for example one simulation scale and
    resolution combination, or the SAR or rWW model), reporting which
    empirical FC

INPUT FILES
    fig3b_wholebrain_fc_crossscale.csv

OUTPUT FILE
    fig3b_wholebrain_fc_by_condition.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3b_wholebrain_fc_by_condition.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 9898be5e-14e3-4830-a60d-c39f6d3c2ffa
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 15:04:04 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3b_wholebrain_fc_by_condition__cell_9898be5e.py
    candidates found   : 3

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
#      (cells 1dbf78d8, 457de626, 49894910, 706899db, c5edbd78)
R='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
FIG=R+'figures/'
D3=FIG+'fig.3/fig3_data/'
def ms(m,s,p=4): return f'{m:.{p}f} ± {s:.{p}f}'
B=pd.read_csv(D3+'fig3b_wholebrain_fc_crossscale.csv')

# ---- computation: recovered from execution-log cell 9898be5e
ORD=['SST Stop Success','SST Stop Failure','MID Reward Antici.','MID Pos. Feedback']
MLAB={'3m_268':'3 M / 268','10m_268':'10 M / 268','10m_1000':'10 M / 1000',
      '10m_own':'10 M voxel, 10 M hyper','10m_voxel':'10 M voxel, 100 M hyper',
      '100m_voxel':'100 M voxel','1b_voxel':'1 B voxel','SAR':'SAR','RWW':'rWW'}
piv=B.pivot_table(index='model',columns='condition',values=['r_mean','r_sd'])
rows=[]
for m in ['3m_268','10m_268','10m_1000','10m_own','10m_voxel','100m_voxel','1b_voxel','SAR','RWW']:
    d={'build':MLAB[m],'n':int(B[B.model==m].n.iloc[0])}
    for c in ORD: d[c]=ms(piv.loc[m,('r_mean',c)],piv.loc[m,('r_sd',c)])
    d['mean of 4 conditions']=f"{B[B.model==m].r_mean.mean():.4f}"
    rows.append(d)
WBT=pd.DataFrame(rows)
WBT.to_csv(D3+'fig3b_wholebrain_fc_by_condition.csv',index=False)
