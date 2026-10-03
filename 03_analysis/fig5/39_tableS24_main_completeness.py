#!/usr/bin/env python3
"""tableS24_main_completeness.csv

Computes
    Row-by-row extraction of the main-figure rows of Supplementary Table S24
    (figure, panel, quantity, statistic, P, effect size, CI), used to check
    that every main-figure quantity carries an effect size and a confidence
    interval.

Inputs
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/14e6f0b7-ee8b-47be-b546-5b12e8540cfc/vfdcde268_280926NatMed_Response_Letter_R1-R4_Claude.docx
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/2b769225-2f82-481d-9d62-9dbbcd5caa07/vf41d01db_290926Supplementary_Information_legends.docx
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/6968fd84-488d-4ed8-ac18-99a9cba0fab6/v5b379bf7_docxedit.py
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/a42c58ac-1e77-4fc4-9b5b-31288ffc2530/vcbd180f3_290926Suppl.Table.xlsx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/280926Supplementary_Information_legends_tracked.docx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/290926NatMed_Manuscript_reviewed_tracked.docx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/290926Suppl.Table_reviewed.xlsx
    - (path built in the chain) 'T_in.xlsx'

Output
    04_figures/_recovered_session_b194cd74/tableS24_main_completeness.csv

Statistical tests
      - none in this script's own computation: it assembles a source-data /
        audit table, and the tests that use it are named in the scripts of
        the tables downstream
    in the recovered chain that prepares its inputs:
      - outcome-permutation null
      - intraclass correlation

Local runnability
    no (local_runnable = no).  Verification: not_run.
    re-run stops at a missing upstream input: /Users/yunman/Desktop/submission
    /revision/text/280926Supplementary_Information_legends_tracked.docx. The
    recovered chain reads the pre-revision manuscript/supplementary files by
    their original names; those files were renamed later in the revision, so
    the derivation is documented but not re-runnable as written
Recovered from
    execution-log cell dda374a2-76ad-44f6-bbf2-c3f8eee52589
    frame b194cd74-5255-435a-9c1e-206638f9adae, cell_index 600, 2026-09-29 11:50 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    2e5aff97, 85b127f1, 00dba3c4, 1300c438, f2540348, 5788277d, dffd61a6,
    528f121b, 0f4f92b0, b9313cf9, 5074a2e6, 9611395d, 5d7d66f3, 29f9f2df,
    830faf45, df49a836, 1098206c, dd87155c, 06d62cd8, 8f33a7a1, dda374a2

Random seed
    fixed in the original run: seed = 0.  Re-running therefore reproduces the
    permutation / resampling statistics     exactly.  No seed was added or
    changed during recovery.

Notes
    Rebuilt by the statistics-layer recovery (docs/RECOVERY_PROTOCOL.md).  The
    computation is the recovered cell chain unchanged: same tests, same
    covariates, same corrections, same seeds.  Only the header, the explicit
    output path and the suppression of the original session's side outputs were
    added.  Lines marked "[recovery: side output suppressed]" wrote files other
    than this script's one deliverable into the author's working tree; they are
    commented out so that running this script cannot modify anything outside
    OUT_DIR.  The verbatim terminal cell is archived at
    recovered/fig5/tableS24_main_completeness__cell_dda374a2.py
"""
import os
import sys

