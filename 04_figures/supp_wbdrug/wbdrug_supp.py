"""Agreement between simulated and empirical whole-brain drug effects
(Supplementary Results 8.4).

a  directional concordance, task-matched vs task-mismatched DTB predictions,
   for the pharmacologically matched pairings
b  the same for cross-receptor pairings - the receptor-specificity control
c  split-half reliability of the empirical drug-effect maps, which bounds the
   agreement any model can attain

Pharmacological sample: 27 healthy volunteers, three within-subject sessions
(placebo, ketamine, midazolam), MID task, Shen-268 whole-brain FC.
Edges entering the test are those with a nominal drug-vs-placebo effect at
P < 0.001. Significance is the node-level sign-flip null (999 permutations);
the binomial test is reported alongside but ignores edge dependence.
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, '../fig_color')
from np_dtb_style import (apply_np_style, panel, C, panel_title, enforce, LW,
                          LABEL_PT, ANNOT_PT, TICK_PT)
from supp_kit import saver, fill, pt_edge
apply_np_style()
D, P = 'data', 'panels'
manifest = []
save = saver(P, manifest)

W3 = pd.read_csv(f'{D}/wbdrug_direction_agreement_n288.csv')
RL = pd.read_csv(f'{D}/wbdrug_map_reliability.csv')
CK, CM = C('ketamine'), C('midazolam')
DCOL = {'Ketamine': CK, 'Midazolam': CM}
LLAB = {'mid_antici_hit': 'MID\nanticipation', 'mid_feed_hit': 'MID\nfeedback',
        'pooled (both MID conditions)': 'pooled'}
LEVELS = ['mid_antici_hit', 'mid_feed_hit', 'pooled (both MID conditions)']


def conc_panel(pairing, title, name):
    W, H = 124, 56
    fig, ax = plt.subplots(figsize=panel(W, H))
    sub = W3[W3.pairing == pairing]
    xs, xl, xc = [], [], []
    k = 0
    for drug in ['Ketamine', 'Midazolam']:
        for lv in LEVELS:
            for tm, dx in [('matched(MID)', -.19), ('mismatched(SST)', .19)]:
                r = sub[(sub.drug == drug) & (sub.level == lv) & (sub.task_match == tm)]
                if not len(r):
                    continue
                r = r.iloc[0]
                col = DCOL[drug]
                x = k + dx
                # node-level sign-flip null: 50% +/- its s.d., shown as a band
                ax.add_patch(plt.Rectangle((x - .15, 50 - r['null_sd_pct']), .30,
                                           2 * r['null_sd_pct'], facecolor='0.90',
                                           edgecolor='none', zorder=0))
                open_marker = tm.startswith('mis')
                ax.scatter(x, r['pct_same'], s=24, marker='o' if not open_marker else 's',
                           facecolor=col if r['p_signflip_node'] < .05 else 'white',
                           edgecolor=col, linewidth=LW, zorder=3)
                ax.text(x, r['pct_same'] + (2.4 if not open_marker else -2.6),
                        f"{int(r['n_same'])}/{int(r['n_edges'])}", ha='center',
                        va='bottom' if not open_marker else 'top',
                        fontsize=TICK_PT, color=col)
            xs.append(k); xl.append(LLAB[lv]); xc.append(DCOL[drug]); k += 1.25
        k += .45
    ax.axhline(50, color='0.45', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.set_xticks(xs); ax.set_xticklabels(xl, fontsize=TICK_PT)
    for t_, c_ in zip(ax.get_xticklabels(), xc):
        t_.set_color(c_)
    ax.set_ylabel('Edges with matching direction (%)')
    ax.set_ylim(30, 100)
    ax.set_xlim(-.7, xs[-1] + .7)
    for drug, xr in [('Ketamine', xs[:3]), ('Midazolam', xs[3:])]:
        ax.text(np.mean(xr), 97, drug, ha='center', fontsize=ANNOT_PT, color=DCOL[drug])
    panel_title(ax, title)
    enforce(fig)
    return fig, W, H


fig, W, H = conc_panel(
    'matched', 'Task-matched predictions agree with the empirical drug effect; '
               'task-mismatched ones do not (ketamine)', 'a')
save(fig, 'figS_wbdrug_a', W, H, 'wbdrug_direction_agreement_n288.csv')
fig, W, H = conc_panel(
    'cross-receptor', 'Cross-receptor pairings agree just as well, so the '
                      'agreement is directional, not receptor-specific', 'b')
save(fig, 'figS_wbdrug_b', W, H, 'wbdrug_direction_agreement_n288.csv')

# --- legend on its own
figL, axL = plt.subplots(figsize=panel(86, 30))
axL.axis('off')
h = [Line2D([], [], marker='o', linestyle='none', markersize=3.2,
            markerfacecolor='0.35', markeredgecolor='0.35'),
     Line2D([], [], marker='s', linestyle='none', markersize=3.2,
            markerfacecolor='white', markeredgecolor='0.35', markeredgewidth=LW),
     Line2D([], [], marker='s', linestyle='none', markersize=4.2,
            markerfacecolor='0.90', markeredgecolor='0.90'),
     Line2D([], [], linestyle=(0, (2.6, 1.7)), color='0.45', lw=LW),
     Line2D([], [], marker='o', linestyle='none', markersize=3.2,
            markerfacecolor='0.35', markeredgecolor='0.35')]
axL.legend(h, ['task-matched (MID) prediction', 'task-mismatched (SST) prediction',
               '\u00b11 s.d. of the sign-flip null', 'chance (50%)',
               'filled = P < 0.05 vs the sign-flip null'],
           loc='center', ncol=2, fontsize=ANNOT_PT, handletextpad=.5,
           labelspacing=.5, columnspacing=1.2, borderpad=0, frameon=False)
enforce(figL); save(figL, 'figS_wbdrug_legend', 86, 30, 'legend for figS_wbdrug')

# ------------------------------------------------ c  split-half reliability
W, H = 80, 54
fig, ax = plt.subplots(figsize=panel(W, H))
RL = RL.sort_values(['drug', 'drug_condition']).reset_index(drop=True)
x = np.arange(len(RL))
cols = [DCOL[d] for d in RL.drug]
ax.bar(x, RL.spearman_brown_reliability, width=.6,
       facecolor=[fill(c) for c in cols], edgecolor=cols, linewidth=LW, zorder=2)
for i, r in RL.iterrows():
    ax.scatter(i, r['max_attainable_r'], s=20, marker='v', facecolor='white',
               edgecolor=cols[i], linewidth=LW, zorder=3)
    ax.text(i, r['max_attainable_r'] + .012,
            f"max attainable\n$r$ = {r['max_attainable_r']:.2f}", ha='center',
            va='bottom', fontsize=TICK_PT, color=cols[i], linespacing=1.15)
    ax.text(i, r['spearman_brown_reliability'] / 2,
            f"{r['spearman_brown_reliability']:.3f}", ha='center', va='center',
            fontsize=TICK_PT, color='black')
ax.set_xticks(x)
ax.set_xticklabels([f"{r['drug']}\n{LLAB[r['drug_condition']].replace(chr(10), ' ')}"
                    for _, r in RL.iterrows()], fontsize=TICK_PT)
for t_, c_ in zip(ax.get_xticklabels(), cols):
    t_.set_color(c_)
ax.set_ylabel('Split-half reliability of the\nempirical drug-effect map')
ax.set_ylim(0, .62)
panel_title(ax, 'Empirical whole-brain drug-effect maps are weakly reliable at '
                'n = 27, which caps attainable agreement')
enforce(fig); save(fig, 'figS_wbdrug_c', W, H, 'wbdrug_map_reliability.csv')

pd.DataFrame(manifest).to_csv(f'{P}/wbdrug_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
