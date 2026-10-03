"""fig4_mid_by_np_grouping_n288  -  MID summed FC by diagnostic group, grouped by the NP-factor response pattern

Computes
    MID summed FC by diagnostic group, grouped by the NP-factor response
    pattern.

Inputs
    04_figures/fig.4/fig4_data  (staged read-only into the scratch mirror)

Output
    $FIG4_OUT/figures/fig.4/fig4_data/fig4_mid_by_np_grouping_n288.csv  (default $FIG4_OUT = 03_analysis/fig4/_scratch)
    reference copy: 04_figures/fig.4/fig4_data/fig4_mid_by_np_grouping_n288.csv

Statistical tests
    One-way ANOVA / Kruskal-Wallis across groups, with group means and SDs.

Cohort
    n = 288.

Runs on a laptop
    yes - seconds on a laptop.

seed
    no random component

Rebuilt from execution-log cell
    d556a9ba-afe4-4e91-94c2-17902bc44e68 (frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 21:09:27 UTC, conda env python, exit ok)
    verbatim archive: recovered/fig4/fig4_mid_by_np_grouping_n288__cell_d556a9ba.py
"""
# --- paths (added when the cell was reorganised; the analysis below is verbatim)
import os as _os, shutil as _shutil, sys as _sys
_sys.dont_write_bytecode = True   # never leave caches in the read-only figure tree

PKG      = _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", ".."))
FIGREF   = _os.path.join(PKG, "04_figures")        # reference figure tree: READ ONLY
UPSTREAM = _os.path.join(PKG, "06_upstream_inputs")
AUTHOR_REV = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs"          # author's working tree
AUTHOR_SUB = "/Users/yunman/Desktop/submission"
OUTROOT  = _os.path.abspath(_os.environ.get("FIG4_OUT", _os.path.join(PKG, "03_analysis", "fig4", "_scratch")))
FIGROOT  = _os.path.join(OUTROOT, "figures")       # every write of this script lands here


def _figpath(rel):
    """Path inside the scratch mirror of the figure tree; data inputs are copied
    in from the read-only reference on first use, so nothing writes into
    04_figures."""
    dst = _os.path.join(FIGROOT, rel)
    src = _os.path.join(FIGREF, rel)
    if _os.path.isdir(src):
        for root, _dirs, files in _os.walk(src):
            for f in files:
                if _os.path.splitext(f)[1].lower() in (".csv", ".xlsx", ".xls", ".mat", ".json", ".txt", ".tsv"):
                    s = _os.path.join(root, f)
                    d = _os.path.join(dst, _os.path.relpath(s, src))
                    _os.makedirs(_os.path.dirname(d), exist_ok=True)
                    if not _os.path.exists(d):
                        _shutil.copyfile(s, d)
        _os.makedirs(dst, exist_ok=True)
    else:
        _os.makedirs(_os.path.dirname(dst) or dst, exist_ok=True)
        if _os.path.exists(src) and not _os.path.exists(dst):
            _shutil.copyfile(src, dst)
    return dst


def _upstream(rel):
    """Upstream analysis input: the package copy if it has been shipped, else the
    author's working tree (the path recorded in the header)."""
    for base in (UPSTREAM, AUTHOR_REV):
        p = _os.path.join(base, rel)
        if _os.path.exists(p):
            return p
    raise FileNotFoundError("upstream input not available: " + rel)


def _sub(rel):
    """Input that sits outside revision/ in the author's tree."""
    p = _os.path.join(AUTHOR_SUB, rel)
    if not _os.path.exists(p):
        raise FileNotFoundError("input not available: " + p)
    return p


ARTIFACT_INPUTS = {
    "025c7b13-ece7-4589-af4e-8c4e6f87d905": "empirical_simul_np_fcs_300subs/np_residualized_290subs.csv",
    "24326e31-3946-449a-b811-adc1579b5e98": "baseline_predict_change/dtb_np_n288_baseline_post.csv",
    "3825bfc5-ca4c-4fe5-8041-681d3930ebd1": "corr_hd_np/increased_responder_proportions_n288_corrected.csv",
    "7eddba98-b1cd-403d-ab4f-a8bc7c93eaff": "benchmark_predict_baseline_np/empirical_np_edges_288subjects.csv",
    "c39c8ccc-6410-47df-a102-00903507ebcd": "empirical_simul_np_fcs_300subs/np_all_subs_3m_wide_corrected.csv",
    "c4723113-4cde-4ada-aa70-10d3e8a1a900": ""
}


def _art(vid):
    """Resolve an input the original cell read through the platform artifact
    store to its file in this package or in the author's tree."""
    rel = ARTIFACT_INPUTS.get(vid)
    if rel:
        for base in (UPSTREAM, AUTHOR_REV):
            p = _os.path.join(base, rel)
            if _os.path.exists(p):
                return p
    try:                                    # inside the analysis platform only
        return host.artifact_path(vid)      # noqa: F821
    except Exception:
        raise FileNotFoundError("artifact input not available: %s (%s)" % (vid, rel))


_os.makedirs(FIGROOT, exist_ok=True)