OUT_DIR = os.environ.get(
    "RECOVERY_OUT_DIR",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scratch"))
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- cell 2e5aff97 (cell_index 448)
# [recovery] this cell raised in the original session at its line 7; only the
# statements that had already executed are carried over
import zipfile, re, os, shutil, glob, json, math, collections
import numpy as np, pandas as pd, openpyxl
from lxml import etree
dest='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'
XL=dest+'280926Suppl.Table_v5.xlsx'

# ---------------------------------------------------------------- cell 85b127f1 (cell_index 489)
# [recovery] this cell raised in the original session at its line 4; only the
# statements that had already executed are carried over
import shutil, os
shutil.copy('/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/6968fd84-488d-4ed8-ac18-99a9cba0fab6/v5b379bf7_docxedit.py','docxedit.py')

# ---------------------------------------------------------------- cell 00dba3c4 (cell_index 490)
# [recovery] this cell raised in the original session at its line 6; only the
# statements that had already executed are carried over
import sys; sys.path.append(os.getcwd())
import docxedit
doc=docxedit.TrackedDoc(SI if 'SI' in dir() else '/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/280926Supplementary_Information_legends_tracked.docx', author='Claude')
SI='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/280926Supplementary_Information_legends_tracked.docx'

# ---------------------------------------------------------------- cell 1300c438 (cell_index 498)
import zipfile, collections
from lxml import etree
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
RL='/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/14e6f0b7-ee8b-47be-b546-5b12e8540cfc/vfdcde268_280926NatMed_Response_Letter_R1-R4_Claude.docx'
z=zipfile.ZipFile(RL); print([n for n in z.namelist() if n.startswith('word/') and n.endswith('.xml')][:15])
root=etree.fromstring(z.read('word/document.xml'))
c=collections.Counter()
for tag in ('ins','del','pPrChange','rPrChange','moveFrom','moveTo'):
    for e in root.iter(W+tag): c[(tag,e.get(W+'author'))]+=1
print('revisions:', dict(c))
print('comments part:', 'word/comments.xml' in z.namelist())
paras=root.findall('.//'+W+'body//'+W+'p')
print('paras', len(paras))

# ---------------------------------------------------------------- cell f2540348 (cell_index 499)
def ptext(p, mode='accept'):
    out=[]
    for node in p.iter():
        if node.tag==W+'t':
            anc={a.tag for a in node.iterancestors()}
            if mode=='accept' and W+'del' in anc: continue
            if mode=='reject' and W+'ins' in anc: continue
            out.append(node.text or '')
        elif node.tag==W+'delText' and mode=='reject':
            out.append(node.text or '')
        elif node.tag==W+'tab': out.append('\t')
    return ''.join(out)
acc=[ptext(p) for p in paras]
open('rl_accepted.txt','w').write('\n'.join('%d\t%s'%(i,t) for i,t in enumerate(acc)))
# comments
cr=etree.fromstring(z.read('word/comments.xml'))
cm={}
for cel in cr.iter(W+'comment'):
    cid=cel.get(W+'id'); cm[cid]=(cel.get(W+'author'), ''.join(t.text or '' for t in cel.iter(W+'t')).strip())
# anchor paragraph for each comment
anch={}
for i,p in enumerate(paras):
    for e in p.iter():
        if e.tag in (W+'commentRangeStart', W+'commentReference'):
            cid=e.get(W+'id')
            anch.setdefault(cid, i)
print('COMMENTS (%d):'%len(cm))
for cid,(au,tx) in sorted(cm.items(), key=lambda kv:int(kv[0])):
    print('\n--- id%s [%s] para %s'%(cid,au,anch.get(cid)))
    print(tx[:1200])

# ---------------------------------------------------------------- cell 5788277d (cell_index 502)
FILES={'MS':'14ee7f62-5e94-47c9-838c-3f3f82db848a','MET':'13d8a62b-c4cf-46f5-a102-3538544fe331','SI':'f41d01db-37b1-4977-a6cc-5e5eaa4ad3c4'}
TXT={}
for k,v in FILES.items():
    None; None  # [recovery: unresolvable interactive debris removed]  # [recovery: unresolvable interactive debris removed]
    ps=rr.findall('.//'+W+'body//'+W+'p')
    TXT[k]=[ptext(p) for p in ps]
    pass  # [recovery: side output suppressed] open('cur_%s.txt'%k,'w').write('\n'.join('%d\t%s'%(i,t) for i,t in enumerate(TXT[k])))
    print(k, len(ps), 'paras,', sum(len(t) for t in TXT[k]), 'chars')
xl=openpyxl.load_workbook('/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/a42c58ac-1e77-4fc4-9b5b-31288ffc2530/vcbd180f3_290926Suppl.Table.xlsx')
print('table sheets:', len(xl.sheetnames))
w24=xl['Table S24']; S24=[[('' if c is None else str(c).strip()) for c in r[:17]] for r in w24.iter_rows(min_row=1, values_only=True)]
print('S24 rows:', sum(1 for r in S24 if r[0] or r[1]))
KEYS=['0.09','Bonferroni','Benjamini','0.0072','permutation','restoration','ΔR','R2','Δ R']
for k in ['MS','MET','SI']:
    print('\n==',k)
    for kw in ['r = 0.09','Bonferroni','Benjamini','0.0072','0.0095','ΔR']:
        idx=[i for i,t in enumerate(TXT[k]) if kw in t]
        print('  %-12s %s'%(kw, idx[:12]))

# ---------------------------------------------------------------- cell dffd61a6 (cell_index 504)
import re
RX=re.compile(r'([A-Za-zΔ][A-Za-zΔ²\s\.\-\(\)0-9,]{0,18}?)\s*=\s*(-?\d+(?:\.\d+)?(?:\s*[×x]\s*10[-−–\u2212]?\d+)?)')
def stats_of(lines):
    out=collections.defaultdict(set)
    for i,t in enumerate(lines):
        for m in RX.finditer(t):
            lab=re.sub(r'\s+',' ',m.group(1)).strip(' ,.(')
            if len(lab)<1 or lab.lower() in ('and','or','the','of','to'): continue
            out[(lab, m.group(2))].add(i)
    return out
SL=stats_of(acc)
FL={k:stats_of(TXT[k]) for k in TXT}
allf=set()
for k in FL: allf|=set(FL[k].keys())
# letter stats absent from all files
labs_in_files=collections.defaultdict(set)
for (lab,val) in allf: labs_in_files[lab].add(val)
miss=[(lab,val,sorted(SL[(lab,val)])) for (lab,val) in SL if (lab,val) not in allf and lab in labs_in_files]
print('letter stats whose label exists in the current files but with a different value: %d'%len(miss))
for lab,val,ps in sorted(miss, key=lambda x:x[2]):
    print('  para%-5s %-14s letter=%-10s files=%s'%(ps[0], lab, val, sorted(labs_in_files[lab])[:8]))

# ---------------------------------------------------------------- cell 528f121b (cell_index 539)
# skill:figure-style kernel.py (auto-injected on skill load)
META_GREY = "#888888"


def apply_figure_style(*, frame="open", font=None, sizes=(8, 7, 6), grid=False):
    """Set matplotlib rcParams for publication-grade output. Call once before plotting.

    This sets mechanics (role-mapped font-size ladder, outward ticks, frameless
    legends, 300-dpi save, Type-42 embedded fonts) — not a house aesthetic.
    Frame, font and the size ladder are parameters.

    frame : 'open' (bottom+left spines, default) | 'boxed' (all four) | 'none'
    font  : sans-serif family name; None = system default sans-serif
    sizes : (base, secondary, tick) — titles/axis-labels, legend/annotation, ticks
    grid  : whether to draw axes.grid (default False)
    """
    import matplotlib as mpl
    if frame not in ("open", "boxed", "none"):
        raise ValueError(f"frame must be 'open'|'boxed'|'none', got {frame!r}")

    try:
        import os, sys, glob, matplotlib.font_manager as fm
        fdir = os.path.join(os.environ.get("CONDA_PREFIX") or sys.prefix, "fonts")
        if os.path.isdir(fdir):
            known = {f.fname for f in fm.fontManager.ttflist}
            for f in glob.glob(os.path.join(fdir, "*.ttf")):
                if f not in known:
                    fm.fontManager.addfont(f)
    except Exception:
        pass
    base, secondary, tick = sizes
    boxed = (frame == "boxed")
    rc = {
        "font.family": "sans-serif",
        "font.size": base,
        "axes.labelsize": base,
        "axes.titlesize": base,
        "legend.fontsize": secondary,
        "xtick.labelsize": tick,
        "ytick.labelsize": tick,
        "axes.linewidth": 0.6,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 3, "ytick.major.size": 3,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "axes.spines.top": boxed, "axes.spines.right": boxed,
        "axes.spines.left": frame != "none", "axes.spines.bottom": frame != "none",
        "axes.grid": bool(grid),
        "legend.frameon": False,
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.titleweight": "normal",
        "axes.titlelocation": "left",
        "axes.labelweight": "normal",
        "lines.linewidth": 1.2,
        "patch.linewidth": 0.6,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    }
    if font:
        rc["font.sans-serif"] = [font, "DejaVu Sans"]
    mpl.rcParams.update(rc)


def set_frame(ax, style="open"):
    """§3: set spine visibility on an existing axes. style ∈ {'open','boxed','none'}."""
    show = {"open": (False, False, True, True),
            "boxed": (True, True, True, True),
            "none": (False, False, False, False)}[style]
    for side, vis in zip(("top", "right", "bottom", "left"), show):
        ax.spines[side].set_visible(vis)
        if vis:
            ax.spines[side].set_linewidth(0.6)
    ax.tick_params(direction="out", length=0 if style == "none" else 3, width=0.6)


def panel_letter(ax, letter, dx=-0.18, dy=1.02, case="lower", fontsize=None):
    """§5.7: bold panel letter outside top-left of axes. case ∈ {'lower','upper'}."""
    import matplotlib.pyplot as plt
    if fontsize is None:
        fontsize = plt.rcParams.get("font.size", 8) + 1
    s = letter.lower() if case == "lower" else letter.upper()
    ax.text(dx, dy, s, transform=ax.transAxes,
            fontweight="bold", fontsize=fontsize, va="bottom", ha="left")


def focal_palette(labels, focal, focal_color, other="muted", base_colors=None):
    """§4.2: map labels → colors with the focal series visually dominant.

    other='muted'   — desaturate base_colors (or a default cycle) toward gray
    other='grey'    — uniform light gray for all non-focal
    other='ordinal' — non-focal on a single light→dark gray ramp (input order)
    """
    import matplotlib.colors as mcolors
    import matplotlib.pyplot as plt
    focal_set = {focal} if isinstance(focal, str) else set(focal)
    n = len(labels)
    if not focal_set & set(labels):
        raise ValueError(f"focal {focal!r} not found in labels")
    if base_colors is None:
        base_colors = plt.rcParams["axes.prop_cycle"].by_key().get("color", ["#444444"])
    base_colors = [base_colors[i % len(base_colors)] for i in range(n)]
    if other == "grey":
        rest = ["#BCBCBC"] * n
    elif other == "ordinal":
        nf = max(1, n - len(focal_set))
        ramp = [mcolors.to_hex((v, v, v)) for v in
                ([0.55] if nf == 1 else [0.80 - 0.35 * i / (nf - 1) for i in range(nf)])]
        rest, k = [], 0
        for l in labels:
            rest.append(ramp[min(k, nf - 1)]); k += (l not in focal_set)
    else:
        def mute(c):
            r, g, b = mcolors.to_rgb(c)
            m = (r + g + b) / 3
            return mcolors.to_hex((0.3 * r + 0.7 * m, 0.3 * g + 0.7 * m, 0.3 * b + 0.7 * m))
        rest = [mute(c) for c in base_colors]
    return [focal_color if l in focal_set else rest[i] for i, l in enumerate(labels)]


def bar_with_points(ax, x, ymat, labels, colors, jitter=0.08, show_points=True,
                    errorbar=None, point_alpha=0.5, point_size=8):
    """§6.1: bar = mean; optionally overlay raw points or draw an interval.

    colors   : per-label color list (e.g. from focal_palette)
    errorbar : None | 'sd' | 'ci95' — drawn only when show_points is False.
               'ci95' is the t-distribution 95% CI of the mean
               (half-width t_{0.975,n-1} · s/√n); correct at small n where the
               z-approximation (1.96·s/√n) is markedly too narrow.
    """
    import numpy as np
    means = np.array([np.mean(y) for y in ymat], float)
    err = None
    if errorbar and not show_points:
        if errorbar == "sd":
            err = np.array([np.std(y, ddof=1) if np.asarray(y).size > 1 else 0 for y in ymat])
        elif errorbar == "ci95":
            from scipy.stats import t
            def _hw(y):
                n = np.asarray(y).size
                return t.ppf(0.975, n - 1) * np.std(y, ddof=1) / np.sqrt(n) if n > 1 else 0
            err = np.array([_hw(y) for y in ymat])
    ax.bar(x, means, color=colors, width=0.7, edgecolor="none",
           yerr=err, error_kw={"elinewidth": 0.8, "capsize": 0})
    if show_points:
        for xi, ys in zip(x, ymat):
            ys = np.asarray(ys)
            if ys.ndim and ys.size > 1:
                jit = (np.random.rand(ys.size) - 0.5) * 2 * jitter
                ax.scatter(np.full(ys.size, xi) + jit, ys, s=point_size, color="black",
                           alpha=point_alpha, zorder=3, linewidths=0)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    return ax


def strip_with_median(ax, groups, values, colors=None, jitter=0.12):
    """§6.1: jittered points + bold horizontal median tick per group."""
    import numpy as np
    labs = list(groups)
    if colors is None:
        colors = ["#444444"] * len(labs)
    for i, (ys, c) in enumerate(zip(values, colors)):
        ys = np.asarray(ys)
        jit = (np.random.rand(ys.size) - 0.5) * 2 * jitter
        ax.scatter(np.full(ys.size, i) + jit, ys, s=10, color=c, alpha=0.6, linewidths=0, zorder=2)
        m = np.median(ys)
        ax.plot([i - 0.22, i + 0.22], [m, m], color="black", lw=1.6, zorder=3)
    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs)
    return ax


