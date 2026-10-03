"""fig3c_similarity_pvalues.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code compares "connectivity profiles" (12 edge values per
    subject) across seven different pipeline builds, for ten selected
    pairs of builds grouped into three family relationships (within voxel
    family, within regional family, between families). For each pair it
    pools all subjects and edges together to get one Spearman correlation,
    separately computes a per-subject Spearman correlation across the 12
    edges and tests whether that within-subject correlation is reliably
    nonzero via a one-sample t-test on Fisher-transformed values, and also
    runs a permutation test that shuffles edge order within each subject
    to build a null distribution for the pooled correlation. One row of
    the output table therefore represents a single build-pair comparison,
    reporting its pooled correlation and naive p-value, the mean and
    spread of the twelve within-subject correlations plus how many were
    positive, the t-statistic and p-value for the within-subject test, and
    the permutation-based p-value for the pooled correlation along with a
    note

INPUT FILES
    np12_edges_12subs_by_build_and_state.csv

OUTPUT FILE
    fig3c_similarity_pvalues.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3c_similarity_pvalues.csv

STATISTICAL TESTS
    one-sample two-sided t test
    Spearman rank correlation
    permutation test
    Fisher z transform

RUNNABLE ON A LAPTOP
    no -- a name inherited from the session could not be recovered; see the NOT RECOVERED block

SEED
    fixed in the original run (seed = 0)

PROVENANCE
    execution-log cell : b42ded68-ec4f-4c9e-8bee-77c2935547bf
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-23 17:01:07 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3c_similarity_pvalues__cell_b42ded68.py
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

from scipy import stats as st
from scipy.stats import spearmanr
import numpy as np
import pandas as pd

# -------------------------------------------------------------------------
# NOT RECOVERED.  This script needs the name(s)
#     R
# which the interactive session inherited from a cell that is not present in
# the execution log (or, for `host`, from the platform session object).  The
# script therefore cannot run as shipped.  They are used below as:
#     FIG=R+'figures/'
#     R=pd.DataFrame(rows)
#     R.insert(1,'family_role',['within voxel family (100 M hyper)']*3+['wit
# Supply them before running.  Nothing has been invented in their place.
# -------------------------------------------------------------------------

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 49894910, 706899db, 821bf2cd, 94c7c2fe, cb450b31, f2c30c3d, fcd11712)
FIG=R+'figures/'
SUB='/Users/yunman/Desktop/submission/'
D3=FIG+'fig.3/fig3_data/'
O=SUB+'revision/text/figures/fig.3/fig3_simulated_fc_12subs/'
NPt=pd.read_csv(O+'np12_edges_12subs_by_build_and_state.csv')
E12=[f'edge{k}' for k in range(1,13)]
BU=['3m_268','10m_268','10m_1000','10m_own','10m','100m','1b']
PROF={b:NPt[(NPt.build==b)&(NPt.state=='baseline')].set_index('subject_id').loc[
        [int(s) for s in NPt[NPt.build=='3m_268'].subject_id],E12].values for b in BU}
BETW=[(a,b) for a in ['3m_268','10m_268'] for b in ['10m','100m','1b']]
REGF=[('3m_268','10m_268')]
VOX=[('10m','100m'),('10m','1b'),('100m','1b')]
def pair_stats(x,y,nperm=20000,seed=0):
    A_,B_=PROF[x],PROF[y]
    sr=spearmanr(A_.ravel(),B_.ravel()); rho=sr.statistic
    # within-participant rho across the 12 edges, then a participant-level test
    wr=np.array([spearmanr(A_[i],B_[i]).statistic for i in range(12)])
    z=np.arctanh(np.clip(wr,-.999999,.999999)); tt=st.ttest_1samp(z,0)
    # participant-block permutation of the POOLED rho: shuffle edge order within
    # each participant independently in one build, which breaks the edge
    # correspondence while keeping every participant's own distribution intact
    rng=np.random.default_rng(seed); null=np.empty(nperm)
    for k in range(nperm):
        Bp=np.array([B_[i][rng.permutation(12)] for i in range(12)])
        null[k]=spearmanr(A_.ravel(),Bp.ravel()).statistic
    p_perm=(1+np.sum(np.abs(null)>=abs(rho)))/(nperm+1)
    return dict(pair=f'{x} vs {y}',rho_pooled=round(rho,4),p_naive_144cells=sr.pvalue,
                within_subj_rho_mean=round(wr.mean(),4),within_subj_rho_sd=round(wr.std(ddof=1),4),
                n_pos_of_12=int((wr>0).sum()),t_11=round(tt.statistic,3),p_participant=tt.pvalue,
                p_block_perm=p_perm)
rows=[pair_stats(*p,nperm=5000) for p in VOX+REGF+BETW]
R=pd.DataFrame(rows)

# ---- computation: recovered from execution-log cell b42ded68
R.insert(1,'family_role',['within voxel family (100 M hyper)']*3+['within regional family (3 M-268 hyper)']+
         ['between families']*6)
R['n_participants']=12
R['n_cells_pooled']=144
R['p_block_perm_note']='5,000 participant-block permutations; 0 exceedances, so P is at the resolution floor 1/5001'
R.to_csv(D3+'fig3c_similarity_pvalues.csv',index=False)
