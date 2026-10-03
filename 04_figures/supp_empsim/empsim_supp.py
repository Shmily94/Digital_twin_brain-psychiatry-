"""Comparison of simulated and empirical NP factor scores, within diagnostic group.

a  residualised scores (age, sex, site, mean FD regressed out, each measure
   centred separately) - the specification behind the manuscript sentence
b  raw scores - the same test without residualisation, shown because the two
   measures carry a constant offset that residualisation removes by construction
"""
import sys, numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, '../fig_color')
from np_dtb_style import (apply_np_style, panel, C, panel_title, enforce, LW,
                          LABEL_PT, ANNOT_PT, TICK_PT)
from supp_kit import saver, boxes, fill, pt_edge
apply_np_style()
D, P = 'data', 'panels'
manifest = []
save = saver(P, manifest)

sl = pd.read_csv(f'{D}/empsim_subject_level_n288.csv')
ST = pd.read_csv(f'{D}/empsim_paired_tests_n288.csv')
GRPS = ['HC', 'High-symptom', 'Patient']
GLAB = {'HC': 'Healthy\ncontrols', 'High-symptom': 'High-symptom', 'Patient': 'Patients'}
GCOL = {'HC': C('hc'), 'High-symptom': C('high_symptom'), 'Patient': C('patient')}
# Measure is encoded by fill, group by outline colour: empirical = open,
# simulated = filled, so the same three group colours carry both panels.


def emp_sim_panel(cols, scored, title, name, src):
    """Box + all individual observations, the same grammar as the main figures.
    Empirical = open box, simulated = filled box; group identity is the colour."""
    W, H = 108, 56
    fig, ax = plt.subplots(figsize=panel(W, H))
    rng = np.random.default_rng(0)
    pos, vals, cols_, filled_ = [], [], [], []
    for gi, g in enumerate(GRPS):
        sub = sl[sl.Group == g]
        for mi, c in enumerate(cols):
            pos.append(gi * 2.6 + mi * 0.95)
            vals.append(sub[c].values)
            cols_.append(GCOL[g]); filled_.append(mi == 1)
    bp = ax.boxplot(vals, positions=pos, widths=.62, showfliers=False,
                    patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
    for i, v in enumerate(vals):
        bp['boxes'][i].set_facecolor(fill(cols_[i]) if filled_[i] else 'white')
        bp['boxes'][i].set_edgecolor('black')
        if filled_[i]:
            ax.scatter(pos[i] + rng.uniform(-.15, .15, len(v)), v, s=4.5,
                       facecolor=cols_[i], edgecolor=pt_edge(cols_[i]),
                       linewidth=LW * .4, alpha=.85, zorder=3)
        else:                      # empirical: open markers, same group colour
            ax.scatter(pos[i] + rng.uniform(-.15, .15, len(v)), v, s=4.5,
                       facecolor='none', edgecolor=cols_[i],
                       linewidth=LW * .6, alpha=.85, zorder=3)
    ymax = float(sl[list(cols)].max().max())
    for gi, g in enumerate(GRPS):
        r = ST[(ST.group == g) & (ST.scores == scored)].iloc[0]
        x = gi * 2.6 + .475
        ax.plot([gi * 2.6, gi * 2.6 + .95], [ymax * 1.10] * 2, color='0.45', lw=LW)
        p_ = r['p_paired_t']
        ptxt = f'P = {p_:.3f}' if p_ >= .001 else f'P = {p_:.1e}'
        ax.text(x, ymax * 1.13, f"$t$ = {r['t']:+.2f}\n{ptxt}", ha='center',
                va='bottom', fontsize=TICK_PT, linespacing=1.15,
                color='0.35' if p_ >= .05 else C('patient'))
    ax.set_xticks([gi * 2.6 + .475 for gi in range(len(GRPS))])
    ax.set_xticklabels([f"{GLAB[g]}\nn = "
                        f"{int(ST[(ST.group == g) & (ST.scores == scored)].iloc[0]['n'])}"
                        for g in GRPS], fontsize=TICK_PT)
    for t_, g in zip(ax.get_xticklabels(), GRPS):
        t_.set_color(GCOL[g])
    ax.set_ylabel('NP factor' + ('  (residualised)' if scored == 'residualised' else ''))
    ax.set_ylim(-ymax * 1.12, ymax * 1.50)
    ax.set_xlim(-.7, (len(GRPS) - 1) * 2.6 + 1.65)
    ax.axhline(0, color='0.85', lw=LW, zorder=0)
    panel_title(ax, title)
    enforce(fig); save(fig, name, W, H, src)


# --- legend, exported on its own so it can be placed freely in the layout
figL, axL = plt.subplots(figsize=panel(64, 28))
axL.axis('off')
hM = [Line2D([], [], marker='o', linestyle='none', markersize=3.2,
             markerfacecolor='none', markeredgecolor='0.35', markeredgewidth=LW),
      Line2D([], [], marker='o', linestyle='none', markersize=3.2,
             markerfacecolor='0.55', markeredgecolor='0.35', markeredgewidth=LW * .4)]
hG = [Line2D([], [], marker='s', linestyle='none', markersize=3.4,
             markerfacecolor=GCOL[g], markeredgecolor=GCOL[g]) for g in GRPS]
axL.legend(hM + hG, ['empirical', 'simulated'] + [GLAB[g] for g in GRPS],
           loc='center', ncol=2, fontsize=ANNOT_PT, handletextpad=.5,
           labelspacing=.5, columnspacing=1.2, borderpad=0, frameon=False)
enforce(figL); save(figL, 'figS_empsim_legend', 64, 28, 'legend for figS_empsim')

emp_sim_panel(('empirical_resid', 'simulated_resid'), 'residualised',
              'Simulated and empirical scores do not differ within any group',
              'figS_empsim_a', 'empsim_paired_tests_n288.csv')
emp_sim_panel(('empirical', 'simulated'), 'raw',
              'Before residualisation the simulated scores carry a downward offset',
              'figS_empsim_b', 'empsim_paired_tests_n288.csv')
pd.DataFrame(manifest).to_csv(f'{P}/empsim_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