def goodness_arrow(ax, text="higher = better", loc="upper left", axis="y", fontsize=None):
    """§3.6: small upright direction-of-goodness cue in the margin."""
    import matplotlib.pyplot as plt
    if fontsize is None:
        fontsize = plt.rcParams["legend.fontsize"]
    pos = {"upper left": (0.02, 0.98), "upper right": (0.98, 0.98),
           "lower left": (0.02, 0.02), "lower right": (0.98, 0.02)}[loc]
    ha = "left" if "left" in loc else "right"
    va = "top" if "upper" in loc else "bottom"
    arrow = "↑ " if axis == "y" else "→ "
    ax.text(pos[0], pos[1], arrow + text, transform=ax.transAxes,
            fontsize=fontsize, color=META_GREY, ha=ha, va=va)


def two_tier_label(name, meta):
    """§5: two-line label string (name / metadata). Meta line styled separately by caller."""
    return f"{name}\n{meta}"


def end_of_line_labels(ax, xs, ys, labels, colors=None, dx=0.01, fontsize=None):
    """§6.3 / §7.3: label each line series at its right end instead of a legend box."""
    import matplotlib.pyplot as plt
    if fontsize is None:
        fontsize = plt.rcParams["font.size"]
    if colors is None:
        colors = [None] * len(labels)
    span = ax.get_xlim()[1] - ax.get_xlim()[0]
    for x, y, lab, c in zip(xs, ys, labels, colors):
        ax.text(x[-1] + dx * span, y[-1], lab, color=c, va="center", ha="left", fontsize=fontsize)


