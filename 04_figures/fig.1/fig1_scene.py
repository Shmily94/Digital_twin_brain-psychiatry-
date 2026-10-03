"""Figure 1 (framework overview) as a renderer-independent scene.

Builds one list of primitives in a 0-100 x 0-100 space, then renders it twice:
matplotlib (PNG/PDF) and python-pptx (editable slide).  v2 Woo-derived palette.
"""
import numpy as np, pandas as pd

FIG_W, FIG_H = 7.09, 5.75          # inches, 180 mm wide
PAL_V2_VID = 'f00fa6dc-1c4e-4ad7-8955-5d387115e61c'
INK, SOFT, FAINT = '#1A1A1A', '#4D4D4D', '#8C8C8C'
FC2 = ['#2F4F4A', '#819D98', '#D5E0DC', '#F4F2EE', '#FAE3B0', '#C99A46', '#6E4A00']

PAL = dict(zip(*[pd.read_csv(host.artifact_path(PAL_V2_VID))[c] for c in ('token', 'hex')]))

S = []                              # the scene
def rect(x, y, w, h, fill=None, line=None, lw=0.5, round_=0.0, z=2):
    S.append(dict(k='rect', x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, round_=round_, z=z))
def oval(cx, cy, rx, ry, fill=None, line=None, lw=0.5, z=2):
    S.append(dict(k='oval', cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, line=line, lw=lw, z=z))
def line(x1, y1, x2, y2, color=SOFT, lw=0.5, dash=None, arrow=False, z=2):
    S.append(dict(k='line', x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw, dash=dash, arrow=arrow, z=z))
def poly(pts, fill=None, line_=None, lw=0.4, close=True, z=2):
    S.append(dict(k='poly', pts=list(pts), fill=fill, line=line_, lw=lw, close=close, z=z))
def arc(x1, y1, x2, y2, rad=0.2, color=SOFT, lw=0.8, arrow=True, n=40, z=2):
    """quadratic-ish arc between two points, bulge = rad (matplotlib arc3 convention)"""
    p0, p1 = np.array([x1, y1]), np.array([x2, y2])
    mid = (p0 + p1) / 2
    d = p1 - p0
    ctrl = mid + rad * np.array([-d[1], d[0]])
    t = np.linspace(0, 1, n)[:, None]
    pts = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * ctrl + t ** 2 * p1
    S.append(dict(k='path', pts=[tuple(p) for p in pts], color=color, lw=lw, arrow=arrow, z=z))
def text(x, y, s, size=5.4, color=SOFT, bold=False, ha='left', va='center', rot=0, ls=1.35, z=5):
    S.append(dict(k='text', x=x, y=y, s=s, size=size, color=color, bold=bold,
                  ha=ha, va=va, rot=rot, ls=ls, z=z))

class Frame:
    """maps a local data box onto a rectangle of the global 0-100 canvas"""
    def __init__(self, gx, gy, gw, gh, xlim, ylim):
        self.gx, self.gy, self.gw, self.gh = gx, gy, gw, gh
        self.x0, self.x1 = xlim; self.y0, self.y1 = ylim
    def X(self, v): return self.gx + (np.asarray(v, float) - self.x0) / (self.x1 - self.x0) * self.gw
    def Y(self, v): return self.gy + (np.asarray(v, float) - self.y0) / (self.y1 - self.y0) * self.gh
    def W(self, v): return np.asarray(v, float) / (self.x1 - self.x0) * self.gw
    def H(self, v): return np.asarray(v, float) / (self.y1 - self.y0) * self.gh

