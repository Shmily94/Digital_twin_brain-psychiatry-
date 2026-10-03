"""Build an editable PowerPoint version of Fig. 1 (panels a-f).

Every piece is a separate, movable object:
  * cards, header bands, letter badges, colour chips and legend swatches -> shapes
  * all prose, statistics and axis captions                             -> text boxes
  * each data plot                                                      -> its own PNG
    (exported here from the same tables that produce Figs 2-5, at final size,
     transparent background, 600 dpi; matching PDFs are written alongside)
  * pictorial items                                                     -> the
    author's own assets in fig1_assets/ (tinted copies written to fig1_ppt_parts/)

Geometry mirrors fig1_v4.py 1:1, so the deck opens looking like the rendered
figure; positions can then be nudged in PowerPoint without touching the data.

Outputs: fig1_editable.pptx, fig1_ppt_parts/*.png|pdf
"""
import os, sys
import numpy as np, pandas as pd
from scipy import stats as sstats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from PIL import Image
from pptx import Presentation
from pptx.util import Mm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, C, LW       # noqa: E402
from supp_kit import fill                            # noqa: E402
from fig1_synapse_vector import draw_synapse, dark   # noqa: E402
apply_np_style()

D = os.path.join(HERE, 'fig1_data')
A = os.path.join(HERE, 'fig1_assets')
P = os.path.join(HERE, 'fig1_ppt_parts')
F2 = os.path.join(HERE, '..', 'fig.2', 'fig2_data')
F4 = os.path.join(HERE, '..', 'fig.4', 'fig4_data')
os.makedirs(P, exist_ok=True)

INK, SOFT, FAINT, HAIR = '#1A1A1A', '#4D4D4D', '#8C8C8C', '#D9D9D9'
BAND, RULE = '#F0F0F0', '#E0E0E0'

# ----------------------------------------------------------------- data ------
STR = pd.read_csv(f'{F2}/fig2c_profile_scores.csv')
EDG = pd.read_csv(f'{D}/fig1_mini_np12_edges.csv')
FID = pd.read_csv(f'{D}/fig1_mini_fidelity.csv')
POP = pd.read_csv(f'{F4}/fig4_subject_level_n288.csv')
HV = pd.read_csv(f'{D}/fig1_mini_healthy_n27.csv')
CLI = pd.read_csv(f'{D}/fig1_mini_clinical_n36.csv')
LON = pd.read_csv(f'{D}/fig1_mini_longitudinal_n85.csv')
hc = STR.loc[STR.Diseased == 'HC', 'Neg_NP'].values
pt_ = STR.loc[STR.Diseased != 'HC', 'Neg_NP'].values
dKET = (HV.Ketamine - HV.Placebo).values
dMID = (HV.Midazolam - HV.Placebo).values
CLI['d'] = CLI.FC_d2 - CLI.FC_p2
rRAW = sstats.pearsonr(LON.ampa_restoration_index, LON.fu3_symptom_change)[0]
RNG = np.random.default_rng(3)

# ------------------------------------------------------------ part export ----
def part(name, w_mm, h_mm, draw, dpi=600):
    """render one element to fig1_ppt_parts/<name>.png|pdf on a transparent ground"""
    fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    draw(ax, w_mm, h_mm)
    fig.savefig(f'{P}/{name}.png', dpi=dpi, transparent=True)
    fig.savefig(f'{P}/{name}.pdf', transparent=True)
    plt.close(fig)
    return f'{P}/{name}.png'


