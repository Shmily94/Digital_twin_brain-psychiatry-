"""Supplementary figure | conductance sensitivity of the perturbation results.

Each conductance knob was re-run at a weaker and a stronger setting around the
value used in the main analysis (AMPA 0.0040 / 0.0044 / 0.0048 S/cm2; GABA-A
0.0035 / 0.0040 / 0.0045 S/cm2), n = 288 twins.  Panels show the group-level
effect, the responder proportion by diagnostic group, and how many of the six
settings each twin increased under.

    cd revision/text/figures/supp_conductance && python conductance_supp.py
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from supp_kit import saver, pt_edge, fill
apply_np_style()
D, OUTD = f'{HERE}/data', f'{HERE}/panels'
G = pd.read_csv(f'{D}/conductance_grid_summary_n288.csv')
ST = pd.read_csv(f'{D}/conductance_responder_by_group_n288.csv')
IN = pd.read_csv(f'{D}/conductance_subject_level_n288.csv')
manifest = []
save = saver(OUTD, manifest)
KCOL = {'AMPA': C('ampa'), 'GABA-A': C('gaba')}
ORDER = ['weaker', 'original', 'stronger']
SET = ['ampa_low', 'ampa', 'ampa_high', 'gaba_low', 'gaba', 'gaba_high']
SETLAB = dict(zip(SET, ['0.0040', '0.0044', '0.0048', '0.0035', '0.0040', '0.0045']))
GRP = ['HC', 'High-symptom', 'Patient']
GCOL = {'HC': C('hc'), 'High-symptom': C('high_symptom'), 'Patient': C('patient')}

# ---- a  group-level mean delta NP, six settings ------------------------------
W, H = 78, 54
fig, ax = plt.subplots(figsize=panel(W, H))
x, ticks, blocks = 0.0, [], []
for knob in ['AMPA', 'GABA-A']:
    sub = G[G.knob == knob].set_index('setting').loc[ORDER]
    blockmax = float(sub.ci_hi.max())
    first = x
    for s in ORDER:
        r = sub.loc[s]
        ax.bar(x, r.mean_delta, width=.62, facecolor=fill(KCOL[knob]),
               edgecolor='black', linewidth=LW, zorder=2)
        ax.plot([x, x], [r.ci_lo, r.ci_hi], color='black', lw=LW, zorder=3)
        ax.text(x, blockmax + (.15 if ORDER.index(s) % 2 == 0 else .62),
                f'$d$ = {r.cohens_d:.2f}', ha='center', va='bottom',
                fontsize=ANNOT_PT, color='0.35')
        if s == 'original':
            ax.text(x, -.22, 'used in\nmain text', ha='center', va='top',
                    fontsize=ANNOT_PT, color=KCOL[knob])
        ticks.append((x, f'{r.conductance:.4f}')); x += 1.0
    blocks.append(((first + x - 1) / 2, knob)); x += 1.3
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_xticks([t[0] for t in ticks])
ax.set_xticklabels([t[1] for t in ticks], fontsize=TICK_PT)
ax.set_xlim(ticks[0][0] - .75, ticks[-1][0] + .75)
ax.set_ylim(-1.05, G.ci_hi.max() * 1.40)
ax.set_ylabel('Mean Δ NP (95% CI)')
tr = ax.get_xaxis_transform()
for xc, bl in blocks:
    ax.text(xc, -.175, f'{bl} (S cm$^{{-2}}$)', transform=tr, ha='center', va='top',
            fontsize=ANNOT_PT, clip_on=False)
panel_title(ax, 'Group-level increase at every setting')
enforce(fig); save(fig, 'figS_cond_a', W, H, 'conductance_grid_summary_n288.csv')

# ---- b  responder proportion by diagnostic group -----------------------------
W, H = 74, 54
fig, ax = plt.subplots(figsize=panel(W, H))
piv = ST[ST.group.isin(GRP)].pivot_table(index='setting', columns='group',
                                         values='pct_up').reindex(SET)[GRP]
x = np.arange(len(SET)); wid = .26
for i, g in enumerate(GRP):
    ax.bar(x + (i - 1) * wid, piv[g].values, width=wid, facecolor=fill(GCOL[g]),
           edgecolor='black', linewidth=LW, zorder=2, label=g)
chi = ST[ST.group == 'chi2 across groups'].set_index('setting').loc[SET]
for xi, s in zip(x, SET):
    ax.text(xi, 103, ('%.3g' % chi.loc[s, 'p']), ha='center', va='bottom',
            rotation=90, fontsize=ANNOT_PT, color='0.35')
ax.text(-.55, 103, 'χ² $P$ →', ha='left', va='bottom', rotation=90,
        fontsize=ANNOT_PT, color='0.35')
ax.set_xticks(x)
ax.set_xticklabels([f'{SETLAB[s]}\n{"weaker" if s.endswith("_low") else "stronger" if s.endswith("_high") else "original"}'
                    for s in SET], fontsize=TICK_PT)
ax.set_ylim(0, 138); ax.set_yticks([0, 50, 100])
ax.set_ylabel('Twins with increased NP (%)')
ax.set_xlim(-.6, len(SET) - .4)
tr = ax.get_xaxis_transform()
ax.text(1, -.30, 'AMPA', transform=tr, ha='center', va='top', fontsize=ANNOT_PT,
        color=C('ampa'), clip_on=False)
ax.text(4, -.30, 'GABA-A', transform=tr, ha='center', va='top', fontsize=ANNOT_PT,
        color=C('gaba'), clip_on=False)
ax.legend(loc='upper center', fontsize=ANNOT_PT, frameon=False, borderaxespad=.1,
          handlelength=1.1, handletextpad=.5, labelspacing=.2, ncol=3,
          columnspacing=1.2)
panel_title(ax, 'Patients respond most often, under every AMPA setting')
enforce(fig); save(fig, 'figS_cond_b', W, H, 'conductance_responder_by_group_n288.csv')

# ---- c  how many of the six settings each twin increased under ---------------
W, H = 52, 54
fig, ax = plt.subplots(figsize=panel(W, H))
cnt = IN.n_settings_up.value_counts().reindex(range(7), fill_value=0)
ax.bar(cnt.index, cnt.values, width=.72, facecolor=fill(C('increased')),
       edgecolor='black', linewidth=LW, zorder=2)
for i, v in cnt.items():
    if v:
        ax.text(i, v + 3, f'{v}', ha='center', va='bottom', fontsize=ANNOT_PT,
                color='0.35')
ax.set_xticks(range(7)); ax.set_xticklabels(range(7), fontsize=TICK_PT)
ax.set_xlabel('Settings with increased NP (of 6)')
ax.set_ylabel('Twins')
ax.set_ylim(0, cnt.max() * 1.20)
ax.text(.03, .97, f'{cnt[6]}/{int(cnt.sum())} = {100 * cnt[6] / cnt.sum():.1f}% '
        f'increased\nunder all six', transform=ax.transAxes, ha='left', va='top',
        fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Direction is stable within twin')
enforce(fig); save(fig, 'figS_cond_c', W, H, 'conductance_subject_level_n288.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/conductance_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
