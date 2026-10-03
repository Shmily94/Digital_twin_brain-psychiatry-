"""Supplementary figure | bidirectional perturbation response in the EFT task.

Three digital twins (HC01, MDD, AUD) built from the emotional face-evaluation
task (EFT) and perturbed at the same conductances used in the main analysis
(AMPA 0.0044, GABA-A 0.0040 S/cm2).  Panel b shows the same three twins on the
12-edge NP profile of the reward/inhibition tasks, so the EFT result can be read
against the response those twins show in the main analysis.  HC02 is excluded
here for the same reason as in the model sweeps.

    cd revision/text/figures/supp_eft && python eft_supp.py
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from supp_kit import saver, pt_edge
apply_np_style()
D, OUTD = f'{HERE}/data', f'{HERE}/panels'
E = pd.read_csv(f'{D}/eft_3subs.csv')
N = pd.read_csv(f'{D}/np_task_3subs.csv')
manifest = []
save = saver(OUTD, manifest)
SUBS = ['HC01', 'MDD', 'AUD']
MRK = {'HC01': 'o', 'MDD': 's', 'AUD': '^'}
PCOL = {'AMPA': C('ampa'), 'GABA-A': C('gaba')}


def paired(T, stem, ylab, title, note, src):
    W, H = 62, 54
    fig, ax = plt.subplots(figsize=panel(W, H))
    xpos = {'AMPA': (0, 1), 'GABA-A': (2.3, 3.3)}
    for pert in ['AMPA', 'GABA-A']:
        x0, x1 = xpos[pert]
        for s in SUBS:
            r = T[(T.perturbation == pert) & (T.subject == s)].iloc[0]
            ax.plot([x0, x1], [r.baseline, r.perturbed], color=PCOL[pert],
                    lw=LW * 1.4, zorder=2, solid_capstyle='round')
            for xx, yy, fc in [(x0, r.baseline, 'white'), (x1, r.perturbed, PCOL[pert])]:
                ax.scatter([xx], [yy], s=26, marker=MRK[s], facecolor=fc,
                           edgecolor=PCOL[pert] if fc == 'white' else pt_edge(PCOL[pert]),
                           linewidth=LW, zorder=3)
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.set_xticks([0, 1, 2.3, 3.3])
    ax.set_xticklabels(['base-\nline', 'AMPA', 'base-\nline', 'GABA-A'], fontsize=TICK_PT)
    ax.set_xlim(-.55, 3.85)
    ax.set_ylabel(ylab)
    hd = [Line2D([], [], marker=MRK[s], linestyle='none', markersize=3.4,
                 markerfacecolor='0.45', markeredgecolor='none') for s in SUBS]
    ax.legend(hd, SUBS, loc='upper left', fontsize=ANNOT_PT, frameon=False,
              borderaxespad=.2, handletextpad=.4, labelspacing=.22, ncol=3,
              columnspacing=.8)
    _l, _h = ax.get_ylim(); ax.set_ylim(_l, _h + (_h - _l) * .20)
    ax.text(.97, .03, note, transform=ax.transAxes, ha='right', va='bottom',
            fontsize=ANNOT_PT, color='0.35')
    panel_title(ax, title)
    enforce(fig); save(fig, stem, W, H, src)


def dirs(T, pert):
    d = T[T.perturbation == pert]
    return f'{int((d.delta > 0).sum())} up / {int((d.delta < 0).sum())} down'


paired(E, 'figS_eft_a', 'Summed EFT NP FC',
       'Emotional face task: responses go both ways',
       f'AMPA {dirs(E, "AMPA")}\nGABA-A {dirs(E, "GABA-A")}', 'eft_3subs.csv')
paired(N, 'figS_eft_b', 'Summed NP FC (12 edges)',
       'Same twins on the reward / inhibition tasks',
       f'AMPA {dirs(N, "AMPA")}\nGABA-A {dirs(N, "GABA-A")}', 'np_task_3subs.csv')

# ---- c  change against baseline, both tasks ---------------------------------
W, H = 52, 54
fig, ax = plt.subplots(figsize=panel(W, H))
for T, mk, lab in [(E, 'o', 'EFT'), (N, 'D', 'NP task')]:
    for pert in ['AMPA', 'GABA-A']:
        d = T[T.perturbation == pert]
        ax.scatter(d.baseline, d.delta, s=24, marker=mk, facecolor=PCOL[pert],
                   edgecolor=pt_edge(PCOL[pert]), linewidth=LW * .55, zorder=3)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.axvline(0, color='0.85', lw=LW, zorder=1)
ax.set_xlabel('Baseline FC'); ax.set_ylabel('Change after perturbation')
hd = [Line2D([], [], marker='o', linestyle='none', markersize=3.4,
             markerfacecolor='0.45', markeredgecolor='none'),
      Line2D([], [], marker='D', linestyle='none', markersize=3.2,
             markerfacecolor='0.45', markeredgecolor='none'),
      Line2D([], [], marker='s', linestyle='none', markersize=3.4,
             markerfacecolor=C('ampa'), markeredgecolor='none'),
      Line2D([], [], marker='s', linestyle='none', markersize=3.4,
             markerfacecolor=C('gaba'), markeredgecolor='none')]
ax.legend(hd, ['EFT', 'NP task', 'AMPA', 'GABA-A'], loc='upper right',
          fontsize=ANNOT_PT, frameon=False, borderaxespad=.2, handletextpad=.4,
          labelspacing=.22)
_l, _h = ax.get_ylim(); ax.set_ylim(_l, _h + (_h - _l) * .22)
panel_title(ax, 'Baseline and change, three twins')
enforce(fig); save(fig, 'figS_eft_c', W, H, 'eft_3subs.csv + np_task_3subs.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/eft_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
for T, nm in [(E, 'EFT'), (N, 'NP task')]:
    for pert in ['AMPA', 'GABA-A']:
        d = T[T.perturbation == pert]
        print(f'{nm:8s} {pert:7s} ' + ', '.join(f'{r.subject} {r.delta:+.3f}'
                                                for r in d.itertuples()))