def bx(ax, xc, v, col, w=.30, pts=True, ps=2.0, ylim=None):
    """box plot in axes fraction coordinates; xc and ylim in data units"""
    v = np.asarray(v, float)
    lo_, hi_ = ylim
    Y = lambda t: (np.asarray(t, float) - lo_) / (hi_ - lo_)
    q1, med, q3 = np.percentile(v, [25, 50, 75]); iqr = q3 - q1
    lo = v[v >= q1 - 1.5 * iqr].min(); hi = v[v <= q3 + 1.5 * iqr].max()
    ax.plot([xc, xc], [Y(lo), Y(hi)], color=INK, lw=LW * .8, zorder=3)
    ax.add_patch(FancyBboxPatch((xc - w / 2, Y(q1)), w, Y(q3) - Y(q1),
                                boxstyle='round,pad=0,rounding_size=0.004',
                                facecolor=fill(col), edgecolor=INK, lw=LW * .8, zorder=4))
    ax.plot([xc - w / 2, xc + w / 2], [Y(med)] * 2, color=INK, lw=LW * 1.1, zorder=6)
    if pts:
        jx = RNG.uniform(-w * .26, w * .26, len(v))
        ax.scatter(xc + jx, Y(v), s=ps, facecolor=col, edgecolor=INK, linewidth=.10,
                   zorder=5, alpha=.9)


def tint_asset(src, out, col):
    im = np.array(Image.open(os.path.join(A, src)).convert('RGBA')).astype(float) / 255.0
    rgb = mcolors.to_rgb(col)
    im[..., 0], im[..., 1], im[..., 2] = rgb
    Image.fromarray((im * 255).astype(np.uint8)).save(f'{P}/{out}')
    return f'{P}/{out}'


def crop_asset(src, out, crop):
    im = Image.open(os.path.join(A, src))
    l, t, r, b = crop
    W, H = im.size
    im.crop((int(l * W), int(t * H), W - int(r * W), H - int(b * H))).save(f'{P}/{out}')
    return f'{P}/{out}'


# ---- a: NP ring -------------------------------------------------------------
def _ring(ax, w, h):
    nodes = sorted(pd.unique(EDG[['i_217', 'j_217']].values.ravel()))
    th = np.linspace(90, -270, len(nodes), endpoint=False) * np.pi / 180
    R = .44
    ax.add_patch(Circle((.5, .5), R, facecolor='none', edgecolor='#EDEDED',
                        linewidth=3.0, transform=ax.transData, zorder=2))
    pos = {n: (.5 + R * np.cos(t), .5 + R * np.sin(t)) for n, t in zip(nodes, th)}
    for _, e in EDG.iterrows():
        a_, b_ = pos[e.i_217], pos[e.j_217]
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=C('np12'), lw=1.4, alpha=.9,
                zorder=3, solid_capstyle='round')
    for n, (px, py) in pos.items():
        ax.add_patch(Circle((px, py), .034, facecolor='white', edgecolor=C('np12'),
                            linewidth=LW, zorder=4))


