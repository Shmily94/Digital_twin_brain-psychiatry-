"""Fig. 1 - analysis flow diagram (structural draft).

A schematic only: every number in it is a cohort size or a design fact taken
from the corresponding data table, not a computed result.
"""
import os, sys
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, panel, C, LW
apply_np_style()

STAGES = [
    dict(no='1', title='Derive the\ncircuit',
         data=['IMAGEN baseline\n$n$ = 1,050', 'STRATIFY validation\n$n$ = 427'],
         method='Task FC (SST, MID, EFT)\n217 nodes \u00b7 23,436 edges\nCPM edge selection',
         out='Negative profile 29 edges\nPositive profile 34 edges\n'
             '$\\bf{NP\\ factor}$ = 12 cortico-\nsubcortical edges',
         fig='Fig. 2\nSupp. STRATIFY, PET maps', col='np12'),
    dict(no='2', title='Build the\ndigital twins',
         data=['12 participants\nSC + task BOLD'],
         method='Data assimilation\n7 builds \u00d7 (neurons,\nhyper-parameters, resolution)\n+ SAR, rWW benchmarks',
         out='1 B  \u2192 fidelity reference\n100 M \u2192 parameter search\n3 M / 268 \u2192 population runs',
         fig='Fig. 3\nSupp. assimilation region', col='model_voxel'),
    dict(no='3', title='Perturb\nin silico',
         data=['Population twins $n$ = 288\nHC 69 \u00b7 high-symptom 89\npatient 130'],
         method='Conductance grid search\non 100 M, then applied\nat 3 M / 268:\nAMPA \u2191, then GABA-A \u2191',
         out='Per-participant \u0394NP\nResponse pattern\n(both-up vs any-down)',
         fig='Fig. 4\nSupp. conductance grid', col='ampa'),
    dict(no='4', title='Validate\nagainst drugs',
         data=['Healthy crossover $n$ = 27\nplacebo / ketamine /\nmidazolam',
               'Clinical ketamine $n$ = 36\nMDD 22 \u00b7 HC 14'],
         method='6 NP-related MID edges\nand whole-brain maps;\ndirectional concordance,\nno refitting',
         out='Drug direction vs\nvirtual perturbation\nRelated to symptom change',
         fig='Fig. 5a\u2013g\nSupp. paired MID,\nwhole-brain drug, Oldham', col='midazolam'),
    dict(no='5', title='Forecast\nsymptom change',
         data=['IMAGEN follow-up\n$n$ = 85, age 19 \u2192 23'],
         method='Nested regression,\npermutation null,\n10-fold cross-validation',
         out='AMPA index adds variance\nover baseline behaviour\nand baseline connectivity',
         fig='Fig. 5h\nSupp. longitudinal', col='high_symptom'),
]

W, H = 186, 136
fig, ax = plt.subplots(figsize=panel(W, H))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

x0, gap = 4.0, 2.6
bw = (W - 2 * x0 - gap * (len(STAGES) - 1)) / len(STAGES)
ROWS = [('data', 91.0, 17.0), ('method', 68.0, 20.0), ('out', 43.0, 21.0), ('fig', 24.0, 13.0)]


def box(x, y, w, h, fc, ec, lw=LW, r=1.2, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))


for k, s in enumerate(STAGES):
    x = x0 + k * (bw + gap)
    col = C(s['col'])
    # header
    box(x, 110, bw, 13, col, 'none', z=2)
    hcol = 'white' if s['col'] in ('np12', 'model_voxel') else '0.12'
    ax.text(x + 2.4, 121.0, s['no'], ha='center', va='center', fontsize=8,
            fontweight='bold', color=hcol)
    ax.text(x + bw / 2 + 1.2, 116.5, s['title'], ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=hcol, linespacing=1.15)
    # data
    y, h = ROWS[0][1], ROWS[0][2]
    sub = h / len(s['data'])
    for j, d in enumerate(s['data']):
        box(x, y + (len(s['data']) - 1 - j) * sub, bw, sub - .8, '#F2F2F2', '0.55')
        ax.text(x + bw / 2, y + (len(s['data']) - 1 - j) * sub + (sub - .8) / 2, d,
                ha='center', va='center', fontsize=6, color='0.15', linespacing=1.25)
    # method
    box(x, ROWS[1][1], bw, ROWS[1][2], 'white', '0.55')
    ax.text(x + bw / 2, ROWS[1][1] + ROWS[1][2] / 2, s['method'], ha='center', va='center',
            fontsize=6, color='0.15', linespacing=1.3)
    # output
    box(x, ROWS[2][1], bw, ROWS[2][2], tuple(1 - .18 * (1 - np.array(plt.matplotlib.colors.to_rgb(col)))), col)
    ax.text(x + bw / 2, ROWS[2][1] + ROWS[2][2] / 2, s['out'], ha='center', va='center',
            fontsize=6, color='0.12', linespacing=1.3)
    # figure tag
    ax.text(x + bw / 2, ROWS[3][1] + ROWS[3][2] / 2, s['fig'], ha='center', va='center',
            fontsize=5.6, style='italic', color='0.35', linespacing=1.35)
    if k:
        ax.add_patch(FancyArrowPatch((x - gap + .3, 76), (x - .3, 76),
                                     arrowstyle='-|>', mutation_scale=7, lw=LW, color='0.45', zorder=1))

# row labels
for lab, (_, y, h) in zip(['Data', 'Method', 'Output', 'Figures'], ROWS):
    ax.text(1.4, y + h / 2, lab, ha='center', va='center', fontsize=6.5, rotation=90,
            color='0.45', fontweight='bold')

# feedback arrows
ax.annotate('', xy=(x0 + 3 * (bw + gap) + bw / 2, 20), xytext=(x0 + 2 * (bw + gap) + bw / 2, 20),
            arrowprops=dict(arrowstyle='-|>', color=C('ampa'), lw=LW * 1.4,
                            connectionstyle='arc3,rad=-0.28', mutation_scale=7))
ax.text((x0 + 2.5 * (bw + gap) + bw / 2), 13.0,
        'perturbation \u2192 response mapping applied to empirical data without refitting',
        ha='center', va='center', fontsize=6, color=C('ampa'))
ax.annotate('', xy=(x0 + 2 * (bw + gap) + bw / 2, 124.5), xytext=(x0 + (bw + gap) + bw / 2, 124.5),
            arrowprops=dict(arrowstyle='-|>', color=C('model_voxel'), lw=LW * 1.4,
                            connectionstyle='arc3,rad=-0.25', mutation_scale=7))
ax.text(x0 + 1.5 * (bw + gap) + bw / 2, 132.0, 'build choice fixes which inference is admissible',
        ha='center', va='center', fontsize=6, color=C('model_voxel'))

fig.savefig(os.path.join(HERE, 'fig1_flow_draft.png'), dpi=400, bbox_inches='tight')
fig.savefig(os.path.join(HERE, 'fig1_flow_draft.pdf'), bbox_inches='tight')
print('done')