def _byname(fn):
    """An input the original cell looked up by filename in the platform artifact
    store; resolve it by name under the package or the author's tree."""
    for base in (UPSTREAM, AUTHOR_REV):
        for root, _d, files in _os.walk(base):
            if fn in files:
                return _os.path.join(root, fn)
    raise FileNotFoundError("upstream input not available: " + fn)


class _Prefix(str):
    """A directory prefix the original cell built by string concatenation.
    Adding a relative path resolves it against the package copy first, then the
    author's working tree."""

    def __new__(cls, rel):
        o = str.__new__(cls, _os.path.join(AUTHOR_REV, rel) + _os.sep)
        o._rel = rel
        return o

    def __add__(self, rest):
        for base in (UPSTREAM, AUTHOR_REV):
            p = _os.path.join(base, self._rel, str(rest).lstrip("/"))
            if _os.path.exists(p):
                return p
        return _os.path.join(AUTHOR_REV, self._rel, str(rest).lstrip("/"))

# --- write guard: this script must never write outside its scratch directory --
def _assert_out(path):
    p = _os.path.abspath(path)
    root = _os.path.abspath(OUTROOT)
    if not (p == root or p.startswith(root + _os.sep)):
        raise RuntimeError("refusing to write outside $FIG4_OUT: " + p)
    _os.makedirs(_os.path.dirname(p), exist_ok=True)
    return p


import pandas as _pd_guard
import matplotlib.figure as _mplfig

def _wrap_writer(fn):
    def w(self, path_or_buf=None, *a, **k):
        if isinstance(path_or_buf, str):
            path_or_buf = _assert_out(path_or_buf)
        return fn(self, path_or_buf, *a, **k)
    return w

_pd_guard.DataFrame.to_csv = _wrap_writer(_pd_guard.DataFrame.to_csv)
_pd_guard.Series.to_csv = _wrap_writer(_pd_guard.Series.to_csv)
_pd_guard.DataFrame.to_excel = _wrap_writer(_pd_guard.DataFrame.to_excel)
_orig_xlw = _pd_guard.ExcelWriter
def _ExcelWriter(path, *a, **k):
    return _orig_xlw(_assert_out(path) if isinstance(path, str) else path, *a, **k)
_pd_guard.ExcelWriter = _ExcelWriter
_orig_savefig = _mplfig.Figure.savefig
def _savefig(self, fname, *a, **k):
    return _orig_savefig(self, _assert_out(fname) if isinstance(fname, str) else fname, *a, **k)
_mplfig.Figure.savefig = _savefig


# --- recovered analysis (verbatim; only paths and imports were made explicit)
# imports hoisted to the top when the cells were merged
import numpy as np, pandas as pd
from scipy import stats
D4=_figpath('fig.4/fig4_data')
PD=pd.read_csv(f'{D4}/fig4_paired_np_mid_n288.csv'); print(PD.shape, list(PD.columns))
M = PD.copy()
M['d_ampa_mid'] = M.mid_ampa - M.mid_baseline
M['d_gaba_mid'] = M.mid_gaba - M.mid_baseline
M['pattern_mid'] = np.where((M.d_ampa_mid>0)&(M.d_gaba_mid>0), 'both up', 'any down')
M['pattern_np']  = np.where((M.np_ampa-M.np_baseline>0)&(M.np_gaba-M.np_baseline>0),'both up','any down')
OUT=_figpath('fig.4/fig4_data')
M['d_ampa_np'] = M.np_ampa - M.np_baseline; M['d_gaba_np'] = M.np_gaba - M.np_baseline
rows=[]
for col,nm in [('mid_baseline','simulated baseline MID FC'),('d_ampa_mid','MID change after AMPA'),
               ('d_gaba_mid','MID change after GABA-A')]:
    for pat in ['both up','any down']:
        v=M.loc[M.pattern_np==pat,col]; t_,p_=stats.ttest_1samp(v,0)
        rows.append(dict(grouping='NP-based both-up / any-down', group=pat, measure=nm, n=len(v),
                         mean=round(float(v.mean()),4), sd=round(float(v.std(ddof=1)),4),
                         test='one-sample t vs 0', stat=round(float(t_),3), p=float(f'{p_:.3g}')))
    a=M.loc[M.pattern_np=='both up',col]; b=M.loc[M.pattern_np=='any down',col]
    t_,p_=stats.ttest_ind(a,b,equal_var=False); _,pu=stats.mannwhitneyu(a,b)
    sp=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    rows.append(dict(grouping='NP-based both-up / any-down', group='both up vs any down', measure=nm,
                     n=len(M), mean=round(float(a.mean()-b.mean()),4),
                     sd=round(float((a.mean()-b.mean())/sp),3),
                     test=f'Welch t (sd col = Hedges g); Mann-Whitney P = {pu:.3g}',
                     stat=round(float(t_),3), p=float(f'{p_:.3g}')))
    print(f'{nm:28s} both up {a.mean():+.3f} (n={len(a)}) vs any down {b.mean():+.3f} (n={len(b)})  '
          f't={t_:+.2f} P={p_:.3g} MW P={pu:.3g} g={(a.mean()-b.mean())/sp:+.2f}')
MS2=pd.DataFrame(rows)
MS2.to_csv(f'{OUT}/fig4_mid_by_np_grouping_n288.csv', index=False)
