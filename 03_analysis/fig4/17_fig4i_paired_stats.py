"""fig4i_paired_stats  -  Panel i

Computes
    Panel i: per-twin paired comparison of the simulated baseline against each
    perturbation, for the 12-edge NP factor and for the 6 MID edges.

Inputs
    04_figures/fig.4  (staged read-only into the scratch mirror)

Output
    $FIG4_OUT/figures/fig.4/fig4_data/fig4i_paired_stats.csv  (default $FIG4_OUT = 03_analysis/fig4/_scratch)
    reference copy: 04_figures/fig.4/fig4_data/fig4i_paired_stats.csv

Statistical tests
    Paired t test, Wilcoxon signed-rank test, Cohen's d_z, and the proportion of
    twins that increased.

Cohort
    n = 288.

Runs on a laptop
    yes - seconds on a laptop.

seed
    np.random.default_rng(4) is fixed in the original code (plot jitter only)

Rebuilt from execution-log cell
    430c5712-5091-41c6-b544-5d65d756d89c (frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 16:30:21 UTC, conda env python, exit ok)
    the computation itself lives in 04_figures/fig.4/fig4.py; this cell authored it
    verbatim archive: recovered/fig4/fig4i_paired_stats__cell_430c5712.py
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
_sys.path.insert(0, _os.path.join(FIGREF, 'fig_color'))
_sys.path.insert(0, FIGREF)
import matplotlib as _mpl; _mpl.use('Agg')
# imports hoisted to the top when the cells were merged
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
HERE = _figpath('fig.4')
D = os.path.join(HERE, 'fig4_data')
PD = pd.read_csv(f'{D}/fig4_paired_np_mid_n288.csv')
CONDS = [('baseline', 'Baseline', C('baseline')), ('ampa', '+AMPA', C('ampa')),
         ('gaba', '+GABA-A', C('gaba'))]
PMEAS = [('np', 'NP factor (12 edges)'), ('mid', 'MID summed FC (6 edges)')]
PAIR_POINTS = False        # False = no jittered per-twin points
PAIR_LINES  = False        # at n = 288 the 576 connecting strokes carry no
W, H = 110, 56
fig, axes = plt.subplots(1, 2, figsize=panel(W, H), gridspec_kw=dict(wspace=.42))
prows = []
rng = np.random.default_rng(4)
for ax, (meas, mlab) in zip(axes, PMEAS):
    vals = [PD[f'{meas}_{k}'].values for k, _, _ in CONDS]
    if PAIR_LINES:                                        # per-twin pairing
        for j, (k, _, col) in enumerate(CONDS[1:], start=1):
            for y0, y1 in zip(vals[0], vals[j]):
                ax.plot([0, j], [y0, y1], color=col, lw=LW * .6, alpha=.10, zorder=1)
    bp = ax.boxplot(vals, positions=np.arange(3), widths=.5, showfliers=False,
                    patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    if PAIR_POINTS:            # the connecting lines already show every twin,
        for j, (k, _, col) in enumerate(CONDS):     # so the points are optional
            ax.scatter(j + rng.uniform(-.11, .11, len(vals[j])), vals[j], s=2.6,
                       facecolor=col, edgecolor='none', alpha=.7, zorder=3)
    else:                      # colour the box instead, so the condition is still
        for j, (k, _, col) in enumerate(CONDS):     # identifiable without points.
            rgb = np.array(plt.matplotlib.colors.to_rgb(col))   # opaque light tint
            bp['boxes'][j].set_facecolor(tuple(1 - .42 * (1 - rgb)))  # so the lines
            bp['boxes'][j].set_zorder(2.5)                            # don't muddy it
            for el in ('whiskers', 'caps', 'medians'):
                for art in bp[el]:
                    art.set_zorder(2.6)
    hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
    step = (hi - lo) * .12
    y = hi + step * .4
    for j, (k, _, col) in enumerate(CONDS[1:], start=1):
        t_, p_ = stats.ttest_rel(vals[j], vals[0])
        dd = vals[j] - vals[0]
        w_, pw = stats.wilcoxon(vals[j], vals[0])
        prows.append(dict(measure=mlab, perturbation=CONDS[j][1].lstrip('+'),
                          n=len(dd), mean_baseline=round(vals[0].mean(), 4),
                          mean_modulated=round(vals[j].mean(), 4),
                          mean_diff=round(dd.mean(), 4), sd_diff=round(dd.std(ddof=1), 4),
                          n_increased=int((dd > 0).sum()),
                          pct_increased=round(100 * (dd > 0).mean(), 1),
                          t=round(float(t_), 3), df=len(dd) - 1,
                          p_paired_t=float(f'{p_:.3g}'), wilcoxon_p=float(f'{pw:.3g}'),
                          cohens_dz=round(float(dd.mean() / dd.std(ddof=1)), 3)))
        ax.plot([0, 0, j, j], [y, y + step * .3, y + step * .3, y], color='black', lw=LW)
        ax.text(1.0, y + step * .38,   # centred on the axis, clear of the y labels
                f'$t$({len(dd)-1}) = {t_:.1f}, $P$ = {p_:.0e}\n$d_z$ = '
                f'{dd.mean()/dd.std(ddof=1):.2f}, {100*(dd>0).mean():.0f}% up',
                ha='center', va='bottom', fontsize=ANNOT_PT)
        y += step * 2.5
    ax.set_ylim(lo - step * .4, y + step * .2)
    ax.set_xticks(range(3)); ax.set_xticklabels([c[1] for c in CONDS], fontsize=TICK_PT)
    ax.set_xlim(-.6, 2.6)
    ax.set_ylabel(mlab)
    panel_title(ax, {'np': 'Whole 12-edge NP factor',
                     'mid': 'MID edges only (6 of the 12)'}[meas])
PTT = pd.DataFrame(prows)
PTT.to_csv(f'{D}/fig4i_paired_stats.csv', index=False)