def panel_crops(fig, dpi=None, pad_px=6, bbox_inches=None, pad_inches=None):
    """§9.2: pixel-space crop boxes for each lettered panel in the SAVED PNG.

    Returns ``{letter: (x0, y0, x1, y1)}`` in image-space pixels (origin
    top-left, matching ``host.view_image(path, crop=...)`` and PIL's
    ``Image.crop``). Panels are detected as bold single-character ``Text``
    objects placed by :func:`panel_letter`; each panel's crop is its axes'
    tightbbox mapped into the saved file's pixel space, padded by ``pad_px``.
    For §3.4 composites (abutting subplots sharing an axis, letter on the
    leftmost only) the crop unions in letterless ``sharex``/``sharey`` siblings
    on the same grid row/col so the whole composite is covered. When no axes
    carries a panel letter (standalone plot, or a figure-composer sub-agent),
    falls back to one crop per axes keyed by index.

    ``bbox_inches`` mirrors ``Figure.savefig`` semantics: ``None`` means
    *consult rcParams* (so under :func:`apply_figure_style` it resolves to
    ``'tight'``); pass an explicit ``Bbox`` only if you saved with one. The
    boxes are clamped to the saved image extent regardless.

        >>> fig.savefig("fig.png")            # bbox_inches='tight' via rcParams
        >>> for letter, box in panel_crops(fig).items():
        ...     host.view_image("fig.png", crop=box)
    """
    import matplotlib as mpl
    import matplotlib.text
    if dpi is None:
        dpi = mpl.rcParams.get("savefig.dpi", fig.dpi)
        if dpi == "figure":
            dpi = fig.dpi
    dpi = float(dpi)
    if bbox_inches is None:
        bbox_inches = mpl.rcParams.get("savefig.bbox")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    if bbox_inches == "tight":
        if pad_inches is None:
            pad_inches = mpl.rcParams.get("savefig.pad_inches", 0.1)
        tb = fig.get_tightbbox(r).padded(pad_inches)
        ox_in, oy_in = tb.x0, tb.y0
        W_in, H_in = tb.width, tb.height
    elif isinstance(bbox_inches, mpl.transforms.BboxBase):
        ox_in, oy_in = bbox_inches.x0, bbox_inches.y0
        W_in, H_in = bbox_inches.width, bbox_inches.height
    else:
        ox_in, oy_in = 0.0, 0.0
        W_in, H_in = fig.get_size_inches()
    W_px, H_px = int(round(W_in * dpi)), int(round(H_in * dpi))
    lettered = {}
    for ax in fig.axes:
        for t in ax.findobj(matplotlib.text.Text):
            s = (t.get_text() or "").strip()
            if len(s) == 1 and s.isalpha() and t.get_fontweight() in ("bold", 700):
                lettered[ax] = s
                break



    if not lettered:
        lettered = {ax: str(i) for i, ax in enumerate(fig.axes)}
    out = {}
    for ax, letter in lettered.items():
        bbs = [ax.get_tightbbox(r)]




        ss = ax.get_subplotspec()
        for sib in fig.axes:
            if sib is ax or sib in lettered:
                continue
            ssib = sib.get_subplotspec()
            same_row = ss is None or ssib is None or ss.rowspan == ssib.rowspan
            same_col = ss is None or ssib is None or ss.colspan == ssib.colspan
            if ((ax.get_shared_y_axes().joined(ax, sib) and same_row)
                    or (ax.get_shared_x_axes().joined(ax, sib) and same_col)):
                bbs.append(sib.get_tightbbox(r))
        bb = mpl.transforms.Bbox.union(bbs)

        bx0 = (bb.x0 / fig.dpi - ox_in) * dpi
        bx1 = (bb.x1 / fig.dpi - ox_in) * dpi
        by0 = H_px - (bb.y1 / fig.dpi - oy_in) * dpi
        by1 = H_px - (bb.y0 / fig.dpi - oy_in) * dpi
        out[letter] = (
            max(int(bx0) - pad_px, 0),
            max(int(by0) - pad_px, 0),
            min(int(bx1) + pad_px, W_px),
            min(int(by1) + pad_px, H_px),
        )
    return out

