#!/usr/bin/env python3
"""long85_add_summed_empirical_to_sim12.csv

Computes
    Whether the summed baseline empirical NP connectivity adds predictive
    information beyond the covariate + 12-simulated-edge model (n = 85): the
    nested R2 increment with its F test, the resulting model R2 and leave-one-
    out r, and a Williams test comparing the two dependent leave-one-out
    prediction correlations.

Inputs
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/14e6f0b7-ee8b-47be-b546-5b12e8540cfc/vfdcde268_280926NatMed_Response_Letter_R1-R4_Claude.docx
    - /Users/yunman/.claude-science/orgs/226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/artifacts/proj_d1fb16c901b1/a42c58ac-1e77-4fc4-9b5b-31288ffc2530/vcbd180f3_290926Suppl.Table.xlsx
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/text/
    - /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data/
    - (path built in the chain) F3+f
    - (path built in the chain) F3+'fig3c_similarity_pvalues.csv'
    - (path built in the chain) F3+'fig3c_cross_scale_similarity.csv'
    - (path built in the chain) F3+'fig3c_cross_scale_similarity_ampa.csv'
    - (path built in the chain) B+f
    - (path built in the chain) B+'np_beha_85subjects_all_quantities.csv'
    - (path built in the chain) B+'np85_12edges_repetitions_wide.csv'

Output
    04_figures/_recovered_session_b194cd74/long85_add_summed_empirical_to_sim12.csv

Statistical tests
    in this script's own computation:
      - outcome-permutation null
      - leave-one-out cross-validation
      - Williams test for dependent correlations
    in the recovered chain that prepares its inputs:
      - paired two-sided t test
      - Wilcoxon signed-rank test
      - ordinary least squares GLM with covariates
      - nested-model F test for the R2 increment

Local runnability
    partial (local_runnable = partial).  Verification: not_run.
    re-run stops on a name the recovery could not carry over ('rr'): it was
    bound by an interactive step that depends on the platform artifact store
    or on a workspace-only helper, which the recovery does not fabricate
Recovered from
    execution-log cell e44e3f3e-dba6-40b3-9f11-4c6982757fe8
    frame b194cd74-5255-435a-9c1e-206638f9adae, cell_index 711, 2026-09-29 14:15 UTC, conda env "python"
    dependency chain recovered from the same session, in order:
    e414d80b, 71a4711e, 706dc695, c29ac0b3, 8d74c997, e44e3f3e

Random seed
    fixed in the original run: seed = 0, seed = 1.  Re-running therefore
    reproduces the permutation / resampling statistics     exactly.  No seed
    was added or changed during recovery.

Notes
    Rebuilt by the statistics-layer recovery (docs/RECOVERY_PROTOCOL.md).  The
    computation is the recovered cell chain unchanged: same tests, same
    covariates, same corrections, same seeds.  Only the header, the explicit
    output path and the suppression of the original session's side outputs were
    added.  Lines marked "[recovery: side output suppressed]" wrote files other
    than this script's one deliverable into the author's working tree; they are
    commented out so that running this script cannot modify anything outside
    OUT_DIR.  The verbatim terminal cell is archived at
    recovered/fig5/long85_add_summed_empirical_to_sim12__cell_e44e3f3e.py
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

# ---------------------------------------------------------------- cell d9658333 (cell_index 450)
XL=dest+'290926Suppl.Table.xlsx'
wb=openpyxl.load_workbook(XL); print(wb.sheetnames[-3:], '| S24 dims', wb['Table S24'].dimensions)
ws=wb['Table S24']
COLS=[ws.cell(row=2,column=c).value for c in range(1,18)]
rows=[[('' if c is None else str(c).strip()) for c in r[:17]] for r in ws.iter_rows(min_row=3, values_only=True)]
T=pd.DataFrame(rows, columns=COLS)
T=T[T['Figure'].str.strip().astype(bool) | T['Panel'].str.strip().astype(bool)].copy()
T['Figure']=T['Figure'].replace('', np.nan).ffill()
T['xlrow']=[i for i in range(3,3+len(T))]
print('rows:', len(T), '| has S21 chi2 rows:', T['Test statistic'].str.contains('chi2 = 11.234').any(), '| S5 fixed:', T['Sample size'].str.contains('HC01').any())
g6=T[T['Figure'].str.contains('S6', na=False)]
for _,r in g6.iterrows():
    print('\nrow',r['xlrow'],'panel',r['Panel'],'|',r['Quantity tested'][:78])
    print('   test:',r['Statistical test'][:95]); print('   stat:',r['Test statistic'][:120]); print('   P:',repr(r['Exact P']),'| corrP:',repr(r['Corrected P']),'| notes:',r['Source data file and notes'][:95])

# ---------------------------------------------------------------- cell 9dbc1f50 (cell_index 451)
F3='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data/'
print(sorted(os.path.basename(p) for p in glob.glob(F3+'fig3c*')))
for f in ['fig3c_similarity_pvalues.csv','fig3c_cross_scale_similarity.csv','fig3c_cross_scale_similarity_ampa.csv','fig3c_cross_scale_similarity_gaba.csv']:
    try:
        d=pd.read_csv(F3+f); print('\n==',f, d.shape, list(d.columns)); print(d.head(12).to_string())
    except Exception as e: print(f,'ERR',e)
# also check S5 rows in the current file
print('\nS5 rows:'); print(T[T['Figure']=='Supplementary Fig. S5'][['xlrow','Panel','Sample size','Unit of observation']].to_string(index=False))

# ---------------------------------------------------------------- cell c6ea1e8b (cell_index 454)
from scipy import stats
def pooled_p(rho, n=144):
    t=rho*math.sqrt((n-2)/max(1e-12,1-rho**2)); return t, 2*stats.t.sf(abs(t), n-2)
pv=pd.read_csv(F3+'fig3c_similarity_pvalues.csv')
chkrows=[]
for _,r in pv.iterrows():
    t,p=pooled_p(r.rho_pooled, int(r.n_cells_pooled)); chkrows.append((r.pair, r.rho_pooled, r.p_naive_144cells, p, abs(math.log10(p)-math.log10(r.p_naive_144cells))<0.02))
print('formula validation against p_naive_144cells:')
for x in chkrows: print('   %-20s rho=%.4f source=%.3g recomputed=%.3g match=%s'%x)
base=pd.read_csv(F3+'fig3c_cross_scale_similarity.csv', index_col=0)
ampa=pd.read_csv(F3+'fig3c_cross_scale_similarity_ampa.csv', index_col=0)
own=[(c, base.loc['10m_own',c]) for c in base.columns if c!='10m_own']
print('\n10m_own baseline pairs:')
for c,rho in own: t,p=pooled_p(rho); print('   10m_own vs %-9s rho=%.4f  t(142)=%.2f  P=%.3g'%(c,rho,t,p))
reg=[('3m_268','10m_268'),('3m_268','10m_1000'),('10m_268','10m_1000')]
print('\nAMPA regional-build pairs:')
for a,b in reg: 
    rho=ampa.loc[a,b]; t,p=pooled_p(rho); print('   %s vs %-9s rho=%.4f  t(142)=%.2f  P=%.3g'%(a,b,rho,t,p))

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

# ---------------------------------------------------------------- cell f4e4ce35 (cell_index 528)
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/'
for f in ['np85_12edges_repetitions_wide.csv','np85_empirical_simulated_modulated.csv','np_beha_85subjects_all_quantities.csv']:
    d=pd.read_csv(B+f); print('\n===',f,d.shape); print(list(d.columns)[:30])

# ---------------------------------------------------------------- cell bb989df6 (cell_index 529)
M=pd.read_csv(B+'np_beha_85subjects_all_quantities.csv')
print([c for c in M.columns if 'sim' in c or 'change' in c or 'sum' in c][:40])
sim=[f'simbase_edge{i}' for i in range(1,13)]; emp=[f'emp_edge{i}' for i in range(1,13)]
import statsmodels.api as sm
def fit(X,y):
    Xc=sm.add_constant(np.asarray(X,float)); m=sm.OLS(np.asarray(y,float),Xc).fit(); return m
for yc in ['beha_change_raw','beha_change_resi']:
    y=M[yc].values
    r2s=fit(M[sim],y).rsquared; r2e=fit(M[emp],y).rsquared; r2b=fit(M[['beha19_sum']],y).rsquared
    print('%-18s sim R2=%.4f  emp R2=%.4f  symptoms R2=%.4f'%(yc,r2s,r2e,r2b))

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

# ---------------------------------------------------------------- cell 92ac61de (cell_index 641)
def nested(cov, add, y=y):
    X0=sm.add_constant(np.asarray(M[cov],float)) if cov else np.ones((len(y),1))
    X1=sm.add_constant(np.asarray(M[cov+add],float))
    m0=sm.OLS(y,X0).fit(); m1=sm.OLS(y,X1).fit()
    k=len(add); df2=int(m1.df_resid)
    dR2=m1.rsquared-m0.rsquared
    F=(dR2/k)/((1-m1.rsquared)/df2); p=stats.f.sf(F,k,df2)
    return dict(dR2=dR2,F=F,df1=k,df2=df2,P=p)
FAM={
 '12 simulated edges beyond age-19 symptoms': nested(['beha19_sum'],sim),
 '12 empirical edges beyond age-19 symptoms': nested(['beha19_sum'],emp),
 'summed empirical NP beyond the 12 simulated edges': nested(sim,['emp_np_sum']),
 '12 simulated edges beyond the summed empirical NP': nested(['emp_np_sum'],sim),
 '12 simulated edges beyond symptoms + summed empirical NP': nested(['beha19_sum','emp_np_sum'],sim),
 'summed empirical NP beyond age-19 symptoms': nested(['beha19_sum'],['emp_np_sum']),
}
F=pd.DataFrame(FAM).T
from statsmodels.stats.multitest import multipletests
F['q_BH']=multipletests(F.P,method='fdr_bh')[1]; F['P_bonf']=np.minimum(F.P*len(F),1)
print(F[['dR2','F','df1','df2','P','q_BH','P_bonf']].to_string(float_format=lambda v:'%.4g'%v))

# ---------------------------------------------------------------- cell 7ffbb1ff (cell_index 646)
print([c for c in M.columns if not re.match(r'^(emp_edge|simbase_edge|mod_|beha)',c)][:40])
W85=pd.read_csv(B+'np85_12edges_repetitions_wide.csv')
print('\nwide file covariates:', [c for c in W85.columns if not '__' in c])
print(W85[['sex','site','headmotion','age_baseline']].head(3).to_string())
print('\nID overlap:', M.sub_id.isin(W85.sub_id).all() if 'sub_id' in M else 'no sub_id in M', list(M.columns)[:3])

# ---------------------------------------------------------------- cell dfac7fd2 (cell_index 647)
MM=M.merge(W85[['sub_id','sex','site','headmotion','age_baseline']], on='sub_id', how='left')
assert MM[['sex','site','headmotion']].notna().all().all()
COV=pd.get_dummies(MM[['sex','site']], drop_first=True).astype(float)
COV['headmotion']=MM['headmotion'].values
COVC=list(COV.columns); MM=pd.concat([MM,COV],axis=1)
print('covariate columns (%d):'%len(COVC), COVC)
def nested2(cov, add, base=COVC):
    X0=sm.add_constant(np.asarray(MM[base+cov],float)); X1=sm.add_constant(np.asarray(MM[base+cov+add],float))
    m0=sm.OLS(y,X0).fit(); m1=sm.OLS(y,X1).fit(); k=len(add); df2=int(m1.df_resid)
    dR2=m1.rsquared-m0.rsquared; F=(dR2/k)/((1-m1.rsquared)/df2)
    return dict(dR2=dR2,F=F,df1=k,df2=df2,P=stats.f.sf(F,k,df2))
ADJ={
 'summed simulated NP beyond covariates': nested2([], ['simbase_np_sum']),
 'summed empirical NP beyond covariates': nested2([], ['emp_np_sum']),
 'summed simulated beyond summed empirical': nested2(['emp_np_sum'],['simbase_np_sum']),
 'summed empirical beyond summed simulated': nested2(['simbase_np_sum'],['emp_np_sum']),
 '12 simulated edges beyond covariates': nested2([], sim),
 '12 empirical edges beyond covariates': nested2([], emp),
 '12 simulated edges beyond the 12 empirical edges': nested2(emp, sim),
 '12 empirical edges beyond the 12 simulated edges': nested2(sim, emp),
 '12 simulated edges beyond symptoms': nested2(['beha19_sum'], sim),
 '12 empirical edges beyond symptoms': nested2(['beha19_sum'], emp),
}
Z2=pd.DataFrame(ADJ).T; Z2['q_BH']=multipletests(Z2.P,method='fdr_bh')[1]
print(Z2[['dR2','F','df1','df2','P','q_BH']].to_string(float_format=lambda v:'%.4g'%v))

# ---------------------------------------------------------------- cell 0eb1725b (cell_index 690)
TASK_A = """Audit numerical and methodological consistency across the five final files of a Nature Medicine revision (digital-twin-brain / negative-profile connectivity paper).