def boxplot(fr, xc, vals, color, width=0.34, pt=True, rng=None, ptsize=0.28):
    v = np.sort(np.asarray(vals, float))
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    iqr = q3 - q1
    lo = v[v >= q1 - 1.5 * iqr].min(); hi = v[v <= q3 + 1.5 * iqr].max()
    xL, xR = fr.X(xc - width / 2), fr.X(xc + width / 2)
    line(fr.X(xc), fr.Y(lo), fr.X(xc), fr.Y(hi), color=color, lw=0.6, z=3)
    for yy in (lo, hi):
        line(fr.X(xc - width / 5), fr.Y(yy), fr.X(xc + width / 5), fr.Y(yy), color=color, lw=0.6, z=3)
    rect(xL, fr.Y(q1), xR - xL, fr.Y(q3) - fr.Y(q1), fill='#FFFFFF', line=color, lw=0.7, z=4)
    line(xL, fr.Y(med), xR, fr.Y(med), color=color, lw=1.2, z=5)
    if pt:
        jx = rng.uniform(-width * 0.28, width * 0.28, len(v))
        for xj, vv in zip(jx, v):
            oval(fr.X(xc + xj), fr.Y(vv), ptsize, ptsize * FIG_W / FIG_H, fill=color, line=None, lw=0, z=6)
    return q1, med, q3


