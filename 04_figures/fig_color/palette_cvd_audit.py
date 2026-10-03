"""Colour-vision / greyscale audit of the manuscript palette.

Renders every registered colour under normal, deuteranope and protanope
simulation (Machado et al. 2009, severity 1.0) and in luminance-only form,
and scores the pairs that share a figure.  Writes palette_cvd_audit.png/.pdf
and palette_cvd_distances.csv next to this script.
"""
import sys, itertools, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, '/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig_color')
from np_dtb_style import apply_np_style, panel, LABEL_PT, ANNOT_PT, TICK_PT, LW, enforce
apply_np_style()
HERE = '/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig_color'

# ---- colour science --------------------------------------------------------
M_RGB2XYZ = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]])
WP = np.array([.95047, 1.0, 1.08883])
DEU = np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413],
                [-0.011820, 0.042940, 0.968881]])
PRO = np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216],
                [-0.003882, -0.048116, 1.051998]])

def _lin(c):  return np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)
def lab(h):
    x = M_RGB2XYZ @ _lin(np.array(matplotlib.colors.to_rgb(h))) / WP
    f = np.where(x > 0.008856, np.cbrt(x), 7.787 * x + 16 / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])
def dE(a, b):    return float(np.linalg.norm(lab(a) - lab(b)))
def cvd(h, Mx):  return matplotlib.colors.to_hex(np.clip(Mx @ np.array(matplotlib.colors.to_rgb(h)), 0, 1))
def grey(h):
    y = float(_lin(np.array(matplotlib.colors.to_rgb(h))) @ M_RGB2XYZ[1])
    v = 1.055 * y ** (1 / 2.4) - .055 if y > .0031308 else 12.92 * y
    return matplotlib.colors.to_hex((v, v, v))
VIEWS = [('Normal', lambda h: h), ('Deuteranopia', lambda h: cvd(h, DEU)),
         ('Protanopia', lambda h: cvd(h, PRO)), ('Greyscale', grey)]

# ---- what is registered, and where it is used ------------------------------
ENTRIES = [
    ('HC / placebo / baseline / reference', '#7F7F7F', 'Fig 2-5'),
    ('High-symptom',                        '#E69F00', 'Fig 2, 4'),
    ('Patient / MDD / AUD',                 '#D55E00', 'Fig 2, 4, 5'),
    ('AMPA / ketamine',                     '#E1D09A', 'Fig 3-5'),
    ('GABA-A / midazolam',                  '#96B9AD', 'Fig 3-5'),
    ('Response: increased  (former)', '#D9A5B3', 'replaced'),
    ('Response: decreased  (former)', '#8DA0B4', 'replaced'),
    ('NP factor, 12 edges',                 '#0072B2', 'Fig 2, 3'),
    ('Negative profile, 29 edges',          '#6BAED6', 'Fig 2'),
    ('Positive profile, 34 edges',          '#C878A0', 'Fig 2'),
    ('Non-NP edges',                        '#BFBFBF', 'Fig 2'),
    ('Model family: regional',              '#8E7CC3', 'Fig 3'),
    ('Model family: voxel',                 '#4C3F8C', 'Fig 3'),
    ('Response: increased  (in use)', '#8C4A6B', 'Fig 4f-g, 5b-c'),
    ('Response: decreased  (in use)', '#E8C4D2', 'Fig 4f-g, 5b-c'),
]

# ---- pairwise table --------------------------------------------------------
rows = []
for (n1, h1, _), (n2, h2, _) in itertools.combinations(ENTRIES, 2):
    d = {v: dE(f(h1), f(h2)) for v, f in VIEWS}
    rows.append(dict(colour_1=n1, hex_1=h1, colour_2=n2, hex_2=h2,
                     **{f'dE_{k.lower()}': round(v, 1) for k, v in d.items()},
                     dE_worst_case_colour_vision=round(min(
                         d['Normal'], d['Deuteranopia'], d['Protanopia']), 1)))
D = pd.DataFrame(rows).sort_values('dE_worst_case_colour_vision').reset_index(drop=True)
D.to_csv(f'{HERE}/palette_cvd_distances.csv', index=False)

