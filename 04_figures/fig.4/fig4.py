"""Figure 4 | Virtual perturbation of the digital twins (n = 288).

ONE FILE PER PANEL -> ./panels/ as .png (400 dpi), .pdf (vector) and .pptx.

  a  empirical NP by group
  b  simulated baseline NP by group
  c  NP after AMPA up-regulation, by group
  d  NP after GABA-A up-regulation, by group
  e  distribution of the four conditions across the whole cohort
  f  per-twin response: delta NP under AMPA vs under GABA-A
  g  who shows the 'both up' pattern, and what their baseline looks like
  h  SDQ symptom items compared between the two response patterns

Cohort: the 290-subject modulation sample minus the two twins with head motion
> 0.5 mm -> n = 288 (HC 69, high-symptom 89, patient 130).  Panels a-d use NP
residualised on sex, recruitment site and mean head motion, REFIT on these 288
(the stored *_resid columns of the source table were fitted on 290).  Deltas in
f-h are raw perturbed - baseline, because residualising the two conditions
separately does not preserve the within-subject difference.

Colours: ../fig_color/np_dtb_style.py (USER_PALETTE).  HC grey, high-symptom
#E69F00, patient #D55E00; AMPA #E1D09A, GABA-A #96B9AD; response patterns
#D9A5B3 (increased) and #8DA0B4 (decreased).

    cd revision/text/figures/fig.4 && python fig4.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy import stats
from scipy.stats import gaussian_kde
from statsmodels.stats.multitest import multipletests
import statsmodels.formula.api as smf
import statsmodels.api as sm
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
sys.path.insert(0, os.path.join(HERE, '..'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx
import figA4_kit as PK          # the frozen main-figure type scale, 8/9/10 pt

D = os.path.join(HERE, 'fig4_data')
OUTD = os.path.join(HERE, 'panels')
os.makedirs(OUTD, exist_ok=True)
DPI = 400
apply_np_style()

GRP = ['HC', 'High-symptom', 'Patient']
GCOL = {'HC': C('hc'), 'High-symptom': C('high_symptom'), 'Patient': C('patient')}
PAT = ['both up', 'any down']
PCOL = {'both up': C('increased'), 'any down': C('decreased')}
COND = [('empirical', 'Empirical', 'black', (0, (2.6, 1.7))),
        ('simulated', 'Simulated baseline', C('baseline'), '-'),
        ('ampa', 'After AMPA', C('ampa'), '-'),
        ('gaba', 'After GABA-A', C('gaba'), '-')]
manifest = []

T = pd.read_csv(f'{D}/fig4_subject_level_n288.csv')
S = pd.read_csv(f'{D}/fig4_sdq_items_n287.csv')
SDQ = [c for c in S.columns if c not in ('ID', 'pattern', 'Group')]
assert len(T) == 288 and set(T.Group) == set(GRP)

# residuals refit on these 288 (see docstring)
for c in ['empirical', 'simulated', 'ampa', 'gaba']:
    # NB: C() here would be the palette helper, so let patsy treat the
    # string columns as categorical on their own
    # residual + that condition's own mean: covariates are removed but the
    # condition stays on its real NP scale (OLS residuals alone are all
    # forced to mean zero, which would hide the perturbation shift)
    T[c + '_r'] = (smf.ols(f'{c} ~ sex + site + headmotion', data=T).fit().resid
                   + T[c].mean())


def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    with mpl.rc_context({'savefig.bbox': None}):   # else the raster is cropped
        fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)   # and the text layer
                                                           # sits off-register
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}',
                         dpi=round(px[0] / (w_mm / 25.4)), source=note))
    plt.close(fig)


def box_points(ax, groups, values, colours, width=.55, jitter=.14, seed=0, s=3.2):
    rng = np.random.default_rng(seed)
    bp = ax.boxplot(values, positions=np.arange(len(groups)), widths=width,
                    showfliers=False, patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    for i, v in enumerate(values):
        ax.scatter(i + rng.uniform(-jitter, jitter, len(v)), v, s=s,
                   facecolor=colours[i], edgecolor='none', alpha=.75, zorder=3)


def star(q):
    return '***' if q < .001 else '**' if q < .01 else '*' if q < .05 else None


# ------------------------------------------------- a-d  group comparisons ----
ad_stats = []
PANELS = [('fig4a', 'empirical_r', 'Empirical NP',
           'Empirical NP is lowest in patients'),
          ('fig4b', 'simulated_r', 'Simulated NP',
           'The twins reproduce the patient deficit'),
          ('fig4c', 'ampa_r', 'NP after AMPA',
           'AMPA up-regulation removes the group difference'),
          ('fig4d', 'gaba_r', 'NP after GABA-A',
           'GABA-A up-regulation removes the group difference')]
for stem, col, ylab, ttl in PANELS:
    W, H = 42, 50
    fig, ax = plt.subplots(figsize=panel(W, H))
    vals = [T.loc[T.Group == g, col].values for g in GRP]
    box_points(ax, GRP, vals, [GCOL[g] for g in GRP])
    F, pF = stats.f_oneway(*vals)
    pairs = [(0, 1), (0, 2), (1, 2)]
    ps = [stats.ttest_ind(vals[i], vals[j], equal_var=False).pvalue for i, j in pairs]
    qs = multipletests(ps, method='fdr_bh')[1]
    ad_stats.append(dict(panel=stem, measure=col[:-2], F=round(float(F), 3),
                         p_anova=float(f'{pF:.3g}'),
                         **{f'{GRP[i]}_vs_{GRP[j]}_p': float(f'{ps[k]:.3g}')
                            for k, (i, j) in enumerate(pairs)},
                         **{f'{GRP[i]}_vs_{GRP[j]}_q': float(f'{qs[k]:.3g}')
                            for k, (i, j) in enumerate(pairs)}))
    lo = min(v.min() for v in vals); hi = max(v.max() for v in vals)
    step = (hi - lo) * .12
    y = hi + step * .6
    for k, (i, j) in enumerate(pairs):            # brackets only where q < 0.05
        sg = star(qs[k])
        if sg is None:
            continue
        ax.plot([i, i, j, j], [y, y + step * .25, y + step * .25, y], color='black',
                lw=LW, clip_on=False)
        ax.text((i + j) / 2, y + step * .3, sg, ha='center', va='bottom',
                fontsize=ANNOT_PT)
        y += step * .95
    ax.set_ylim(lo - step * .5, max(y, hi + step))
    ax.set_xticks(range(len(GRP)))
    ax.set_xticklabels(['HC', 'High-\nsymptom', 'Patient'], fontsize=TICK_PT)
    ax.set_xlim(-.6, len(GRP) - .4)
    ax.set_ylabel(ylab)
    panel_title(ax, ttl)
    enforce(fig); save(fig, stem, W, H, 'fig4_subject_level_n288.csv')
pd.DataFrame(ad_stats).to_csv(f'{D}/fig4ad_group_stats.csv', index=False)

# ------- e  group distributions before and after perturbation ---------------
# The point of this panel is NOT that the whole cohort moves, but that the
# HC / patient separation present at baseline is gone after either
# perturbation.  Four densities of the same residualised NP factor used in
# a-d, one small axis per condition, three group curves in each.
ECOND = [('empirical_r', 'Empirical'), ('simulated_r', 'Simulated baseline'),
         ('ampa_r', 'After AMPA'), ('gaba_r', 'After GABA-A')]
W, H = 180, 46
fig, axes = plt.subplots(1, 4, figsize=panel(W, H), sharey=True,
                         gridspec_kw=dict(wspace=.22))
for ax, (col, lab) in zip(axes, ECOND):
    xs = np.linspace(T[col].min() - .5, T[col].max() + .5, 400)
    # HC and high-symptom nearly coincide in the simulated condition, so the
    # middle group is dashed and HC is drawn last -- otherwise the grey curve
    # disappears under the gold one.
    GLS = {'HC': '-', 'High-symptom': (0, (3.0, 1.6)), 'Patient': '-'}
    for g in ['High-symptom', 'Patient', 'HC']:
        v = T.loc[T.Group == g, col].values
        kde = gaussian_kde(v)
        ax.plot(xs, kde(xs), color=GCOL[g], lw=LW * 1.6, ls=GLS[g],
                zorder=3 if g != 'HC' else 4, label=g)
        ax.plot([v.mean()] * 2, [0, kde(v.mean())[0]], color=GCOL[g], lw=LW,
                ls=(0, (1.2, 1.2)), zorder=2)
    hc = T.loc[T.Group == 'HC', col].values
    pt = T.loc[T.Group == 'Patient', col].values
    t_, p_ = stats.ttest_ind(hc, pt, equal_var=False)
    d_ = (hc.mean() - pt.mean()) / np.sqrt((hc.var(ddof=1) + pt.var(ddof=1)) / 2)
    ax.set_xlim(xs[0], xs[-1])
    ax.set_xlabel('NP factor')
    panel_title(ax, lab)
    ax.text(.03, .97, f'HC vs patient\n$d$ = {d_:+.2f}, $P$ = {p_:.2g}',
            transform=ax.transAxes, ha='left', va='top', fontsize=ANNOT_PT,
            color='0.35')
axes[0].set_ylabel('Density')
_ymax = max(l.get_ydata().max() for ax in axes for l in ax.get_lines())
axes[0].set_ylim(0, _ymax * 1.30)        # headroom so the annotation clears the curves
_h4, _l4 = axes[-1].get_legend_handles_labels()
_hl = dict(zip(_l4, _h4))
axes[-1].legend([_hl[g] for g in GRP], GRP, loc='center right', fontsize=ANNOT_PT,
                handletextpad=.5, labelspacing=.3, borderaxespad=.2, frameon=False)
enforce(fig); save(fig, 'fig4e_density', W, H, 'fig4_subject_level_n288.csv')

# ------- e  the claim itself: HC - patient effect size across conditions -----
# a-d show the data condition by condition; this panel shows the quantity the
# claim is about -- how the HC/patient separation changes once the twins are
# perturbed -- with 95% CIs, so "no longer detectable" is not read as "equal".
EM = [('empirical', 'Empirical', C('baseline'), True),
      ('simulated', 'Simulated\nbaseline', C('baseline'), False),
      ('ampa', 'After\nAMPA', C('ampa'), False),
      ('gaba', 'After\nGABA-A', C('gaba'), False)]
W, H = 66, 50
fig, ax = plt.subplots(figsize=panel(W, H))
erows = []
for i, (c_, lab, col, open_) in enumerate(EM):
    hc = T.loc[T.Group == 'HC', c_ + '_r'].values
    pt = T.loc[T.Group == 'Patient', c_ + '_r'].values
    n1, n2 = len(hc), len(pt)
    sp_ = np.sqrt(((n1 - 1) * hc.var(ddof=1) + (n2 - 1) * pt.var(ddof=1)) / (n1 + n2 - 2))
    dd = (hc.mean() - pt.mean()) / sp_
    se = np.sqrt((n1 + n2) / (n1 * n2) + dd ** 2 / (2 * (n1 + n2)))
    t_, p_ = stats.ttest_ind(hc, pt, equal_var=False)
    erows.append(dict(condition=lab.replace('\n', ' '), n_hc=n1, n_patient=n2,
                      cohens_d=round(float(dd), 3),
                      ci_lo=round(float(dd - 1.96 * se), 3),
                      ci_hi=round(float(dd + 1.96 * se), 3),
                      t=round(float(t_), 3), p=float(f'{p_:.3g}')))
    ax.vlines(i, dd - 1.96 * se, dd + 1.96 * se, color=col, lw=LW, zorder=2)
    ax.plot([i - .13, i + .13], [dd - 1.96 * se] * 2, color=col, lw=LW, zorder=2)
    ax.plot([i - .13, i + .13], [dd + 1.96 * se] * 2, color=col, lw=LW, zorder=2)
    ax.scatter([i], [dd], s=13, facecolor='white' if open_ else col,
               edgecolor=col, linewidth=LW, zorder=4)
    ax.text(i - .32 if i == 0 else i, dd + 1.96 * se + .05,   # keep the first
            f'$P$ = {p_:.2g}', ha='left' if i == 0 else 'center',  # label inside
            va='bottom', fontsize=ANNOT_PT, color='0.35')
E4 = pd.DataFrame(erows)
E4.to_csv(f'{D}/fig4e_effect_size.csv', index=False)
ax.plot(range(len(EM)), E4.cohens_d, color='0.6', lw=LW, zorder=1)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_xticks(range(len(EM)))
ax.set_xticklabels([e[1] for e in EM], fontsize=TICK_PT)
ax.set_xlim(-.5, len(EM) - .5)
ax.set_ylim(min(E4.ci_lo) - .12, max(E4.ci_hi) + .28)
ax.set_ylabel("Cohen's $d$ (HC − patient)")
hEM = [Line2D([], [], marker='o', linestyle='none', markersize=3.2,
              markerfacecolor='white', markeredgecolor=C('baseline'),
              markeredgewidth=LW),
       Line2D([], [], marker='o', linestyle='none', markersize=3.2,
              markerfacecolor=C('baseline'), markeredgecolor=C('baseline'),
              markeredgewidth=LW)]
ax.legend(hEM, ['empirical', 'simulated'], loc='lower left', fontsize=ANNOT_PT,
          handletextpad=.4, borderaxespad=.2, frameon=False)
panel_title(ax, 'The HC–patient separation is no longer detectable')
enforce(fig); save(fig, 'fig4e', W, H, 'fig4_subject_level_n288.csv')

# ------------------------------------- f  per-twin response, AMPA vs GABA-A --
W, H = 62, 60
fig, ax = plt.subplots(figsize=panel(W, H))
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.axvline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
for pat in PAT:
    sub = T[T.pattern == pat]
    ax.scatter(sub.d_ampa, sub.d_gaba, s=13, facecolor=PCOL[pat],
               edgecolor='#6E3A54' if pat == 'any down' else 'none', linewidth=LW * .55,
               alpha=.9, zorder=3, label=f'{pat} (n = {len(sub)})')
def lims(v, pad=.08):                      # data range, zero always visible
    lo, hi = float(v.min()), float(v.max()); r = hi - lo
    return min(lo - pad * r, 0), max(hi + pad * r, 0)
ax.set_xlim(*lims(T.d_ampa)); ax.set_ylim(*lims(T.d_gaba))
ax.set_xlabel('Δ NP after AMPA'); ax.set_ylabel('Δ NP after GABA-A')
ax.legend(loc='lower right', fontsize=ANNOT_PT, handletextpad=.3, borderaxespad=.2,
          markerscale=1.6)
panel_title(ax, f'{int((T.pattern == "both up").sum())} of 288 twins increase '
                'under both')
enforce(fig); save(fig, 'fig4f', W, H, 'fig4_subject_level_n288.csv')

# ---------------------- g  who responds, and where they start ----------------
W, H = 100, 50
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=panel(W, H),
                               gridspec_kw=dict(width_ratios=[1.6, 1], wspace=.45))
ct = pd.crosstab(T.Group, T.pattern).loc[GRP, PAT]
frac = ct.div(ct.sum(1), axis=0) * 100
bottom = np.zeros(len(GRP))
for pat in PAT:
    ax1.bar(np.arange(len(GRP)), frac[pat].values, bottom=bottom, width=.62,
            facecolor=PCOL[pat], edgecolor='black', linewidth=LW, zorder=2,
            label=pat)
    bottom += frac[pat].values
for i, g in enumerate(GRP):
    ax1.text(i, 102, f'{ct.loc[g, "both up"]}/{ct.loc[g].sum()}', ha='center',
             fontsize=ANNOT_PT, color='0.35')
chi2, pchi, dof, _ = stats.chi2_contingency(ct.values)
ax1.set_xticks(range(len(GRP)))
ax1.set_xticklabels(['HC', 'High-\nsymptom', 'Patient'], fontsize=TICK_PT)
ax1.set_xlim(-.6, len(GRP) + .55); ax1.set_ylim(0, 122)
ax1.set_yticks([0, 50, 100])
ax1.set_ylabel('Twins (%)')
# segments named beside the last bar instead of in a legend box
_h = frac.loc['Patient']
ax1.text(2.45, _h['both up'] / 2, 'both up', ha='left', va='center',
         fontsize=ANNOT_PT, color=PCOL['both up'])
ax1.text(2.45, _h['both up'] + _h['any down'] / 2, 'any down', ha='left',
         va='center', fontsize=ANNOT_PT, color=PCOL['any down'])
ax1.text(1.0, 112, f'χ² = {chi2:.1f}, P = {pchi:.1e}', ha='center',
         fontsize=ANNOT_PT, color='0.35')

vals = [T.loc[T.pattern == p, 'simulated'].values for p in PAT]
box_points(ax2, PAT, vals, [PCOL[p] for p in PAT], s=9.0, seed=1)
tb, pb = stats.ttest_ind(*vals, equal_var=False)
ax2.set_xticks(range(len(PAT)))
ax2.set_xticklabels(['both\nup', 'any\ndown'], fontsize=TICK_PT)
ax2.set_xlim(-.6, len(PAT) - .4)
ax2.set_ylabel('Simulated baseline NP')
hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
ax2.plot([0, 0, 1, 1], [hi + .3, hi + .5, hi + .5, hi + .3], color='black', lw=LW)
ax2.text(.5, hi + .55, f'P = {pb:.0e}', ha='center', va='bottom', fontsize=ANNOT_PT)
ax2.set_ylim(lo - .3, hi + 1.4)
fig.suptitle('Responders are more often patients, and start lower',
             fontsize=LABEL_PT, x=.02, y=1.0, ha='left')
enforce(fig); save(fig, 'fig4g', W, H, 'fig4_subject_level_n288.csv')

# ------------------------ h  symptoms between the response groups ------------
# Two ways of splitting the cohort are drawn: the joint pattern (both
# perturbations up vs at least one down) and the AMPA direction alone.
# Significance is the nominal Mann-Whitney P (no multiplicity correction, at
# the author's request); BH q is kept in the accompanying CSV.
S = S.merge(T[['ID', 'd_ampa']], on='ID')
SPLITS = [('fig4h', 'pattern', 'both up', 'any down', 'both up', 'any down'),
          ('fig4h_ampa', 'ampa_dir', 'AMPA up', 'AMPA down', 'AMPA up', 'AMPA down')]
S['ampa_dir'] = np.where(S.d_ampa > 0, 'AMPA up', 'AMPA down')
for stem, key, up, dn, lab_up, lab_dn in SPLITS:
    rows = []
    for it in SDQ:
        x = S.loc[S[key] == up, it].astype(float)
        y = S.loc[S[key] == dn, it].astype(float)
        u, pu = stats.mannwhitneyu(x, y, alternative='two-sided')
        n1, n2 = len(x), len(y)
        sp = np.sqrt(((n1 - 1) * x.var(ddof=1) + (n2 - 1) * y.var(ddof=1)) / (n1 + n2 - 2))
        gg = (x.mean() - y.mean()) / sp * (1 - 3 / (4 * (n1 + n2) - 9))
        se = np.sqrt((n1 + n2) / (n1 * n2) + gg ** 2 / (2 * (n1 + n2)))
        rows.append(dict(item=it, split=f'{lab_up} vs {lab_dn}', n_up=n1, n_down=n2,
                         mean_up=round(x.mean(), 3), mean_down=round(y.mean(), 3),
                         hedges_g=round(gg, 3), ci_lo=round(gg - 1.96 * se, 3),
                         ci_hi=round(gg + 1.96 * se, 3), U=float(u),
                         p_mw=float(f'{pu:.3g}')))
    H4 = pd.DataFrame(rows)
    H4['q_bh'] = multipletests(H4.p_mw, method='fdr_bh')[1].round(4)
    H4 = H4.sort_values('hedges_g').reset_index(drop=True)
    H4.to_csv(f'{D}/{stem}_sdq_stats.csv', index=False)

    W, H = 180, 58           # 8-10 pt type and 25 rotated item labels
    fig, ax = plt.subplots(figsize=panel(W, H))
    x = np.arange(len(H4))
    sig = (H4.p_mw < .05).values          # nominal P, no multiplicity correction
    cols = [PCOL['both up'] if v > 0 else PCOL['any down'] for v in H4.hedges_g]
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    for i in range(len(H4)):
        ax.vlines(x[i], H4.ci_lo[i], H4.ci_hi[i], color=cols[i], lw=LW, zorder=2)
    ax.scatter(x[sig], H4.hedges_g[sig], s=16,
               facecolor=[c for c, m in zip(cols, sig) if m],
               edgecolor=[c for c, m in zip(cols, sig) if m], linewidth=LW, zorder=3)
    ax.scatter(x[~sig], H4.hedges_g[~sig], s=16, facecolor='white',
               edgecolor=[c for c, m in zip(cols, ~sig) if m], linewidth=LW, zorder=3)
    ylo_lab = float(H4.ci_lo.min())
    for k, i in enumerate(np.where(sig)[0]):   # name the items reaching P < 0.05,
        ax.text(x[i] + .25, ylo_lab - .03 - .10 * k,   # stacked so labels never
                f'P = {H4.p_mw[i]:.3g}', ha='left',    # overlap when adjacent
                va='top', fontsize=PK.ANNOT_PT, color=cols[i])
    ax.set_ylim(float(H4.ci_lo.min()) - .10 * max(1, int(sig.sum())) - .10,
                float(H4.ci_hi.max()) + .16)
    ax.set_xticks(x)
    ax.set_xticklabels(H4.item, fontsize=PK.TICK_PT, rotation=45, ha='right')
    ax.tick_params(axis='y', labelsize=PK.TICK_PT)
    ax.set_xlim(-.7, len(H4) - .3)
    ax.set_ylabel("Hedges' $g$\n" + f'({lab_up} \u2212 {lab_dn})',
                  fontsize=PK.LABEL_PT)
    handles = [Patch(facecolor=PCOL['both up'], edgecolor='none'),
               Patch(facecolor=PCOL['any down'], edgecolor='none'),
               Line2D([], [], marker='o', linestyle='none', markersize=3.2,
                      markerfacecolor='white', markeredgecolor='0.4',
                      markeredgewidth=LW)]
    ax.legend(handles, [f'higher in "{lab_up}"', f'higher in "{lab_dn}"',
                       'P \u2265 0.05'],
              loc='upper left', ncol=3, fontsize=PK.ANNOT_PT, handletextpad=.4,
              columnspacing=1.0, borderaxespad=.2)
    _s = H4.item[sig].tolist()
    # no declarative panel title: the group sizes, the named items and the
    # uncorrected-P caveat belong in the legend (house rule)
    enforce(fig); save(fig, stem, W, H, 'fig4_sdq_items_n287.csv')
    print(f'{stem}: ' + ', '.join(f'{i} (P={q:.3g}, g={g:.2f})'
          for i, q, g in zip(H4.item[sig], H4.p_mw[sig], H4.hedges_g[sig])))


# --------------- h (alt)  DAWBA symptom domains between the response groups --
# Six DAWBA band scores (ADHD, conduct, eating, depression, generalised anxiety,
# social phobia) and their sum, for the 284 twins with symptom data.  Same
# split logic and same nominal-P marking as the SDQ panel; BH q across the
# seven measures is kept in the CSV and annotated where it survives.
DW = pd.read_csv(f'{D}/fig4_dawba_domains_n284.csv')
MEAS = ['adhd', 'cd', 'eat', 'dep', 'gad', 'sp', 'sym6_sum']
MLABEL = {'adhd': 'ADHD', 'cd': 'Conduct', 'eat': 'Eating', 'dep': 'Depression',
          'gad': 'Gen. anxiety', 'sp': 'Social phobia', 'sym6_sum': 'Sum of 6'}
for stem, key, up, dn in [('fig4h_dawba', 'ampa_dir', 'AMPA up', 'AMPA down'),
                          ('fig4h_dawba_pattern', 'pattern', 'both up', 'any down')]:
    rows = []
    for m in MEAS:
        xx = DW.loc[DW[key] == up, m].astype(float)
        yy = DW.loc[DW[key] == dn, m].astype(float)
        u, pu = stats.mannwhitneyu(xx, yy, alternative='two-sided')
        n1, n2 = len(xx), len(yy)
        sp_ = np.sqrt(((n1 - 1) * xx.var(ddof=1) + (n2 - 1) * yy.var(ddof=1)) / (n1 + n2 - 2))
        gg = (xx.mean() - yy.mean()) / sp_ * (1 - 3 / (4 * (n1 + n2) - 9))
        se = np.sqrt((n1 + n2) / (n1 * n2) + gg ** 2 / (2 * (n1 + n2)))
        rows.append(dict(measure=m, split=f'{up} vs {dn}', n_up=n1, n_down=n2,
                         mean_up=round(xx.mean(), 3), mean_down=round(yy.mean(), 3),
                         hedges_g=round(gg, 3), ci_lo=round(gg - 1.96 * se, 3),
                         ci_hi=round(gg + 1.96 * se, 3), U=float(u),
                         p_mw=float(f'{pu:.3g}')))
    DT = pd.DataFrame(rows)
    DT['q_bh'] = multipletests(DT.p_mw, method='fdr_bh')[1].round(4)
    DT.to_csv(f'{D}/{stem}_stats.csv', index=False)

    W, H = 86, 50
    fig, ax = plt.subplots(figsize=panel(W, H))
    xx = np.arange(len(DT))
    sg = (DT.p_mw < .05).values
    cols = [PCOL['both up'] if v > 0 else PCOL['any down'] for v in DT.hedges_g]
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    ax.axvline(len(MEAS) - 1.5, color='0.85', lw=LW, zorder=0)
    for i in range(len(DT)):
        ax.vlines(xx[i], DT.ci_lo[i], DT.ci_hi[i], color=cols[i], lw=LW, zorder=2)
    ax.scatter(xx[sg], DT.hedges_g[sg], s=10, facecolor=[c for c, m in zip(cols, sg) if m],
               edgecolor=[c for c, m in zip(cols, sg) if m], linewidth=LW, zorder=3)
    ax.scatter(xx[~sg], DT.hedges_g[~sg], s=10, facecolor='white',
               edgecolor=[c for c, m in zip(cols, ~sg) if m], linewidth=LW, zorder=3)
    for i in np.where(sg)[0]:
        lab = f'P = {DT.p_mw[i]:.3g}'
        if DT.q_bh[i] < .05:
            lab += f', q = {DT.q_bh[i]:.3g}'
        ax.text(xx[i] + .18, DT.ci_lo[i] - .03, lab, ha='left', va='top',
                fontsize=ANNOT_PT, color=cols[i])
    ax.set_xticks(xx)
    ax.set_xticklabels([MLABEL[m] for m in DT.measure], fontsize=TICK_PT,
                       rotation=45, ha='right')
    ax.set_xlim(-.7, len(DT) - .3)
    ax.set_ylim(float(DT.ci_lo.min()) - .30, float(DT.ci_hi.max()) + .16)
    ax.set_ylabel("Hedges' g\n" + f'({up} − {dn})')
    panel_title(ax, f'{up} (n = {DT.n_up[0]}) vs {dn} (n = {DT.n_down[0]}): '
                    'DAWBA symptom domains')
    enforce(fig); save(fig, stem, W, H, 'fig4_dawba_domains_n284.csv')
    print(f'{stem}: ' + ', '.join(f'{m} (P={q:.3g}, q={qq:.3g}, g={g:.2f})'
          for m, q, qq, g in zip(DT.measure[sg], DT.p_mw[sg], DT.q_bh[sg],
                                 DT.hedges_g[sg])))


# ------------- i  paired tests: baseline vs perturbed, NP and MID sums -------
# Per-twin paired comparison of the simulated baseline against each virtual
# perturbation, for the full 12-edge NP factor and for the 6 MID edges alone
# (NP = SST sum + MID sum, so the MID panel is a subset of the NP panel).
PD = pd.read_csv(f'{D}/fig4_paired_np_mid_n288.csv')
CONDS = [('baseline', 'Baseline', C('baseline')), ('ampa', '+AMPA', C('ampa')),
         ('gaba', '+GABA-A', C('gaba'))]
PMEAS = [('np', 'NP factor (12 edges)'), ('mid', 'MID summed FC (6 edges)')]
PAIR_POINTS = False        # False = no jittered per-twin points
PAIR_LINES  = False        # at n = 288 the 576 connecting strokes carry no
                           # readable information; boxes + paired stats instead
W, H = 110, 56
fig, axes = plt.subplots(1, 2, figsize=panel(W, H), gridspec_kw=dict(wspace=.42))
prows = []
rng = np.random.default_rng(4)
for ax, (meas, mlab) in zip(axes, PMEAS):
    vals = [PD[f'{meas}_{k}'].values for k, _, _ in CONDS]
    if PAIR_LINES:                                        # per-twin pairing
        for j, (k, _, col) in enumerate(CONDS[1:], start=1):
            for y0, y1 in zip(vals[0], vals[j]):
                ax.plot([0, j], [y0, y1], color=col, lw=LW * .6, alpha=.10, zorder=1)
    bp = ax.boxplot(vals, positions=np.arange(3), widths=.5, showfliers=False,
                    patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    if PAIR_POINTS:            # the connecting lines already show every twin,
        for j, (k, _, col) in enumerate(CONDS):     # so the points are optional
            ax.scatter(j + rng.uniform(-.11, .11, len(vals[j])), vals[j], s=2.6,
                       facecolor=col, edgecolor='none', alpha=.7, zorder=3)
    else:                      # colour the box instead, so the condition is still
        for j, (k, _, col) in enumerate(CONDS):     # identifiable without points.
            rgb = np.array(plt.matplotlib.colors.to_rgb(col))   # opaque light tint
            bp['boxes'][j].set_facecolor(tuple(1 - .42 * (1 - rgb)))  # so the lines
            bp['boxes'][j].set_zorder(2.5)                            # don't muddy it
            for el in ('whiskers', 'caps', 'medians'):
                for art in bp[el]:
                    art.set_zorder(2.6)
    hi = max(v.max() for v in vals); lo = min(v.min() for v in vals)
    step = (hi - lo) * .12
    y = hi + step * .4
    for j, (k, _, col) in enumerate(CONDS[1:], start=1):
        t_, p_ = stats.ttest_rel(vals[j], vals[0])
        dd = vals[j] - vals[0]
        w_, pw = stats.wilcoxon(vals[j], vals[0])
        prows.append(dict(measure=mlab, perturbation=CONDS[j][1].lstrip('+'),
                          n=len(dd), mean_baseline=round(vals[0].mean(), 4),
                          mean_modulated=round(vals[j].mean(), 4),
                          mean_diff=round(dd.mean(), 4), sd_diff=round(dd.std(ddof=1), 4),
                          n_increased=int((dd > 0).sum()),
                          pct_increased=round(100 * (dd > 0).mean(), 1),
                          t=round(float(t_), 3), df=len(dd) - 1,
                          p_paired_t=float(f'{p_:.3g}'), wilcoxon_p=float(f'{pw:.3g}'),
                          cohens_dz=round(float(dd.mean() / dd.std(ddof=1)), 3)))
        ax.plot([0, 0, j, j], [y, y + step * .3, y + step * .3, y], color='black', lw=LW)
        ax.text(1.0, y + step * .38,   # centred on the axis, clear of the y labels
                f'$t$({len(dd)-1}) = {t_:.1f}, $P$ = {p_:.0e}\n$d_z$ = '
                f'{dd.mean()/dd.std(ddof=1):.2f}, {100*(dd>0).mean():.0f}% up',
                ha='center', va='bottom', fontsize=ANNOT_PT)
        y += step * 2.5
    ax.set_ylim(lo - step * .4, y + step * .2)
    ax.set_xticks(range(3)); ax.set_xticklabels([c[1] for c in CONDS], fontsize=TICK_PT)
    ax.set_xlim(-.6, 2.6)
    ax.set_ylabel(mlab)
    panel_title(ax, {'np': 'Whole 12-edge NP factor',
                     'mid': 'MID edges only (6 of the 12)'}[meas])
PTT = pd.DataFrame(prows)
PTT.to_csv(f'{D}/fig4i_paired_stats.csv', index=False)
enforce(fig); save(fig, 'fig4i', W, H, 'fig4_paired_np_mid_n288.csv')
print(PTT.to_string(index=False))


# ------- j  baseline vs change: three views of the same AMPA response --------
# Naive baseline-vs-change, Oldham (mean-vs-change) and the regression of the
# perturbed value on baseline.  They answer DIFFERENT questions, which is why
# they disagree; see fig4j_baseline_change_stats.csv for both perturbations.
PDj = pd.read_csv(f'{D}/fig4_paired_np_mid_n288.csv')
jrows = []
for drug in ['ampa', 'gaba']:
    pre = PDj.np_baseline.values; post = PDj[f'np_{drug}'].values
    dlt = post - pre; mn = (pre + post) / 2
    Xj = sm.add_constant(pre); mj = sm.OLS(post, Xj).fit()
    b, se = float(mj.params[1]), float(mj.bse[1]); ci = mj.conf_int()[1]
    t1 = (b - 1) / se; p1 = 2 * stats.t.sf(abs(t1), mj.df_resid)
    r_n, p_n = stats.pearsonr(pre, dlt)
    r_o, p_o = stats.pearsonr(mn, dlt)
    r_pp, _ = stats.pearsonr(pre, post)
    jrows.append(dict(perturbation=drug.upper(), n=len(pre),
                      r_naive=round(float(r_n), 4), p_naive=float(f'{p_n:.3g}'),
                      r_oldham=round(float(r_o), 4), p_oldham=float(f'{p_o:.3g}'),
                      r_pre_post=round(float(r_pp), 4),
                      slope_post_on_pre=round(b, 4), slope_se=round(se, 4),
                      slope_ci_lo=round(float(ci[0]), 4), slope_ci_hi=round(float(ci[1]), 4),
                      t_slope_vs_1=round(float(t1), 3), p_slope_vs_1=float(f'{p1:.3g}'),
                      sd_baseline=round(float(pre.std(ddof=1)), 4),
                      sd_perturbed=round(float(post.std(ddof=1)), 4),
                      var_ratio=round(float(post.var(ddof=1) / pre.var(ddof=1)), 4)))
J = pd.DataFrame(jrows)
J.to_csv(f'{D}/fig4j_baseline_change_stats.csv', index=False)

DRUGJ = 'ampa'
pre = PDj.np_baseline.values; post = PDj[f'np_{DRUGJ}'].values
dlt = post - pre; mn = (pre + post) / 2
jc = C(DRUGJ)
j0 = J[J.perturbation == DRUGJ.upper()].iloc[0]
W, H = 170, 52
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=panel(W, H),
                                 gridspec_kw=dict(wspace=.42))

# (1) the interpretable view: perturbed value on baseline, against identity
a1.scatter(pre, post, s=4, facecolor=jc, edgecolor='none', alpha=.8, zorder=3)
lim = [min(pre.min(), post.min()) - .3, max(pre.max(), post.max()) + .3]
a1.plot(lim, lim, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
xx = np.linspace(pre.min(), pre.max(), 50)
a1.plot(xx, j0.slope_post_on_pre * xx + float(sm.OLS(post, sm.add_constant(pre)).fit().params[0]),
        color='black', lw=LW, zorder=4)
a1.set_xlim(*lim); a1.set_ylim(*lim)
a1.set_xlabel('Baseline NP'); a1.set_ylabel('NP after AMPA')
a1.text(.04, .96, f'slope = {j0.slope_post_on_pre:.2f}\n'
        f'(95% CI {j0.slope_ci_lo:.2f}–{j0.slope_ci_hi:.2f})\n'
        f'vs 1: $P$ = {j0.p_slope_vs_1:.0e}', transform=a1.transAxes, ha='left',
        va='top', fontsize=ANNOT_PT, color='0.35')
panel_title(a1, 'Perturbed value vs baseline')

# (2) what was asked for: baseline vs change
a2.scatter(pre, dlt, s=4, facecolor=jc, edgecolor='none', alpha=.8, zorder=3)
a2.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
sl2 = np.polyfit(pre, dlt, 1)
a2.plot(xx, np.polyval(sl2, xx), color='black', lw=LW, zorder=4)
a2.set_xlabel('Baseline NP'); a2.set_ylabel('Δ NP (AMPA − baseline)')
a2.text(.04, .96, f'$r$ = {j0.r_naive:.2f}, $P$ = {j0.p_naive:.0e}\n'
        '(same $P$ as slope vs 1)', transform=a2.transAxes, ha='left', va='top',
        fontsize=ANNOT_PT, color='0.35')
panel_title(a2, 'Baseline vs change (naive)')

# (3) Oldham / Pitman-Morgan: mean vs change = a paired variance test
a3.scatter(mn, dlt, s=4, facecolor=jc, edgecolor='none', alpha=.8, zorder=3)
a3.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
xm = np.linspace(mn.min(), mn.max(), 50)
a3.plot(xm, np.polyval(np.polyfit(mn, dlt, 1), xm), color='black', lw=LW, zorder=4)
a3.set_xlabel('Mean of baseline and AMPA'); a3.set_ylabel('Δ NP (AMPA − baseline)')
a3.text(.04, .96, f'$r$ = {j0.r_oldham:.2f}, $P$ = {j0.p_oldham:.0e}\n'
        f's.d. {j0.sd_baseline:.2f} → {j0.sd_perturbed:.2f}\n'
        f'(variance ratio {j0.var_ratio:.2f})', transform=a3.transAxes, ha='left',
        va='top', fontsize=ANNOT_PT, color='0.35')
panel_title(a3, 'Oldham: mean vs change')
enforce(fig); save(fig, 'fig4j', W, H, 'fig4_paired_np_mid_n288.csv')
print(J.to_string(index=False))

mf = pd.DataFrame(manifest)
mf.to_csv(f'{OUTD}/fig4_panel_manifest.csv', index=False)
print(mf.to_string(index=False))
print('\na-d group stats')
print(pd.DataFrame(ad_stats).to_string(index=False))
print(f'\nf  both up {int((T.pattern == "both up").sum())} / any down '
      f'{int((T.pattern == "any down").sum())}')
print(f'g  chi2 = {chi2:.2f}, P = {pchi:.3g}; baseline NP '
      f'{vals[0].mean():.3f} vs {vals[1].mean():.3f}, t = {tb:.2f}, P = {pb:.3g}')
