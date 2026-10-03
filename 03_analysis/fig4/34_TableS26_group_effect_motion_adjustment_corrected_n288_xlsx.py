"""TableS26_group_effect_motion_adjustment_corrected_n288_xlsx  -  Excel copy of Table S26 (corrected), single sheet 'Table S26 (corrected)'

Computes
    Excel copy of Table S26 (corrected), single sheet 'Table S26 (corrected)'.

Inputs
    04_figures/fig.4/fig4_data  (staged read-only into the scratch mirror)
    04_figures/  (scratch mirror root)
    04_figures/supp_motion  (staged read-only into the scratch mirror)
    /Users/yunman/Desktop/submission/  (author's tree, not shipped in this package)

Output
    $FIG4_OUT/figures/supp_motion/data/TableS26_group_effect_motion_adjustment_corrected_n288.xlsx  (default $FIG4_OUT = 03_analysis/fig4/_scratch)
    reference copy: 04_figures/supp_motion/data/TableS26_group_effect_motion_adjustment_corrected_n288.xlsx

Statistical tests
    None - format conversion of the CSV.

Cohort
    n = 288.

Runs on a laptop
    partial - one or more inputs are not shipped in this package (listed under
    Inputs); with them present it runs on a laptop in seconds.

seed
    no random component

Rebuilt from execution-log cell
    1c75aa2e-28a8-487e-999c-fc7fca6bf6a9 (frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 21:53:03 UTC, conda env python, exit ok)
    verbatim archive: recovered/fig4/TableS26_group_effect_motion_adjustment_corrected_n288_xlsx__cell_1c75aa2e.py
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
import scipy.io as sio, pandas as pd, numpy as np, os
import statsmodels.formula.api as smf, statsmodels.api as sm2
D4=_figpath('fig.4/fig4_data')
B=_sub('')
SL4=pd.read_csv(f'{D4}/fig4_subject_level_n288.csv')
FIG=_figpath('')
dirs={k: f'{FIG}/supp_{k}' for k in ['assim','fingerprint','conductance','eft','motion']}
OUTM=f"{dirs['motion']}/data"
M2=SL4[['ID','Group','sex','site','headmotion','empirical','simulated','ampa','gaba']].copy()
M2['d_ampa']=M2.ampa-M2.simulated; M2['d_gaba']=M2.gaba-M2.simulated
M2['grp']=M2.Group.astype('category'); M2['fd']=M2.headmotion
M2['sx']=M2.sex.astype('category'); M2['st']=M2.site.astype('category')
def peta(formula, term='grp'):
    mod=smf.ols(formula, data=M2).fit(); a=sm2.stats.anova_lm(mod, typ=2)
    ss=a.loc[term,'sum_sq']; ssr=a.loc['Residual','sum_sq']
    return ss/(ss+ssr), float(a.loc[term,'F']), float(a.loc[term,'PR(>F)']), int(a.loc[term,'df']), int(mod.df_resid)
ROWS2=[('Empirical NP factor','empirical'),('Simulated NP','simulated'),
       ('Manipulated NP (AMPA)','ampa'),('Manipulated NP (GABA-A on high AMPA)','gaba'),
       ('Delta NP (AMPA)','d_ampa'),('Delta NP (GABA-A on high AMPA)','d_gaba')]
gr=[]
for lab,c in ROWS2:
    e0,F0,p0,df0,dr0 = peta(f'{c} ~ grp')
    e1,F1,p1,df1,dr1 = peta(f'{c} ~ grp + fd')
    e2,F2,p2,df2,dr2 = peta(f'{c} ~ grp + fd + sx + st')
    gr.append(dict(Measure=lab, n=len(M2),
                   eta2_group_no_FD=round(100*e0,2), F_no_FD=round(F0,3),
                   P_no_FD=float(f'{p0:.3g}'), df_no_FD=f'{df0}, {dr0}',
                   eta2_group_with_FD=round(100*e1,2), F_with_FD=round(F1,3),
                   P_with_FD=float(f'{p1:.3g}'), df_with_FD=f'{df1}, {dr1}',
                   eta2_group_full_cov=round(100*e2,2), P_full_cov=float(f'{p2:.3g}'),
                   df_full_cov=f'{df2}, {dr2}'))
GR=pd.DataFrame(gr)
GR['P_no_FD_bonf']=np.minimum(1,GR.P_no_FD*len(GR)).round(4)
GR['P_with_FD_bonf']=np.minimum(1,GR.P_with_FD*len(GR)).round(4)
GR['P_full_cov_bonf']=np.minimum(1,GR.P_full_cov*len(GR)).round(4)
GR.to_csv(f'{OUTM}/TableS26_group_effect_motion_adjustment_corrected_n288.csv', index=False)
_os.chdir(_figpath('supp_motion'))

# --- final step, verbatim from bash cell 1c75aa2e (heredoc, cwd = supp_motion)
d=pd.read_csv('data/TableS26_group_effect_motion_adjustment_corrected_n288.csv')
with pd.ExcelWriter('data/TableS26_group_effect_motion_adjustment_corrected_n288.xlsx') as w:
    d.to_excel(w, sheet_name='Table S26 (corrected)', index=False)

