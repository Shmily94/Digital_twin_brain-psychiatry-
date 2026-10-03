"""fig3h_claim_support_1b.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code compares neural pathway (NP) edge changes under two
    pharmacological modulations (AMPA and GABA-A) against a baseline
    condition, using model 1b data for 12 edges across subjects. For each
    drug, it computes the group-level mean change in summed NP value,
    checks how many of the 12 edges have mean change in the same direction
    as that group mean, and separately counts, per subject, how many of
    the 12 edges shift in a concordant direction, testing that per-subject
    count against a chance value of 6 via a one-sample t-test and a
    Wilcoxon signed-rank test. It also measures how concentrated the
    absolute change is across edges by computing, per subject, the share
    of total absolute change carried by the single largest edge and the
    minimum number of edges needed to account for at least half of the
    total absolute change, then averages these across subjects. One row of
    the output table corresponds to one modulation condition (AMPA or
    GABA-A), summarizing these group-level and subject

INPUT FILES
    (no external file path appears in the recovered slice)

OUTPUT FILE
    fig3h_claim_support_1b.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3h_claim_support_1b.csv

STATISTICAL TESTS
    one-sample two-sided t test
    Wilcoxon signed-rank test

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : ab30ab4e-bdcd-4b3c-9fc0-b792607c2cc9
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-21 15:37:53 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3h_claim_support_1b__cell_ab30ab4e.py
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
#      (cells 2f52d573, 5eb2d51f, 5fff7e36, bbc97276)
pe=pd.read_csv("/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/edge_level/np_baseline_and_modulated_per_edge_6models.csv")
s=pe[pe.model=='1b'].groupby(['sub_id','condition']).value.sum().unstack()
EORD=[f'edge{i}' for i in range(1,13)]
long1b = pe[pe.model=='1b'].pivot_table(index=['sub_id','edge'],columns='condition',values='value')
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
from scipy import stats
res={}
for drug in ['ampa','gaba']:
    dsum = s[drug]-s['baseline']
    # group level: sign of the MEAN edge change vs sign of the MEAN summed change
    ge = long1b.groupby('edge').apply(lambda z: (z[drug]-z['baseline']).mean()).loc[EORD]
    res[drug]=dict(group_mean_dNP=float(dsum.mean()),
                   group_edges_same_sign=int((np.sign(ge)==np.sign(dsum.mean())).sum()))
    # subject level: n concordant edges out of 12, tested against chance (6)
    cnt = psub[psub.modulation==('AMPA' if drug=='ampa' else 'GABA-A')].n_edges_concordant.values
    t_,p_ = stats.ttest_1samp(cnt,6.0)
    w_,pw_ = stats.wilcoxon(cnt-6.0)
    res[drug].update(mean_conc=float(cnt.mean()), sd=float(cnt.std(ddof=1)),
                     t=float(t_), p=float(p_), wilcoxon_p=float(pw_),
                     pct=100*cnt.mean()/12)
    # how concentrated is the change?  share of total |delta| carried by the largest edge,
    # and how many edges are needed to reach 50% of the total absolute change
    tops, nhalf = [], []
    for sid in s.index:
        de=(long1b.xs(sid,level='sub_id').loc[EORD][drug]-long1b.xs(sid,level='sub_id').loc[EORD]['baseline']).abs().values
        de=np.sort(de)[::-1]; c=np.cumsum(de)/de.sum()
        tops.append(de[0]/de.sum()); nhalf.append(int(np.argmax(c>=.5))+1)
    res[drug].update(top_edge_share=float(np.mean(tops)), n_edges_for_half=float(np.mean(nhalf)))

# ---- computation: recovered from execution-log cell ab30ab4e
sup=pd.DataFrame([dict(modulation='AMPA', **res['ampa']), dict(modulation='GABA-A', **res['gaba'])])
sup=sup.rename(columns={'mean_conc':'mean_edges_concordant_of12','sd':'sd_edges_concordant',
                        't':'t_vs_chance6','p':'p_vs_chance6','pct':'pct_edges_concordant',
                        'group_edges_same_sign':'group_level_edges_same_sign_of12',
                        'top_edge_share':'mean_share_of_total_abs_change_largest_edge',
                        'n_edges_for_half':'mean_n_edges_for_50pct_of_abs_change'})
sup=sup.round(4)
p='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data/fig3h_claim_support_1b.csv'
sup.to_csv(p,index=False)
