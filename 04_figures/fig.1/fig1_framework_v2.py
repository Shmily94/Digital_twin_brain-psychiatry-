"""Fig. 1 - framework overview, v2.

Keeps the layout and palette of fig1_framework.png (five numbered stage cards,
cohort chips, top/bottom feedback arrows, colour-correspondence strip) but
replaces every mini-plot with the real data.  The original fig1_scene.py drew
its violins, perturbation fan, drug box plots and forecast scatter from
np.random.default_rng(7); nothing here is simulated for illustration - every
point plotted comes from the same tables that produce Figs 2-5.

Data sources
  stage 1  fig.2/fig2_data/fig2c_profile_scores.csv          (STRATIFY n = 427)
           fig1_data/fig1_mini_np12_edges.csv                (12 NP edges)
  stage 2  fig1_data/fig1_mini_fidelity.csv                  (7 builds, 12 twins)
  stage 3  fig.4/fig4_data/fig4_subject_level_n288.csv        (population twins)
  stage 4  fig1_data/fig1_mini_healthy_n27.csv               (crossover)
           fig1_data/fig1_mini_clinical_n36.csv              (clinical ketamine)
  stage 5  fig1_data/fig1_mini_longitudinal_n85.csv          (IMAGEN follow-up)

Palette: NP-DTB v2 token table (artifact f00fa6dc-1c4e-4ad7-8955-5d387115e61c),
hexes inlined below so the script runs standalone.

Outputs: fig1_framework_v2.png (450 dpi), fig1_framework_v2.pdf
"""
import os, sys
import numpy as np, pandas as pd
from scipy import stats as sstats
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, C, LW       # noqa: E402
from supp_kit import fill, pt_edge                   # noqa: E402
apply_np_style()

D = os.path.join(HERE, 'fig1_data')
F2 = os.path.join(HERE, '..', 'fig.2', 'fig2_data')
F4 = os.path.join(HERE, '..', 'fig.4', 'fig4_data')

P = dict(                                # registered NP-DTB palette, as in Figs 2-5
    exc_ampa=C('ampa'), exc_ketamine=C('ketamine'), exc_restore=C('ampa'),
    inh_gaba=C('gaba'), inh_midazolam=C('midazolam'),
    unp_baseline=C('baseline'), unp_placebo=C('placebo'),
    circ_neg29=C('neg_profile'), circ_np12=C('np12'), pos_prof34=C('pos_profile'),
    hlth_hc=C('hc'), clin_highsymp=C('high_symptom'), clin_patients=C('patient'),
    clin_mdd=C('mdd'), clin_aud=C('aud'),
    scale_3m=C('model_regional'), scale_10m=C('model_regional'),
    scale_100m=C('model_voxel'), scale_1b=C('model_voxel'),
    coh_imagen=C('np12'), coh_stratify=C('neg_profile'), coh_pharm_hv=C('ketamine'),
    coh_pharm_clin=C('midazolam'), coh_imagen_fu3=C('high_symptom'))
INK, SOFT, FAINT, HAIR = '#1A1A1A', '#4D4D4D', '#8C8C8C', '#D9D9D9'

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
HVd = dict(ket=(HV.Ketamine - HV.Placebo).values, mid=(HV.Midazolam - HV.Placebo).values)
CLI['d'] = CLI.FC_d2 - CLI.FC_p2
LONr = sstats.pearsonr(LON.ampa_restoration_index, LON.fu3_symptom_change)

# --------------------------------------------------------------- canvas ------
FIG_W_MM, FIG_H_MM = 180.0, 152.0
fig = plt.figure(figsize=(FIG_W_MM / 25.4, FIG_H_MM / 25.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
AR = FIG_W_MM / FIG_H_MM


def rbox(x, y, w, h, fc, ec='none', lw=LW, r=.9, z=2, **kw):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, **kw))


