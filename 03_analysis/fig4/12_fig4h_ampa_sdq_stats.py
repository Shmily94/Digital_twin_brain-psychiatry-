"""fig4h_ampa_sdq_stats  -  Panel h (AMPA split)

Computes
    Panel h (AMPA split): SDQ items compared between twins whose NP rose under
    AMPA and those whose NP fell.

Inputs
    04_figures/fig.4  (staged read-only into the scratch mirror)

Output
    $FIG4_OUT/figures/fig.4/fig4_data/fig4h_ampa_sdq_stats.csv  (default $FIG4_OUT = 03_analysis/fig4/_scratch)
    reference copy: 04_figures/fig.4/fig4_data/fig4h_ampa_sdq_stats.csv

Statistical tests
    Mann-Whitney U per item, Hedges' g with a 95% CI, and Benjamini-Hochberg FDR
    across the 26 items.

Cohort
    n = 287.

Runs on a laptop
    yes - seconds on a laptop.

seed
    no random component

Rebuilt from execution-log cell
    37142daa-f186-4e77-98d3-783912832160 (frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 16:16:39 UTC, conda env python, exit ok)
    the computation itself lives in 04_figures/fig.4/fig4.py; this cell authored it
    verbatim archive: recovered/fig4/fig4h_ampa_sdq_stats__cell_37142daa.py

Note
    Written by the same loop in fig4.py as fig4h_sdq_stats.csv.
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
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy import stats
from statsmodels.stats.multitest import multipletests
import statsmodels.formula.api as smf
from PIL import Image
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx
import figA4_kit as PK          # the frozen main-figure type scale, 8/9/10 pt
HERE = _figpath('fig.4')
D = os.path.join(HERE, 'fig4_data')
OUTD = os.path.join(HERE, 'panels')
DPI = 400
PCOL = {'both up': C('increased'), 'any down': C('decreased')}
manifest = []
T = pd.read_csv(f'{D}/fig4_subject_level_n288.csv')
S = pd.read_csv(f'{D}/fig4_sdq_items_n287.csv')
SDQ = [c for c in S.columns if c not in ('ID', 'pattern', 'Group')]
for c in ['empirical', 'simulated', 'ampa', 'gaba']:
    # NB: C() here would be the palette helper, so let patsy treat the
    # string columns as categorical on their own
    # residual + that condition's own mean: covariates are removed but the
    # condition stays on its real NP scale (OLS residuals alone are all
    # forced to mean zero, which would hide the perturbation shift)
    T[c + '_r'] = (smf.ols(f'{c} ~ sex + site + headmotion', data=T).fit().resid
                   + T[c].mean())
def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    with mpl.rc_context({'savefig.bbox': None}):   # else the raster is cropped
        fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)   # and the text layer
                                                           # sits off-register
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}',
                         dpi=round(px[0] / (w_mm / 25.4)), source=note))
    plt.close(fig)
S = S.merge(T[['ID', 'd_ampa']], on='ID')
SPLITS = [('fig4h', 'pattern', 'both up', 'any down', 'both up', 'any down'),
          ('fig4h_ampa', 'ampa_dir', 'AMPA up', 'AMPA down', 'AMPA up', 'AMPA down')]
S['ampa_dir'] = np.where(S.d_ampa > 0, 'AMPA up', 'AMPA down')
for stem, key, up, dn, lab_up, lab_dn in SPLITS:
    rows = []
    for it in SDQ:
        x = S.loc[S[key] == up, it].astype(float)
        y = S.loc[S[key] == dn, it].astype(float)
        u, pu = stats.mannwhitneyu(x, y, alternative='two-sided')
        n1, n2 = len(x), len(y)
        sp = np.sqrt(((n1 - 1) * x.var(ddof=1) + (n2 - 1) * y.var(ddof=1)) / (n1 + n2 - 2))
        gg = (x.mean() - y.mean()) / sp * (1 - 3 / (4 * (n1 + n2) - 9))
        se = np.sqrt((n1 + n2) / (n1 * n2) + gg ** 2 / (2 * (n1 + n2)))
        rows.append(dict(item=it, split=f'{lab_up} vs {lab_dn}', n_up=n1, n_down=n2,
                         mean_up=round(x.mean(), 3), mean_down=round(y.mean(), 3),
                         hedges_g=round(gg, 3), ci_lo=round(gg - 1.96 * se, 3),
                         ci_hi=round(gg + 1.96 * se, 3), U=float(u),
                         p_mw=float(f'{pu:.3g}')))
    H4 = pd.DataFrame(rows)
    H4['q_bh'] = multipletests(H4.p_mw, method='fdr_bh')[1].round(4)
    H4 = H4.sort_values('hedges_g').reset_index(drop=True)
    H4.to_csv(f'{D}/{stem}_sdq_stats.csv', index=False)

    W, H = 180, 58           # 8-10 pt type and 25 rotated item labels
    fig, ax = plt.subplots(figsize=panel(W, H))
    x = np.arange(len(H4))
    sig = (H4.p_mw < .05).values          # nominal P, no multiplicity correction
    cols = [PCOL['both up'] if v > 0 else PCOL['any down'] for v in H4.hedges_g]
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    for i in range(len(H4)):
        ax.vlines(x[i], H4.ci_lo[i], H4.ci_hi[i], color=cols[i], lw=LW, zorder=2)
    ax.scatter(x[sig], H4.hedges_g[sig], s=16,
               facecolor=[c for c, m in zip(cols, sig) if m],
               edgecolor=[c for c, m in zip(cols, sig) if m], linewidth=LW, zorder=3)
    ax.scatter(x[~sig], H4.hedges_g[~sig], s=16, facecolor='white',
               edgecolor=[c for c, m in zip(cols, ~sig) if m], linewidth=LW, zorder=3)
    ylo_lab = float(H4.ci_lo.min())
    for k, i in enumerate(np.where(sig)[0]):   # name the items reaching P < 0.05,
        ax.text(x[i] + .25, ylo_lab - .03 - .10 * k,   # stacked so labels never
                f'P = {H4.p_mw[i]:.3g}', ha='left',    # overlap when adjacent
                va='top', fontsize=PK.ANNOT_PT, color=cols[i])
    ax.set_ylim(float(H4.ci_lo.min()) - .10 * max(1, int(sig.sum())) - .10,
                float(H4.ci_hi.max()) + .16)
    ax.set_xticks(x)
    ax.set_xticklabels(H4.item, fontsize=PK.TICK_PT, rotation=45, ha='right')
    ax.tick_params(axis='y', labelsize=PK.TICK_PT)
    ax.set_xlim(-.7, len(H4) - .3)
    ax.set_ylabel("Hedges' $g$\n" + f'({lab_up} \u2212 {lab_dn})',
                  fontsize=PK.LABEL_PT)
    handles = [Patch(facecolor=PCOL['both up'], edgecolor='none'),
               Patch(facecolor=PCOL['any down'], edgecolor='none'),
               Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                      markerfacecolor='white', markeredgecolor='0.4',
                      markeredgewidth=LW)]
    ax.legend(handles, [f'higher in "{lab_up}"', f'higher in "{lab_dn}"',
                       'P \u2265 0.05'],
              loc='upper left', ncol=3, fontsize=PK.ANNOT_PT, handletextpad=.4,
              columnspacing=1.0, borderaxespad=.2)
    _s = H4.item[sig].tolist()
    # no declarative panel title: the group sizes, the named items and the
    # uncorrected-P caveat belong in the legend (house rule)
    enforce(fig); save(fig, stem, W, H, 'fig4_sdq_items_n287.csv')
    print(f'{stem}: ' + ', '.join(f'{i} (P={q:.3g}, g={g:.2f})'
          for i, q, g in zip(H4.item[sig], H4.p_mw[sig], H4.hedges_g[sig])))
# this script reports the 'fig4h_ampa' arm of the loop above

