"""Supplementary figure: Oldham's test for the GABA-A contrast in the DTB model
and in the two pharmacology datasets.

Oldham's test avoids the mathematical coupling that inflates a plain
baseline-versus-change correlation: the change (post - pre) is regressed on the
AVERAGE of the two measurements, (post + pre)/2, rather than on the baseline.
It is shift-invariant, so it is unaffected by the per-condition mean-centring in
the pharmacology score files.

Note on interpretation.  cov(mean, diff) = [var(post) - var(pre)] / 2 exactly,
so the sign of Oldham's r is determined entirely by the variance ratio and the
test is algebraically the paired variance-equality (Pitman-Morgan) test.  It
answers "did the perturbation compress or expand between-subject differences",
NOT "did participants with a high baseline change more".

Datasets
--------
a, e  DTB model, IMAGEN n = 288: simulated baseline -> GABA-A (a) and -> AMPA (e).
b, c  Healthy pharmacology n = 27: placebo -> midazolam (b), -> ketamine (c);
      raw summed FC over the six NP-related MID edges.
d     Clinical ketamine n = 36 (MDD 22 + HC 14): placebo session p2 -> d2.
f     All contrasts together, including the head-motion-residualised versions
      of b and c and the MDD-only subgroup of d.

Inputs : data/oldham_tests.csv, data/oldham_subject_level.csv
Outputs: panels/figS_oldham_*.png|.pdf, panels/oldham_panel_manifest.csv
"""
import os, sys
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, panel, C, panel_title, LW
from supp_kit import saver, fill, pt_edge, forest

apply_np_style()
manifest = []
save = saver(os.path.join(HERE, 'panels'), manifest)
T = pd.read_csv(os.path.join(HERE, 'data', 'oldham_tests.csv'))
D = pd.read_csv(os.path.join(HERE, 'data', 'oldham_subject_level.csv'))

SPEC = [
    ('a', 'model_gaba',   'gaba',      'DTB model, GABA-A up-regulation',
     'Mean of baseline and GABA-A state', 'GABA-A state \u2212 baseline'),
    ('b', 'healthy_mid',  'midazolam', 'Healthy cohort, midazolam',
     'Mean of placebo and midazolam', 'Midazolam \u2212 placebo'),
    ('c', 'healthy_ket',  'ketamine',  'Healthy cohort, ketamine',
     'Mean of placebo and ketamine', 'Ketamine \u2212 placebo'),
    ('d', 'clinical_ket', 'ketamine',  'Clinical cohort, ketamine',
     'Mean of placebo and ketamine session', 'Ketamine \u2212 placebo'),
    ('e', 'model_ampa',   'ampa',      'DTB model, AMPA up-regulation',
     'Mean of baseline and AMPA state', 'AMPA state \u2212 baseline'),
]


def scatter_panel(letter, key, colour_key, title, xlab, ylab):
    s = D[D.series == key]
    x, y = s.mean_pre_post.values, s.difference.values
    col = C(colour_key)
    r = T[T.series == key].iloc[0]
    fig, ax = plt.subplots(figsize=panel(56, 52))
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.scatter(x, y, s=7, facecolor=col, edgecolor=pt_edge(col),
               linewidth=LW * .45, alpha=.9, zorder=3)
    xs = np.linspace(x.min(), x.max(), 100)
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    pr = fit.get_prediction(sm.add_constant(xs)).summary_frame(alpha=.05)
    ax.fill_between(xs, pr.mean_ci_lower, pr.mean_ci_upper, color=fill(col),
                    alpha=.55, lw=0, zorder=2)
    ax.plot(xs, pr['mean'], color=col, lw=LW * 1.6, zorder=4)
    ax.set_xlabel(xlab); ax.set_ylabel(ylab)
    lo, hi = y.min(), y.max(); sp = hi - lo
    ax.set_ylim(lo - .08 * sp, hi + .34 * sp)
    pstr = (f"{r.oldham_p:.1e}".replace('e-', '\u00d710$^{-') + '}$') if r.oldham_p < 1e-3 \
        else f'{r.oldham_p:.3f}'
    ax.text(.5, .995,
            f"Oldham $r$ = {r.oldham_r:+.3f} (95% CI {r.oldham_ci95_lo:+.2f}, {r.oldham_ci95_hi:+.2f})\n"
            f"$t$({int(r.df)}) = {r.oldham_t:.2f}, $P$ = {pstr}\n"
            f"variance ratio = {r.variance_ratio_post_pre:.2f}, $n$ = {int(r.n)}",
            transform=ax.transAxes, ha='center', va='top', fontsize=6,
            color='0.25', linespacing=1.25)
    panel_title(ax, title)
    fig.tight_layout()
    save(fig, f'figS_oldham_{letter}', 56, 52, 'oldham_tests.csv / oldham_subject_level.csv')


for a in SPEC:
    scatter_panel(*a)

# ---- panel f: every contrast, Oldham r with 95% CI ---------------------------
F = T.copy()
SHORT = {'model_gaba': 'DTB model, GABA-A\n$n$ = 288',
         'model_ampa': 'DTB model, AMPA\n$n$ = 288 (reference)',
         'healthy_mid': 'Healthy, midazolam\n$n$ = 27, raw FC',
         'healthy_ket': 'Healthy, ketamine\n$n$ = 27, raw FC',
         'healthy_mid_resid': 'Healthy, midazolam\n$n$ = 27, motion-residualised',
         'healthy_ket_resid': 'Healthy, ketamine\n$n$ = 27, motion-residualised',
         'clinical_ket': 'Clinical, ketamine\n$n$ = 36 (MDD + HC)',
         'clinical_ket_mdd': 'Clinical, ketamine\n$n$ = 22 (MDD only)'}
lab = [SHORT[k] for k in F.series]
cols = [C('gaba') if 'GABA' in s else C('ampa') for s in F.drug_or_perturbation]
fig, ax = plt.subplots(figsize=panel(80, 72))
forest(ax, lab, F.oldham_r.values, F.oldham_ci95_lo.values, F.oldham_ci95_hi.values,
       cols, "Oldham's $r$ (change vs. mean of the two measurements)")
for y, (_, r) in zip(np.arange(len(F))[::-1], F.iterrows()):
    ax.text(1.02, y, '***' if r.oldham_p < .001 else '**' if r.oldham_p < .01
            else '*' if r.oldham_p < .05 else 'n.s.', transform=ax.get_yaxis_transform(),
            va='center', ha='left', fontsize=6, color='0.3')
ax.set_xlim(-.75, .95)
panel_title(ax, "Oldham's test: model versus drug data")
fig.tight_layout()
save(fig, 'figS_oldham_f', 80, 72, 'oldham_tests.csv')

MF = pd.DataFrame(manifest)
MF.to_csv(os.path.join(HERE, 'panels', 'oldham_panel_manifest.csv'), index=False)
print(MF.to_string(index=False))
