"""Fig. 1 - schematic of the full analytical pipeline, sample selection to outputs.

Pictorial schematic in the style of the original framework figure, rebuilt with
(i) the registered NP-DTB palette, (ii) the current numbers, and (iii) an
explicit sample-selection strand in every stage, as requested by the reviewer.

Nothing in this figure is hand-drawn data: every mini-plot is rendered from the
tables in fig1_data/, which are extracts of the same source files that produce
Figs. 2-5.  Stage headers are neutral grey; colour is spent only on entities,
with the same meaning as in the data figures (see the correspondence strip).

Inputs : fig1_data/*.csv
Outputs: fig1_pipeline.png|.pdf
"""
import os, sys, textwrap
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, C, LW
from supp_kit import fill, pt_edge
apply_np_style()
D = os.path.join(HERE, 'fig1_data')

SEL = pd.read_csv(f'{D}/fig1_sample_selection.csv')
FID = pd.read_csv(f'{D}/fig1_mini_fidelity.csv')
PER = pd.read_csv(f'{D}/fig1_mini_perturbation_n288.csv')
H27 = pd.read_csv(f'{D}/fig1_mini_healthy_n27.csv')
M36 = pd.read_csv(f'{D}/fig1_mini_clinical_n36.csv')
L85 = pd.read_csv(f'{D}/fig1_mini_longitudinal_n85.csv')
EDG = pd.read_csv(f'{D}/fig1_mini_np12_edges.csv')
STR = pd.read_csv(os.path.join(HERE, '..', 'fig.2', 'fig2_data', 'fig2c_profile_scores.csv'))