# ---------------------------------------------------------------- cell 0f4f92b0 (cell_index 557)
SIP='/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/2b769225-2f82-481d-9d62-9dbbcd5caa07/vf41d01db_290926Supplementary_Information_legends.docx'; shutil.copy(SIP,'SI_in.docx')
si=docxedit.TrackedDoc('SI_in.docx', author='Claude Science')
INCL=("Comparison of included and excluded participants. Of the 414 STRATIFY participants with symptom data available, 198 entered "
 "the population-scale sample. Patients were preferentially modelled, because digital twins were built only where diffusion and "
 "task data were both complete and patient scans were prioritised (129 of 199 patients versus 69 of 215 controls; "
 "\u03c7\u00b2(1) = 43.07, P < 0.0001), so the modelled participants had higher six-domain symptom scores overall "
 "(15.00 \u00b1 11.38 versus 10.75 \u00b1 9.73; two-sided Welch t(389.4) = 4.07, P < 0.0001; Hedges' g = 0.40). Within diagnostic strata, "
 "included and excluded participants did not differ in symptom severity (controls 6.96 \u00b1 6.26 versus 6.69 \u00b1 6.20, "
 "t(132.3) = 0.29, P = 0.77, g = 0.04; patients 19.30 \u00b1 11.18 versus 19.21 \u00b1 10.35, t(151.4) = 0.06, P = 0.96, g = 0.01), and the "
 "ratio of MDD to AUD did not differ between included and excluded patients (\u03c7\u00b2(1) = 1.98, P = 0.16). The 89 IMAGEN participants "
 "in the population sample were selected by a prespecified symptom threshold and are therefore not comparable with unselected "
 "IMAGEN participants in this respect.")
LONGADD=("The measured NP edges are not uninformative when they are summed rather than entered individually. The summed age-19 "
 "empirical NP factor was associated with symptom change (r = 0.39, P = 0.0002, n = 85), and the simulated and measured "
 "read-outs are partly complementary: adding the summed measured factor to the 12 simulated edges increased the explained "
 "variance (\u0394R\u00b2 = 0.07, F(1,71) = 8.15, P = 0.0056; leave-one-out r 0.29 to 0.38, permutation P = 0.0015), and adding the 12 "
 "simulated edges to the summed measured factor increased it as well (\u0394R\u00b2 = 0.21, F(12,71) = 1.95, P = 0.043). With age-19 "
 "symptoms and the summed measured factor both included, the 12 simulated edges gave a further \u0394R\u00b2 = 0.17 that did not reach "
 "significance (F(12,70) = 1.69, P = 0.088). The difference between simulated and measured connectivity therefore concerns the "
 "12 edges taken individually and not the summed factor, and the two sources of prognostic information overlap in part. "
 "Leave-one-out predictions for the four model specifications are shown in Fig. S15.")
S15=("Fig. S15 Leave-one-out prediction of four-year symptom change under four model specifications. Leave-one-out predicted "
 "against observed symptom change (age 23 minus age 19) in the 85 longitudinal participants. a, Age-19 symptom load alone "
 "(r = 0.35). b, Age-19 symptoms with the 12 simulated NP edges (r = 0.40). c, Age-19 symptoms with the 12 empirical NP edges "
 "(r = 0.23). d, The 12 empirical NP edges alone (r = 0.13); the same 12 edges simulated by the digital twins are shown in "
 "Fig. 5h. Negative values denote symptom reduction. Points are individual participants and the line is an ordinary "
 "least-squares fit with its 95% confidence band, shown to indicate direction and not as an additional test; no other error "
 "indicators are drawn. Prediction used ordinary least squares with leave-one-out cross-validation and a two-sided Pearson "
 "correlation between predicted and observed change; significance was assessed against a permutation null (2,000 shuffles of "
 "the outcome with the complete leave-one-out procedure repeated): a, P = 0.0010; b, P = 0.0010; c, P = 0.034; d, P = 0.12. "
 "In-sample statistics: a, R\u00b2 = 0.16, F(1,83) = 15.41, P = 0.0002; b, R\u00b2 = 0.37, F(13,71) = 3.18, P = 0.0009; c, R\u00b2 = 0.27, "
 "F(13,71) = 1.98, P = 0.035; d, R\u00b2 = 0.21, adjusted R\u00b2 = 0.07, F(12,72) = 1.56, P = 0.12. No multiple-comparison correction "
 "was applied across the four nested specifications; exact statistics are listed in Table S24.")
i15=[i for i,t in enumerate(TXT['SI']) if t.strip().startswith('Fig. S15')][0]
i6=[i for i,t in enumerate(TXT['SI']) if t.strip().startswith('Fig. S6')][0]
c6=re.search(r'c, AMPA\s+GABA-A perturbation', TXT['SI'][i6]).group(0)
SIEDITS=[
 (120,'r = 0.35, P = 0.001)','r = 0.35, permutation P = 0.0010)'),
 (120,'r = 0.29, P = 0.0072)','r = 0.29, permutation P = 0.0095)'),
 (120,'r = 0.13, P = 0.22;','r = 0.13, permutation P = 0.12;'),
 (120,'r = 0.40, P = 0.0002)','r = 0.40, permutation P = 0.0010)'),
 (120,'r = 0.23, P = 0.033)','r = 0.23, permutation P = 0.034)'),
 (120,'significance of the simulated-edge model was assessed against a permutation null',
      'significance of every model was assessed against a permutation null'),
 (i6, c6, 'c, GABA-A perturbation'),
 (i15, TXT['SI'][i15].strip(), S15),
]
for pi,old,new in SIEDITS:
    print(pi, TXT['SI'][pi].count(old), '|', repr(old[:50]))

# ---------------------------------------------------------------- cell b9313cf9 (cell_index 558)
for pi,old,new in SIEDITS:
    assert si.replace(old,new,para=pi) is not None, (pi,old[:40])
si.new_paragraph_after(89, INCL)
si.new_paragraph_after(120, LONGADD)
SIOUT='290926Supplementary_Information_S18incl_long_tracked.docx'
None; None  # [recovery: side output suppressed]  # [recovery: side output suppressed]
rr=etree.fromstring(zipfile.ZipFile('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'+SIOUT).read('word/document.xml'))
cc=collections.Counter()
for tag in ('ins','del','pPrChange'):
    for e in rr.iter(W+tag): cc[(tag,e.get(W+'author'))]+=1