def T(x, y, s, size=5.0, color=SOFT, bold=False, ha='left', va='center', ls=1.32,
      z=6, style=None, rot=0):
    ax.text(x, y, s, fontsize=size, color=color, fontweight='bold' if bold else 'normal',
            ha=ha, va=va, linespacing=ls, zorder=z, style=style, rotation=rot,
            rotation_mode='anchor' if rot else None)


class Fr:
    """a data box mapped onto canvas coordinates"""
    def __init__(self, gx, gy, gw, gh, xlim, ylim):
        self.gx, self.gy, self.gw, self.gh, self.xl, self.yl = gx, gy, gw, gh, xlim, ylim

    def X(self, v):
        return self.gx + (np.asarray(v, float) - self.xl[0]) / (self.xl[1] - self.xl[0]) * self.gw

    def Y(self, v):
        return self.gy + (np.asarray(v, float) - self.yl[0]) / (self.yl[1] - self.yl[0]) * self.gh


def box(fr, xc, v, col, w=.30, pts=True, ptsize=.9, rng=None):
    """box plot of the real values, with every observation overplotted"""
    v = np.asarray(v, float)
    q1, med, q3 = np.percentile(v, [25, 50, 75]); iqr = q3 - q1
    lo = v[v >= q1 - 1.5 * iqr].min(); hi = v[v <= q3 + 1.5 * iqr].max()
    ax.plot([fr.X(xc)] * 2, [fr.Y(lo), fr.Y(hi)], color=INK, lw=LW * .7, zorder=3)
    rbox(fr.X(xc - w / 2), fr.Y(q1), fr.X(xc + w / 2) - fr.X(xc - w / 2),
         fr.Y(q3) - fr.Y(q1), fill(col), INK, lw=LW * .7, r=.12, z=4)
    ax.plot([fr.X(xc - w / 2), fr.X(xc + w / 2)], [fr.Y(med)] * 2, color=INK, lw=LW, zorder=6)
    if pts:
        jx = rng.uniform(-w * .26, w * .26, len(v))
        ax.scatter(fr.X(xc + jx), fr.Y(v), s=ptsize, facecolor=col, edgecolor=pt_edge(col),
                   linewidth=.12, zorder=5, alpha=.9)


RNG = np.random.default_rng(3)          # jitter of the plotted real points only

# ---------------------------------------------------------------- title ------
T(2.0, 97.4, 'Fig. 1 | A perturbation-capable digital twin brain for a symptom-linked circuit',
  size=8.2, color=INK, bold=True)
T(2.0, 93.1, 'A circuit whose connectivity tracks symptom load is identified empirically, rebuilt inside individual '
             'digital twin brains and perturbed in silico; the resulting\nresponse is then tested against two drug '
             'datasets and against symptom change four years later. The NP factor is the single quantity carried '
             'through all five stages.', size=5.5, color=SOFT, ls=1.45)

X0, GAP = 2.0, 1.2
CW = (100 - 2 * X0 - 4 * GAP) / 5
CY, CH = 15.5, 68.5
xs = [X0 + i * (CW + GAP) for i in range(5)]

TITLES = ['Derive the circuit\nphenotype', 'Build and calibrate\nindividual twins',
          'Perturb the circuit\nin silico', 'Validate against\ntwo drug datasets',
          'Forecast four-year\nsymptom change']
CHIPS = [[('coh_imagen', 'IMAGEN', 'n = 1,050'), ('coh_stratify', 'STRATIFY', 'n = 427')],
         [('scale_3m', 'cross-scale twins', 'n = 12, seven builds'),
          ('scale_1b', 'hyper-parameter', 'grid 3 M / 100 M')],
         [('scale_100m', 'parameter search', '100 M, 12 twins'),
          ('scale_3m', 'population twins', 'n = 288, 3 M / 268')],
         [('coh_pharm_hv', 'healthy crossover', 'n = 27'),
          ('coh_pharm_clin', 'clinical ketamine', 'n = 41 (36 paired)')],
         [('coh_imagen_fu3', 'IMAGEN follow-up', 'n = 85'),
          ('coh_imagen', 'symptom change', 'age 19 \u2192 23')]]