Files (use the markers directly in your code; they resolve to readable paths):
- Manuscript: {{artifact:727e49a0-9803-49b6-ae06-ced3ffbdab95}}
- Online Methods: {{artifact:bfbbb659-12ff-4acd-93df-849a18b5bd14}}
- Supplementary Information: {{artifact:cfb4921d-728a-4379-b20b-d8ff31836c35}}
- Supplementary Tables workbook (sheet 'Table S24' is the statistics-reporting table): {{artifact:d2a2a06a-30f0-4353-b3f9-94cc82d0adbb}}

The .docx files contain tracked changes. Read the ACCEPTED view: parse word/document.xml with lxml, take every w:t but SKIP any w:t inside a w:del, and ignore w:delText. Do not use python-docx (it does not handle revisions correctly).

What to deliver:
1. Every statistic that appears in more than one file with DIFFERENT values for the same quantity (e.g. a t, F, r, rho, R2, dR2, P, q, d, g, n reported one way in the manuscript and another way in the Methods, SI or Table S24). Match on the surrounding wording, not on the bare label, and ignore differences that are only rounding of the same value (e.g. 0.0104 vs 0.01) - but DO report rounding that changes the second significant digit.
2. Every statistic in the manuscript or SI that is absent from Table S24, and every Table S24 row whose test statistic or P value contradicts the corresponding text.
3. Methodological contradictions: the same analysis described with different tests, different covariates, different correction methods (Bonferroni vs Benjamini-Hochberg vs none), different permutation counts, or different sample sizes. Check in particular: correction method for the clinical AMPA-state similarity analysis; permutation counts for the longitudinal analysis; whether the longitudinal models are described as including sex, recruitment site and mean framewise displacement as covariates everywhere; sample sizes for the clinical pharmacological dataset (41 vs 36) and for the longitudinal sample (85).
4. Number-format violations of the project rule: statistics to two decimals; P < 0.0001 written as "P < 0.0001"; P >= 0.0001 written as a plain decimal (no scientific notation) with at most four decimals; when a correction was applied, the corrected value must be given with the correction method named.