print('SI revisions:', dict(cc))
ps3=rr.findall('.//'+W+'body//'+W+'p')
for i in (90,121,122,180,222):
    print('\n--- %d ---\n%s'%(i, ptext(ps3[i])[:420]))

# ---------------------------------------------------------------- cell 5074a2e6 (cell_index 560)
def alltext(path, mode):
    r=etree.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
    return [ptext(p,mode) for p in r.findall('.//'+W+'body//'+W+'p')]
o_rej=alltext(SIP,'reject'); n_rej=alltext('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'+SIOUT,'reject')
n_rej2=[t for i,t in enumerate(n_rej) if i not in (90,122)]
print('rejected view identical after removing my two new paragraphs:', o_rej==n_rej2)
if o_rej!=n_rej2:
    for i,(a,b) in enumerate(zip(o_rej,n_rej2)):
        if a!=b: print('diff at',i,'\n  orig:',a[:200],'\n  new :',b[:200]); break

# ---------------------------------------------------------------- cell 9611395d (cell_index 569)
TP='/Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/a42c58ac-1e77-4fc4-9b5b-31288ffc2530/vcbd180f3_290926Suppl.Table.xlsx'; shutil.copy(TP,'T_in.xlsx')
wb=openpyxl.load_workbook('T_in.xlsx'); ws=wb['Table S24']
hdr=[('' if c is None else str(c).strip()) for c in next(ws.iter_rows(min_row=2,max_row=2,values_only=True))]
print(ws.max_row, ws.max_column); print([ (i+1,h) for i,h in enumerate(hdr) if h][:20])
rows=[(r, [('' if c is None else str(c).strip()) for c in ws[r]][:8]) for r in range(3, ws.max_row+1)]
cur=''
for r,v in rows:
    if v[0]: cur=v[0]
    if 'S15' in cur or 'S15' in v[0]: print(r, v[:6])

# ---------------------------------------------------------------- cell 5d7d66f3 (cell_index 576)
wb=openpyxl.load_workbook('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/290926Suppl.Table_reviewed.xlsx')
w=wb['Table S18']
rows=[(r,[w.cell(row=r,column=c).value for c in range(1,5)]) for r in range(1,w.max_row+1)]
for r,v in rows:
    if any(x is not None for x in v): print(r, ' | '.join('' if x is None else str(x)[:120] for x in v))

# ---------------------------------------------------------------- cell 29f9f2df (cell_index 578)
s24=wb['Table S24']
for r in range(3, s24.max_row+1):
    row=[s24.cell(row=r,column=c).value for c in range(1,18)]
    txt=' '.join('' if x is None else str(x) for x in row)
    if '0.0068' in txt or 'similarity' in txt.lower():
        print(r, [('' if x is None else str(x)[:70]) for x in row[:3]], '|', [('' if x is None else str(x)[:60]) for x in row[6:14]])

# ---------------------------------------------------------------- cell 830faf45 (cell_index 593)
from decimal import Decimal, ROUND_HALF_UP
def rhu(v,d):
    return float(Decimal(repr(float(v))).quantize(Decimal('1.'+'0'*d), rounding=ROUND_HALF_UP))
def fmt_p(v):
    if v<1e-4: return '< 0.0001'
    s='%.4f'%rhu(v,4)
    s=s.rstrip('0')
    if len(s.split('.')[1])<2: s=('%.2f'%rhu(v,2))
    return s
def fmt_stat(v):
    av=abs(v)
    if v==int(v) and av<10000: return str(int(v))
    r2=rhu(av,2)
    if r2==0.0 or (r2==round(av) and av<1 and abs(av-round(av))>1e-9): return None
    if r2==0.0: return None
    return ('%.2f'%rhu(v,2))
NUMTOK=re.compile(r'(?<![\w.])(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)(?![\w])')
PCOLS={13,14}
STCOLS={11,15}
log=[]
for r in range(3, s24.max_row+1):
    for c in sorted(PCOLS|STCOLS):
        v=s24.cell(row=r,column=c).value
        if v is None: continue
        if isinstance(v,(int,float)):
            s=str(v)
        else:
            s=str(v)
        def repl(m):
            x=float(m.group(1))
            if c in PCOLS:
                if not (0<=x<=1): return m.group(1)
                out=fmt_p(x)
                return out if out.startswith('<') else out
            f=fmt_stat(x)
            return m.group(1) if f is None else f
        new=NUMTOK.sub(repl, s)
        new=re.sub(r'=\s*< 0\.0001','< 0.0001',new)
        if new!=s:
            s24.cell(row=r,column=c,value=new)
            log.append(dict(row=r, column=hdr[c-1] if c-1<len(hdr) else c, before=s, after=new))
L=pd.DataFrame(log); L.to_csv('tableS24_format_log.csv',index=False)
print('cells reformatted:', len(L))
print(L.head(25).to_string(max_colwidth=58))

# ---------------------------------------------------------------- cell df49a836 (cell_index 594)
def fmt_p2(v):
    if v<1e-4: return '< 0.0001'
    if v<1.5e-4: return '%.5f'%rhu(v,5)
    s='%.4f'%rhu(v,4); s=s.rstrip('0')
    if len(s.split('.')[1])<2: s='%.2f'%rhu(v,2)
    return s
def fmt_stat2(tok):
    v=float(tok)
    if '.' not in tok and 'e' not in tok.lower(): return tok           # integers / df
    av=abs(v)
    if av<0.1 and av>0:                                                # 2 significant digits
        d=int(np.floor(np.log10(av))); s='%.*f'%(max(2,-d+1), rhu(v,max(2,-d+1)))
        return s.rstrip('0').rstrip('.') if '.' in s else s
    if rhu(av,2)==round(av) and av<1: return tok                       # 0.9951 -> keep
    return '%.2f'%rhu(v,2)

