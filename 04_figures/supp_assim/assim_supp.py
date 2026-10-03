"""Supplementary figure | assimilation stability across five independent runs.

Five independent HMDA assimilation runs (ensemble Kalman filter, 30 parallel
realisations) on the reward-task (MID) BOLD of one representative healthy
control at 100-million-neuron resolution.  Each run repeated assimilation and
forward simulation from scratch, so the spread includes EnKF and
Ornstein-Uhlenbeck forward-noise contributions.  Only the six reward-task NP
edges are covered: the repeats were run on MID, not SST.

    cd revision/text/figures/supp_assim && python assim_supp.py
"""
import os, sys, itertools
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from supp_kit import saver, pt_edge
apply_np_style()
D, OUTD = f'{HERE}/data', f'{HERE}/panels'
E = pd.read_csv(f'{D}/assim5_edges_mid.csv')
S = pd.read_csv(f'{D}/assim5_stats.csv').set_index('statistic')['value']
RUNS = ['run1', 'run2', 'run3', 'run4', 'run5']
R = E[RUNS].values
manifest = []
save = saver(OUTD, manifest)
COL = C('np12')                      # these are NP-factor edges

# ---- a  every run, every edge -----------------------------------------------
W, H = 74, 52
fig, ax = plt.subplots(figsize=panel(W, H))
x = np.arange(len(E))
ax.bar(x, E['mean'], width=.62, facecolor='0.92', edgecolor='black', linewidth=LW,
       zorder=2, label='across-run mean')
rng = np.random.default_rng(0)
for j, r in enumerate(RUNS):
    ax.scatter(x + rng.uniform(-.17, .17, len(E)), E[r], s=13, facecolor=COL,
               edgecolor='none', alpha=.85, zorder=3)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_xticks(x)
ax.set_xticklabels([f'{e.replace("edge", "e")}\n{p}' for e, p in
                    zip(E.edge, E.pair_217space)], fontsize=TICK_PT)
ax.set_ylabel('Simulated FC')
ax.scatter([], [], s=13, facecolor=COL, edgecolor='none', label='individual run (5)')
ax.legend(loc='upper left', fontsize=ANNOT_PT, frameon=False, borderaxespad=.2,
          handletextpad=.5, labelspacing=.25)
_l, _h = ax.get_ylim(); ax.set_ylim(_l, _h + (_h - _l) * .18)
panel_title(ax, 'Five independent assimilation runs, six reward-task NP edges')
enforce(fig); save(fig, 'figS_assim_a', W, H, 'assim5_edges_mid.csv')

# ---- b  all run pairs against each other ------------------------------------
W, H = 52, 52
fig, ax = plt.subplots(figsize=panel(W, H))
lo, hi = R.min(), R.max(); pad = (hi - lo) * .10
ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color='0.6', lw=LW,
        ls=(0, (2.6, 1.7)), zorder=1)
for i, j in itertools.combinations(range(len(RUNS)), 2):
    ax.scatter(R[:, i], R[:, j], s=13, facecolor=COL, edgecolor='none', alpha=.7,
               zorder=3)
ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(lo - pad, hi + pad)
ax.set_xlabel('Run $i$ (simulated FC)'); ax.set_ylabel('Run $j$ (simulated FC)')
ax.text(.03, .97, f'ICC(3,1) = {S["ICC(3,1), runs fixed"]:.3f}\n'
        f'profile $r$ = {S["mean between-run profile r"]:.3f} '
        f'({S["min between-run profile r"]:.3f}–{S["max between-run profile r"]:.3f})\n'
        f'10 run pairs × 6 edges', transform=ax.transAxes, ha='left', va='top',
        fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Runs agree edge by edge')
enforce(fig); save(fig, 'figS_assim_b', W, H, 'assim5_edges_mid.csv')

# ---- c  biological spread vs run-to-run spread ------------------------------
W, H = 46, 52
fig, ax = plt.subplots(figsize=panel(W, H))
sig, noi = float(S['SD between edges (signal)']), E['sd'].values
ax.bar([0], [sig], width=.55, facecolor='0.92', edgecolor='black', linewidth=LW, zorder=2)
ax.bar([1], [noi.mean()], width=.55, facecolor='0.92', edgecolor='black',
       linewidth=LW, zorder=2)
rng = np.random.default_rng(1)
ax.scatter(1 + rng.uniform(-.14, .14, len(noi)), noi, s=13, facecolor=COL,
           edgecolor='none', alpha=.85, zorder=3)
ax.set_yscale('log')
ax.set_xticks([0, 1]); ax.set_xticklabels(['between\nedges', 'between\nruns'],
                                          fontsize=TICK_PT)
ax.set_xlim(-.6, 1.6)
ax.set_ylabel('SD of simulated FC (log scale)')
ax.text(.5, .97, f'{S["signal/noise SD ratio"]:.1f}× in SD\n'
        f'({S["signal/noise SD ratio"]**2:.0f}× in variance)', transform=ax.transAxes,
        ha='center', va='top', fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Signal exceeds run noise')
enforce(fig); save(fig, 'figS_assim_c', W, H, 'assim5_edges_mid.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/assim_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