TAKE = ['Only the 29-edge negative\nprofile separates patients\nfrom controls',
        'Build choice decides which\ninference is admissible \u2014\nnot a free parameter',
        'Both perturbations move NP\nconnectivity, in a\nparticipant-specific direction',
        'Drug effects follow the\nvirtual perturbation without\nrefitting of the mapping',
        'The perturbational response\ncarries prospective\ninformation about symptoms']
REFS = ['Fig. 2 \u00b7 Figs S1\u2013S3\nTables S4\u2013S6',
        'Fig. 3 \u00b7 Figs S19, S22\nTables S9\u2013S12',
        'Fig. 4 \u00b7 Figs S17, S18\nTables S15, S17',
        'Fig. 5a\u2013c \u00b7 Figs S9, S12, S13\nTable S21',
        'Fig. 5h, i \u00b7 Fig. S14']

for i, x in enumerate(xs):
    rbox(x, CY, CW, CH, 'white', HAIR, lw=LW, r=1.1, z=1)
    rbox(x, CY + CH - 7.4, CW, 7.4, '#F0F0F0', 'none', r=1.1, z=2)
    rbox(x, CY + CH - 7.4, CW, 3.0, '#F0F0F0', 'none', r=0, z=2)
    ax.add_patch(Circle((x + 2.3, CY + CH - 3.7), 1.3, facecolor=SOFT, edgecolor='none', zorder=4))
    T(x + 2.3, CY + CH - 3.75, str(i + 1), size=5.8, color='white', bold=True, ha='center', z=5)
    T(x + 4.5, CY + CH - 3.7, TITLES[i], size=6.4, color=INK, bold=True, ls=1.2)
    for j, (tok, lab, sub) in enumerate(CHIPS[i]):                       # cohort chips
        cy = CY + CH - 9.0 - j * 4.3
        rbox(x + 1.0, cy - .85, 1.7, 1.7, P[tok], HAIR, lw=LW * .6, r=.25, z=4)
        T(x + 3.3, cy + .55, lab, size=4.6, color=INK)
        T(x + 3.3, cy - 1.15, sub, size=4.4, color=SOFT)
    ax.plot([x + .9, x + CW - .9], [CY + 11.6] * 2, color='#E0E0E0', lw=LW, zorder=2)
    T(x + .9, CY + 8.0, TAKE[i], size=4.9, color=SOFT, ls=1.45)
    T(x + .9, CY + 3.0, REFS[i], size=4.2, color=FAINT, va='center', style='italic', ls=1.4)
    if i:
        ax.add_patch(FancyArrowPatch((x - GAP + .2, CY + CH / 2), (x - .2, CY + CH / 2),
                                     arrowstyle='-|>', mutation_scale=5, lw=LW,
                                     color='#B0B0B0', zorder=1))

PT, PB = CY + CH - 19.5, CY + 12.6          # plot band of every card

# ============================== stage 1 ======================================
x = xs[0]
nodes = sorted(pd.unique(EDG[['i_217', 'j_217']].values.ravel()))
th = np.linspace(90, -270, len(nodes), endpoint=False) * np.pi / 180
rr = CW * .215
cx, cy = x + CW * .50, PT - 5.6
pos = {n: (cx + rr * np.cos(t), cy + rr * AR * np.sin(t)) for n, t in zip(nodes, th)}
for _, e in EDG.iterrows():
    a, b = pos[e.i_217], pos[e.j_217]
    ax.plot([a[0], b[0]], [a[1], b[1]], color=P['circ_np12'], lw=LW, alpha=.85, zorder=3)
