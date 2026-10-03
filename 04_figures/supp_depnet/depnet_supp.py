"""Supplementary figure | Depression-specific network (27 edges), n = 141.

Drawn in the same style as the main NP figures (../fig_color/np_dtb_style.py):
one file per panel into ./panels/ as .png (400 dpi), .pdf and .pptx.

  a  summed depression-network FC by group, four conditions
  b  adjusted HC - MDD difference across the four conditions, with 95% CIs
  c  paired comparison of the simulated baseline against each perturbation
  d  per-edge HC - MDD difference across the 27 edges

Cohort: MDD (n = 72) and HC (n = 69) of the population-scale simulation
subsample, i.e. the sample the network was defined in (SI Results 5).
Group tests are GLMs with sex, recruitment site and mean head motion as
covariates, matching compare_dep_network_unified.py; the four group
statistics reproduce the SI text exactly (t(136) = -4.98, -5.13, -0.97, -2.78).
Panels a and c display adjusted values (residual + that condition's own mean),
so the covariates are removed without moving the condition off its real scale.

    cd revision/text/figures/supp_depnet && python depnet_supp.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy import stats
import statsmodels.formula.api as smf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx

D = os.path.join(HERE, 'depnet_data')
OUTD = os.path.join(HERE, 'panels')
os.makedirs(OUTD, exist_ok=True)
DPI = 400
apply_np_style()

GRP = ['HC', 'MDD']
GCOL = {'HC': C('hc'), 'MDD': C('mdd')}
CONDS = [('empirical', 'Empirical', C('baseline'), True),
         ('simulated', 'Simulated baseline', C('baseline'), False),
         ('ampa', 'After AMPA', C('ampa'), False),
         ('gaba', 'After GABA-A', C('gaba'), False)]
manifest = []

T = pd.read_csv(f'{D}/depnet_subject_level_n141.csv')
E = pd.read_csv(f'{D}/depnet_edge_source_data.csv')
assert len(T) == 141 and set(T.group) == {'HC', 'MDD'}
T['MDD'] = (T.group == 'MDD').astype(int)
for c_, _, _, _ in CONDS:                      # adjusted values (see docstring)
    T[c_ + '_a'] = (smf.ols(f'{c_} ~ sex + site + headmotion', data=T).fit().resid
                    + T[c_].mean())


def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}',
                         dpi=round(px[0] / (w_mm / 25.4)), source=note))
    plt.close(fig)


def box_points(ax, values, colours, width=.55, jitter=.14, seed=0, s=3.4):
    rng = np.random.default_rng(seed)
    bp = ax.boxplot(values, positions=np.arange(len(values)), widths=width,
                    showfliers=False, patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    for i, v in enumerate(values):
        ax.scatter(i + rng.uniform(-jitter, jitter, len(v)), v, s=s,
                   facecolor=colours[i], edgecolor='none', alpha=.75, zorder=3)
    return bp


# ---- GLM group statistics (the numbers the SI quotes) -----------------------
grows = []
for c_, lab, _, _ in CONDS:
    mod = smf.ols(f'{c_} ~ MDD + sex + site + headmotion', data=T).fit()
    hc = T.loc[T.group == 'HC', c_].values; md = T.loc[T.group == 'MDD', c_].values
    n1, n2 = len(hc), len(md)
    sp = np.sqrt(((n1 - 1) * hc.var(ddof=1) + (n2 - 1) * md.var(ddof=1)) / (n1 + n2 - 2))
    d_ = (hc.mean() - md.mean()) / sp
    se_d = np.sqrt((n1 + n2) / (n1 * n2) + d_ ** 2 / (2 * (n1 + n2)))
    ci = mod.conf_int().loc['MDD']
    grows.append(dict(condition=lab, n_hc=n1, n_mdd=n2,
                      hc_mean=round(float(hc.mean()), 4), hc_sd=round(float(hc.std(ddof=1)), 4),
                      mdd_mean=round(float(md.mean()), 4), mdd_sd=round(float(md.std(ddof=1)), 4),
                      adj_diff_hc_minus_mdd=round(-float(mod.params['MDD']), 4),
                      ci_lo=round(-float(ci[1]), 4), ci_hi=round(-float(ci[0]), 4),
                      t=round(float(mod.tvalues['MDD']), 3), df=int(mod.df_resid),
                      p=float(f"{mod.pvalues['MDD']:.3g}"),
                      cohens_d_unadj=round(float(d_), 3),
                      d_ci_lo=round(float(d_ - 1.96 * se_d), 3),
                      d_ci_hi=round(float(d_ + 1.96 * se_d), 3)))
G = pd.DataFrame(grows)
G.to_csv(f'{D}/depnet_group_stats_n141.csv', index=False)

# ---- a  four conditions, HC vs MDD -----------------------------------------
for i, (c_, lab, _, _) in enumerate(CONDS):
    W, H = 42, 50
    fig, ax = plt.subplots(figsize=panel(W, H))
    vals = [T.loc[T.group == g, c_ + '_a'].values for g in GRP]
    box_points(ax, vals, [GCOL[g] for g in GRP])
    g0 = G.iloc[i]
    hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
    step = (hi - lo) * .12
    ax.plot([0, 0, 1, 1], [hi + step * .4, hi + step * .7, hi + step * .7, hi + step * .4],
            color='black', lw=LW)
    ax.text(.5, hi + step * .78, f'$P$ = {g0.p:.2g}', ha='center', va='bottom',
            fontsize=ANNOT_PT)
    ax.set_ylim(lo - step * .4, hi + step * 1.9)
    ax.set_xticks(range(2)); ax.set_xticklabels(GRP, fontsize=TICK_PT)
    ax.set_xlim(-.6, 1.6)
    ax.set_ylabel('Depression-network FC')
    panel_title(ax, lab)
    enforce(fig); save(fig, f'figS_depnet_a{i + 1}', W, H,
                       'depnet_subject_level_n141.csv')

# ---- b  adjusted group difference across conditions ------------------------
W, H = 66, 50
fig, ax = plt.subplots(figsize=panel(W, H))
for i, (c_, lab, col, open_) in enumerate(CONDS):
    g0 = G.iloc[i]
    ax.vlines(i, g0.ci_lo, g0.ci_hi, color=col, lw=LW, zorder=2)
    for yy in (g0.ci_lo, g0.ci_hi):
        ax.plot([i - .13, i + .13], [yy] * 2, color=col, lw=LW, zorder=2)
    ax.scatter([i], [g0.adj_diff_hc_minus_mdd], s=13,
               facecolor='white' if open_ else col, edgecolor=col, linewidth=LW,
               zorder=4)
    ax.text(i - .32 if i == 0 else i, g0.ci_hi + .05, f'$P$ = {g0.p:.2g}',
            ha='left' if i == 0 else 'center', va='bottom', fontsize=ANNOT_PT,
            color='0.35')
ax.plot(range(len(CONDS)), G.adj_diff_hc_minus_mdd, color='0.6', lw=LW, zorder=1)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_xticks(range(len(CONDS)))
ax.set_xticklabels(['Empirical', 'Simulated\nbaseline', 'After\nAMPA', 'After\nGABA-A'],
                   fontsize=TICK_PT)
ax.set_xlim(-.5, len(CONDS) - .5)
ax.set_ylim(min(G.ci_lo) - .15, max(G.ci_hi) + .45)
ax.set_ylabel('Adjusted HC − MDD difference')
hE = [Line2D([], [], marker='o', linestyle='none', markersize=3.2,
             markerfacecolor='white', markeredgecolor=C('baseline'), markeredgewidth=LW),
      Line2D([], [], marker='o', linestyle='none', markersize=3.2,
             markerfacecolor=C('baseline'), markeredgecolor=C('baseline'),
             markeredgewidth=LW)]
ax.legend(hE, ['empirical', 'simulated'], loc='lower left', fontsize=ANNOT_PT,
          handletextpad=.4, borderaxespad=.2, frameon=False)
panel_title(ax, 'AMPA removes the group difference; GABA-A does not')
enforce(fig); save(fig, 'figS_depnet_b', W, H, 'depnet_subject_level_n141.csv')

# ---- c  paired: simulated baseline vs each perturbation --------------------
PC = [('simulated', 'Baseline', C('baseline')), ('ampa', '+AMPA', C('ampa')),
      ('gaba', '+GABA-A', C('gaba'))]
W, H = 70, 54
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [T[k + '_a'].values for k, _, _ in PC]
bp = box_points(ax, vals, [c for _, _, c in PC], s=2.8, seed=1)
for j, (k, _, col) in enumerate(PC):           # opaque light tint, no points glare
    rgb = np.array(plt.matplotlib.colors.to_rgb(col))
    bp['boxes'][j].set_facecolor(tuple(1 - .42 * (1 - rgb)))
prows = []
hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
step = (hi - lo) * .11
y = hi + step * .4
for j, (k, lab, col) in enumerate(PC[1:], start=1):
    dif = T[k].values - T['simulated'].values
    t_raw, p_raw = stats.ttest_rel(T[k].values, T['simulated'].values)
    adj = smf.ols('dif ~ sex + site + headmotion', data=T.assign(dif=dif)).fit()
    prows.append(dict(comparison=f'Simulated vs {lab.lstrip("+")}', n=len(dif),
                      mean_diff=round(float(dif.mean()), 4),
                      sd_diff=round(float(dif.std(ddof=1)), 4),
                      n_increased=int((dif > 0).sum()),
                      pct_increased=round(100 * (dif > 0).mean(), 1),
                      raw_t=round(float(t_raw), 3), raw_df=len(dif) - 1,
                      raw_p=float(f'{p_raw:.3g}'),
                      adj_t=round(float(adj.tvalues['Intercept']), 3),
                      adj_df=int(adj.df_resid),
                      adj_p=float(f"{adj.pvalues['Intercept']:.3g}")))
    ax.plot([0, 0, j, j], [y, y + step * .3, y + step * .3, y], color='black', lw=LW)
    ax.text(1.0, y + step * .38,
            f'$t$({int(adj.df_resid)}) = {float(adj.tvalues["Intercept"]):.2f}, '
            f'$P$ = {float(adj.pvalues["Intercept"]):.2g}\n'
            f'{100 * (dif > 0).mean():.0f}% increased',
            ha='center', va='bottom', fontsize=ANNOT_PT)
    y += step * 2.5
pd.DataFrame(prows).to_csv(f'{D}/depnet_paired_stats_n141.csv', index=False)
ax.set_ylim(lo - step * .4, y + step * .2)
ax.set_xticks(range(3)); ax.set_xticklabels([l for _, l, _ in PC], fontsize=TICK_PT)
ax.set_xlim(-.6, 2.6)
ax.set_ylabel('Depression-network FC')
panel_title(ax, 'Both perturbations raise depression-network FC')
enforce(fig); save(fig, 'figS_depnet_c', W, H, 'depnet_subject_level_n141.csv')

# ---- d  per-edge HC - MDD difference, 27 edges ------------------------------
W, H = 180, 44
fig, ax = plt.subplots(figsize=panel(W, H))
# The source file's own d_ column is unadjusted AND signed MDD-minus-HC, while
# its t_/p_ come from the covariate GLM; to keep one convention, the plotted
# effect size is converted from the GLM t and oriented HC - MDD.
E = E.assign(d_adj_hc_minus_mdd=(-E.t_Empirical * np.sqrt(1 / 69 + 1 / 72)).round(4))
E.to_csv(f'{D}/depnet_edge_stats_used.csv', index=False)
E2 = E.sort_values('d_adj_hc_minus_mdd').reset_index(drop=True)
x = np.arange(len(E2))
sig = (E2.p_Empirical < .05).values
COLD = C('mdd')
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.scatter(x[sig], E2.d_adj_hc_minus_mdd[sig], s=10, facecolor=COLD, edgecolor=COLD,
           linewidth=LW, zorder=3)
ax.scatter(x[~sig], E2.d_adj_hc_minus_mdd[~sig], s=10, facecolor='white', edgecolor=COLD,
           linewidth=LW, zorder=3)
ax.set_xticks(x)
ax.set_xticklabels([f'E{int(e)}' for e in E2.edge], fontsize=TICK_PT, rotation=90)
ax.set_xlim(-.7, len(E2) - .3)
ax.set_ylabel("Adjusted Cohen's $d$\n(HC − MDD)")
handles = [Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                  markerfacecolor=COLD, markeredgecolor=COLD, markeredgewidth=LW),
           Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                  markerfacecolor='white', markeredgecolor=COLD, markeredgewidth=LW)]
ax.legend(handles, ['$P$ < 0.05', 'n.s.'], loc='upper left', ncol=2,
          fontsize=ANNOT_PT, handletextpad=.4, columnspacing=1.0, borderaxespad=.2)
panel_title(ax, f'{int(sig.sum())} of the 27 depression-network edges differ '
                'between HC and MDD (empirical, uncorrected)')
enforce(fig); save(fig, 'figS_depnet_d', W, H, 'depnet_edge_source_data.csv')

mf = pd.DataFrame(manifest)
mf.to_csv(f'{OUTD}/depnet_panel_manifest.csv', index=False)
print(mf.to_string(index=False))
print('\ngroup stats (GLM, covariates sex + site + head motion)')
print(G[['condition', 'hc_mean', 'mdd_mean', 'adj_diff_hc_minus_mdd', 'ci_lo',
         'ci_hi', 't', 'df', 'p', 'cohens_d_unadj']].to_string(index=False))
print('\npaired vs simulated baseline')
print(pd.DataFrame(prows).to_string(index=False))
print(f'\nd: {int(sig.sum())}/27 edges P<0.05 empirical; '
      f'{int((E.p_Simulated < .05).sum())}/27 in the simulation')