INK, SOFT, FAINT = '#1A1A1A', '#4D4D4D', '#8C8C8C'
FIG_W_MM, FIG_H_MM = 180.0, 150.0
fig = plt.figure(figsize=(FIG_W_MM / 25.4, FIG_H_MM / 25.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
AR = FIG_W_MM / FIG_H_MM            # x-unit : y-unit aspect for circles


def rbox(x, y, w, h, fc, ec='none', lw=LW, r=.9, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))


def T(x, y, s, size=5.2, color=SOFT, bold=False, ha='left', va='center', ls=1.3, z=6, style=None):
    ax.text(x, y, s, fontsize=size, color=color, fontweight='bold' if bold else 'normal',
            ha=ha, va=va, linespacing=ls, zorder=z, style=style)


class Fr:
    """sub-axes in canvas coordinates"""
    def __init__(self, gx, gy, gw, gh, xlim, ylim):
        self.gx, self.gy, self.gw, self.gh = gx, gy, gw, gh
        self.xl, self.yl = xlim, ylim
    def X(self, v):
        return self.gx + (np.asarray(v, float) - self.xl[0]) / (self.xl[1] - self.xl[0]) * self.gw
    def Y(self, v):
        return self.gy + (np.asarray(v, float) - self.yl[0]) / (self.yl[1] - self.yl[0]) * self.gh


def minibox(fr, xc, v, col, w=.34):
    v = np.asarray(v, float)
    q1, med, q3 = np.percentile(v, [25, 50, 75]); iqr = q3 - q1
    lo = v[v >= q1 - 1.5 * iqr].min(); hi = v[v <= q3 + 1.5 * iqr].max()
    ax.plot([fr.X(xc)] * 2, [fr.Y(lo), fr.Y(hi)], color=INK, lw=LW * .7, zorder=3)
    rbox(fr.X(xc - w / 2), fr.Y(q1), fr.X(xc + w / 2) - fr.X(xc - w / 2),
         fr.Y(q3) - fr.Y(q1), fill(col), INK, lw=LW * .7, r=.18, z=4)
    ax.plot([fr.X(xc - w / 2), fr.X(xc + w / 2)], [fr.Y(med)] * 2, color=INK, lw=LW * .9, zorder=5)


# ---------------------------------------------------------------- title ------
T(2.0, 97.4, 'Fig. 1 | Analytical pipeline, from sample selection to final outputs',
  size=8.4, color=INK, bold=True)
T(2.0, 93.4, 'A symptom-linked circuit is derived empirically, rebuilt inside individual digital twin brains and '
             'perturbed in silico; the simulated response is then tested\nagainst two pharmacological datasets and '
             'against four-year symptom change. The NP factor is the single quantity carried through all five stages.',
  size=5.6, color=SOFT, ls=1.45)

X0, GAP = 2.0, 1.15
CW = (100 - 2 * X0 - 4 * GAP) / 5
CY, CH = 18.5, 64.0
xs = [X0 + i * (CW + GAP) for i in range(5)]

TITLES = ['Derive the circuit\nphenotype', 'Build and select\nthe digital twin',
          'Perturb the circuit\nin silico', 'Validate against\ntwo drug datasets',
          'Forecast four-year\nsymptom change']
TAKE = ['The 29-edge negative profile,\nand its 12-edge NP factor,\nseparate patients from controls',
        'Build choice decides which\ninference is admissible \u2014\nit is not a free parameter',
        'Both perturbations move NP\nconnectivity, in a\nparticipant-specific direction',
        'Drug effects follow the\nvirtual perturbation without\nany refitting of the mapping',
        'The perturbational response\ncarries prospective\ninformation about symptoms']
FIGREF = ['Fig. 2 \u00b7 Supp. STRATIFY, PET', 'Fig. 3 \u00b7 Supp. assimilation region',
          'Fig. 4 \u00b7 Supp. conductance grid',
          'Fig. 5a\u2013g \u00b7 Supp. paired MID,\nwhole-brain drug, Oldham',
          'Fig. 5h \u00b7 Supp. longitudinal']

for i, x in enumerate(xs):
    rbox(x, CY, CW, CH, 'white', '#D9D9D9', lw=LW, r=1.1, z=1)
    rbox(x, CY + CH - 7.4, CW, 7.4, '#F0F0F0', 'none', r=1.1, z=2)
    rbox(x, CY + CH - 7.4, CW, 3.0, '#F0F0F0', 'none', r=0, z=2)
    ax.add_patch(Circle((x + 2.4, CY + CH - 3.7), 1.35 / AR * AR * .9, facecolor=SOFT,
                        edgecolor='none', zorder=4))
    T(x + 2.4, CY + CH - 3.75, str(i + 1), size=5.8, color='white', bold=True, ha='center', z=5)
    T(x + 4.6, CY + CH - 3.7, TITLES[i], size=6.4, color=INK, bold=True, ls=1.2)
    T(x + .9, CY + 8.0, TAKE[i], size=5.0, color=SOFT, ls=1.45, va='center')
    T(x + .9, CY + 4.2, FIGREF[i], size=4.6, color=FAINT, va='top', style='italic')
    ax.plot([x + .9, x + CW - .9], [CY + 11.8] * 2, color='#E0E0E0', lw=LW, zorder=2)
    if i:
        ax.add_patch(FancyArrowPatch((x - GAP + .18, CY + CH / 2), (x - .18, CY + CH / 2),
                                     arrowstyle='-|>', mutation_scale=5, lw=LW, color='#B0B0B0', zorder=1))

# ------------------------------------------------- sample-selection strand ---
SY = CY + CH - 20.0
for i, x in enumerate(xs):
    T(x + .9, CY + CH - 9.4, 'SAMPLE SELECTION', size=4.5, color=FAINT, bold=True)
    rows = SEL[SEL.stage == i + 1]
    yy = SY + 7.6
    for _, r in rows.iterrows():
        T(x + .9, yy, r.cohort, size=5.0, color=INK, bold=True)
        if r.excluded:
            T(x + .9, yy - 2.7, f"{r.screened:,} screened", size=4.7, color=SOFT)
            wrapped = textwrap.fill(f"\u2212{r.excluded:,}  {r.reason_short}", 30)
            nl = wrapped.count('\n')
            T(x + .9, yy - 4.6 - .9 * nl, wrapped, size=4.1, color=C('patient'), ls=1.28)
            T(x + .9, yy - 7.4 - 1.9 * nl, f"$\\bf{{{r.analysed:,}}}$ analysed", size=4.9, color=INK)
            yy -= 10.4 + 1.9 * nl
        else:
            T(x + .9, yy - 2.8, f"$\\bf{{{r.analysed:,}}}$ analysed", size=4.9, color=INK)
            yy -= 5.8

# ============================ stage 1: node ring + STRATIFY NP boxes ==========
g1x, g1y, g1w, g1h = xs[0] + 1.0, CY + 17.0, CW - 2.0, 16.0
nodes = sorted(pd.unique(EDG[['i_217', 'j_217']].values.ravel()))
th = np.linspace(90, -270, len(nodes), endpoint=False) * np.pi / 180
cx, cy, rx = g1x + g1w * .30, g1y + g1h * .56, g1w * .26
ry = rx * (FIG_W_MM / FIG_H_MM) * (100 / 100)
P = {n: (cx + rx * np.cos(t), cy + ry * AR * np.cos(0) * np.sin(t) * .78) for n, t in zip(nodes, th)}
for _, e in EDG.iterrows():
    a, b = P[e.i_217], P[e.j_217]
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C('np12'), lw=LW * .9, alpha=.75, zorder=3)
for n, (px, py) in P.items():
    ax.add_patch(Circle((px, py), .40, facecolor='white', edgecolor=C('np12'),
                        linewidth=LW * .8, zorder=4))
