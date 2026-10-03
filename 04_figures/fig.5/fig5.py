"""Figure 5 | In vivo pharmacology and longitudinal prediction.

ONE FILE PER PANEL -> ./panels/ as .png (400 dpi), .pdf and .pptx.

  a   healthy cohort (n = 27): summed MID FC under placebo, ketamine and
      midazolam, split by the two k-means response subgroups
  b   the same cohort, change from placebo            } same panel grammar
  d   MDD vs HC, ketamine-induced change in NP FC     } (change panels)
  c   placebo (drug-free) level of the two subgroups  } same panel grammar
  e   placebo level of MDD vs HC                      } (level panels)
  f   MDD: NP change vs symptom change, both residualised on baseline
  g   MDD: similarity of the ketamine state to the AMPA-perturbed digital twin
      vs MADRS change
  h1  IMAGEN follow-up (n = 85): added-variable plot for the AMPA restoration
      index over a model containing the four baseline behaviour scores
  h2  the same increment against its permutation null, and against the GABA-A
      restoration index (specificity)

Colours (../fig_color/np_dtb_style.py).  One referent per colour within this
figure, with a single documented exception: grey is "the reference condition"
throughout the manuscript, so it marks placebo in a and the healthy control
group in d/e.  ketamine/AMPA #E1D09A, midazolam/GABA-A #96B9AD, MDD #D55E00,
response subgroups dark/pale plum #8C4A6B / #E8C4D2.

    cd revision/text/figures/fig.5 && python fig5.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx

D = os.path.join(HERE, 'fig5_data')
OUTD = os.path.join(HERE, 'panels')
os.makedirs(OUTD, exist_ok=True)
DPI = 400
apply_np_style()

HC27 = pd.read_csv(f'{D}/fig5_healthy_n27.csv')
PH36 = pd.read_csv(f'{D}/fig5_mdd_hc_n36.csv')
F22 = pd.read_csv(f'{D}/fig5f_np_symptom_resid_MDD_n22.csv')
G22 = pd.read_csv(f'{D}/fig5g_state_similarity_MDD_n22.csv')
AV85 = pd.read_csv(f'{D}/fig5h_added_variable_n85.csv')
NEST = pd.read_csv(f'{D}/fig5h_nested_models.csv')
DNULL = pd.read_csv(f'{D}/fig5h_deltaR2_null.csv')

def adj_group_t(df, y):
    """Group coefficient of y on group + age + sex + infusion order + placebo-
    session mean FD -- the model the main text reports for the clinical cohort
    (New_pharma_dataset/supplementary_methods.md section 3.4).  Returns
    (coefficient, t, P, residual df)."""
    import statsmodels.formula.api as smf
    d = df.assign(grp=(df.group == 'MDD').astype(int))
    m = smf.ols(f'{y} ~ grp + age + sexM + fd_p2 + drug_first', data=d).fit()
    return (float(m.params['grp']), float(m.tvalues['grp']),
            float(m.pvalues['grp']), int(m.df_resid))


SUBG = ['increasers', 'decreasers']
SCOL = {'increasers': C('increased'), 'decreasers': C('decreased')}
DRUG = [('Placebo', C('placebo')), ('Ketamine', C('ketamine')),
        ('Midazolam', C('midazolam'))]
GCOL = {'HC': C('hc'), 'MDD': C('mdd')}
S_BOX, S_SCAT = 13.0, 22.0            # point areas: boxes / scatter panels
manifest, stats_rows = [], []


def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}',
                         dpi=round(px[0] / (w_mm / 25.4)), source=note))
    plt.close(fig)


# ---- shared drawing grammar -------------------------------------------------
def _lum(col):
    r, g, b = mcolors.to_rgb(col)
    return .2126 * r + .7152 * g + .0722 * b


def _fill(col):
    """Pale colours are used as-is; saturated ones are tinted so the black box
    outline and the points on top stay legible."""
    rgb = np.array(mcolors.to_rgb(col))
    f = .35 if _lum(col) > .70 else .45       # pale colours get a lighter fill so
    return tuple(1 - f * (1 - rgb))           # the two tones of a pair separate


def _pt_edge(col):
    return tuple(np.array(mcolors.to_rgb(col)) * .55) if _lum(col) > .70 else 'none'


def stars(p):
    return '***' if p < .001 else '**' if p < .01 else '*' if p < .05 else ''


def boxes(ax, positions, values, colours, width=.62, jitter=.15, seed=0, s=S_BOX):
    """Box + all individual points, filled by the group colour."""
    bp = ax.boxplot(values, positions=positions, widths=width, showfliers=False,
                    patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
    rng = np.random.default_rng(seed)
    for i, v in enumerate(values):
        bp['boxes'][i].set_facecolor(_fill(colours[i]))
        bp['boxes'][i].set_edgecolor('black')
        ax.scatter(positions[i] + rng.uniform(-jitter, jitter, len(v)), v, s=s,
                   facecolor=colours[i], edgecolor=_pt_edge(colours[i]),
                   linewidth=LW * .55, alpha=.9, zorder=3)
    return bp


def bracket(ax, x0, x1, y, p, dy):
    ax.plot([x0, x0, x1, x1], [y, y + dy, y + dy, y], color='black', lw=LW,
            clip_on=False, zorder=5)
    ax.text((x0 + x1) / 2, y + dy * 1.15, f'$P$ = {p:.2g}', ha='center',
            va='bottom', fontsize=ANNOT_PT, clip_on=False, zorder=5)


def change_panel(ax, blocks, ylabel, zero_ref=True, seed=0, p_between=None):
    """b and d share this grammar: one block per drug, two contrasted groups of
    subjects inside each block, change from the drug-free condition on y.
    Asterisks = one-sample test against zero; bracket = between-group test."""
    pos, vals, cols, ticks, tlabs, blocklab = [], [], [], [], [], []
    x = 0.0
    for bl, entries in blocks:
        first = x
        for lab, v, col in entries:
            pos.append(x); vals.append(v); cols.append(col)
            ticks.append(x); tlabs.append(lab); x += 1.0
        blocklab.append(((first + x - 1) / 2, bl))
        x += 1.35
    boxes(ax, pos, vals, cols, seed=seed)
    if zero_ref:
        ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    span = max(v.max() for v in vals) - min(v.min() for v in vals)
    for i, v in enumerate(vals):
        t_, p_ = stats.ttest_1samp(v, 0)
        if stars(p_):
            ax.text(pos[i], v.max() + span * .04, stars(p_), ha='center',
                    va='bottom', fontsize=ANNOT_PT)
    k = 0
    tops = []
    for bl, entries in blocks:
        v0, v1 = entries[0][1], entries[1][1]
        t_, p_ = stats.ttest_ind(v0, v1, equal_var=False)
        if p_between is not None:
            p_ = p_between
        y = max(v0.max(), v1.max()) + span * .13
        bracket(ax, pos[k], pos[k + 1], y, p_, span * .05)
        tops.append(y + span * .05 * 1.15 + span * .05)
        k += 2
    lo = min(v.min() for v in vals)
    ax.set_ylim(lo - span * .07, max(tops + [max(v.max() for v in vals)]) + span * .06)
    ax.set_xticks(ticks); ax.set_xticklabels(tlabs, fontsize=TICK_PT)
    ax.set_xlim(pos[0] - .75, pos[-1] + .75)
    tr = ax.get_xaxis_transform()
    yb = -.155 - .115 * (max(t.count('\n') for t in tlabs))   # clear multi-line ticks
    for xc, bl in blocklab:
        ax.text(xc, yb, bl, transform=tr, ha='center', va='top',
                fontsize=ANNOT_PT, clip_on=False)
    ax.set_ylabel(ylabel)


def level_panel(ax, labels, values, colours, ylabel, seed=0, p_between=None):
    """c and e share this grammar: the drug-free level of the same two groups."""
    pos = [0, 1]
    boxes(ax, pos, values, colours, seed=seed)
    ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    t_, p_ = stats.ttest_ind(values[0], values[1], equal_var=False)
    if p_between is not None:
        p_ = p_between
    hi = max(v.max() for v in values); lo = min(v.min() for v in values)
    span = hi - lo
    bracket(ax, 0, 1, hi + span * .08, p_, span * .05)
    ax.set_ylim(lo - span * .10, hi + span * .30)
    ax.set_xticks(pos); ax.set_xticklabels(labels, fontsize=TICK_PT)
    ax.set_xlim(-.75, 1.75)
    ax.set_ylabel(ylabel)
    return t_, p_


def scatter_fit(ax, x, y, col, spearman=False, s=S_SCAT):
    ax.scatter(x, y, s=s, facecolor=col, edgecolor=_pt_edge(col),
               linewidth=LW * .55, alpha=.9, zorder=3)
    b = np.polyfit(x, y, 1)
    xx = np.linspace(min(x), max(x), 50)
    ax.plot(xx, np.polyval(b, xx), color='black', lw=LW, zorder=4)
    return stats.spearmanr(x, y) if spearman else stats.pearsonr(x, y)


# ---- a  healthy cohort: three conditions by response subgroup --------------
W, H = 80, 54
fig, ax = plt.subplots(figsize=panel(W, H))
pos, labs, cols, vals = [], [], [], []
for gi, sg in enumerate(SUBG):
    for di, (dn, dc) in enumerate(DRUG):
        pos.append(gi * 3.9 + di); labs.append(dn[:3]); cols.append(dc)
        vals.append(HC27.loc[HC27.subgroup == sg, dn].values)
boxes(ax, pos, vals, cols, seed=0)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_xticks(pos); ax.set_xticklabels(labs, fontsize=TICK_PT)
_lo, _hi = ax.get_ylim()
ax.set_ylim(_lo, _hi + (_hi - _lo) * .16)
for gi, sg in enumerate(SUBG):
    n = int((HC27.subgroup == sg).sum())
    ax.text(gi * 3.9 + 1, _hi + (_hi - _lo) * .02, f'{sg} (n = {n})', ha='center',
            va='bottom', fontsize=ANNOT_PT, color=SCOL[sg])
ax.set_ylabel('Summed MID FC')
panel_title(ax, 'Healthy volunteers split into two response subgroups')
enforce(fig); save(fig, 'fig5a', W, H, 'fig5_healthy_n27.csv')

# ---- b  change from placebo, healthy cohort --------------------------------
W, H = 66, 54
fig, ax = plt.subplots(figsize=panel(W, H))
blocks = []
for dkey, dn in [('d_ket', 'Ketamine'), ('d_mid', 'Midazolam')]:
    entries = []
    for sg in SUBG:
        v = HC27.loc[HC27.subgroup == sg, dkey].values
        entries.append(({'increasers': 'incr.', 'decreasers': 'decr.'}[sg], v, SCOL[sg]))
        t_, p_ = stats.ttest_1samp(v, 0)
        stats_rows.append(dict(panel='b', cohort='healthy', condition=dn, group=sg,
                               n=len(v), test='one-sample t vs 0',
                               value=round(float(v.mean()), 4), stat=round(float(t_), 3),
                               p=float(f'{p_:.3g}')))
    t_, p_ = stats.ttest_ind(entries[0][1], entries[1][1], equal_var=False)
    stats_rows.append(dict(panel='b', cohort='healthy', condition=dn,
                           group='increasers vs decreasers', n=len(HC27),
                           test='Welch t', value=round(float(entries[0][1].mean() -
                                                            entries[1][1].mean()), 4),
                           stat=round(float(t_), 3), p=float(f'{p_:.3g}')))
    blocks.append((dn, entries))
change_panel(ax, blocks, 'Δ summed MID FC (drug − placebo)', seed=1)
panel_title(ax, 'The two subgroups move in opposite directions')
enforce(fig); save(fig, 'fig5b', W, H, 'fig5_healthy_n27.csv')

# ---- c  drug-free level of the two subgroups -------------------------------
W, H = 48, 54
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [HC27.loc[HC27.subgroup == s, 'Placebo'].values for s in SUBG]
t_, p_ = level_panel(ax, ['incr.', 'decr.'], vals, [SCOL[s] for s in SUBG],
                     'Placebo summed MID FC', seed=2)
stats_rows.append(dict(panel='c', cohort='healthy', condition='Placebo',
                       group='increasers vs decreasers', n=len(HC27), test='Welch t',
                       value=round(float(vals[0].mean() - vals[1].mean()), 4),
                       stat=round(float(t_), 3), p=float(f'{p_:.3g}')))
panel_title(ax, 'They start from different levels')
enforce(fig); save(fig, 'fig5c', W, H, 'fig5_healthy_n27.csv')

# ---- d  ketamine-induced change, MDD vs HC (same grammar as b) -------------
W, H = 48, 54
fig, ax = plt.subplots(figsize=panel(W, H))
entries = []
for g in ['MDD', 'HC']:                      # MDD first, matching a-c where the
                                             # increasing subgroup is on the left
    v = PH36.loc[PH36.group == g, 'FC_delta'].values
    entries.append((g, v, GCOL[g]))
    t_, p_ = stats.ttest_1samp(v, 0)
    stats_rows.append(dict(panel='d', cohort='pharmacology', condition='Ketamine',
                           group=g, n=len(v), test='one-sample t vs 0',
                           value=round(float(v.mean()), 4), stat=round(float(t_), 3),
                           p=float(f'{p_:.3g}')))
b_, t_, p_, dfr = adj_group_t(PH36, 'FC_delta')
stats_rows.append(dict(panel='d', cohort='pharmacology', condition='Ketamine',
                       group='MDD vs HC', n=len(PH36),
                       test=f'group x drug: OLS group coefficient, adjusted for '
                            f'age + sex + infusion order + placebo-session mean FD, '
                            f'df = {dfr}',
                       value=round(b_, 4), stat=round(float(t_), 3),
                       p=float(f'{p_:.3g}')))
change_panel(ax, [('Ketamine', entries)], 'Δ NP FC (ketamine − placebo)', seed=3,
             p_between=p_)
panel_title(ax, 'Opposite response direction')
enforce(fig); save(fig, 'fig5d', W, H, 'fig5_mdd_hc_n36.csv')

# ---- e  placebo level, MDD vs HC (same grammar as c) -----------------------
W, H = 48, 54
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [PH36.loc[PH36.group == g, 'FC_p2'].values for g in ['MDD', 'HC']]
b_, t_, p_, dfr = adj_group_t(PH36, 'FC_p2')
level_panel(ax, ['MDD', 'HC'], vals, [GCOL[g] for g in ['MDD', 'HC']],
            'Placebo NP FC', seed=4, p_between=p_)
stats_rows.append(dict(panel='e', cohort='pharmacology', condition='Placebo',
                       group='MDD vs HC', n=len(PH36),
                       test=f'OLS group coefficient, adjusted for age + sex + '
                            f'infusion order + placebo-session mean FD, df = {dfr}',
                       value=round(b_, 4), stat=round(float(t_), 3),
                       p=float(f'{p_:.3g}')))
panel_title(ax, 'And from different baselines')
enforce(fig); save(fig, 'fig5e', W, H, 'fig5_mdd_hc_n36.csv')

# ---- f  NP change vs symptom change (MDD) ----------------------------------
W, H = 58, 54
fig, ax = plt.subplots(figsize=panel(W, H))
r, _ = scatter_fit(ax, F22.x_NPchange_resid.values, F22.y_sympPC1change_resid.values,
                   C('mdd'))
# Both axes are residuals on four covariates (baseline severity, age, infusion
# order, placebo-session FD), so the correct residual df is n - 4 - 2, not n - 2.
_dfp = len(F22) - 4 - 2
_tp = r * np.sqrt(_dfp / (1 - r ** 2))
p = float(2 * stats.t.sf(abs(_tp), _dfp))
stats_rows.append(dict(panel='f', cohort='pharmacology', condition='Ketamine',
                       group='MDD', n=len(F22),
                       test='partial Pearson r, adjusted for baseline severity, '
                            f'age, infusion order and placebo-session mean FD '
                            f'(df = {_dfp})',
                       value=round(float(r), 3), stat=round(float(r), 3),
                       p=float(f'{p:.3g}')))
ax.axhline(0, color='0.85', lw=LW, zorder=1); ax.axvline(0, color='0.85', lw=LW, zorder=1)
_l, _h = ax.get_ylim(); ax.set_ylim(_l, _h + (_h - _l) * .16)   # room for the stats text
ax.set_xlabel('Δ NP FC (residual)'); ax.set_ylabel('Δ symptom PC1 (residual)')
ax.text(.03, .97, f'$r$ = {r:.2f}, $P$ = {p:.3g}\nn = {len(F22)}',
        transform=ax.transAxes, ha='left', va='top', fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Larger connectivity change, larger symptom gain')
enforce(fig); save(fig, 'fig5f', W, H, 'fig5f_np_symptom_resid_MDD_n22.csv')

# ---- g  similarity to the AMPA-perturbed twin vs MADRS change --------------
def resid(v, Z):
    v = np.asarray(v, float); A = np.column_stack([np.ones(len(v)), Z])
    return v - A @ np.linalg.lstsq(A, v, rcond=None)[0]


Z = np.column_stack([G22.age.astype(float),
                     (G22.sex.astype(str).str.upper() == 'M').astype(float),
                     (G22.infusion_1.astype(str) == 'd').astype(float),
                     G22.fd_p2.astype(float)])
xg, yg = resid(G22.pref_d2, Z), resid(G22.MADRS_delta, Z)
W, H = 58, 54
fig, ax = plt.subplots(figsize=panel(W, H))
rho, pg = scatter_fit(ax, xg, yg, C('mdd'), spearman=True)
stats_rows.append(dict(panel='g', cohort='pharmacology', condition='Ketamine',
                       group='MDD', n=len(G22), test='Spearman rho (residualised)',
                       value=round(float(rho), 3), stat=round(float(rho), 3),
                       p=float(f'{pg:.3g}')))
ax.set_xlabel('Similarity to AMPA-perturbed twin\n(residual)')
ax.set_ylabel('Δ MADRS (residual)')
ax.text(.03, .05, f'Spearman $\\rho$ = {rho:.2f}\n$P_{{perm}}$ = 0.0068, n = {len(G22)}',
        transform=ax.transAxes, ha='left', va='bottom', fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Closer to the perturbed twin, greater improvement')
enforce(fig); save(fig, 'fig5g', W, H, 'fig5g_state_similarity_MDD_n22.csv')

# ---- h1  added-variable plot for the AMPA restoration index ----------------
A = NEST.set_index('predictor').loc['AMPA restoration index']
G = NEST.set_index('predictor').loc['GABA-A restoration index']
W, H = 60, 54
fig, ax = plt.subplots(figsize=panel(W, H))
r, p = scatter_fit(ax, AV85.ampa_index_resid.values, AV85.fu3_change_resid.values,
                   C('ampa'))
ax.axhline(0, color='0.85', lw=LW, zorder=1); ax.axvline(0, color='0.85', lw=LW, zorder=1)
ax.set_xlabel('AMPA restoration index (residual)')
ax.set_ylabel('Δ symptoms at follow-up (residual)')
ax.text(.03, .97, f'partial $r$ = {r:.2f}\n$P$ = {p:.3f}, n = {len(AV85)}',
        transform=ax.transAxes, ha='left', va='top', fontsize=ANNOT_PT, color='0.35')
panel_title(ax, 'Predicts symptom change beyond baseline behaviour')
stats_rows.append(dict(panel='h1', cohort='IMAGEN FU3', condition='AMPA index',
                       group='partial, adjusted for 4 baseline scores', n=len(AV85),
                       test='partial Pearson r', value=round(float(r), 3),
                       stat=round(float(r), 3), p=float(f'{p:.3g}')))
enforce(fig); save(fig, 'fig5h1', W, H, 'fig5h_added_variable_n85.csv')

# ---- h2  incremental variance under two covariate sets, AMPA vs GABA-A -----
# The increment over baseline BEHAVIOUR separates the two indices; the increment
# over baseline empirical NP connectivity does not.  Both are shown so the panel
# cannot be read as a stronger specificity claim than the data support.
INC = pd.read_csv(f'{D}/fig5h_increments.csv')
INULL = pd.read_csv(f'{D}/fig5h_increment_nulls.csv')
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
W, H = 76, 54
fig, ax = plt.subplots(figsize=panel(W, H))
COVS = ['baseline behaviour (4)', 'baseline empirical NP (1)']
IDXS = [('AMPA', C('ampa')), ('GABA-A', C('gaba'))]
TOP = 0.115
pos, ticks, blocklab = [], [], []
x = 0.0
for cov in COVS:
    first = x
    for k, (nm, col) in enumerate(IDXS):
        row = INC[(INC['index'] == nm) & (INC.covariates == cov)].iloc[0]
        null = INULL[f'{nm}|{cov}'].values
        vp = ax.violinplot([null[null <= TOP]], positions=[x], widths=.80,
                           showextrema=False)
        for bd in vp['bodies']:
            bd.set_facecolor('0.88'); bd.set_edgecolor('0.72')
            bd.set_linewidth(LW * .8); bd.set_alpha(1); bd.set_zorder(1)
        ax.plot([x - .40, x + .40], [row.null_p95] * 2, color='0.35', lw=LW,
                ls=(0, (2.2, 1.6)), zorder=2)
        ax.bar(x, row.delta_R2, width=.34, facecolor=col, edgecolor='black',
               linewidth=LW, zorder=3)
        ax.text(x, TOP * (.70 if k else .88),          # staggered so the two
                f'$P$ = {row.p_change:.3f}\n'           # labels of a block cannot
                f'$P_{{perm}}$ = {row.p_perm_deltaR2:.3f}',   # collide
                ha='center', va='top', fontsize=ANNOT_PT, color='0.35',
                linespacing=1.35)
        ticks.append(x); pos.append(x); x += 1.0
        stats_rows.append(dict(panel='h2', cohort='IMAGEN FU3', condition=f'{nm} index',
                               group=f'added to {cov}', n=int(row.n),
                               test=f'nested F(1, {int(row.df2)}); 5000-permutation null '
                                    f'P = {row.p_perm_deltaR2:.3f}',
                               value=float(row.delta_R2), stat=float(row.F_change),
                               p=float(row.p_change)))
    blocklab.append(((first + x - 1) / 2, cov.replace(' (', '\n(')))
    x += 1.25
ax.set_xticks(ticks)
ax.set_xticklabels([n for _ in COVS for n, _ in IDXS], fontsize=TICK_PT)
ax.set_xlim(pos[0] - .75, pos[-1] + .75)
ax.set_ylim(0, TOP)
ax.set_ylabel('Δ$R^2$ over the covariate model')
tr = ax.get_xaxis_transform()
for xc, bl in blocklab:
    ax.text(xc, -.135, bl, transform=tr, ha='center', va='top', fontsize=ANNOT_PT,
            clip_on=False)
ax.legend([Patch(facecolor='0.88', edgecolor='0.72', linewidth=LW * .8),
           Line2D([], [], color='0.35', lw=LW, ls=(0, (2.2, 1.6)))],
          ['null (5,000 permutations)', '95th percentile'],
          loc='upper right', fontsize=ANNOT_PT, frameon=False, borderaxespad=.15,
          handlelength=1.6, handletextpad=.5, labelspacing=.25)
panel_title(ax, 'Adds variance over baseline behaviour, less so over baseline NP')
enforce(fig); save(fig, 'fig5h2', W, H, 'fig5h_increments.csv')

# ---- h3-h6  the four relationships stated in the longitudinal paragraph -----
# h3 is the added-variable plot for the second increment model (covariate =
# baseline empirical NP connectivity); h4 is the same association unadjusted;
# h5 and h6 are the two discriminant checks -- both null, which is the point.
SC = pd.read_csv(f'{D}/fig5h_paragraph_scatters_n85.csv')
SCST = pd.read_csv(f'{D}/fig5h_paragraph_scatter_stats.csv')
SCAT = [
    ('fig5h3', 'index_resid_on_empNP', 'fu3change_resid_on_empNP',
     'AMPA restoration index\n(residual on baseline empirical NP)',
     'Δ symptoms at follow-up, residual\n(negative = improvement)', 'partial $r$',
     'Holds when baseline NP connectivity is the covariate'),
    ('fig5h4', 'ampa_index', 'fu3_symptom_change',
     'AMPA restoration index', 'Δ symptoms at follow-up\n(negative = improvement)', '$r$',
     'Unadjusted association'),
    ('fig5h5', 'ampa_index', 'empirical_baseline_np_sum',
     'AMPA restoration index', 'Baseline empirical NP FC', '$r$',
     'Not explained by baseline connectivity'),
    ('fig5h6', 'ampa_index', 'baseline_symptom_sum',
     'AMPA restoration index', 'Baseline symptom score', '$r$',
     'Not explained by baseline symptoms'),
]
for stem, xc, yc, xlab, ylab, rlab, title in SCAT:
    W, H = 46, 50
    fig, ax = plt.subplots(figsize=panel(W, H))
    r, p = scatter_fit(ax, SC[xc].values, SC[yc].values, C('ampa'), s=16)
    row = SCST.iloc[[i for i, t in enumerate(SCAT) if t[0] == stem][0]]
    ax.text(.03, .97, f'{rlab} = {r:.2f} ({row.ci_low:.2f} to {row.ci_high:.2f})\n'
            f'$P$ = {p:.3f}, n = {len(SC)}', transform=ax.transAxes, ha='left',
            va='top', fontsize=ANNOT_PT, color='0.35')
    _l, _h = ax.get_ylim(); ax.set_ylim(_l, _h + (_h - _l) * .20)
    ax.set_xlabel(xlab); ax.set_ylabel(ylab)
    panel_title(ax, title)
    stats_rows.append(dict(panel=stem, cohort='IMAGEN FU3', condition='AMPA index',
                           group=row.relationship, n=int(row.n), test=row.test,
                           value=round(float(r), 3), stat=round(float(r), 3),
                           p=float(f'{p:.3g}')))
    enforce(fig); save(fig, stem, W, H, 'fig5h_paragraph_scatters_n85.csv')

pd.DataFrame(stats_rows).to_csv(f'{D}/fig5_panel_stats.csv', index=False)
mf = pd.DataFrame(manifest)
mf.to_csv(f'{OUTD}/fig5_panel_manifest.csv', index=False)
print(mf.to_string(index=False))
print()
print(pd.DataFrame(stats_rows).to_string(index=False))

# ---------------------------------------------------------------------------
# Variant grouping: the Fig. 4 response rule applied to the in vivo cohort.
# The k-means subgroups in a-c are a data-driven split of the same 27 people
# and do NOT coincide with "both up / any down": every k-means decreaser is
# any-down, but the increasers split 8 both-up / 11 any-down.  These two
# panels re-run b and c under the Fig. 4 rule so the two analyses are on the
# same footing.
# ---------------------------------------------------------------------------
HC27['pattern'] = np.where((HC27.d_ket > 0) & (HC27.d_mid > 0), 'both up', 'any down')
HC27['detail'] = np.select(
    [(HC27.d_ket > 0) & (HC27.d_mid > 0), (HC27.d_ket <= 0) & (HC27.d_mid <= 0),
     (HC27.d_ket > 0) & (HC27.d_mid <= 0)],
    ['both up', 'both down', 'ketamine up only'], 'midazolam up only')
PAT = ['both up', 'any down']
PCOL = {'both up': C('increased'), 'any down': C('decreased')}
prows = []
for pat in PAT:
    s = HC27[HC27.pattern == pat]
    for col, nm in [('d_ket', 'change under ketamine'), ('d_mid', 'change under midazolam'),
                    ('Placebo', 'placebo level')]:
        t_, p_ = stats.ttest_1samp(s[col], 0)
        prows.append(dict(rule='both-up / any-down', group=pat, n=len(s), measure=nm,
                          mean=round(float(s[col].mean()), 4),
                          sd=round(float(s[col].std(ddof=1)), 4),
                          test='one-sample t vs 0', stat=round(float(t_), 3),
                          p=float(f'{p_:.3g}')))
for col, nm in [('d_ket', 'change under ketamine'), ('d_mid', 'change under midazolam'),
                ('Placebo', 'placebo level')]:
    a = HC27.loc[HC27.pattern == 'both up', col]; b = HC27.loc[HC27.pattern == 'any down', col]
    t_, p_ = stats.ttest_ind(a, b, equal_var=False)
    _, pu = stats.mannwhitneyu(a, b)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) /
                 (len(a) + len(b) - 2))
    prows.append(dict(rule='both-up / any-down', group='both up vs any down', n=len(HC27),
                      measure=nm, mean=round(float(a.mean() - b.mean()), 4),
                      sd=round(float((a.mean() - b.mean()) / sp), 3),
                      test='Welch t (sd column = Hedges g); Mann-Whitney P in notes',
                      stat=round(float(t_), 3), p=float(f'{p_:.3g}')))
    prows.append(dict(rule='both-up / any-down', group='both up vs any down', n=len(HC27),
                      measure=nm, mean=round(float(a.mean() - b.mean()), 4), sd=np.nan,
                      test='Mann-Whitney U', stat=np.nan, p=float(f'{pu:.3g}')))
for det, s in HC27.groupby('detail'):
    for col, nm in [('d_ket', 'change under ketamine'), ('d_mid', 'change under midazolam'),
                    ('Placebo', 'placebo level')]:
        prows.append(dict(rule='four-way breakdown', group=det, n=len(s), measure=nm,
                          mean=round(float(s[col].mean()), 4),
                          sd=round(float(s[col].std(ddof=1)), 4), test='descriptive',
                          stat=np.nan, p=np.nan))
pd.DataFrame(prows).to_csv(f'{D}/fig5_healthy_pattern_rule_n27.csv', index=False)
HC27.to_csv(f'{D}/fig5_healthy_n27_with_pattern.csv', index=False)

W, H = 66, 54
fig, ax = plt.subplots(figsize=panel(W, H))
blocks = []
for dkey, dn in [('d_ket', 'Ketamine'), ('d_mid', 'Midazolam')]:
    blocks.append((dn, [(f'both\nup' if p == 'both up' else 'any\ndown',
                         HC27.loc[HC27.pattern == p, dkey].values, PCOL[p]) for p in PAT]))
change_panel(ax, blocks, 'Δ summed MID FC (drug − placebo)', seed=6)
panel_title(ax, 'Same split as Fig. 4: both up vs any down')
enforce(fig); save(fig, 'fig5b_pattern', W, H, 'fig5_healthy_n27_with_pattern.csv')

W, H = 48, 54
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [HC27.loc[HC27.pattern == p, 'Placebo'].values for p in PAT]
t_, p_ = level_panel(ax, ['both\nup', 'any\ndown'], vals, [PCOL[p] for p in PAT],
                     'Placebo summed MID FC', seed=7)
panel_title(ax, 'Both-up volunteers start lower')
enforce(fig); save(fig, 'fig5c_pattern', W, H, 'fig5_healthy_n27_with_pattern.csv')

pd.DataFrame(manifest).to_csv(f'{OUTD}/fig5_panel_manifest.csv', index=False)
print()
print(pd.crosstab(HC27.subgroup, HC27.pattern).to_string())