for n, (px, py) in pos.items():
    ax.add_patch(Circle((px, py), .30, facecolor='white', edgecolor=P['circ_np12'],
                        linewidth=LW * .8, zorder=4))
T(x + 1.0, PT + 1.6, 'task FC \u2192 CPM, IMAGEN', size=4.5, color=SOFT)
LY = cy - rr * AR - 2.2
for k, (tok, lab) in enumerate([('circ_neg29', 'negative, 29 edges'),
                                ('pos_prof34', 'positive, 34 edges'),
                                ('circ_np12', 'NP factor, 12 edges')]):
    yy = LY - k * 1.9
    ax.plot([x + 1.4, x + 3.0], [yy] * 2, color=P[tok], lw=1.3, zorder=4)
    T(x + 3.6, yy, lab, size=4.3, color=SOFT)
T(x + 1.0, LY - 6.6, 'negative NP profile, STRATIFY', size=4.4, color=SOFT)
f1 = Fr(x + CW * .22, PB + 4.4, CW * .56, LY - 9.0 - (PB + 4.4), (-.6, 1.6), (-4.6, 4.6))
ax.plot([f1.X(-.6), f1.X(1.6)], [f1.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
box(f1, 0.0, hc, P['hlth_hc'], rng=RNG)
box(f1, 1.0, pt, P['clin_patients'], rng=RNG)
T(f1.X(0.0), PB + 3.4, 'HC\n225', size=4.3, color=SOFT, ha='center', va='top', ls=1.2)
T(f1.X(1.0), PB + 3.4, 'patients\n202', size=4.3, color=SOFT, ha='center', va='top', ls=1.2)
T(x + 1.0, PB - 1.0, '$g$ = 0.37 [0.18, 0.56] \u00b7 $P_{\\rm Bonf}$ = 2.96 \u00d7 10$^{-4}$',
  size=4.1, color=INK, va='center')

# ============================== stage 2 ======================================
x = xs[1]
ecx, ecy = x + CW * .28, PT - 3.4                     # E / I unit glyph
for dx, lab, col in [(-2.2, 'E', P['exc_ampa']), (2.2, 'I', P['inh_gaba'])]:
    ax.add_patch(Circle((ecx + dx, ecy), 1.35, facecolor='white', edgecolor=col,
                        linewidth=1.0, zorder=4))
    T(ecx + dx, ecy - .05, lab, size=5.0, color=col, bold=True, ha='center', z=5)
ax.add_patch(FancyArrowPatch((ecx - .85, ecy + 1.05), (ecx + .85, ecy + 1.05), arrowstyle='-|>',
                             mutation_scale=4, lw=LW, color=P['exc_ampa'],
                             connectionstyle='arc3,rad=-.45', zorder=4))
ax.add_patch(FancyArrowPatch((ecx + .85, ecy - 1.05), (ecx - .85, ecy - 1.05), arrowstyle='-|>',
                             mutation_scale=4, lw=LW, color=P['inh_gaba'],
                             connectionstyle='arc3,rad=-.45', zorder=4))
T(x + 1.0, PT + 1.6, 'LIF E / I units \u00b7 AMPA \u00b7 GABA-A', size=4.5, color=SOFT)
T(x + CW * .66, ecy + 1.2, 'SC + FC +\ntask BOLD', size=4.3, color=SOFT, ha='center', ls=1.25)
ax.add_patch(FancyArrowPatch((x + CW * .59, ecy), (x + CW * .45, ecy), arrowstyle='-|>',
                             mutation_scale=4.4, lw=LW, color='#B5B5B5', zorder=3))
T(x + 1.0, PT - 8.4, 'assimilated-region BOLD $r$, 12 twins', size=4.4, color=SOFT)
ORD = ['3m_268', '10m_268', '10m_1000', '10m_own', '10m', '100m', '1b']
LBL = ['3M/268', '10M/268', '10M/1k', '10M/vox*', '10M/vox', '100M/vox', '1B/vox']
COL = [P['scale_3m'], P['scale_10m'], P['scale_10m'], P['scale_100m'],
       P['scale_100m'], P['scale_100m'], P['scale_1b']]
BB, BT = PB + 7.2, PT - 10.6
f2 = Fr(x + 3.6, BB, CW - 5.4, BT - BB, (-.75, 6.75), (0.60, 0.95))
for gv in (0.7, 0.8, 0.9):
    ax.plot([f2.X(-.75), f2.X(6.75)], [f2.Y(gv)] * 2, color='#EFEFEF', lw=LW, zorder=1)
    T(f2.X(-.9), f2.Y(gv), f'{gv:.1f}', size=3.9, color=FAINT, ha='right')
for k, (m, c) in enumerate(zip(ORD, COL)):
    v = float(FID.loc[FID.model == m, 'bold_r_mean'].iloc[0])
    rbox(f2.X(k - .34), f2.Y(0.60), f2.X(k + .34) - f2.X(k - .34), f2.Y(v) - f2.Y(0.60),
         c, 'none', lw=0, r=.1, z=4)
    T(f2.X(k) + .30, BB - .6, LBL[k], size=3.6, color=SOFT, ha='right', va='center', rot=52)
T(x + 1.0, PB + .6, '* 10 M hyper-parameters; all other builds use\n3 M (268 regions) or 100 M (voxel-wise)',
  size=3.9, color=FAINT, va='center', ls=1.4)

# ============================== stage 3 ======================================
x = xs[2]
f3 = Fr(x + CW * .17, PB + 8.6, CW * .70, PT - 1.5 - (PB + 8.6), (-.45, 2.45), (-3.4, 12.6))
ax.plot([f3.X(-.45), f3.X(2.45)], [f3.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
sub = POP.sample(120, random_state=1)                    # thin lines, all 288 in the boxes
for _, r in sub.iterrows():
    ax.plot(f3.X([0, 1, 2]), f3.Y([r.simulated, r.ampa, r.gaba]),
            color='#C9C9C9', lw=.16, alpha=.55, zorder=2)
box(f3, 0.0, POP.simulated, P['unp_baseline'], pts=False)
box(f3, 1.0, POP.ampa, P['exc_ampa'], pts=False)
box(f3, 2.0, POP.gaba, P['inh_gaba'], pts=False)
for k, lab in enumerate(['baseline', 'AMPA \u2191', 'GABA-A \u2191']):
    T(f3.X(k), PB + 7.6, lab, size=4.3, color=SOFT, ha='center', va='top')
T(x + 1.0, PT + 1.6, 'simulated NP factor, $n$ = 288', size=4.5, color=SOFT)
T(x + 1.0, PB + 2.6,
  'AMPA +0.78, $t$(287) = 14.14, 234 / 288 up\nGABA-A +2.74, $t$(287) = 27.11, 282 / 288 up\n'
  '229 both-up \u00b7 59 any-down',
  size=4.1, color=INK, va='center', ls=1.5)
T(x + 1.0, PT - 2.2, 'group difference gone after perturbation:\n'
  '$F$(2,285) = 0.95, $P$ = 0.39 (AMPA);\n0.85, 0.43 (GABA-A)',
  size=3.9, color=FAINT, ha='left', va='top', ls=1.45)

# ============================== stage 4 ======================================
x = xs[3]
f4 = Fr(x + CW * .20, PT - 10.0, CW * .62, 8.8, (-.45, 1.45), (-2.6, 2.6))
ax.plot([f4.X(-.45), f4.X(1.45)], [f4.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
box(f4, 0.0, HVd['ket'], P['exc_ketamine'], rng=RNG, ptsize=1.1)
box(f4, 1.0, HVd['mid'], P['inh_midazolam'], rng=RNG, ptsize=1.1)
T(f4.X(0.0), PT - 10.9, 'ketamine', size=4.2, color=SOFT, ha='center', va='top')
T(f4.X(1.0), PT - 10.9, 'midazolam', size=4.2, color=SOFT, ha='center', va='top')
T(x + 1.0, PT + 1.6, '\u0394 NP, drug \u2212 placebo \u00b7 $n$ = 27', size=4.5, color=SOFT)
T(x + 1.0, PT - 14.2, 'slope on placebo 0.55 ($P$ = 0.069)\nand 0.18 ($P$ = 0.0056), both < 1',
  size=3.9, color=FAINT, ls=1.45, va='center')
T(x + 1.0, PT - 18.2, '\u0394 NP under ketamine, clinical cohort', size=4.4, color=SOFT)
f5 = Fr(x + CW * .20, PB + 7.6, CW * .62, PT - 20.0 - (PB + 7.6), (-.45, 1.45), (-5.4, 5.4))
ax.plot([f5.X(-.45), f5.X(1.45)], [f5.Y(0)] * 2, color='#E6E6E6', lw=LW, ls=(0, (2.4, 1.8)), zorder=2)
box(f5, 0.0, CLI.loc[CLI.group == 'MDD', 'd'], P['clin_mdd'], rng=RNG, ptsize=1.1)
box(f5, 1.0, CLI.loc[CLI.group == 'HC', 'd'], P['hlth_hc'], rng=RNG, ptsize=1.1)
T(f5.X(0.0), PB + 6.8, 'MDD 22', size=4.2, color=SOFT, ha='center', va='top')
T(f5.X(1.0), PB + 6.8, 'HC 14', size=4.2, color=SOFT, ha='center', va='top')
T(x + 1.0, PB + 2.6, 'group \u00d7 drug $t$(30) = 3.43, $P$ = 0.0018\n'
                     'placebo baseline, $n$ = 41:\n$t$(35) = \u22122.51, $P$ = 0.017',
  size=4.1, color=INK, ls=1.5, va='center')

# ============================== stage 5 ======================================
x = xs[4]
xv, yv = LON.ampa_restoration_index.values, LON.fu3_symptom_change.values
SB = PB + 8.6
f6 = Fr(x + CW * .24, SB, CW * .66, PT - 1.5 - SB,
        (xv.min() - .12 * np.ptp(xv), xv.max() + .12 * np.ptp(xv)),
        (yv.min() - .12 * np.ptp(yv), yv.max() + .12 * np.ptp(yv)))
ax.scatter(f6.X(xv), f6.Y(yv), s=1.8, facecolor=P['exc_ampa'], edgecolor=pt_edge(P['exc_ampa']),
           linewidth=.14, zorder=4)
b1, b0 = np.polyfit(xv, yv, 1)
gx = np.linspace(xv.min(), xv.max(), 20)
ax.plot(f6.X(gx), f6.Y(b0 + b1 * gx), color=pt_edge(P['exc_ampa']), lw=1.0, zorder=5)
T(x + 1.0, PT + 1.6, 'AMPA restoration index vs \u0394 symptoms', size=4.5, color=SOFT)
T(x + CW * .24 - 1.4, (f6.Y(f6.yl[0]) + f6.Y(f6.yl[1])) / 2, 'observed \u0394 symptoms, 19 \u2192 23',
  size=4.1, color=SOFT, ha='center', va='center', rot=90)
T((f6.X(f6.xl[0]) + f6.X(f6.xl[1])) / 2, SB - 1.0, 'restoration index (model)',
  size=4.1, color=SOFT, ha='center', va='top')
T(x + 1.0, PB + 2.6, f'$r$ = {LONr[0]:.2f} unadjusted\npartial $r$ = 0.24, $P$ = 0.026\n'
                     'model $R^2$ = 0.23, $F$(5,79) = 4.80, $P$ = 0.0007',
  size=4.1, color=INK, ls=1.5, va='center')

# --------------------------------------------------------- feedback arrows ---
ax.add_patch(FancyArrowPatch((xs[0] + CW * .55, CY + CH + .7), (xs[4] + CW * .45, CY + CH + .7),
                             arrowstyle='-|>', mutation_scale=5.6, lw=.9,
                             color=P['scale_100m'], connectionstyle='arc3,rad=-.09', zorder=3))
T(50, CY + CH + 5.0, 'NP \u2192 symptom map fitted once at age 19, then reused',
  size=4.8, color=P['scale_100m'], ha='center')
ax.add_patch(FancyArrowPatch((xs[2] + CW * .55, CY - .7), (xs[3] + CW * .55, CY - .7),
                             arrowstyle='-|>', mutation_scale=5.6, lw=.9,
                             color=pt_edge(P['exc_ampa']), connectionstyle='arc3,rad=.30', zorder=3))
T(xs[3] + CW * .05, CY - 4.6, 'perturbation \u2192 response mapping, applied to empirical data without refitting',
  size=4.8, color=pt_edge(P['exc_ampa']), ha='center')

# ------------------------------------------------------- colour reference ----
T(2.0, 8.8, 'Colour correspondence', size=5.2, color=INK, bold=True)
PAIRS = [('exc_ampa', 'exc_ketamine', 'virtual AMPA \u2194 ketamine'),
         ('inh_gaba', 'inh_midazolam', 'virtual GABA-A \u2194 midazolam'),
         ('unp_baseline', 'unp_placebo', 'simulated baseline \u2194 placebo')]
for k, (a, b, lab) in enumerate(PAIRS):
    xx = 2.0 + k * 21.0
    rbox(xx, 5.5, 1.5, 1.5, P[a], HAIR, lw=LW * .5, r=.2, z=4)
    rbox(xx + 1.6, 5.5, 1.5, 1.5, P[b], HAIR, lw=LW * .5, r=.2, z=4)
    T(xx + 3.9, 6.25, lab, size=4.3, color=SOFT)
SINGLES = [('circ_np12', 'NP factor / negative profile'), ('pos_prof34', 'positive profile'),
           ('scale_3m', 'regional build'), ('scale_100m', 'voxel build'),
           ('hlth_hc', 'HC / baseline / placebo'), ('clin_highsymp', 'high-symptom'),
           ('clin_patients', 'patient / MDD'), ('clin_aud', 'AUD')]
for k, (tok, lab) in enumerate(SINGLES):
    xx = 2.0 + (k % 4) * 19.6
    yy = 3.2 if k < 4 else 0.9
    rbox(xx, yy - .75, 1.5, 1.5, P[tok], HAIR, lw=LW * .5, r=.2, z=4)
    T(xx + 2.0, yy, lab, size=4.2, color=SOFT)
T(66.0, 6.25, 'every point plotted is an observed or simulated participant value;\n'
              'no element of this figure is schematic data', size=3.9, color=FAINT, ls=1.45)

fig.savefig(os.path.join(HERE, 'fig1_framework_v2.png'), dpi=450)
fig.savefig(os.path.join(HERE, 'fig1_framework_v2.pdf'))
import matplotlib as mpl
rnd = fig.canvas.get_renderer()
tx = [(t, t.get_window_extent(rnd)) for t in fig.findobj(mpl.text.Text)
      if t.get_text().strip() and t.get_visible()]
ov = [(p.get_text()[:26], q.get_text()[:26]) for i, (p, bp) in enumerate(tx)
      for q, bq in tx[i + 1:] if bp.overlaps(bq)]
print('texts %d  overlaps %d' % (len(tx), len(ov)))
for o in ov[:20]:
    print('  OVERLAP', o)
print('saved  n_STRATIFY=%d/%d  n_pop=%d  n_hv=%d  n_cli=%d  n_lon=%d  r_raw=%.4f'
      % (len(hc), len(pt), len(POP), len(HV), len(CLI), len(LON), LONr[0]))