Save a CSV artifact named `consistency_audit_final.csv` with one row per finding and columns: severity (conflict | missing | format), quantity, value_in_manuscript, value_in_methods, value_in_SI, value_in_tableS24, files_involved, context_snippet, recommended_fix. Keep context_snippet under 200 characters.

Report only what you can substantiate by quoting the text; do not infer. If a value appears only once, that is not a finding."""

SCHEMA_A = {"type":"object","properties":{
 "n_conflicts":{"type":"integer"},"n_missing":{"type":"integer"},"n_format":{"type":"integer"},
 "top_findings":{"type":"array","items":{"type":"object","properties":{
    "severity":{"type":"string"},"quantity":{"type":"string"},"detail":{"type":"string"},"recommended_fix":{"type":"string"}},
    "required":["severity","quantity","detail","recommended_fix"]}},
 "artifacts":{"type":"array","items":{"type":"string"}}},
 "required":["n_conflicts","n_missing","n_format","top_findings"]}

TASK_B = """Determine which promises made in a Nature Medicine response letter are NOT yet implemented in the revised manuscript, Online Methods or Supplementary Information.

Files (markers resolve to readable paths):
- Response letter (contains tracked changes by several authors): {{artifact:af1fa416-a5a0-49be-b2d2-5e56e246f267}}
- Manuscript: {{artifact:727e49a0-9803-49b6-ae06-ced3ffbdab95}}
- Online Methods: {{artifact:bfbbb659-12ff-4acd-93df-849a18b5bd14}}
- Supplementary Information: {{artifact:cfb4921d-728a-4379-b20b-d8ff31836c35}}