# pairs that must stay distinguishable because they appear in the same panel
CRIT = [('Response: increased  (former)', 'Response: decreased  (former)'),
        ('Response: increased  (in use)', 'Response: decreased  (in use)'),
        ('AMPA / ketamine', 'GABA-A / midazolam'),
        ('HC / placebo / baseline / reference', 'GABA-A / midazolam'),
        ('High-symptom', 'Patient / MDD / AUD'),
        ('HC / placebo / baseline / reference', 'Patient / MDD / AUD')]
HEX = {n: h for n, h, _ in ENTRIES}

# ---- figure ----------------------------------------------------------------
W, H = 178, 132
fig = plt.figure(figsize=panel(W, H))
gs = fig.add_gridspec(2, 1, height_ratios=[15, 8.2], hspace=.10,
                      left=.235, right=.985, top=.955, bottom=.045)

# top: every registered colour under four views
ax = fig.add_subplot(gs[0]); ax.set_axis_off()
n = len(ENTRIES)
for r, (name, hx, use) in enumerate(ENTRIES):
    y = n - 1 - r
    ax.text(-.012, y + .5, name, ha='right', va='center', fontsize=TICK_PT,
            color='0.55' if 'former' in name else 'black')
    for c, (vname, f) in enumerate(VIEWS):
        ax.add_patch(Rectangle((c * 1.06, y + .12), 1.0, .76, facecolor=f(hx),
                               edgecolor='black', lw=LW * .7))
    live = {n for n, _, u in ENTRIES if u != 'replaced'} - {name}
    worst = D.loc[((D.colour_1 == name) & D.colour_2.isin(live)) |
                  ((D.colour_2 == name) & D.colour_1.isin(live)),
                  'dE_worst_case_colour_vision'].min()
    ax.text(4 * 1.06 + .10, y + .5, f'{hx}   nearest other colour: ΔE = {worst:.0f}',
            ha='left', va='center', fontsize=TICK_PT, color='0.35')
for c, (vname, _) in enumerate(VIEWS):
    ax.text(c * 1.06 + .5, n + .08, vname, ha='center', va='bottom', fontsize=ANNOT_PT)
ax.set_xlim(-.02, 4 * 1.06 + 2.6); ax.set_ylim(0, n + .62)
ax.text(-.012, n + .08, 'Registered colour', ha='right', va='bottom', fontsize=ANNOT_PT)

# bottom: the pairs that share a panel
ax2 = fig.add_subplot(gs[1]); ax2.set_axis_off()
m = len(CRIT)
for r, (n1, n2) in enumerate(CRIT):
    y = m - 1 - r
    lab_ = f'{n1.split("  ")[0]}  vs  {n2.split("  ")[0]}'
    if 'former' in n1: lab_ += '  (former)'
    if 'in use' in n1: lab_ += '  (in use)'
    ax2.text(-.012, y + .70, lab_, ha='right', va='center', fontsize=TICK_PT)
    for c, (vname, f) in enumerate(VIEWS):
        ax2.add_patch(Rectangle((c * 1.06, y + .44), .48, .52, facecolor=f(HEX[n1]),
                                edgecolor='black', lw=LW * .7))
        ax2.add_patch(Rectangle((c * 1.06 + .50, y + .44), .48, .52, facecolor=f(HEX[n2]),
                                edgecolor='black', lw=LW * .7))
        d = dE(f(HEX[n1]), f(HEX[n2]))
        ax2.text(c * 1.06 + .49, y + .36, f'ΔE {d:.0f}', ha='center', va='top',
                 fontsize=TICK_PT, color='#B2182B' if d < 15 else '0.35')
for c, (vname, _) in enumerate(VIEWS):
    ax2.text(c * 1.06 + .49, m + .10, vname, ha='center', va='bottom', fontsize=ANNOT_PT)
ax2.text(-.012, m + .10, 'Pair sharing one panel', ha='right', va='bottom', fontsize=ANNOT_PT)
ax2.text(4 * 1.06 + .10, m / 2 + .3, 'ΔE < 15 (red) = not reliably\nseparable at a glance.\n'
         'Greyscale is reported for\ninformation only; the journal\nprints in colour.',
         ha='left', va='center', fontsize=TICK_PT, color='0.35')
ax2.set_xlim(-.02, 4 * 1.06 + 2.6); ax2.set_ylim(.05, m + .70)

enforce(fig)
fig.savefig(f'{HERE}/palette_cvd_audit.png', dpi=400)
fig.savefig(f'{HERE}/palette_cvd_audit.pdf')
print(D.head(8).to_string(index=False))