wb=openpyxl.load_workbook('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/290926Suppl.Table_reviewed.xlsx')
w=wb['Table S18']; s24=wb['Table S24']
# (a) S18 percent formats + footnotes
for r in range(3, w.max_row+1):
    c=w.cell(row=r,column=4)
    if isinstance(c.value,(int,float)): c.value=float(c.value); c.number_format='0.0%'
w.cell(row=25,column=1,value=('Pearson chi-squared test of independence between response group and recruitment site: chi-squared(8) = 14.32, P = 0.074 '
 '(two-sided, uncorrected). Because 7 of 18 expected counts were below 5, the asymptotic P value is approximate; a Monte-Carlo '
 'permutation test (10,000 random reassignments of response group) gave P = 0.065. Collapsing the two London sub-sites into a single '
 'London site gives chi-squared(7) = 10.43, P = 0.166.'))
w.cell(row=36,column=1,value=('Pearson chi-squared test of independence between response group and sex: chi-squared(1) = 5.29, P = 0.021 (two-sided, '
 'uncorrected); Fisher exact test P = 0.018. In the model reported in Supplementary Results, which regresses response group on sex, '
 'diagnostic group and recruitment site, the sex effect is attenuated (linear model, t = -1.93, P = 0.055); the attenuation is '
 'specification-dependent, because a logistic regression of the same model leaves it nominally significant (z = -2.10, P = 0.036; '
 'odds ratio 0.44, 95% CI 0.20-0.95 for male versus female). All negative-profile connectivity measures were residualised for sex, '
 'site and head motion before analysis.'))
w.cell(row=38,column=1,value=('Response groups were defined from the 288 participants with individually fitted digital twins: Increased n = 229, '
 'Decreased n = 59. Site, sex and response group were taken from figures/fig.4/fig4_data/fig4_subject_level_n288.csv; the London '
 'sub-site assignment (London-Invicro = LONDON, London-CNS = LONDON2) from Figures/Figure4/mani_ampa_gaba_subs_diff_london_site.csv. '
 'Recomputed 29 September; the previous version was based on 290 participants (251 increased / 39 decreased) under an earlier '
 'response-group definition.'))
print('S18 footnotes restored')

# ---------------------------------------------------------------- cell 1098206c (cell_index 596)
log=[]
for r in range(3, s24.max_row+1):
    for c in (11,13,14,15):
        v=s24.cell(row=r,column=c).value
        if v is None: continue
        s=str(v)
        def repl(m):
            tok=m.group(1); x=float(tok)
            if c in (13,14):
                return tok if not (0<=x<=1) else fmt_p2(x)
            return fmt_stat2(tok)
        new=NUMTOK.sub(repl,s)
        new=re.sub(r'=\s*< 0\.0001','< 0.0001',new)
        if new!=s:
            s24.cell(row=r,column=c,value=new); log.append(dict(row=r,column=hdr[c-1],before=s,after=new))
L=pd.DataFrame(log); L.to_csv('tableS24_format_log.csv',index=False)
print('cells reformatted:',len(L))
print(L.sample(min(18,len(L)),random_state=0).to_string(max_colwidth=56))

# ---------------------------------------------------------------- cell dd87155c (cell_index 597)
for e in log: s24.cell(row=e['row'], column=hdr.index(e['column'])+1, value=e['before'])
NUMTOK2=re.compile(r'(?<![\w.])(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)(?![\w%])')
LIST=re.compile(r'^\s*(-?\d+\.\d+)(\s*,\s*-?\d+\.\d+){2,}\s*$')
def dec_needed(tok):
    v=abs(float(tok)); 
    if v==0: return 2
    if v<0.1: return max(2, -int(np.floor(np.log10(v)))+1)
    return 2
log2=[]
for r in range(3, s24.max_row+1):
    for c in (11,13,14,15):
        v=s24.cell(row=r,column=c).value
        if v is None: continue
        s=str(v)
        if c in (11,15) and LIST.match(s):
            toks=[t.strip() for t in s.split(',')]; d=max(dec_needed(t) for t in toks)
            new=', '.join('%.*f'%(d, rhu(float(t),d)) for t in toks)
        else:
            def repl(m):
                tok=m.group(1); x=float(tok)
                if c in (13,14): return tok if not (0<=x<=1) else fmt_p2(x)
                return fmt_stat2(tok)
            new=NUMTOK2.sub(repl,s)
            new=re.sub(r'=\s*< 0\.0001','< 0.0001',new)
        if new!=s:
            s24.cell(row=r,column=c,value=new); log2.append(dict(row=r,column=hdr[c-1],before=s,after=new))
L=pd.DataFrame(log2); L.to_csv('tableS24_format_log.csv',index=False)
print('cells reformatted:',len(L))
for q in ['70.7','6.8%','MSE = 0.0067','0.1662 versus']:
    hit=L[L.before.str.contains(re.escape(q))]
    if len(hit): print('\n', hit.iloc[0].to_dict())

# ---------------------------------------------------------------- cell 06d62cd8 (cell_index 598)
for e in log2: s24.cell(row=e['row'], column=hdr.index(e['column'])+1, value=e['before'])
RUN=re.compile(r'(-?\d+\.\d+(?:\s*,\s*-?\d+\.\d+){2,})')
PAIR=re.compile(r'(-?\d+\.\d+)(\s+(?:versus|vs\.?)\s+)(-?\d+\.\d+)')
def unify_runs(s):
    def f(m):
        toks=[t.strip() for t in m.group(1).split(',')]; d=max(dec_needed(t) for t in toks)
        return ', '.join('%.*f'%(d,rhu(float(t),d)) for t in toks)
    s=RUN.sub(f,s)
    def g(m):
        d=max(dec_needed(m.group(1)),dec_needed(m.group(3)))
        return '%.*f%s%.*f'%(d,rhu(float(m.group(1)),d),m.group(2),d,rhu(float(m.group(3)),d))
    return PAIR.sub(g,s)