# ---- b: STRATIFY boxes ------------------------------------------------------
def _bbox(ax, w, h):
    yl = (-4.6, 4.6)
    ax.plot([0, 1], [.5, .5], color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
    bx(ax, .28, hc, C('hc'), w=.26, ps=1.6, ylim=yl)
    bx(ax, .72, pt_, C('patient'), w=.26, ps=1.6, ylim=yl)
    ax.text(.28, -.035, 'HC', fontsize=4.2, color=SOFT, ha='center', va='top')
    ax.text(.72, -.035, 'patients', fontsize=4.2, color=SOFT, ha='center', va='top')


# ---- c: build fidelity bars -------------------------------------------------
def _bars(ax, w, h):
    ORD = ['3m_268', '10m_268', '10m_1000', '10m_own', '10m', '100m', '1b']
    LBL = ['3M/268', '10M/268', '10M/1k', '10M/vox*', '10M/vox', '100M/vox', '1B/vox']
    COL = [C('model_regional')] * 3 + [C('model_voxel')] * 4
    lo_, hi_ = .60, .95
    Y = lambda t: (t - lo_) / (hi_ - lo_)
    for gv in (.7, .8, .9):
        ax.plot([.02, 1], [Y(gv)] * 2, color='#EFEFEF', lw=LW, zorder=1)
        ax.text(.005, Y(gv), f'{gv:.1f}', fontsize=3.8, color=FAINT, ha='right', va='center')
    for k, (m, c) in enumerate(zip(ORD, COL)):
        v = float(FID.loc[FID.model == m, 'bold_r_mean'].iloc[0])
        xc = .09 + k * .135
        ax.add_patch(FancyBboxPatch((xc - .048, 0), .096, Y(v),
                                    boxstyle='round,pad=0,rounding_size=0.003',
                                    facecolor=c, edgecolor='none', lw=0, zorder=4))
        ax.text(xc + .022, -.03, LBL[k], fontsize=3.7, color=SOFT, ha='right', va='top',
                rotation=52, rotation_mode='anchor')


# ---- d: perturbation trajectories ------------------------------------------
def _traj(ax, w, h):
    yl = (-3.4, 12.6)
    Y = lambda t: (np.asarray(t, float) - yl[0]) / (yl[1] - yl[0])
    XS = [.16, .5, .84]
    ax.plot([0, 1], [Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
    for _, r in POP.sample(110, random_state=1).iterrows():
        ax.plot(XS, Y([r.simulated, r.ampa, r.gaba]), color='#CCCCCC', lw=.14,
                alpha=.5, zorder=2)
    for xc, col, v in zip(XS, [C('baseline'), C('ampa'), C('gaba')],
                          [POP.simulated, POP.ampa, POP.gaba]):
        bx(ax, xc, v, col, w=.20, pts=False, ylim=yl)
    for xc, lab in zip(XS, ['baseline', 'AMPA \u2191', 'GABA-A \u2191']):
        ax.text(xc, -.03, lab, fontsize=4.1, color=SOFT, ha='center', va='top')


# ---- e: drug effects, four boxes -------------------------------------------
def _drug(ax, w, h):
    yl = (-5.6, 5.6)
    ax.plot([0, 1], [.5, .5], color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
    XS = [.13, .37, .63, .87]
    for xc, v, col in zip(XS, [dKET, dMID, CLI.loc[CLI.group == 'MDD', 'd'].values,
                               CLI.loc[CLI.group == 'HC', 'd'].values],
                          [C('ketamine'), C('midazolam'), C('mdd'), C('hc')]):
        bx(ax, xc, v, col, w=.15, ps=1.8, ylim=yl)
    ax.plot([.5, .5], [0, 1], color='#EAEAEA', lw=LW, zorder=1)
    for xc, lab in zip(XS, ['ketamine', 'midazolam', 'MDD 22', 'HC 14']):
        ax.text(xc, -.03, lab, fontsize=4.0, color=SOFT, ha='center', va='top')
    ax.text(.25, 1.02, 'healthy, $n$ = 27', fontsize=4.0, color=SOFT, ha='center', va='bottom')
    ax.text(.75, 1.02, 'clinical, ketamine', fontsize=4.0, color=SOFT, ha='center', va='bottom')


# ---- f: forecast scatter ----------------------------------------------------
def _scatter(ax, w, h):
    xv, yv = LON.ampa_restoration_index.values, LON.fu3_symptom_change.values
    X = lambda t: (t - (xv.min() - .1 * np.ptp(xv))) / (1.2 * np.ptp(xv))
    Y = lambda t: (t - (yv.min() - .1 * np.ptp(yv))) / (1.2 * np.ptp(yv))
    ax.scatter(X(xv), Y(yv), s=2.6, facecolor=C('ampa'), edgecolor=dark(C('ampa')),
               linewidth=.14, zorder=4)
    b1, b0 = np.polyfit(xv, yv, 1)
    gx = np.linspace(xv.min(), xv.max(), 20)
    ax.plot(X(gx), Y(b0 + b1 * gx), color=dark(C('ampa')), lw=1.0, zorder=5)


PARTS = {
    'a_ring': part('a_ring', 18.0, 18.0, _ring),
    'b_box': part('b_box', 34.0, 15.0, _bbox),
    'c_bars': part('c_bars', 33.5, 15.0, _bars),
    'd_traj': part('d_traj', 38.0, 24.0, _traj),
    'e_drug': part('e_drug', 44.0, 26.0, _drug),
    'f_scatter': part('f_scatter', 36.0, 26.0, _scatter),
    'synapse': os.path.join(A, 'synapse_palette.png'),
    'checklist': tint_asset('checklist.png', 'checklist_t.png', SOFT),
    'scanner': tint_asset('scanner.png', 'scanner_t.png', SOFT),
    'syringe': tint_asset('syringe.png', 'syringe_t.png', SOFT),
    'monitor': tint_asset('monitor.png', 'monitor_t.png', SOFT),
    'neuron': tint_asset('neuron.png', 'neuron_t.png', SOFT),
    'head_hc': tint_asset('head_brain.png', 'head_hc_t.png', C('hc')),
    'head_mdd': tint_asset('head_mood.png', 'head_mdd_t.png', C('mdd')),
    'head_aud': tint_asset('head_aud.png', 'head_aud_t.png', C('aud')),
    'gmv': crop_asset('gmv_slices.png', 'gmv_c.png', (.635, .069, .102, .188)),
    'wm': crop_asset('wm_fibers.png', 'wm_c.png', (0, .306, 0, .313)),
    'brain': os.path.join(A, 'glass_brain.png'),
    'bold_sst': crop_asset('bold_sst.png', 'bold_sst_c.png', (0, .408, 0, 0)),
    'bold_mid': crop_asset('bold_mid.png', 'bold_mid_c.png', (0, .403, 0, 0)),
}

# ------------------------------------------------------------------ deck -----
SW, SH = 180.0, 235.0
prs = Presentation()
prs.slide_width, prs.slide_height = Mm(SW), Mm(SH)
sl = prs.slides.add_slide(prs.slide_layouts[6])
UX, UY = SW / 100.0, SH / 100.0


def mx(u):
    return Mm(u * UX)


def my(u):                      # canvas y (0 = bottom) -> slide y (0 = top)
    return Mm((100 - u) * UY)


def rgb(h):
    h = mcolors.to_hex(h).lstrip('#')
    return RGBColor.from_string(h.upper())


def shape(kind, x, y, w, h, fc=None, lc=None, lw=.6, txt=None, size=5.0, col=INK,
          bold=False, align=PP_ALIGN.CENTER):
    """x, y = canvas units of the TOP-LEFT corner; w, h = canvas units"""
    s = sl.shapes.add_shape(kind, mx(x), my(y), Mm(w * UX), Mm(h * UY))
    if fc is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fc)
    if lc is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = rgb(lc); s.line.width = Pt(lw)
    s.shadow.inherit = False
    tf = s.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = txt or ''
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = rgb(col)
    r.font.name = 'Arial'
    return s


def text(x, y, s_, size=4.6, col=SOFT, bold=False, w=40, h=4, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False, spacing=1.25):
    tb = sl.shapes.add_textbox(mx(x), my(y), Mm(w * UX), Mm(h * UY))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(str(s_).split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = rgb(col); r.font.name = 'Arial'
    return tb


def pic_h(path, w):
    im = Image.open(path)
    return w * (im.size[1] / im.size[0]) * (UX / UY)


def pic(path, x, y, w):
    """place an image with its aspect preserved; x, y = top-left in canvas units"""
    im = Image.open(path)
    h = w * (im.size[1] / im.size[0]) * (UX / UY)
    sl.shapes.add_picture(path, mx(x), my(y), width=Mm(w * UX))
    return h


def arrow(kind, x, y, w, h, col):
    s = sl.shapes.add_shape(kind, mx(x), my(y), Mm(w * UX), Mm(h * UY))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(col)
    s.line.fill.background(); s.shadow.inherit = False
    return s


RECT, RRECT, OVAL = MSO_SHAPE.RECTANGLE, MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.OVAL

# --- title -------------------------------------------------------------------
text(2.0, 99.6, 'Fig. 1 | A perturbation-capable digital twin brain for a symptom-linked circuit',
     size=8.0, col=INK, bold=True, w=96, h=4)
text(2.0, 96.4, 'A circuit whose connectivity tracks symptom load is identified empirically (a, b), rebuilt '
                'inside individual digital twin brains (c) and perturbed in silico (d); the simulated response '
                'is then tested against two pharmacological datasets (e) and against symptom change four years '
                'later (f).', size=5.3, col=SOFT, w=96, h=6, spacing=1.35)

X0, GAP = 2.0, 1.4
W2 = (96 - GAP) / 2
W3 = (96 - 2 * GAP) / 3
RY1, RH1 = 69.5, 24.5
RY2, RH2 = 50.0, 18.0
RY3, RH3 = 12.5, 36.0

CARDS = [('a', X0, RY1, W2, RH1, 'A shared brain phenotype of transdiagnostic symptoms'),
         ('b', X0 + W2 + GAP, RY1, W2, RH1, 'Validation of the phenotype in an independent clinical sample'),
         ('c', X0, RY2, 96.0, RH2, 'Construction of personalised task-state digital twin brains'),
         ('d', X0, RY3, W3, RH3, 'Virtual manipulation of neurotransmitter systems'),
         ('e', X0 + W3 + GAP, RY3, W3, RH3, 'Validation in pharmacological fMRI data'),
         ('f', X0 + 2 * (W3 + GAP), RY3, W3, RH3, 'Forecasting four-year symptom change')]
for letter, x, y, w, h, title in CARDS:
    shape(RRECT, x, y + h, w, h, fc='white', lc=HAIR, lw=.6)
    shape(RECT, x, y + h, w, 5.2, fc=BAND)
    shape(OVAL, x + 1.05, y + h - 1.5, 2.1, 2.1 * (UX / UY), fc=SOFT, txt=letter,
          size=5.2, col='white', bold=True)
    text(x + 4.0, y + h - 1.0, title, size=5.5, col=INK, bold=True, w=w - 5.0, h=4.4,
         spacing=1.15)

# --- a -----------------------------------------------------------------------
x, y, w, h = X0, RY1, W2, RH1
top = y + h - 6.0
hh = pic(PARTS['checklist'], x + 1.4, top, 2.6)
text(x + 4.8, top - .3, 'six DAWBA symptom bands', size=4.1, w=22, h=2)
pic(PARTS['scanner'], x + 1.2, top - 4.6, 5.0)
text(x + 7.0, top - 5.0, 'MID and SST fMRI,\nsix task conditions', size=4.1, w=20, h=4)
arrow(MSO_SHAPE.RIGHT_ARROW, x + 16.4, top - 3.0, 1.4, 1.2, '#B0B0B0')
text(x + 18.6, top - .3, 'connectome-based predictive modelling', size=4.1, col=INK, w=26, h=2)
for k, (col, lab) in enumerate([(C('neg_profile'), 'negative profile, 29 edges'),
                                (C('pos_profile'), 'positive profile, 34 edges'),
                                (C('np12'), 'NP factor, 12 DTB-representable edges')]):
    yy = top - 2.6 - k * 2.0
    shape(RECT, x + 18.8, yy, 1.6, .5, fc=col)
    text(x + 21.1, yy + .9, lab, size=4.1, w=24, h=2)
pic(PARTS['a_ring'], x + w - 11.5, y + h / 2 + 4.6, 10.0)
text(x + 1.0, y + 8.4, 'Connectivity of one 29-edge profile tracks symptom load across six domains',
     size=4.4, w=w - 2, h=3, spacing=1.35)
text(x + 1.0, y + 4.4, 'Fig. 2a\u2013d \u00b7 Figs S1\u2013S3 \u00b7 Tables S3, S4, S6', size=4.0,
     col=FAINT, italic=True, w=w - 2, h=2.6)

# --- b -----------------------------------------------------------------------
x, y, w, h = X0 + W2 + GAP, RY1, W2, RH1
top = y + h - 6.0
shape(RECT, x + 1.0, top, 1.4, 1.4 * (UX / UY), fc=C('pos_profile'), lc=HAIR, lw=.4)
text(x + 3.0, top + .2, 'STRATIFY / ESTRA', size=4.4, col=INK, w=26, h=2)
text(x + 3.0, top - 1.5, 'n = 427: 225 HC, 104 MDD, 98 AUD', size=4.2, w=28, h=2)
for k, (key, lab, col) in enumerate([('head_hc', 'HC 225', C('hc')),
                                     ('head_mdd', 'MDD 104', C('mdd')),
                                     ('head_aud', 'AUD 98', C('aud'))]):
    xx = x + 1.4 + k * 6.6
    hh2 = pic(PARTS[key], xx, top - 4.0, 2.8)
    text(xx - .3, top - 4.4 - hh2, lab, size=4.1, w=8, h=2)
hb = pic_h(PARTS['b_box'], 15.0)
pic(PARTS['b_box'], x + w * .52, top - 1.2, 15.0)
text(x + w * .52 - 2.2, top - 1.2 - hb / 2 + 3.0, 'negative NP profile (z)', size=4.1, w=12, h=2)
text(x + 1.0, y + 9.6, 'Hedges\u2019 g = 0.37 [0.18, 0.56], t(425) = 3.83, P_Bonferroni = 2.96 \u00d7 10\u207b\u2074;\n'
                       'the positive profile does not separate the groups', size=4.4, w=w - 2, h=4,
     spacing=1.35)
text(x + 1.0, y + 4.4, 'Fig. 2c, e \u00b7 Fig. S1 \u00b7 Table S6', size=4.0, col=FAINT, italic=True,
     w=w - 2, h=2.6)

# --- c -----------------------------------------------------------------------
x, y, w, h = X0, RY2, 96.0, RH2
top = y + h - 6.0
SX = [x + 1.0, x + 20.0, x + 37.6, x + 52.0, x + 73.4]
for k, (sx, lab) in enumerate(zip(SX, ['Empirical data', 'Local dynamics', 'Task-state DTB',
                                       'Assimilated BOLD', 'Model selection'])):
    text(sx, top + .4, lab, size=4.5, col=INK, bold=True, w=20, h=2)
    if k:
        arrow(MSO_SHAPE.RIGHT_ARROW, sx - 2.2, y + h / 2 - 1.0, 1.4, 1.2, '#B0B0B0')
pic(PARTS['gmv'], SX[0] + .2, top - 1.4, 5.6)
text(SX[0] + .2, y + 4.6, 'grey matter volume', size=4.0, w=10, h=3)
pic(PARTS['wm'], SX[0] + 8.2, top - 1.4, 4.6)
text(SX[0] + 7.8, y + 4.6, 'white matter fibres', size=4.0, w=10, h=3)
pic(PARTS['neuron'], SX[1] + .2, top - 1.2, 4.6)
text(SX[1] + .2, y + 4.6, 'leaky integrate-and-fire neurons,\nAMPA and GABA-A synapses', size=4.0,
     w=17, h=4)
pic(PARTS['brain'], SX[2] + 1.2, top - .6, 7.6)
text(SX[2] + .2, y + 4.6, '3 M\u20131 B neurons \u00b7 268 or 1,000 regions, or voxel-wise', size=4.0,
     w=14, h=4)
text(SX[3] + .2, top - 1.0, 'SST, anterior PFC \u00b7 empirical / simulated', size=3.9, w=20, h=2)
pic(PARTS['bold_sst'], SX[3] + .2, top - 2.0, 12.6)
text(SX[3] + .2, top - 5.2, 'MID, nucleus accumbens \u00b7 empirical / simulated', size=3.9, w=20, h=2)
pic(PARTS['bold_mid'], SX[3] + .2, top - 6.2, 12.6)
text(SX[4] + 2.2, top - .2, 'assimilated-region BOLD r, 12 twins', size=3.9, w=20, h=2)
pic(PARTS['c_bars'], SX[4] + 1.6, top - 1.6, 18.6)
text(x + 1.0, y + 4.2, 'Fig. 3 \u00b7 Figs S4, S19, S22 \u00b7 Tables S8\u2013S12   |   * 10 M assimilation '
                       'hyper-parameters; every other build uses 3 M (268 regions) or 100 M (voxel-wise)',
     size=4.0, col=FAINT, italic=True, w=w - 2, h=2.6)

# --- d -----------------------------------------------------------------------
x, y, w, h = X0, RY3, W3, RH3
top = y + h - 6.0
shape(RECT, x + 1.0, top, 1.4, 1.4 * (UX / UY), fc=C('ampa'), lc=HAIR, lw=.4)
text(x + 2.9, top + .2, 'AMPA 0.0044, then GABA-A 0.0040', size=4.4, col=INK, w=27, h=2)
text(x + 2.9, top - 1.5, 'n = 288 twins, 3 M / 268 regions', size=4.2, w=27, h=2)
hs = pic(PARTS['synapse'], x + .8, top - 3.4, 21.5)
ht = pic_h(PARTS['d_traj'], 14.5)
ytraj = top - 3.4 - hs - 2.4
text(x + 1.0, ytraj + 1.4, 'simulated NP factor, n = 288 twins', size=4.1, w=28, h=2)
pic(PARTS['d_traj'], x + 5.0, ytraj, 14.5)
text(x + 1.0, y + 10.0, 'AMPA +0.78, t(287) = 14.14, 234 / 288 up; GABA-A +2.74,\n'
                        't(287) = 27.11, 282 / 288 up; 229 both-up \u00b7 59 any-down',
     size=4.4, w=w - 2, h=4, spacing=1.35)
text(x + 1.0, y + 4.4, 'Fig. 4 \u00b7 Figs S17, S18 \u00b7 Tables S13\u2013S15, S17', size=4.0,
     col=FAINT, italic=True, w=w - 2, h=2.6)

# --- e -----------------------------------------------------------------------
x, y, w, h = X0 + W3 + GAP, RY3, W3, RH3
top = y + h - 6.0
shape(RECT, x + 1.0, top, 1.4, 1.4 * (UX / UY), fc=C('ketamine'), lc=HAIR, lw=.4)
text(x + 2.9, top + .2, 'crossover n = 27 \u00b7 clinical n = 41', size=4.4, col=INK, w=27, h=2)
text(x + 2.9, top - 1.5, 'placebo / ketamine / midazolam', size=4.2, w=27, h=2)
pic(PARTS['syringe'], x + 1.0, top - 3.8, 3.4)
arrow(MSO_SHAPE.RIGHT_ARROW, x + 5.2, top - 5.0, 1.2, 1.1, '#B0B0B0')
pic(PARTS['scanner'], x + 6.6, top - 3.8, 4.8)
pic(PARTS['monitor'], x + 12.6, top - 4.0, 3.4)
text(x + 16.8, top - 4.6, 'resting state\nand MID', size=4.0, w=12, h=4)
hd = pic_h(PARTS['e_drug'], 19.9)
ydrug = top - 8.6
text(x + 1.0, ydrug + 1.4, '\u0394 NP-related connectivity, drug \u2212 placebo', size=4.1, w=28, h=2)
pic(PARTS['e_drug'], x + 5.0, ydrug, 19.9)
text(x + 1.0, y + 10.4, 'group \u00d7 drug t(30) = 3.43, P = 0.0018; placebo baseline,\n'
                        'n = 41: t(35) = \u22122.51, P = 0.017; slopes on placebo < 1',
     size=4.4, w=w - 2, h=4, spacing=1.35)
text(x + 1.0, y + 4.4, 'Fig. 5a\u2013c \u00b7 Figs S9, S12, S13 \u00b7 Table S21', size=4.0,
     col=FAINT, italic=True, w=w - 2, h=2.6)

# --- f -----------------------------------------------------------------------
x, y, w, h = X0 + 2 * (W3 + GAP), RY3, W3, RH3
top = y + h - 6.0
shape(RECT, x + 1.0, top, 1.4, 1.4 * (UX / UY), fc=C('high_symptom'), lc=HAIR, lw=.4)
text(x + 2.9, top + .2, 'IMAGEN follow-up', size=4.4, col=INK, w=27, h=2)
text(x + 2.9, top - 1.5, 'n = 85, age 19 \u2192 23', size=4.2, w=27, h=2)
arrow(MSO_SHAPE.RIGHT_ARROW, x + 1.6, top - 3.8, w - 3.2, .7, C('high_symptom'))
text(x + 1.4, top - 5.2, 'age 19\nDTB built', size=4.0, w=10, h=4)
text(x + w - 9.0, top - 5.2, 'age 23\nsymptoms', size=4.0, w=8, h=4, align=PP_ALIGN.RIGHT)
hf = pic_h(PARTS['f_scatter'], 18.0)
yscat = top - 7.4
text(x + 1.0, yscat + 1.4, 'perturbational response vs symptom change', size=4.1, w=28, h=2)
pic(PARTS['f_scatter'], x + 6.0, yscat, 18.0)
text(x + 1.0, y + 10.4, f'r = {rRAW:.2f} unadjusted; partial r = 0.24, P = 0.026 given\n'
                        'empirical baseline NP; model R\u00b2 = 0.23, F(5,79) = 4.80',
     size=4.4, w=w - 2, h=4, spacing=1.35)
text(x + 1.0, y + 4.4, 'Fig. 5h, i \u00b7 Fig. S14', size=4.0, col=FAINT, italic=True, w=w - 2, h=2.6)

# --- flow arrows -------------------------------------------------------------
arrow(MSO_SHAPE.DOWN_ARROW, X0 + W2 * .5, RY1 - .4, 1.2, 1.2, '#B0B0B0')
arrow(MSO_SHAPE.DOWN_ARROW, X0 + W2 + GAP + W2 * .5, RY1 - .4, 1.2, 1.2, '#B0B0B0')
arrow(MSO_SHAPE.DOWN_ARROW, X0 + 46.0, RY2 - .4, 1.2, 1.2, '#B0B0B0')
arrow(MSO_SHAPE.RIGHT_ARROW, X0 + W3 + .1, RY3 + RH3 * .60, 1.2, 1.1, dark(C('ampa')))
arrow(MSO_SHAPE.RIGHT_ARROW, X0 + 2 * W3 + GAP + .1, RY3 + RH3 * .60, 1.2, 1.1, C('high_symptom'))

# --- colour reference --------------------------------------------------------
text(2.0, 10.0, 'Colour correspondence', size=5.0, col=INK, bold=True, w=40, h=2.4)
PAIRS = [(C('ampa'), C('ketamine'), 'virtual AMPA \u2194 ketamine'),
         (C('gaba'), C('midazolam'), 'virtual GABA-A \u2194 midazolam'),
         (C('baseline'), C('placebo'), 'simulated baseline \u2194 placebo')]
for k, (a1, b1, lab) in enumerate(PAIRS):
    xx = 2.0 + k * 21.0
    shape(RECT, xx, 7.6, 1.3, 1.3 * (UX / UY), fc=a1, lc=HAIR, lw=.4)
    shape(RECT, xx + 1.4, 7.6, 1.3, 1.3 * (UX / UY), fc=b1, lc=HAIR, lw=.4)
    text(xx + 3.4, 7.5, lab, size=4.1, w=18, h=2)
SING = [(C('np12'), 'NP factor / negative profile'), (C('pos_profile'), 'positive profile'),
        (C('model_regional'), 'regional build'), (C('model_voxel'), 'voxel build'),
        (C('hc'), 'HC / baseline / placebo'), (C('high_symptom'), 'high-symptom'),
        (C('patient'), 'patient / MDD'), (C('aud'), 'AUD')]
for k, (col, lab) in enumerate(SING):
    xx = 2.0 + (k % 4) * 19.6
    yy = 5.2 if k < 4 else 3.0
    shape(RECT, xx, yy, 1.3, 1.3 * (UX / UY), fc=col, lc=HAIR, lw=.4)
    text(xx + 1.9, yy - .1, lab, size=4.0, w=17, h=2)
text(66.0, 7.5, 'every plotted point is one participant\u2019s observed or simulated value;\n'
                'no data element of this figure is schematic', size=3.9, col=FAINT, w=32, h=4)

out = os.path.join(HERE, 'fig1_editable.pptx')
prs.save(out)
print('wrote', out)
print('parts:', len([f for f in os.listdir(P) if f.endswith('.png')]), 'png in', P)
print('shapes on slide:', len(sl.shapes.__iter__.__self__._spTree) - 2)
