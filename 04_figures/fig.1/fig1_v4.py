"""Fig. 1 - framework overview, v4.

Layout and card grammar from fig1_pipeline / fig1_framework_v2 (lettered badge,
grey header band, cohort chips, takeaway line, figure pointer, colour strip).
Pictorial items are the author's own assets, lifted from framework.pptx and kept
in fig1_assets/ (tractography, anatomy, LIF neuron, AMPA synapse cartoon,
assimilated BOLD traces, study-design icons).  Every colour that carries meaning
comes from the registered manuscript palette (np_dtb_style.C), and every data
panel is drawn from the same tables that produce Figs 2-5 - nothing is schematic
data.

Panels follow the author's framework.pptx, plus f:
  a  shared brain phenotype of transdiagnostic symptoms      IMAGEN n = 1,050
  b  validation of the phenotype in a clinical sample        STRATIFY n = 427
  c  construction of personalised task-state digital twins   12 twins, 7 builds
  d  virtual manipulation of neurotransmitter systems        n = 288 twins
  e  validation in pharmacological fMRI data                 n = 27 / n = 41
  f  forecasting four-year symptom change                    n = 85

Data sources
  a  fig1_data/fig1_mini_np12_edges.csv
  b  fig.2/fig2_data/fig2c_profile_scores.csv
  c  fig1_data/fig1_mini_fidelity.csv
  d  fig.4/fig4_data/fig4_subject_level_n288.csv
  e  fig1_data/fig1_mini_healthy_n27.csv, fig1_mini_clinical_n36.csv
  f  fig1_data/fig1_mini_longitudinal_n85.csv

Image items in c are raster assets from the author's slide deck; the BOLD traces
they contain were produced by the author's own assimilation runs.  The synapse
schematic in d is redrawn as vector art in the manuscript palette by
fig1_synapse_vector.py.

Outputs: fig1_v4.png (450 dpi), fig1_v4.pdf
"""
import os, sys
import numpy as np, pandas as pd
from scipy import stats as sstats
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.image import imread

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, C, LW       # noqa: E402
from supp_kit import fill, pt_edge                   # noqa: E402
import matplotlib.colors as _mc


def dark(c, k=0.55):
    """readable ink for text/arrows in a palette colour (pt_edge returns 'none'
    for dark colours, which makes text invisible)."""
    return tuple(np.array(_mc.to_rgb(c)) * k)
apply_np_style()

D = os.path.join(HERE, 'fig1_data')
A = os.path.join(HERE, 'fig1_assets')
F2 = os.path.join(HERE, '..', 'fig.2', 'fig2_data')
F4 = os.path.join(HERE, '..', 'fig.4', 'fig4_data')

INK, SOFT, FAINT, HAIR = '#1A1A1A', '#4D4D4D', '#8C8C8C', '#D9D9D9'
CIRC, POSP, HCC, PTC = C('np12'), C('pos_profile'), C('hc'), C('patient')
AMPA, GABA, BASE = C('ampa'), C('gaba'), C('baseline')
KET, MID, MDDC = C('ketamine'), C('midazolam'), C('mdd')
REG, VOX = C('model_regional'), C('model_voxel')

# ----------------------------------------------------------------- data ------
STR = pd.read_csv(f'{F2}/fig2c_profile_scores.csv')
EDG = pd.read_csv(f'{D}/fig1_mini_np12_edges.csv')
FID = pd.read_csv(f'{D}/fig1_mini_fidelity.csv')
POP = pd.read_csv(f'{F4}/fig4_subject_level_n288.csv')
HV = pd.read_csv(f'{D}/fig1_mini_healthy_n27.csv')
CLI = pd.read_csv(f'{D}/fig1_mini_clinical_n36.csv')
LON = pd.read_csv(f'{D}/fig1_mini_longitudinal_n85.csv')
hc = STR.loc[STR.Diseased == 'HC', 'Neg_NP'].values
pt = STR.loc[STR.Diseased != 'HC', 'Neg_NP'].values
dKET = (HV.Ketamine - HV.Placebo).values
dMID = (HV.Midazolam - HV.Placebo).values
CLI['d'] = CLI.FC_d2 - CLI.FC_p2
rRAW = sstats.pearsonr(LON.ampa_restoration_index, LON.fu3_symptom_change)[0]