log3=[]
for r in range(3, s24.max_row+1):
    for c in (11,13,14,15):
        v=s24.cell(row=r,column=c).value
        if v is None: continue
        s=str(v)
        if c in (11,15):
            new=unify_runs(s)
            def repl(m):
                return fmt_stat2(m.group(1))
            # only reformat tokens that were not part of a unified run/pair
            prot=set()
            for m in list(RUN.finditer(new))+list(PAIR.finditer(new)): prot.add((m.start(),m.end()))
            out=[]; last=0
            for m in NUMTOK2.finditer(new):
                if any(a<=m.start()<b for a,b in prot): continue
                out.append((m.start(),m.end(),fmt_stat2(m.group(1))))
            for a,b,t in reversed(out): new=new[:a]+t+new[b:]
        else:
            def replp(m):
                x=float(m.group(1)); return m.group(1) if not (0<=x<=1) else fmt_p2(x)
            new=NUMTOK2.sub(replp,s); new=re.sub(r'=\s*< 0\.0001','< 0.0001',new)
        if new!=s:
            s24.cell(row=r,column=c,value=new); log3.append(dict(row=r,column=hdr[c-1],before=s,after=new))
L=pd.DataFrame(log3); L.to_csv('tableS24_format_log.csv',index=False)
print('cells reformatted:',len(L))
for q in ['MSE = 0.0067','0.1662 versus','70.7','0.9951','2.91e-44']:
    hit=L[L.before.str.contains(re.escape(q))]
    print(q,'->', hit.iloc[0]['after'][:80] if len(hit) else '(unchanged)')

# ---------------------------------------------------------------- cell 8f33a7a1 (cell_index 599)
for e in log3: s24.cell(row=e['row'], column=hdr.index(e['column'])+1, value=e['before'])
def fmt_stat2(tok):
    v=float(tok)
    if '.' not in tok and 'e' not in tok.lower(): return tok
    av=abs(v)
    if av>0.98 and av<1.0: return tok              # ICC / r near 1: 2 dp destroys the value
    if 0<av<0.1:
        d=max(2,-int(np.floor(np.log10(av)))+1); s='%.*f'%(d, rhu(v,d))
        return s
    return '%.2f'%rhu(v,2)
log4=[]
for r in range(3, s24.max_row+1):
    for c in (11,13,14,15):
        v=s24.cell(row=r,column=c).value
        if v is None: continue
        s=str(v)
        if c in (11,15):
            new=unify_runs(s); prot=set()
            for m in list(RUN.finditer(new))+list(PAIR.finditer(new)): prot.add((m.start(),m.end()))
            out=[(m.start(),m.end(),fmt_stat2(m.group(1))) for m in NUMTOK2.finditer(new) if not any(a<=m.start()<b for a,b in prot)]
            for a,b,t in reversed(out): new=new[:a]+t+new[b:]
        else:
            new=NUMTOK2.sub(lambda m: m.group(1) if not (0<=float(m.group(1))<=1) else fmt_p2(float(m.group(1))), s)
            new=re.sub(r'=\s*< 0\.0001','< 0.0001',new)
        if new!=s:
            s24.cell(row=r,column=c,value=new); log4.append(dict(row=r,column=hdr[c-1],before=s,after=new))
L=pd.DataFrame(log4); L.to_csv('tableS24_format_log.csv',index=False)
print('cells reformatted:',len(L))
print(L[L.before.str.contains('ICC')].to_string(max_colwidth=70))
TOUT2='290926Suppl.Table_reviewed_v2.xlsx'; None; None  # [recovery: side output suppressed]  # [recovery: side output suppressed]
ck=openpyxl.load_workbook('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/'+TOUT2)
print('\nsheets',len(ck.sheetnames),'| S24 data rows', sum(1 for r in range(3,ck['Table S24'].max_row+1) if ck['Table S24'].cell(row=r,column=1).value or ck['Table S24'].cell(row=r,column=2).value))
print('S18 footnote present:', str(ck['Table S18'].cell(row=25,column=1).value)[:60])

# ---------------------------------------------------------------- cell dda374a2 (cell_index 600)
MSTXT=[t for t in alltext('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/290926NatMed_Manuscript_reviewed_tracked.docx','accept')]
S=ck['Table S24']
rowsS=[]
cur=''
for r in range(3,S.max_row+1):
    f=str(S.cell(row=r,column=1).value or '').strip()
    if f: cur=f
    rowsS.append(dict(row=r, fig=cur, panel=str(S.cell(row=r,column=2).value or ''),
                      quantity=str(S.cell(row=r,column=3).value or ''),
                      stat=str(S.cell(row=r,column=11).value or ''), p=str(S.cell(row=r,column=13).value or ''),
                      q=str(S.cell(row=r,column=14).value or ''), eff=str(S.cell(row=r,column=15).value or ''),
                      ci=str(S.cell(row=r,column=16).value or '')))
T=pd.DataFrame(rowsS)
main=T[T.fig.str.match(r'^(Fig(ure)?\.? ?\d|Figure \d)')]
print('S24 rows total %d | main-figure rows %d | figures: %s'%(len(T), len(main), sorted(main.fig.unique())))
print('\nmain-figure rows lacking an effect size: %d'%((main.eff.str.strip()=='').sum()))
print('main-figure rows lacking a CI: %d'%((main.ci.str.strip()=='').sum()))
print('main-figure rows lacking an exact P: %d'%((main.p.str.strip()=='').sum()))
gap=main[(main.eff.str.strip()=='')|(main.ci.str.strip()=='')][['row','fig','panel','quantity','stat','p','eff','ci']]
gap.to_csv(os.path.join(OUT_DIR, 'tableS24_main_completeness.csv'), index=False)
print('\n', gap.head(20).to_string(max_colwidth=42))