def build():
    rng = np.random.default_rng(7)
    X0, W, GAP = 2.0, 18.25, 1.19
    BOX_Y, BOX_H = 24.0, 57.0
    xs = [X0 + i * (W + GAP) for i in range(5)]
    Y_TITLE, Y_CHIP0, CHIP_DY = BOX_Y + BOX_H - 2.3, BOX_Y + BOX_H - 6.6, 3.9
    GA_Y, GA_H = 48.0, 19.5
    GB_Y, GB_H = 34.3, 12.2
    Y_TAKE = 28.4

    TITLES = ['Derive the circuit\nphenotype', 'Build and calibrate\nindividual twins',
              'Perturb the circuit\nin silico', 'Validate against\ntwo drug datasets',
              'Forecast four-year\nsymptom change']
    COHORTS = [[('IMAGEN', 'n = 1,050', 'coh_imagen'), ('STRATIFY', 'n = 427', 'coh_stratify')],
               [('12 twins', '1 B neurons', 'coh_imagen'), ('grid search', '100 M', 'coh_stratify')],
               [('12 twins', '1 B', 'coh_imagen'), ('population', 'n = 288, 3 M', 'coh_stratify')],
               [('crossover', 'n = 27', 'coh_pharm_hv'), ('clinical', 'MDD 22 / HC 14', 'coh_pharm_clin')],
               [('IMAGEN follow-up', 'n = 85', 'coh_imagen_fu3'), ('', 'age 19 \u2192 23', 'coh_imagen_fu3')]]
    TAKE = ['Only the 29-edge negative\nprofile separates patients\nfrom controls',
            'Scale decides which\ninference is admissible \u2014\nnot a free parameter',
            'Both perturbations move\nNP connectivity, in a\nparticipant-specific direction',
            'Opposite drug directions,\nand patients and controls\nmove opposite ways',
            'Perturbational response\ncarries prospective\ninformation']

    text(2.0, 97.2, 'Fig. 1 | A perturbation-capable digital twin brain for a symptom-linked circuit',
         size=8.6, color=INK, bold=True)
    text(2.0, 93.0, 'A circuit whose connectivity tracks symptom load is identified empirically, rebuilt inside '
                    'individual digital twin brains and perturbed in silico; the resulting response is then\ntested '
                    'against two drug datasets and against symptom change four years later. The NP factor is the '
                    'single quantity carried through all five stages.', size=6.3, ls=1.55)

    for i, x in enumerate(xs):
        rect(x, BOX_Y, W, BOX_H, fill='#FBFBFA', line='#D8D6D2', lw=0.7, round_=1.2, z=1)
        oval(x + 1.85, Y_TITLE + 0.05, 1.3, 1.3 * FIG_W / FIG_H, fill=INK, line=None, lw=0, z=3)
        text(x + 1.85, Y_TITLE + 0.05, str(i + 1), size=6.2, color='#FFFFFF', bold=True, ha='center', z=4)
        text(x + 3.9, Y_TITLE, TITLES[i], size=6.9, color=INK, bold=True, ls=1.24, z=4)
        cy = Y_CHIP0
        for name, nn, tok in COHORTS[i]:
            if name or nn:
                rect(x + 1.3, cy - 1.35, 1.45, 2.7, fill=PAL[tok], line='#9A9A9A', lw=0.3, z=3)
                if name:
                    text(x + 3.1, cy + 0.6, name, size=5.3, z=3)
                text(x + 3.1, cy - 0.85 if name else cy, nn, size=5.3, color=INK, z=3)
            cy -= CHIP_DY
        text(x + 1.3, Y_TAKE, TAKE[i], size=5.5, ls=1.5, z=3)
        if i < 4:
            line(x + W + 0.10, 55.0, x + W + GAP - 0.10, 55.0, color='#B4B1AC', lw=0.9, arrow=True)

    # ---- 1 | connectogram + case-control gap ------------------------------
    f1 = Frame(xs[0] + 1.25, GA_Y, W - 2.5, GA_H, (-1.15, 1.15), (-1.62, 1.42))
    th = np.linspace(0, 2 * np.pi, 17)[:-1] + 0.1
    R, CY = 0.80, 0.26
    nx, ny = R * np.cos(th), CY + R * np.sin(th)
    oval(f1.X(0), f1.Y(CY), f1.W(R), f1.H(R), fill=None, line='#E6E3DE', lw=0.6)
    for (s, t), tok, lw in ([(p, 'pos_prof34', 0.75) for p in [(0, 3), (6, 10), (9, 15), (2, 5)]] +
                            [(p, 'circ_neg29', 1.2) for p in [(0, 6), (1, 9), (2, 11), (3, 8), (5, 13), (7, 14), (4, 12)]]):
        arc(f1.X(nx[s]), f1.Y(ny[s]), f1.X(nx[t]), f1.Y(ny[t]), rad=0.16,
            color=PAL[tok], lw=lw, arrow=False, n=22, z=3)
    for a_, b_ in zip(nx, ny):
        oval(f1.X(a_), f1.Y(b_), 0.30, 0.30 * FIG_W / FIG_H, fill=PAL['circ_nonnp'], line=SOFT, lw=0.32, z=5)
    text(f1.X(0), f1.Y(1.38), 'task FC \u2192 CPM', size=5.3, ha='center', va='top')
    for k, (lab, tok, yy) in enumerate([('negative, 29 edges', 'circ_neg29', -0.80),
                                        ('positive, 34 edges', 'pos_prof34', -1.12)]):
        line(f1.X(-1.05), f1.Y(yy), f1.X(-0.80), f1.Y(yy), color=PAL[tok], lw=1.2 if k == 0 else 0.75)
        text(f1.X(-0.72), f1.Y(yy), lab, size=5.1, color=INK)

    f2 = Frame(xs[0] + 1.25, GB_Y, W - 6.85, GB_H, (-0.55, 1.55), (-3.15, 2.6))
    for k, (tok, mu, lab) in enumerate([('hlth_hc', 0.42, 'HC'), ('clin_patients', -0.42, 'patients')]):
        v = rng.normal(mu, 0.85, 220)
        kde = np.histogram(v, bins=16, range=(-2.3, 2.3), density=True)[0]
        yy = np.linspace(-2.3, 2.3, 16)
        left = [(f2.X(k - d * 0.30), f2.Y(y)) for d, y in zip(kde, yy)]
        right = [(f2.X(k + d * 0.30), f2.Y(y)) for d, y in zip(kde[::-1], yy[::-1])]
        poly(left + right, fill=PAL[tok], line_=SOFT, lw=0.4, z=3)
        line(f2.X(k - 0.16), f2.Y(mu), f2.X(k + 0.16), f2.Y(mu), color='#FFFFFF', lw=0.9, z=4)
        text(f2.X(k), f2.Y(-2.70), lab, size=5.1, ha='center')
    text(f2.X(-0.50), f2.Y(2.45), 'NP factor', size=5.2, va='top')
    text(xs[0] + W - 5.0, GB_Y + GB_H * 0.52, 'g = 0.34\nP = 0.0013', size=5.1, color=INK, ls=1.35, z=3)

    # ---- 2 | voxel model, E/I unit, scale ladder --------------------------
    f3 = Frame(xs[1] + 1.25, GA_Y + 7.4, W - 2.5, GA_H - 7.4, (0, 2.30), (0, 1.0))
    oval(f3.X(0.40), f3.Y(0.62), f3.W(0.33), f3.H(0.31), fill='#F0EEEA', line=None, lw=0, z=2)
    for gx in np.arange(0.12, 0.70, 0.066):
        line(f3.X(gx), f3.Y(0.35), f3.X(gx), f3.Y(0.89), color='#D4D0CA', lw=0.22, z=3)
    for gy in np.arange(0.36, 0.90, 0.066):
        line(f3.X(0.10), f3.Y(gy), f3.X(0.70), f3.Y(gy), color='#D4D0CA', lw=0.22, z=3)
    oval(f3.X(0.40), f3.Y(0.62), f3.W(0.33), f3.H(0.31), fill=None, line=SOFT, lw=0.65, z=4)
    text(f3.X(0.40), f3.Y(0.19), 'SC + FC +\ntask BOLD', size=5.1, ha='center', ls=1.3)
    line(f3.X(0.80), f3.Y(0.62), f3.X(0.99), f3.Y(0.62), color='#B4B1AC', lw=0.85, arrow=True)
    for tok, lab, xx in [('exc_ampa', 'E', 1.26), ('inh_gaba', 'I', 1.78)]:
        oval(f3.X(xx), f3.Y(0.64), 0.62, 0.62 * FIG_W / FIG_H, fill=PAL[tok], line=SOFT, lw=0.45, z=4)
        text(f3.X(xx), f3.Y(0.64), lab, size=5.4, color='#FFFFFF', bold=True, ha='center', z=5)
    arc(f3.X(1.385), f3.Y(0.72), f3.X(1.655), f3.Y(0.72), rad=0.22, color=PAL['exc_ampa'], lw=0.65, n=16, z=4)
    arc(f3.X(1.655), f3.Y(0.56), f3.X(1.385), f3.Y(0.56), rad=0.22, color=PAL['inh_midazolam'], lw=0.65, n=16, z=4)
    text(f3.X(1.52), f3.Y(0.19), 'LIF E / I units\nAMPA \u00b7 GABA-A', size=5.1, ha='center', ls=1.3)

    f4 = Frame(xs[1] + 1.25, GB_Y - 1.0, W - 7.15, GB_H + 6.0, (-0.52, 4.45), (-0.75, 3.05))
    LAD = [('3M', 'scale_3m', 0.62), ('10M', 'scale_10m', 1.02), ('100M', 'scale_100m', 1.52),
           ('1B', 'scale_1b', 2.20), ('5B', 'scale_5b', 2.48)]
    for k, (lab, tok, hh) in enumerate(LAD):
        rect(f4.X(k * 0.84), f4.Y(0.0), f4.W(0.60), f4.H(hh), fill=PAL[tok], line=SOFT, lw=0.35, z=3)
        text(f4.X(k * 0.84 + 0.30), f4.Y(0.10), lab, size=4.7, rot=90, ha='left', va='center',
             color='#FFFFFF' if tok in ('scale_1b', 'scale_5b', 'scale_100m') else '#3A3A3A', z=5)
    line(f4.X(-0.10), f4.Y(0.0), f4.X(4.30), f4.Y(0.0), color=FAINT, lw=0.5)
    text(f4.X(-0.40), f4.Y(1.5), 'fidelity', size=5.1, rot=90, ha='center')
    for lab, k, yy in [('population\ninference', 0, 0.62), ('grid search', 2, 1.52),
                       ('individual\nreference', 3, 2.20)]:
        line(f4.X(k * 0.84 + 0.62), f4.Y(yy), xs[1] + W - 5.9, f4.Y(yy), color=FAINT, lw=0.4)
        text(xs[1] + W - 5.75, f4.Y(yy), lab, size=4.9, color=INK, ls=1.3, z=3)

    # ---- 3 | bidirectional individual response ----------------------------
    f5 = Frame(xs[2] + 1.25, GA_Y, W - 2.5, GA_H, (-0.50, 2.95), (-1.75, 2.05))
    rect(f5.X(-0.40), f5.Y(0.55), f5.W(3.30), f5.H(0.62), fill=PAL['hlth_norm'], line=None, lw=0, z=1)
    text(f5.X(2.86), f5.Y(0.86), 'control band', size=4.9, color='#54703F', ha='right', z=3)
    line(f5.X(-0.38), f5.Y(-1.45), f5.X(-0.38), f5.Y(1.75), color=FAINT, lw=0.55)
    text(f5.X(-0.56), f5.Y(0.15), 'NP factor', size=5.2, rot=90, ha='center')
    ORI = (0.16, -0.80)
    for xx, tok, lab, col in [(1.10, 'exc_ampa', 'AMPA \u2191', '#C2431C'),
                              (2.45, 'inh_gaba', 'GABA-A \u2191', '#1C7F9B')]:
        for _ in range(9):
            line(f5.X(ORI[0]), f5.Y(ORI[1]), f5.X(xx + rng.normal(0, 0.05)),
                 f5.Y(0.86 + rng.normal(0, 0.16)), color=PAL[tok], lw=0.5, arrow=True, z=4)
        for _ in range(3):
            line(f5.X(ORI[0]), f5.Y(ORI[1]), f5.X(xx + rng.normal(0, 0.05)),
                 f5.Y(-1.32 + rng.normal(0, 0.10)), color=PAL[tok], lw=0.5, dash='dot', arrow=True, z=4)
        text(f5.X(xx - 0.22), f5.Y(1.92), lab, size=5.2, color=col, bold=True, ha='center')
    oval(f5.X(ORI[0]), f5.Y(ORI[1]), 0.52, 0.52 * FIG_W / FIG_H,
         fill=PAL['unp_baseline'], line='#FFFFFF', lw=0.5, z=6)
    text(f5.X(ORI[0]), f5.Y(-1.12), 'baseline', size=5.0, ha='center', va='top')
    text(f5.X(1.30), f5.Y(-1.68), '9 / 12 up  \u00b7  3 / 12 down', size=5.0, ha='center')

    f6 = Frame(xs[2] + 1.25, GB_Y, W - 2.5, GB_H, (-0.30, 2.95), (-1.75, 1.75))
    rect(f6.X(2.02), f6.Y(-0.30), f6.W(0.64), f6.H(0.62), fill=PAL['hlth_norm'], line=None, lw=0, z=1)
    for k, (tok, mu) in enumerate([('hlth_hc', 0.58), ('clin_highsymp', 0.0), ('clin_patients', -0.62)]):
        line(f6.X(0.32), f6.Y(mu - 0.32), f6.X(0.32), f6.Y(mu + 0.32), color=PAL[tok], lw=1.0, z=3)
        oval(f6.X(0.32), f6.Y(mu), 0.28, 0.28 * FIG_W / FIG_H, fill=PAL[tok], line=SOFT, lw=0.3, z=4)
        oval(f6.X(2.34), f6.Y(0.02 + (k - 1) * 0.07), 0.28, 0.28 * FIG_W / FIG_H,
             fill=PAL[tok], line=SOFT, lw=0.3, z=4)
    line(f6.X(0.84), f6.Y(0.0), f6.X(1.82), f6.Y(0.0), color='#B4B1AC', lw=0.85, arrow=True)
    text(f6.X(1.33), f6.Y(0.34), 'perturbation', size=4.9, ha='center')
    text(f6.X(0.32), f6.Y(-1.18), 'baseline', size=4.9, ha='center')
    text(f6.X(2.34), f6.Y(-1.18), 'after', size=4.9, ha='center')
    text(f6.X(1.33), f6.Y(-1.66), 'group difference abolished, n = 288', size=5.0, color=INK, ha='center')

    # ---- 4 | drug datasets, box plots only --------------------------------
    f7 = Frame(xs[3] + 2.9, GA_Y + 1.6, W - 4.4, GA_H - 1.6, (-0.55, 1.55), (-1.75, 1.95))
    line(f7.X(-0.48), f7.Y(0.0), f7.X(1.52), f7.Y(0.0), color='#C9C6C1', lw=0.5, dash='dash')
    line(f7.X(-0.48), f7.Y(-1.25), f7.X(-0.48), f7.Y(1.25), color=FAINT, lw=0.55)
    text(f7.X(-0.78), f7.Y(0.0), '\u0394 NP  (drug \u2212 placebo)', size=5.0, rot=90, ha='center')
    boxplot(f7, 0.10, rng.normal(0.46, 0.34, 27), PAL['exc_ketamine'], rng=rng)
    boxplot(f7, 1.00, rng.normal(-0.44, 0.32, 27), PAL['inh_midazolam'], rng=rng)
    text(f7.X(0.10), f7.Y(-1.36), 'ketamine', size=5.0, ha='center')
    text(f7.X(1.00), f7.Y(-1.36), 'midazolam', size=5.0, ha='center')
    text(f7.X(0.55), f7.Y(1.86), 'crossover, n = 27', size=5.0, color=INK, ha='center')
    text(f7.X(0.55), f7.Y(-1.70), 'r = 0.35 / 0.52 \u00b7 AUC 0.69 / 0.83', size=4.9, ha='center')

    f8 = Frame(xs[3] + 2.9, GB_Y - 0.8, W - 4.4, GB_H + 0.8, (-0.55, 1.55), (-1.95, 1.95))
    line(f8.X(-0.48), f8.Y(0.0), f8.X(1.52), f8.Y(0.0), color='#C9C6C1', lw=0.5, dash='dash')
    line(f8.X(-0.48), f8.Y(-1.10), f8.X(-0.48), f8.Y(1.10), color=FAINT, lw=0.55)
    text(f8.X(-0.78), f8.Y(0.0), '\u0394 NP  (ketamine)', size=5.0, rot=90, ha='center')
    boxplot(f8, 0.10, rng.normal(0.44, 0.30, 22), PAL['clin_mdd'], rng=rng, ptsize=0.26)
    boxplot(f8, 1.00, rng.normal(-0.38, 0.28, 14), PAL['hlth_hc'], rng=rng, ptsize=0.26)
    text(f8.X(0.10), f8.Y(-1.24), 'MDD 22', size=5.0, ha='center')
    text(f8.X(1.00), f8.Y(-1.24), 'HC 14', size=5.0, ha='center')
    text(f8.X(0.55), f8.Y(1.84), 'clinical cohort', size=5.0, color=INK, ha='center')
    text(f8.X(0.55), f8.Y(-1.80), 'group \u00d7 drug  t = 3.43, P = 0.002', size=4.9, ha='center')

    # ---- 5 | prospective prediction ---------------------------------------
    f9 = Frame(xs[4] + 4.0, GB_Y + 1.2, W - 5.4, GA_Y + GA_H - GB_Y - 1.2, (-0.05, 1.05), (-0.05, 1.05))
    line(f9.X(-0.05), f9.Y(-0.05), f9.X(-0.05), f9.Y(1.05), color=FAINT, lw=0.5)
    line(f9.X(-0.05), f9.Y(-0.05), f9.X(1.05), f9.Y(-0.05), color=FAINT, lw=0.5)
    line(f9.X(0), f9.Y(0), f9.X(1), f9.Y(1), color='#C9C6C1', lw=0.5, dash='dash')
    for tok, off in [('exc_restore', 0.02), ('inh_restore', -0.05)]:
        xx = rng.uniform(0.05, 0.96, 42); yy = 0.10 + off + 0.78 * xx + rng.normal(0, 0.105, 42)
        for a_, b_ in zip(xx, yy):
            oval(f9.X(a_), f9.Y(b_), 0.30, 0.30 * FIG_W / FIG_H, fill=PAL[tok], line='#8A8A8A', lw=0.22, z=4)
        line(f9.X(0.03), f9.Y(0.10 + off + 0.78 * 0.03), f9.X(0.97), f9.Y(0.10 + off + 0.78 * 0.97),
             color=PAL[tok], lw=1.0, z=5)
    text(f9.X(0.5), f9.Y(-0.15), 'restoration index (model)', size=5.0, ha='center')
    text(f9.X(-0.19), f9.Y(0.5), 'observed \u0394 symptoms, 19 \u2192 23', size=5.0, rot=90, ha='center')
    for tok, lab, yy in [('exc_restore', 'AMPA index', 0.20), ('inh_restore', 'GABA-A index', 0.10)]:
        line(f9.X(0.56), f9.Y(yy), f9.X(0.68), f9.Y(yy), color=PAL[tok], lw=1.0, z=6)
        text(f9.X(0.71), f9.Y(yy), lab, size=4.9, color=INK, z=6)

    # ---- cross-stage reuse arcs -------------------------------------------
    arc(xs[0] + W * 0.50, BOX_Y + BOX_H + 0.4, xs[4] + W * 0.50, BOX_Y + BOX_H + 0.4,
        rad=0.12, color=PAL['circ_np12'], lw=0.85, n=60)
    text(50.0, 88.6, 'NP \u2192 symptom map fitted once at age 19, then reused',
         size=5.4, color=PAL['circ_np12'], ha='center')
    arc(xs[2] + W * 0.50, BOX_Y - 0.4, xs[3] + W * 0.50, BOX_Y - 0.4,
        rad=-0.45, color=PAL['exc_ketamine'], lw=0.85, n=40)
    text((xs[2] + xs[3]) / 2 + W * 0.50, 15.4,
         'perturbation \u2192 response mapping, applied to empirical data without refitting',
         size=5.4, color=PAL['exc_ketamine'], ha='center')

    # ---- footer -----------------------------------------------------------
    text(2.0, 8.6, 'Colour correspondence', size=6.0, color=INK, bold=True)
    px = 2.0
    for tokA, tokB, lab in [('exc_ampa', 'exc_ketamine', 'virtual AMPA \u2194 ketamine'),
                            ('inh_gaba', 'inh_midazolam', 'virtual GABA-A \u2194 midazolam'),
                            ('unp_baseline', 'unp_placebo', 'baseline \u2194 placebo')]:
        rect(px, 4.1, 1.45, 1.75, fill=PAL[tokA], line='#9A9A9A', lw=0.3)
        rect(px + 1.65, 4.1, 1.45, 1.75, fill=PAL[tokB], line='#9A9A9A', lw=0.3)
        text(px + 3.4, 4.98, lab, size=5.3)
        px += 22.5
    rect(2.0, 0.9, 1.45, 1.75, fill=PAL['exc_ampa'], line='#9A9A9A', lw=0.3)
    rect(3.65, 0.9, 1.45, 1.75, fill='#FFFFFF', line=PAL['exc_ampa'], lw=0.85)
    text(5.4, 1.78, 'solid = DTB-simulated  \u2194  open = empirical', size=5.3)
    nseg = 64
    cm = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in FC2]) / 255
    tt = np.linspace(0, 1, nseg)
    src = np.linspace(0, 1, len(FC2))
    grad = np.stack([np.interp(tt, src, cm[:, j]) for j in range(3)], 1)
    for j in range(nseg):
        rect(70.0 + j * (15.5 / nseg), 0.98, 15.5 / nseg + 0.02, 1.55,
             fill='#%02X%02X%02X' % tuple((grad[j] * 255).round().astype(int)), line=None, lw=0)
    rect(70.0, 0.98, 15.5, 1.55, fill=None, line='#9A9A9A', lw=0.4)
    text(70.0, 4.6, 'FC / \u0394FC, 0-centred', size=5.3)
    text(69.2, 1.78, 'lower', size=5.0, ha='right')
    text(86.3, 1.78, 'higher', size=5.0, ha='left')
    return S