Read the ACCEPTED view of every .docx: parse word/document.xml with lxml, take every w:t but SKIP any w:t inside a w:del, and ignore w:delText. Do not use python-docx. The response letter also has a word/comments.xml - read it too, because several comments are explicit to-do items addressed to the authors.

Method: go through the letter's reply paragraphs and extract every concrete commitment - sentences of the form "we have added", "we now report", "we have clarified", "the revised manuscript states", "we have removed", "we now state as a limitation", "this is described in Supplementary ...", "we will add ... before submission", plus every square-bracket placeholder and every "p. __, l. __" placeholder. For each commitment, search the manuscript, Methods and SI for the content it promises (match on the distinctive nouns and numbers of the claim, not on whole-sentence equality). Classify as implemented, partially implemented or not found, and say where you looked.

Save a CSV artifact named `response_letter_open_items.csv` with columns: letter_paragraph_index, reviewer_or_editor (as far as it can be told from the surrounding text), commitment (quoted, under 200 characters), status (implemented | partial | not_found), searched_for (the terms you searched), found_in (file and paragraph index, or empty), action_needed.

Be strict about the difference between a claim the letter makes about the paper and text that actually exists in the paper. Report the not_found and partial items first. Do not edit any document."""

SCHEMA_B = {"type":"object","properties":{
 "n_commitments":{"type":"integer"},"n_not_found":{"type":"integer"},"n_partial":{"type":"integer"},
 "open_items":{"type":"array","items":{"type":"object","properties":{
   "commitment":{"type":"string"},"status":{"type":"string"},"action_needed":{"type":"string"}},
   "required":["commitment","status","action_needed"]}},
 "artifacts":{"type":"array","items":{"type":"string"}}},
 "required":["n_commitments","n_not_found","n_partial","open_items"]}

pass  # [recovery: unresolvable interactive debris removed] d = host.delegate([
# [recovery: unresolvable interactive debris removed]   {"name":"Stats audit","task":TASK_A,"output_schema":SCHEMA_A,
# [recovery: unresolvable interactive debris removed]    "context_summary":"Final files of a revision about individually fitted digital twin brain models and a 12-edge negative-profile (NP) connectivity phenotype. Recent changes: the longitudinal analysis (n = 85) was switched to a covariate-adjusted specification (sex, recruitment site, mean framewise displacement in every model) and the simulated and measured read-outs are compared at matched degrees of freedom; the clinical AMPA-state similarity analysis uses a permutation P followed by Benjamini-Hochberg FDR across four symptom measures; Table S24 is the reporting table that should carry every statistic."},
# [recovery: unresolvable interactive debris removed]   {"name":"Letter audit","task":TASK_B,"output_schema":SCHEMA_B,
# [recovery: unresolvable interactive debris removed]    "context_summary":"Same revision. The letter was drafted partly by a colleague's AI assistant and contains both replies and internal comments; several replies claim additions that may never have reached the paper (for example a sensitivity power analysis in the Methods, a Discussion limitation sentence, a convergence criterion for the assimilation, a comparison of included versus excluded participants, and a README workflow)."}
# [recovery: unresolvable interactive debris removed] ], wait=False)
print(d)

# ---------------------------------------------------------------- cell e414d80b (cell_index 706)
import pandas as pd, numpy as np, re, os, glob
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/'
q=pd.read_csv(B+'np_beha_85subjects_all_quantities.csv')
w=pd.read_csv(B+'np85_12edges_repetitions_wide.csv')
print(q.shape, list(q.columns))
print(w.shape, list(w.columns)[:20])

# ---------------------------------------------------------------- cell c29ac0b3 (cell_index 709)
SIM12=d[[f'simbase_edge{i}' for i in range(1,13)]].astype(float)
EMP12=d[[f'emp_edge{i}' for i in range(1,13)]].astype(float)
SYM=d[['beha19_sum']].astype(float)
SUMS=d[['simbase_np_sum']].astype(float); SUME=d[['emp_np_sum']].astype(float)
for yname in ['beha_change_resi','beha_change_raw','beha23_sum']:
    print(yname,{k:round(v,4) for k,v in nested(COV,SIM12,d[yname].astype(float).values).items()})

# ---------------------------------------------------------------- cell 8d74c997 (cell_index 710)
y=d['beha_change_raw'].astype(float).values
print('emp12',{k:round(v,4) for k,v in nested(COV,EMP12,y).items()})
print('sumE ',{k:round(v,4) for k,v in nested(COV,SUME,y).items()})

def loo_r(X,y):
    X=np.asarray(X,float); H=X@np.linalg.pinv(X); h=np.diag(H)
    yh=H@y; e=y-yh; pred=y-e/(1-h)
    return np.corrcoef(pred,y)[0,1], pred

BASE=pd.concat([COV,SIM12],axis=1)
FULL=pd.concat([COV,SIM12,SUME],axis=1)
r_b,p_b=loo_r(BASE,y); r_f,p_f=loo_r(FULL,y)
inc=nested(BASE,SUME,y)
print('\nITEM14 increment:',{k:round(v,5) for k,v in inc.items()})
print('LOO r base=%.4f full=%.4f'%(r_b,r_f))
# permutation for the added term: shuffle SUME residualised? standard: permute the added predictor
rng=np.random.default_rng(0); nperm=5000
obs=inc['F']; cnt=0
se=SUME.values.ravel()
for _ in range(nperm):
    pe=pd.DataFrame({'x':rng.permutation(se)},index=SUME.index)
    cnt+= nested(BASE,pe,y)['F']>=obs
print('perm P (F) = %.4f'%((cnt+1)/(nperm+1)))
# out-of-sample paired comparison
e_b=np.abs(y-p_b); e_f=np.abs(y-p_f)
t,pv=stats.ttest_rel(e_b,e_f); print('paired t on |err| t(%d)=%.2f P=%.3f'%(len(y)-1,t,pv))
print('Wilcoxon P=%.3f'%stats.wilcoxon(e_b,e_f).pvalue)

# ---------------------------------------------------------------- cell e44e3f3e (cell_index 711)
def williams(r_jk,r_jh,r_kh,n):
    R=1-r_jk**2-r_jh**2-r_kh**2+2*r_jk*r_jh*r_kh
    t=(r_jk-r_jh)*np.sqrt((n-1)*(1+r_kh)/(2*((n-1)/(n-3))*R+((r_jk+r_jh)**2/4)*(1-r_kh)**3))
    return t, 2*stats.t.sf(abs(t),n-3)
r_kh=np.corrcoef(p_f,p_b)[0,1]
tw,pw=williams(r_f,r_b,r_kh,85)
print('pred-pred r=%.3f  Williams t(82)=%.2f P=%.3f'%(r_kh,tw,pw))
rng=np.random.default_rng(1); nperm=5000; c=0
for _ in range(nperm):
    c+= loo_r(FULL,rng.permutation(y))[0]>=r_f
print('LOO perm P full=%.4f'%((c+1)/(nperm+1)))
out=pd.DataFrame([
 dict(model='covariates + 12 simulated edges',k_added=12,dR2=0.3347,F=3.0169,df1=12,df2=63,P=0.0022,R2=0.4176,LOO_r=round(r_b,4)),
 dict(model='covariates + 12 simulated edges + summed empirical NP',k_added=1,dR2=inc['dR2'],F=inc['F'],df1=1,df2=62,P=inc['P'],R2=inc['R2full'],LOO_r=round(r_f,4)),
])
out.to_csv(os.path.join(OUT_DIR, 'long85_add_summed_empirical_to_sim12.csv'), index=False)
print(out.round(4).to_string(index=False))