T(cx, cy - ry * .78 - 2.4, '12-edge NP factor', size=4.5, color=SOFT, ha='center')
fr1 = Fr(g1x + g1w * .62, g1y + 3.2, g1w * .32, g1h * .62, (-.6, 1.6), (-4.5, 4.5))
for k, (grp, col) in enumerate([('HC', 'hc'), ('Patient', 'patient')]):
    minibox(fr1, k, STR.loc[STR.Group == grp, 'NP_factor'].values, C(col))
    T(fr1.X(k), g1y + 1.2, grp, size=4.4, color=SOFT, ha='center')
T(g1x + g1w * .78, g1y + g1h - .6, 'STRATIFY', size=4.5, color=SOFT, ha='center')

# ============================ stage 2: fidelity bars ==========================
g2x, g2y, g2w, g2h = xs[1] + 1.4, CY + 18.5, CW - 3.2, 15.0
FID = FID.sort_values('bold_r_mean', ascending=False)
LBL = {'10m_268': '10 M/268', '3m_268': '3 M/268', '1b': '1 B', '100m': '100 M',
       '10m': '10 M vox', '10m_own': '10 M own', '10m_1000': '10 M/1000'}
FAM = {'10m_268': 'model_regional', '3m_268': 'model_regional', '10m_1000': 'model_regional',
       '1b': 'model_voxel', '100m': 'model_voxel', '10m': 'model_voxel', '10m_own': 'model_voxel'}
fr2 = Fr(g2x, g2y, g2w, g2h * .74, (-.7, len(FID) - .3), (.6, .95))
for k, (_, r) in enumerate(FID.iterrows()):
    col = C(FAM[r.model])
    ax.add_patch(FancyBboxPatch((fr2.X(k - .34), fr2.Y(.6)), fr2.X(.68) - fr2.X(0),
                                fr2.Y(r.bold_r_mean) - fr2.Y(.6),
                                boxstyle='round,pad=0,rounding_size=0.10',
                                facecolor=col, edgecolor='none', zorder=3))
    T(fr2.X(k), fr2.Y(.6) - (1.0 if k % 2 == 0 else 2.6), LBL[r.model], size=3.9,
      color=SOFT, ha='center', z=5)
T(g2x, g2y + g2h * .74 + 1.9, 'Assimilated-region BOLD $r$', size=4.5, color=SOFT)
for lab, key, dy in [('regional', 'model_regional', 0), ('voxel', 'model_voxel', -1.9)]:
    ax.add_patch(FancyBboxPatch((g2x + g2w * .60, g2y + g2h * .74 - 1.0 + dy), 1.0, .9,
                                boxstyle='round,pad=0,rounding_size=0.12',
                                facecolor=C(key), edgecolor='none', zorder=4))
    T(g2x + g2w * .60 + 1.4, g2y + g2h * .74 - .55 + dy, lab, size=4.2, color=SOFT)
T(g2x, g2y - 5.0, '1 B fidelity reference\n100 M parameter search\n3 M/268 population runs',
  size=4.3, color=FAINT, ls=1.4)

# ============================ stage 3: baseline -> AMPA / GABA-A ==============
g3x, g3y, g3w, g3h = xs[2] + 2.0, CY + 17.5, CW - 4.0, 16.0
fr3 = Fr(g3x, g3y + 2.6, g3w, g3h * .72, (-.6, 2.6), (-3, 8))
for k, (c, col) in enumerate([('simulated', 'baseline'), ('ampa', 'ampa'), ('gaba', 'gaba')]):
    minibox(fr3, k, PER[c].values, C(col))
    T(fr3.X(k), g3y + 1.0, ['baseline', 'AMPA \u2191', 'GABA-A \u2191'][k], size=4.3,
      color=SOFT, ha='center')
T(g3x, g3y + 2.6 + g3h * .72 + 1.7, 'Simulated NP factor, $n$ = 288', size=4.5, color=SOFT)
T(g3x, g3y - 3.4, 'GABA-A is applied on top of AMPA', size=4.3, color=FAINT)

# ============================ stage 4: two drug datasets ======================
g4x, g4y, g4w, g4h = xs[3] + 1.6, CY + 15.5, CW - 3.4, 17.5
fr4a = Fr(g4x, g4y + 9.0, g4w * .52, 7.4, (-.6, 2.6), (-1.2, 2.3))
for k, (c, col) in enumerate([('Placebo', 'placebo'), ('Ketamine', 'ketamine'), ('Midazolam', 'midazolam')]):
    minibox(fr4a, k, H27[c].values, C(col), w=.42)
