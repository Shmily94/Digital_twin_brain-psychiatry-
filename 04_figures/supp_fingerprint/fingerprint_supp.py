"""Supplementary figure | individual fingerprinting on held-out task trials.

Four subjects (HC03, HC04, AUD02, MDD02) x 24 held-out emotional-face trials.
Each trial's voxelwise activation pattern is correlated with every subject's
template; identification is the arg-max over the four templates.  The simulated
columns come from the digital twins run forward on the held-out trials WITHOUT
re-assimilation, so the comparison tests generalisation, not fit.

    cd revision/text/figures/supp_fingerprint && python fingerprint_supp.py
"""
import os, sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          panel_title, enforce)
from supp_kit import saver, pt_edge
apply_np_style()
D, OUTD = f'{HERE}/data', f'{HERE}/panels'
ME = pd.read_csv(f'{D}/fingerprint_similarity_empirical.csv', index_col=0)
MS = pd.read_csv(f'{D}/fingerprint_similarity_simulated.csv', index_col=0)
ACC = pd.read_csv(f'{D}/fingerprint_accuracy.csv')
MG = pd.read_csv(f'{D}/fingerprint_margins.csv')
manifest = []
save = saver(OUTD, manifest)
VMAX = float(max(np.abs(ME.values).max(), np.abs(MS.values).max()))


def heat(Mx, stem, title, acc_row):
    W, H = 58, 84
    fig, ax = plt.subplots(figsize=panel(W, H))
    im = ax.imshow(Mx.values, cmap='RdBu_r', vmin=-VMAX, vmax=VMAX, aspect='auto')
    truth = [t.split('_')[0] for t in Mx.index]
    for i, t in enumerate(truth):                    # outline the correct cell
        j = list(Mx.columns).index(t)
        ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, fill=False, edgecolor='black',
                               lw=LW * 1.3, zorder=4))
        k = int(np.argmax(Mx.values[i]))             # mark the chosen template
        if k != j:
            ax.add_patch(Rectangle((k - .5, i - .5), 1, 1, fill=False,
                                   edgecolor=C('patient'), lw=LW * 1.6, zorder=5))
    ax.set_xticks(range(Mx.shape[1]))
    ax.set_xticklabels(Mx.columns, fontsize=TICK_PT, rotation=90)
    ax.set_yticks(range(Mx.shape[0]))
    ax.set_yticklabels([t.replace('_', ' ') for t in Mx.index], fontsize=TICK_PT)
    ax.set_xlabel('Subject template')
    cb = fig.colorbar(im, ax=ax, fraction=.05, pad=.03)
    cb.set_label('Pattern correlation', fontsize=ANNOT_PT)
    cb.ax.tick_params(labelsize=TICK_PT, length=2, width=LW)
    cb.outline.set_linewidth(LW)
    ax.set_title(f'{title}\n{acc_row.n_correct}/{acc_row.n_trials} correct '
                 f'= {acc_row.accuracy_pct:.1f}%', fontsize=ANNOT_PT, loc='left', pad=4)
    enforce(fig); save(fig, stem, W, H, os.path.basename(stem) + '.csv', pptx=False)


heat(ME, 'figS_finger_a', 'Empirical BOLD', ACC.iloc[0])
heat(MS, 'figS_finger_b', 'Simulated, no re-assimilation', ACC.iloc[1])

# ---- c  identification margin per trial -------------------------------------
W, H = 62, 52
fig, ax = plt.subplots(figsize=panel(W, H))
me = (MG.self_r_empirical - MG.best_other_r_empirical).values
ms = (MG.self_r_simulated - MG.best_other_r_simulated).values
rng = np.random.default_rng(0)
for i, (v, col, lab) in enumerate([(me, C('reference'), 'Empirical'),
                                   (ms, C('np12'), 'Simulated')]):
    bp = ax.boxplot([v], positions=[i], widths=.55, showfliers=False, patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
    bp['boxes'][0].set_facecolor(tuple(1 - .45 * (1 - np.array(
        plt.matplotlib.colors.to_rgb(col))))); bp['boxes'][0].set_edgecolor('black')
    ax.scatter(i + rng.uniform(-.14, .14, len(v)), v, s=13, facecolor=col,
               edgecolor=pt_edge(col), linewidth=LW * .55, alpha=.9, zorder=3)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
t_, p_ = stats.ttest_rel(ms, me)
hi = max(me.max(), ms.max()); lo = min(me.min(), ms.min()); span = hi - lo
ax.plot([0, 0, 1, 1], [hi + span * .07, hi + span * .12, hi + span * .12,
                       hi + span * .07], color='black', lw=LW)
ax.text(.5, hi + span * .135, f'paired $t$ = {t_:.2f}, $P$ = {p_:.3g}', ha='center',
        va='bottom', fontsize=ANNOT_PT)
ax.set_ylim(lo - span * .10, hi + span * .32)
ax.set_xticks([0, 1]); ax.set_xticklabels(['Empirical', 'Simulated'], fontsize=TICK_PT)
ax.set_xlim(-.65, 1.65)
ax.set_ylabel('Identification margin\n(self − best other $r$)')
panel_title(ax, 'Twins identify trials with a wider margin')
enforce(fig); save(fig, 'figS_finger_c', W, H, 'fingerprint_margins.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/fingerprint_panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
print(f'margin: empirical {me.mean():.4f}, simulated {ms.mean():.4f}, '
      f'paired t = {t_:.3f}, P = {p_:.4g}')