# --------------------------------------------------------------- canvas ------
FIG_W_MM, FIG_H_MM = 180.0, 235.0
fig = plt.figure(figsize=(FIG_W_MM / 25.4, FIG_H_MM / 25.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
UX, UY = FIG_W_MM / 100.0, FIG_H_MM / 100.0          # mm per canvas unit
XY = UX / UY                                         # y-units per x-unit at equal mm

INK, SOFT, FAINT, HAIR = '#1A1A1A', '#4D4D4D', '#8C8C8C', '#D9D9D9'


def rbox(x, y, w, h, fc, ec='none', lw=LW, r=.8, z=2, **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, **kw))


def T(x, y, s, size=4.6, color=SOFT, bold=False, ha='left', va='center', ls=1.3,
      z=6, style=None, rot=0):
    ax.text(x, y, s, fontsize=size, color=color, fontweight='bold' if bold else 'normal',
            ha=ha, va=va, linespacing=ls, zorder=z, style=style, rotation=rot,
            rotation_mode='anchor' if rot else None)


def put(name, x, ytop, w, crop=(0, 0, 0, 0), tint=None, z=4, ha='left'):
    """place an asset with aspect preserved; x = left (or centre), ytop = top edge"""
    im = imread(os.path.join(A, name))
    if im.dtype not in (np.float32, np.float64):
        im = im / 255.0
    l, t, r, b = crop
    H, W = im.shape[0], im.shape[1]
    im = im[int(t * H):H - int(b * H), int(l * W):W - int(r * W)]
    if tint is not None and im.ndim == 3 and im.shape[2] == 4:
        rgb = mcolors.to_rgb(tint)
        im = im.copy(); im[..., 0], im[..., 1], im[..., 2] = rgb
    ih, iw = im.shape[0], im.shape[1]
    h = w * (ih / iw) * XY
    if ha == 'center':
        x = x - w / 2
    ax.imshow(im, extent=(x, x + w, ytop - h, ytop), zorder=z,
              interpolation='antialiased', aspect='auto')
    return h


class Fr:
    def __init__(self, gx, gy, gw, gh, xlim, ylim):
        self.gx, self.gy, self.gw, self.gh, self.xl, self.yl = gx, gy, gw, gh, xlim, ylim

    def X(self, v):
        return self.gx + (np.asarray(v, float) - self.xl[0]) / (self.xl[1] - self.xl[0]) * self.gw

    def Y(self, v):
        return self.gy + (np.asarray(v, float) - self.yl[0]) / (self.yl[1] - self.yl[0]) * self.gh


def box(fr, xc, v, col, w=.30, pts=True, ptsize=.8, rng=None):
    v = np.asarray(v, float)
    q1, med, q3 = np.percentile(v, [25, 50, 75]); iqr = q3 - q1
    lo = v[v >= q1 - 1.5 * iqr].min(); hi = v[v <= q3 + 1.5 * iqr].max()
    ax.plot([fr.X(xc)] * 2, [fr.Y(lo), fr.Y(hi)], color=INK, lw=LW * .7, zorder=3)
    rbox(fr.X(xc - w / 2), fr.Y(q1), fr.X(xc + w / 2) - fr.X(xc - w / 2),
         fr.Y(q3) - fr.Y(q1), fill(col), INK, lw=LW * .7, r=.10, z=4)
    ax.plot([fr.X(xc - w / 2), fr.X(xc + w / 2)], [fr.Y(med)] * 2, color=INK, lw=LW, zorder=6)
    if pts:
        jx = rng.uniform(-w * .26, w * .26, len(v))
        ax.scatter(fr.X(xc + jx), fr.Y(v), s=ptsize, facecolor=col, edgecolor=pt_edge(col),
                   linewidth=.12, zorder=5, alpha=.9)


RNG = np.random.default_rng(3)


def chev(x, y, col='#B0B0B0', s=4.4):
    ax.add_patch(FancyArrowPatch((x - .5, y), (x + .5, y), arrowstyle='-|>',
                                 mutation_scale=s, lw=LW, color=col, zorder=5))


def card(x, y, w, h, letter, title, chips=(), take='', ref=''):
    """draw the card chrome and return the free content rectangle (cx, cy, cw, ch)"""
    rbox(x, y, w, h, 'white', HAIR, lw=LW, r=1.0, z=1)
    rbox(x, y + h - 5.2, w, 5.2, '#F0F0F0', 'none', r=1.0, z=2)
    rbox(x, y + h - 5.2, w, 2.4, '#F0F0F0', 'none', r=0, z=2)
    ax.add_patch(Circle((x + 2.1, y + h - 2.6), 1.05, facecolor=SOFT, edgecolor='none', zorder=4))
    T(x + 2.1, y + h - 2.68, letter, size=5.2, color='white', bold=True, ha='center', z=5)
    T(x + 4.0, y + h - 2.6, title, size=5.5, color=INK, bold=True, ls=1.18)
    ybot = y + 1.2
    if ref:
        nl = ref.count('\n') + 1
        T(x + 1.0, ybot + .9 * nl, ref, size=4.0, color=FAINT, style='italic', ls=1.35, va='center')
        ybot += 2.0 * nl
    if take:
        nl = take.count('\n') + 1
        T(x + 1.0, ybot + 1.0 * nl, take, size=4.4, color=SOFT, ls=1.4, va='center')
        ybot += 2.2 * nl
        ax.plot([x + .9, x + w - .9], [ybot] * 2, color='#E0E0E0', lw=LW, zorder=2)
        ybot += .8
    ytop = y + h - 6.0
    for col, lab, sub in chips:
        rbox(x + 1.0, ytop - 1.9, 1.4, 1.4, col, HAIR, lw=LW * .6, r=.2, z=4)
        T(x + 2.9, ytop - .8, lab, size=4.4, color=INK)
        T(x + 2.9, ytop - 2.3, sub, size=4.2, color=SOFT)
        ytop -= 3.7
    return x + 1.0, ybot, w - 2.0, ytop - ybot


# ---------------------------------------------------------------- title ------
T(2.0, 98.4, 'Fig. 1 | A perturbation-capable digital twin brain for a symptom-linked circuit',
  size=8.0, color=INK, bold=True)
T(2.0, 95.6, 'A circuit whose connectivity tracks symptom load is identified empirically (a, b), rebuilt inside '
             'individual digital twin brains (c) and perturbed in silico (d);\nthe simulated response is then tested '
             'against two pharmacological datasets (e) and against symptom change four years later (f).',
  size=5.3, color=SOFT, ls=1.45)

X0, GAP = 2.0, 1.4
W2 = (96 - GAP) / 2
W3 = (96 - 2 * GAP) / 3
RY1, RH1 = 69.5, 24.5
RY2, RH2 = 50.0, 18.0
RY3, RH3 = 12.5, 36.0

# ================================ panel a ====================================
cx, cy, cw, ch = card(
    X0, RY1, W2, RH1, 'a', 'A shared brain phenotype of\ntransdiagnostic symptoms',
    chips=[(C('np12'), 'IMAGEN discovery', 'n = 1,050 adolescents, MID and SST fMRI')],
    take='Connectivity of one 29-edge profile tracks symptom load across six domains',
    ref='Fig. 2a\u2013d \u00b7 Figs S1\u2013S3 \u00b7 Tables S3, S4, S6')
ytop = cy + ch
put('checklist.png', cx + .4, ytop - .2, 2.6, tint=SOFT)
T(cx + 3.8, ytop - 1.4, 'six DAWBA symptom bands', size=4.1, color=SOFT)
put('scanner.png', cx + .2, ytop - 5.0, 5.0, tint=SOFT)
T(cx + 6.0, ytop - 6.1, 'MID and SST fMRI,\nsix task conditions', size=4.1, color=SOFT, ls=1.3)
chev(cx + 16.4, ytop - 3.6)
T(cx + 17.6, ytop - 1.4, 'connectome-based predictive modelling', size=4.1, color=INK)
for k, (col, lab) in enumerate([(C('neg_profile'), 'negative profile, 29 edges'),
                                (C('pos_profile'), 'positive profile, 34 edges'),
                                (C('np12'), 'NP factor, 12 DTB-representable edges')]):
    yy = ytop - 3.6 - k * 1.9
    ax.plot([cx + 17.8, cx + 19.4], [yy] * 2, color=col, lw=1.5, zorder=4)
    T(cx + 20.1, yy, lab, size=4.1, color=SOFT)
rr = 5.0
ringx, ringy = cx + cw - rr * 1.1, cy + ch / 2
ax.add_patch(Circle((ringx, ringy), rr, facecolor='none', edgecolor='#EDEDED', linewidth=3.0, zorder=2))
nodes = sorted(pd.unique(EDG[['i_217', 'j_217']].values.ravel()))
th = np.linspace(90, -270, len(nodes), endpoint=False) * np.pi / 180
pos = {n: (ringx + rr * np.cos(t), ringy + rr * XY * np.sin(t)) for n, t in zip(nodes, th)}
for _, e in EDG.iterrows():
    a_, b_ = pos[e.i_217], pos[e.j_217]
    ax.plot([a_[0], b_[0]], [a_[1], b_[1]], color=C('np12'), lw=1.4, alpha=.9, zorder=3,
            solid_capstyle='round')
for n, (px, py) in pos.items():
    ax.add_patch(Circle((px, py), .40, facecolor='white', edgecolor=C('np12'), linewidth=LW, zorder=4))

# ================================ panel b ====================================
cx, cy, cw, ch = card(
    X0 + W2 + GAP, RY1, W2, RH1, 'b', 'Validation of the phenotype in\nan independent clinical sample',
    chips=[(C('pos_profile'), 'STRATIFY / ESTRA', 'n = 427: 225 HC, 104 MDD, 98 AUD')],
    take='Hedges\u2019 $g$ = 0.37 [0.18, 0.56], $t$(425) = 3.83, $P_{\\rm Bonferroni}$ = 2.96 \u00d7 10$^{-4}$;\n'
         'the positive profile does not separate the groups',
    ref='Fig. 2c, e \u00b7 Fig. S1 \u00b7 Table S6')
ytop = cy + ch
for k, (nm, lab, col) in enumerate([('head_brain.png', 'HC 225', C('hc')),
                                    ('head_mood.png', 'MDD 104', C('mdd')),
                                    ('head_aud.png', 'AUD 98', C('aud'))]):
    yy = ytop - .2 - k * (ch / 3)
    put(nm, cx + .6, yy, 3.6, tint=col)
    T(cx + 5.0, yy - 1.9, lab, size=4.2, color=SOFT)
f1 = Fr(cx + cw * .48, cy + 2.4, cw * .44, ch - 4.4, (-.6, 1.6), (-4.6, 4.6))
ax.plot([f1.X(-.6), f1.X(1.6)], [f1.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
box(f1, 0.0, hc, C('hc'), rng=RNG)
box(f1, 1.0, pt, C('patient'), rng=RNG)
T(f1.X(0.0), cy + 1.6, 'HC', size=4.2, color=SOFT, ha='center', va='top')
T(f1.X(1.0), cy + 1.6, 'patients', size=4.2, color=SOFT, ha='center', va='top')
T(cx + cw * .48 - 1.3, cy + 2.4 + (ch - 4.4) / 2, 'negative NP profile (z)',
  size=4.1, color=SOFT, ha='center', va='center', rot=90)

# ================================ panel c ====================================
cx, cy, cw, ch = card(
    X0, RY2, 96, RH2, 'c', 'Construction of personalised task-state digital twin brains',
    ref='Fig. 3 \u00b7 Figs S4, S19, S22 \u00b7 Tables S8\u2013S12   |   * 10 M assimilation hyper-parameters; '
        'every other build uses 3 M (268 regions) or 100 M (voxel-wise)')
ytop = cy + ch
SX = [cx, cx + 19.0, cx + 36.6, cx + 51.0, cx + 72.4]
for k, (sx, lab) in enumerate(zip(SX, ['Empirical data', 'Local dynamics', 'Task-state DTB',
                                       'Assimilated BOLD', 'Model selection'])):
    T(sx, ytop - .6, lab, size=4.5, color=INK, bold=True)
    if k:
        chev(sx - 1.6, cy + ch / 2 - 1.0)
put('gmv_slices.png', SX[0] + .2, ytop - 2.4, 5.6, crop=(.635, .069, .102, .188))
T(SX[0] + .2, cy + 1.2, 'grey matter\nvolume', size=4.0, color=SOFT, ls=1.25, va='bottom')
put('wm_fibers.png', SX[0] + 8.2, ytop - 2.4, 4.6, crop=(0, .306, 0, .313))
T(SX[0] + 7.8, cy + 1.2, 'white matter\nfibres', size=4.0, color=SOFT, ls=1.25, va='bottom')
put('neuron.png', SX[1] + .2, ytop - 2.2, 4.6, tint=SOFT)
ecx, ecy = SX[1] + 9.6, ytop - 4.6
for dx, lab, col in [(-1.8, 'E', C('ampa')), (1.8, 'I', C('gaba'))]:
    ax.add_patch(Circle((ecx + dx, ecy), 1.1, facecolor='white', edgecolor=dark(col),
                        linewidth=.9, zorder=4))
    T(ecx + dx, ecy - .04, lab, size=4.5, color=dark(col), bold=True, ha='center', z=5)
ax.add_patch(FancyArrowPatch((ecx - .7, ecy + .9), (ecx + .7, ecy + .9), arrowstyle='-|>',
                             mutation_scale=3.4, lw=LW, color=dark(C('ampa')),
                             connectionstyle='arc3,rad=-.45', zorder=4))
ax.add_patch(FancyArrowPatch((ecx + .7, ecy - .9), (ecx - .7, ecy - .9), arrowstyle='-|>',
                             mutation_scale=3.4, lw=LW, color=dark(C('gaba')),
                             connectionstyle='arc3,rad=-.45', zorder=4))
T(SX[1] + .2, cy + 1.2, 'leaky integrate-and-fire neurons,\nAMPA and GABA-A synapses',
  size=4.0, color=SOFT, ls=1.25, va='bottom')
put('glass_brain.png', SX[2] + 1.2, ytop - 1.6, 7.6)
T(SX[2] + .2, cy + 1.2, '3 M\u20131 B neurons \u00b7 268 or 1,000\nregions, or voxel-wise',
  size=4.0, color=SOFT, ls=1.25, va='bottom')
put('bold_sst.png', SX[3] + .2, ytop - 3.0, 12.6, crop=(0, .408, 0, 0))
T(SX[3] + .2, ytop - 2.0, 'SST, anterior PFC · empirical / simulated', size=3.9, color=SOFT)
put('bold_mid.png', SX[3] + .2, ytop - 7.2, 12.6, crop=(0, .403, 0, 0))
T(SX[3] + .2, ytop - 6.2, 'MID, nucleus accumbens · empirical / simulated', size=3.9, color=SOFT)
ORD = ['3m_268', '10m_268', '10m_1000', '10m_own', '10m', '100m', '1b']
LBL = ['3M/268', '10M/268', '10M/1k', '10M/vox*', '10M/vox', '100M/vox', '1B/vox']
COL = [C('model_regional')] * 3 + [C('model_voxel')] * 4
BB, BT = cy + 4.2, ytop - 1.9
f2 = Fr(SX[4] + 2.4, BB, 18.6, BT - BB, (-.75, 6.75), (0.60, 0.95))
for gv in (0.7, 0.9):
    ax.plot([f2.X(-.75), f2.X(6.75)], [f2.Y(gv)] * 2, color='#EFEFEF', lw=LW, zorder=1)
    T(f2.X(-.95), f2.Y(gv), f'{gv:.1f}', size=3.8, color=FAINT, ha='right')
for k, (m, c) in enumerate(zip(ORD, COL)):
    v = float(FID.loc[FID.model == m, 'bold_r_mean'].iloc[0])
    rbox(f2.X(k - .34), f2.Y(0.60), f2.X(k + .34) - f2.X(k - .34), f2.Y(v) - f2.Y(0.60),
         c, 'none', lw=0, r=.08, z=4)
    T(f2.X(k) + .24, BB - .45, LBL[k], size=3.7, color=SOFT, ha='right', va='center', rot=52)
T(SX[4] + 2.2, ytop - 1.2, 'assimilated-region BOLD $r$, 12 twins', size=3.9, color=SOFT)

# ================================ panel d ====================================
cx, cy, cw, ch = card(
    X0, RY3, W3, RH3, 'd', 'Virtual manipulation of\nneurotransmitter systems',
    chips=[(C('ampa'), 'AMPA 0.0044, then GABA-A 0.0040', 'n = 288 twins, 3 M / 268 regions')],
    take='AMPA +0.78, $t$(287) = 14.14, 234 / 288 up; GABA-A +2.74,\n'
         '$t$(287) = 27.11, 282 / 288 up; 229 both-up \u00b7 59 any-down',
    ref='Fig. 4 \u00b7 Figs S17, S18 \u00b7 Tables S13\u2013S15, S17')
ytop = cy + ch
hsy = put('synapse_palette.png', cx, ytop - .2, cw)
f3 = Fr(cx + cw * .16, cy + 2.8, cw * .70, ytop - hsy - 2.4 - (cy + 2.8), (-.45, 2.45), (-3.4, 12.6))
ax.plot([f3.X(-.45), f3.X(2.45)], [f3.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
for _, r in POP.sample(110, random_state=1).iterrows():
    ax.plot(f3.X([0, 1, 2]), f3.Y([r.simulated, r.ampa, r.gaba]),
            color='#CCCCCC', lw=.14, alpha=.5, zorder=2)
box(f3, 0.0, POP.simulated, C('baseline'), pts=False)
box(f3, 1.0, POP.ampa, C('ampa'), pts=False)
box(f3, 2.0, POP.gaba, C('gaba'), pts=False)
for k, lab in enumerate(['baseline', 'AMPA \u2191', 'GABA-A \u2191']):
    T(f3.X(k), cy + 2.0, lab, size=4.1, color=SOFT, ha='center', va='top')
T(cx, ytop - hsy - 1.2, 'simulated NP factor, $n$ = 288 twins', size=4.1, color=SOFT)

# ================================ panel e ====================================
cx, cy, cw, ch = card(
    X0 + W3 + GAP, RY3, W3, RH3, 'e', 'Validation in\npharmacological fMRI data',
    chips=[(C('ketamine'), 'crossover n = 27 \u00b7 clinical n = 41', 'placebo / ketamine / midazolam')],
    take='group \u00d7 drug $t$(30) = 3.43, $P$ = 0.0018; placebo baseline,\n'
         '$n$ = 41: $t$(35) = \u22122.51, $P$ = 0.017; slopes on placebo < 1',
    ref='Fig. 5a\u2013c \u00b7 Figs S9, S12, S13 \u00b7 Table S21')
ytop = cy + ch
put('syringe.png', cx + .6, ytop, 3.4, tint=SOFT)
chev(cx + 5.4, ytop - 1.8)
put('scanner.png', cx + 6.4, ytop - .2, 4.8, tint=SOFT)
put('monitor.png', cx + 12.6, ytop - .4, 3.4, tint=SOFT)
T(cx + 16.6, ytop - 1.8, 'resting state\nand MID', size=4.0, color=SOFT, ls=1.3)
f4 = Fr(cx + cw * .13, cy + 3.6, cw * .80, ytop - 7.4 - (cy + 3.6), (-.5, 3.5), (-5.6, 5.6))
ax.plot([f4.X(-.5), f4.X(3.5)], [f4.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
for k, (v, col) in enumerate([(dKET, C('ketamine')), (dMID, C('midazolam')),
                              (CLI.loc[CLI.group == 'MDD', 'd'].values, C('mdd')),
                              (CLI.loc[CLI.group == 'HC', 'd'].values, C('hc'))]):
    box(f4, k, v, col, w=.42, rng=RNG, ptsize=.9)
for k, lab in enumerate(['ketamine', 'midazolam', 'MDD 22', 'HC 14']):
    T(f4.X(k), cy + 2.8, lab, size=4.0, color=SOFT, ha='center', va='top', rot=0)
ax.plot([f4.X(1.5)] * 2, [cy + 3.6, ytop - 7.4], color='#EAEAEA', lw=LW, zorder=1)
T(f4.X(0.5), ytop - 6.6, 'healthy, $n$ = 27', size=4.0, color=SOFT, ha='center')
T(f4.X(2.5), ytop - 6.6, 'clinical, ketamine', size=4.0, color=SOFT, ha='center')
T(cx, ytop - 8.2, '\u0394 NP-related connectivity, drug \u2212 placebo', size=4.1, color=SOFT)

# ================================ panel f ====================================
cx, cy, cw, ch = card(
    X0 + 2 * (W3 + GAP), RY3, W3, RH3, 'f', 'Forecasting four-year\nsymptom change',
    chips=[(C('high_symptom'), 'IMAGEN follow-up', 'n = 85, age 19 \u2192 23')],
    take='$r$ = 0.26 unadjusted; partial $r$ = 0.24, $P$ = 0.026 given\n'
         'empirical baseline NP; model $R^2$ = 0.23, $F$(5,79) = 4.80',
    ref='Fig. 5h, i \u00b7 Fig. S14')
ytop = cy + ch
ax.add_patch(FancyArrowPatch((cx + 1.6, ytop - 1.2), (cx + cw - 1.6, ytop - 1.2),
                             arrowstyle='-|>', mutation_scale=4.8, lw=.85,
                             color=C('high_symptom'), zorder=4))
T(cx + 1.4, ytop - 3.0, 'age 19\nDTB built', size=4.0, color=SOFT, ls=1.3, va='center')
T(cx + cw - 1.4, ytop - 3.0, 'age 23\nsymptoms', size=4.0, color=SOFT, ha='right', ls=1.3, va='center')
xv, yv = LON.ampa_restoration_index.values, LON.fu3_symptom_change.values
f6 = Fr(cx + cw * .22, cy + 3.6, cw * .72, ytop - 7.0 - (cy + 3.6),
        (xv.min() - .12 * np.ptp(xv), xv.max() + .12 * np.ptp(xv)),
        (yv.min() - .12 * np.ptp(yv), yv.max() + .12 * np.ptp(yv)))
ax.scatter(f6.X(xv), f6.Y(yv), s=1.7, facecolor=C('ampa'), edgecolor=pt_edge(C('ampa')),
           linewidth=.14, zorder=4)
b1, b0 = np.polyfit(xv, yv, 1)
gx = np.linspace(xv.min(), xv.max(), 20)
ax.plot(f6.X(gx), f6.Y(b0 + b1 * gx), color=dark(C('ampa')), lw=1.0, zorder=5)
T(cx + cw * .22 - 1.3, cy + 3.6 + (ytop - 7.0 - (cy + 3.6)) / 2, 'observed \u0394 symptoms',
  size=4.0, color=SOFT, ha='center', va='center', rot=90)
T(cx + cw * .58, cy + 2.8, 'AMPA restoration index', size=4.0, color=SOFT, ha='center', va='top')
T(cx, ytop - 5.9, 'perturbational response vs symptom change', size=4.1, color=SOFT)

# ------------------------------------------------------------ flow arrows ----
ax.add_patch(FancyArrowPatch((X0 + W2 * .5, RY1 - .6), (X0 + W2 * .5, RY2 + RH2 + .6),
                             arrowstyle='-|>', mutation_scale=4.8, lw=.85, color='#B0B0B0', zorder=3))
ax.add_patch(FancyArrowPatch((X0 + W2 + GAP + W2 * .5, RY1 - .6),
                             (X0 + W2 + GAP + W2 * .5, RY2 + RH2 + .6),
                             arrowstyle='-|>', mutation_scale=4.8, lw=.85, color='#B0B0B0', zorder=3))
ax.add_patch(FancyArrowPatch((X0 + 48, RY2 - .6), (X0 + W3 * .5, RY3 + RH3 + .6),
                             arrowstyle='-|>', mutation_scale=4.8, lw=.85, color='#B0B0B0',
                             connectionstyle='arc3,rad=-.10', zorder=3))
ax.add_patch(FancyArrowPatch((X0 + W3 + GAP * .25, RY3 + RH3 * .58),
                             (X0 + W3 + GAP * .95, RY3 + RH3 * .58), arrowstyle='-|>',
                             mutation_scale=4.8, lw=.85, color=dark(C('ampa')), zorder=3))
T(X0 + W3 + GAP * .5, RY3 + RH3 * .58 + 1.0, 'no refitting', size=3.8,
  color=dark(C('ampa')), ha='center', va='bottom', rot=90)
ax.add_patch(FancyArrowPatch((X0 + 2 * W3 + GAP * 1.25, RY3 + RH3 * .58),
                             (X0 + 2 * W3 + GAP * 1.95, RY3 + RH3 * .58), arrowstyle='-|>',
                             mutation_scale=4.8, lw=.85, color=C('high_symptom'), zorder=3))

# ------------------------------------------------------- colour reference ----
T(2.0, 9.4, 'Colour correspondence', size=5.0, color=INK, bold=True)
PAIRS = [(C('ampa'), C('ketamine'), 'virtual AMPA \u2194 ketamine'),
         (C('gaba'), C('midazolam'), 'virtual GABA-A \u2194 midazolam'),
         (C('baseline'), C('placebo'), 'simulated baseline \u2194 placebo')]
for k, (a1, b1c, lab) in enumerate(PAIRS):
    xx = 2.0 + k * 21.0
    rbox(xx, 6.6, 1.3, 1.3, a1, HAIR, lw=LW * .5, r=.18, z=4)
    rbox(xx + 1.4, 6.6, 1.3, 1.3, b1c, HAIR, lw=LW * .5, r=.18, z=4)
    T(xx + 3.4, 7.25, lab, size=4.1, color=SOFT)
SING = [(C('np12'), 'NP factor / negative profile'), (C('pos_profile'), 'positive profile'),
        (C('model_regional'), 'regional build'), (C('model_voxel'), 'voxel build'),
        (C('hc'), 'HC / baseline / placebo'), (C('high_symptom'), 'high-symptom'),
        (C('patient'), 'patient / MDD'), (C('aud'), 'AUD')]
for k, (col, lab) in enumerate(SING):
    xx = 2.0 + (k % 4) * 19.6
    yy = 4.6 if k < 4 else 2.4
    rbox(xx, yy - .65, 1.3, 1.3, col, HAIR, lw=LW * .5, r=.18, z=4)
    T(xx + 1.8, yy, lab, size=4.0, color=SOFT)
T(66.0, 7.25, 'every plotted point is one participant\u2019s observed or simulated value;\n'
              'no data element of this figure is schematic', size=3.9, color=FAINT, ls=1.4)

fig.savefig(os.path.join(HERE, 'fig1_v4.png'), dpi=450)
fig.savefig(os.path.join(HERE, 'fig1_v4.pdf'))
import matplotlib as mpl
rnd = fig.canvas.get_renderer()
tx = [(t, t.get_window_extent(rnd)) for t in fig.findobj(mpl.text.Text)
      if t.get_text().strip() and t.get_visible()]
ov = [(p.get_text()[:24], q.get_text()[:24]) for i, (p, bp) in enumerate(tx)
      for q, bq in tx[i + 1:] if bp.overlaps(bq)]
print('texts %d  overlaps %d' % (len(tx), len(ov)))
for o in ov[:24]:
    print('  OVERLAP', o)
print('n: STRATIFY %d/%d  pop %d  hv %d  cli %d  lon %d  r_raw %.4f'
      % (len(hc), len(pt), len(POP), len(HV), len(CLI), len(LON), rRAW))
