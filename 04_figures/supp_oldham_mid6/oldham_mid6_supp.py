"""Supplementary figure: Oldham's test for the virtual perturbations with the
network phenotype restricted to the six MID-specific NP edges.

Same construction as `supp_oldham/oldham_supp.py`, applied to the six-edge
phenotype instead of the full 12-edge NP factor.  The change (perturbed minus
baseline) is regressed on the AVERAGE of the two states, (post + pre)/2, which
avoids the mathematical coupling that makes a plain baseline-versus-change
correlation uninterpretable.

Because cov(mean, diff) = [var(post) - var(pre)]/2 exactly, the sign of
Oldham's r is set by the variance ratio and the test is algebraically the
paired variance-equality test: it answers "did the perturbation compress or
expand between-participant differences", not "did participants with a high
baseline change more".

Panels
------
a  six-edge phenotype, baseline -> AMPA up-regulation   (n = 288)
b  six-edge phenotype, baseline -> GABA-A up-regulation (n = 288)
c  Oldham's r with 95% CI for the six-edge phenotype next to the published
   full 12-edge NP factor, for both perturbations

Inputs : data/oldham_tests_mid6.csv, data/oldham_subject_level_mid6.csv
Outputs: panels/figS_oldham_mid6_*.png|.pdf, panels/oldham_mid6_panel_manifest.csv
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
T = pd.read_csv(os.path.join(HERE, 'data', 'oldham_tests_mid6.csv'))
D = pd.read_csv(os.path.join(HERE, 'data', 'oldham_subject_level_mid6.csv'))

SPEC = [
    ('a', 'mid6_ampa', 'ampa', 'Six MID edges, AMPA up-regulation',
     'Mean of baseline and AMPA state', 'AMPA state \u2212 baseline'),
    ('b', 'mid6_gaba', 'gaba', 'Six MID edges, GABA-A up-regulation',
     'Mean of baseline and GABA-A state', 'GABA-A state \u2212 baseline'),
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
    save(fig, f'figS_oldham_mid6_{letter}', 56, 52,
         'oldham_tests_mid6.csv / oldham_subject_level_mid6.csv')


for a in SPEC:
    scatter_panel(*a)

# ---- panel c: six-edge phenotype against the published full NP factor --------
ORDER = ['mid6_ampa', 'np12_ampa', 'mid6_gaba', 'np12_gaba']
SHORT = {'mid6_ampa': 'AMPA, six MID edges\n$n$ = 288',
         'np12_ampa': 'AMPA, full NP factor\n$n$ = 288 (published)',
         'mid6_gaba': 'GABA-A, six MID edges\n$n$ = 288',
         'np12_gaba': 'GABA-A, full NP factor\n$n$ = 288 (published)'}
F = T.set_index('series').loc[ORDER].reset_index()
lab = [SHORT[k] for k in F.series]
cols = [C('gaba') if 'GABA' in s else C('ampa') for s in F.drug_or_perturbation]
fig, ax = plt.subplots(figsize=panel(80, 46))
forest(ax, lab, F.oldham_r.values, F.oldham_ci95_lo.values, F.oldham_ci95_hi.values,
       cols, "Oldham's $r$ (change vs. mean of the two states)")
for y, (_, r) in zip(np.arange(len(F))[::-1], F.iterrows()):
    ax.text(1.02, y, '***' if r.oldham_p < .001 else '**' if r.oldham_p < .01
            else '*' if r.oldham_p < .05 else 'n.s.', transform=ax.get_yaxis_transform(),
            va='center', ha='left', fontsize=6, color='0.3')
ax.set_xlim(-.75, .95)
panel_title(ax, "Six-edge phenotype versus the full NP factor")
fig.tight_layout()
save(fig, 'figS_oldham_mid6_c', 80, 46, 'oldham_tests_mid6.csv')

MF = pd.DataFrame(manifest)
MF.to_csv(os.path.join(HERE, 'panels', 'oldham_mid6_panel_manifest.csv'), index=False)
print(MF.to_string(index=False))