T(g4x, g4y + 9.0 + 7.4 + 1.4, 'Healthy, $n$ = 27', size=4.4, color=SOFT)
T(g4x, g4y + 7.8, 'pla \u00b7 ket \u00b7 mid', size=4.0, color=FAINT)
fr4b = Fr(g4x + g4w * .62, g4y + 9.0, g4w * .34, 7.4, (-.6, 1.6), (-4, 4))
for k, (c, col) in enumerate([('FC_p2', 'placebo'), ('FC_d2', 'ketamine')]):
    minibox(fr4b, k, M36[c].values, C(col), w=.42)
T(g4x + g4w * .62, g4y + 9.0 + 7.4 + 1.4, 'Clinical, $n$ = 36', size=4.4, color=SOFT)
T(g4x + g4w * .62, g4y + 7.8, 'pla \u00b7 ket', size=4.0, color=FAINT)
T(g4x, g4y + 3.4, 'Summed NP-related MID FC;\nwhole-brain maps tested for\ndirectional concordance',
  size=4.3, color=FAINT, ls=1.4)

# ============================ stage 5: longitudinal scatter ===================
g5x, g5y, g5w, g5h = xs[4] + 2.2, CY + 18.0, CW - 4.4, 15.5
xv, yv = L85.ampa_restoration_index.values, L85.fu3_symptom_change.values
fr5 = Fr(g5x, g5y + 1.4, g5w, g5h * .80,
         (xv.min() - .1 * np.ptp(xv), xv.max() + .1 * np.ptp(xv)),
         (yv.min() - .1 * np.ptp(yv), yv.max() + .1 * np.ptp(yv)))
ax.scatter(fr5.X(xv), fr5.Y(yv), s=2.2, facecolor=C('ampa'), edgecolor=pt_edge(C('ampa')),
           linewidth=LW * .3, zorder=3)
b, a = np.polyfit(xv, yv, 1)
xx = np.array([xv.min(), xv.max()])
ax.plot(fr5.X(xx), fr5.Y(a + b * xx), color=C('ampa'), lw=LW * 1.5, zorder=4)
T(g5x, g5y + 1.4 + g5h * .80 + 1.7, 'AMPA index vs four-year symptom change', size=4.4, color=SOFT)
T(g5x, g5y - 1.4, '$n$ = 85 \u00b7 $r$ = 0.26 \u00b7 model $R^2$ = 0.23', size=4.3, color=FAINT)

# ------------------------------------------------------- linking arrows ------
ax.annotate('', xy=(xs[2] + CW * .5, CY + CH + 1.0), xytext=(xs[1] + CW * .5, CY + CH + 1.0),
            arrowprops=dict(arrowstyle='-|>', color=C('model_voxel'), lw=LW * 1.3,
                            connectionstyle='arc3,rad=-0.30', mutation_scale=6))
T((xs[1] + xs[2]) / 2 + CW * .5, CY + CH + 5.4,
  'selected build fixes which inference is admissible', size=4.7, color=C('model_voxel'), ha='center')
ax.annotate('', xy=(xs[3] + CW * .5, CY - 1.2), xytext=(xs[2] + CW * .5, CY - 1.2),
            arrowprops=dict(arrowstyle='-|>', color=C('ampa'), lw=LW * 1.3,
                            connectionstyle='arc3,rad=0.30', mutation_scale=6))
T((xs[2] + xs[3]) / 2 + CW * .5, CY - 6.0,
  'perturbation \u2192 response mapping applied to empirical data without refitting',
  size=4.7, color=C('ampa'), ha='center')

# ------------------------------------------------- colour correspondence -----
T(2.0, 7.8, 'Colour correspondence', size=5.4, color=INK, bold=True)
KEYS = [('np12', 'NP factor / negative profile'), ('pos_profile', 'positive profile'),
        ('model_regional', 'regional build'), ('model_voxel', 'voxel build'),
        ('ampa', 'virtual AMPA \u2194 ketamine'), ('gaba', 'virtual GABA-A \u2194 midazolam'),
        ('hc', 'HC / baseline / placebo'), ('high_symptom', 'high-symptom'),
        ('patient', 'patient / MDD'), ('aud', 'AUD')]
cxp, cyp = 2.0, 4.1
for k, (key, lab) in enumerate(KEYS):
    col, row = k % 5, k // 5
    x = cxp + col * 19.4; y = cyp - row * 3.4
    ax.add_patch(FancyBboxPatch((x, y - .75), 1.5, 1.5, boxstyle='round,pad=0,rounding_size=0.18',
                                facecolor=C(key), edgecolor='none', zorder=4))
    T(x + 2.1, y, lab, size=4.6, color=SOFT)

fig.savefig(os.path.join(HERE, 'fig1_pipeline.png'), dpi=450, bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'fig1_pipeline.pdf'), bbox_inches='tight')
print('rendered')
