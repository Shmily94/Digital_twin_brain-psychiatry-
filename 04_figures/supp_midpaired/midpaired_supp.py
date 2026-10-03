"""Paired comparisons of summed NP-related MID functional connectivity
under placebo versus ketamine (a) and placebo versus midazolam (b).

27 healthy volunteers, three within-subject infusion sessions in a randomised
cross-over design.  The plotted quantity is the RAW sum of the six NP-related
MID edges (fc1-fc6).  The score used in Fig. 5 is NOT used here: it is the
residual of that sum on head motion, standardised separately WITHIN each
condition, so a paired placebo-vs-drug difference on it is identically zero by
construction (verified: r = 1.000000 with z(resid on FD) within condition; the
paired t is exactly 0, P = 1).  Head motion is not balanced across sessions -
midazolam has higher FD than placebo (+0.079 mm, t(26) = 2.659, P = 0.013),
ketamine does not (P = 0.82) - so the test reported on each panel is the
motion-adjusted one: the intercept of (drug - placebo) FC regressed on
(drug - placebo) FD, which adjusts for motion without removing the condition
mean.  The unadjusted and pooled-residual versions are in the source table.
Every participant is plotted; the comparison is within-subject and the paired
structure is carried by the test, not by connecting lines.
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

SUB = pd.read_csv(f'{D}/midpaired_subject_level_n27.csv')
ST = pd.read_csv(f'{D}/midpaired_placebo_vs_drug_n27.csv')
C_PL = C('placebo')
DCOL = {'Ketamine': C('ketamine'), 'Midazolam': C('midazolam')}
SCOL = {'increasers': C('increased'), 'decreasers': C('decreased')}


def paired_panel(drug, name):
    W, H = 66, 58
    fig, ax = plt.subplots(figsize=panel(W, H))
    a = SUB['Placebo'].values
    b = SUB[drug].values
    rng = np.random.default_rng(3)
    for x, v, col in [(0, a, C_PL), (1, b, DCOL[drug])]:
        bp = ax.boxplot([v], positions=[x], widths=.42, showfliers=False,
                        patch_artist=True, zorder=3)
        for el in ('boxes', 'whiskers', 'caps', 'medians'):
            for art in bp[el]:
                art.set_linewidth(LW); art.set_color('black')
        bp['boxes'][0].set_facecolor(fill(col)); bp['boxes'][0].set_edgecolor('black')
    for x, v, col in [(0, a, C_PL), (1, b, DCOL[drug])]:
        ax.scatter(x + rng.uniform(-.13, .13, len(v)), v, s=5, facecolor=col,
                   edgecolor=pt_edge(col), linewidth=LW * .4, alpha=.9, zorder=4)
    r = ST[(ST.comparison == f'Placebo vs {drug}') &
           (ST.measure.str.startswith('motion-adjusted (\u0394FC'))].iloc[0]
    top = float(max(a.max(), b.max()))
    ax.plot([0, 1], [top * 1.10] * 2, color='0.45', lw=LW)
    ax.text(.5, top * 1.13,
            f"$t$(25) = {r['t']:.2f}, $P$ = {r['p']:.3f}\n"
            f"$\\Delta$ = {r['mean_diff']:+.3f} (95% CI {r['ci95_lo']:+.3f} to "
            f"{r['ci95_hi']:+.3f})\n{int(r['n_increased'])}/27 increased",
            ha='center', va='bottom', fontsize=TICK_PT, linespacing=1.2, color='0.35')
    ax.set_xticks([0, 1]); ax.set_xticklabels(['Placebo', drug], fontsize=TICK_PT)
    ax.get_xticklabels()[0].set_color(C_PL)
    ax.get_xticklabels()[1].set_color(DCOL[drug])
    ax.set_ylabel('Summed NP-related MID FC\n(6 edges, Fisher $z$)')
    ax.set_xlim(-.55, 1.55)
    ax.set_ylim(min(a.min(), b.min()) - .25, top * 1.42)
    panel_title(ax, f'Placebo versus {drug.lower()} (n = 27)')
    enforce(fig); save(fig, name, W, H, 'midpaired_placebo_vs_drug_n27.csv')


paired_panel('Ketamine', 'figS_midpaired_a')
paired_panel('Midazolam', 'figS_midpaired_b')

pd.DataFrame(manifest).to_csv(f'{P}/midpaired_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
