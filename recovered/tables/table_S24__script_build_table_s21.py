# Verbatim archive of the author's producing SCRIPT (not an execution-log cell).
# Nothing removed, nothing reformatted.
# table            : Table S24 (statistical-reporting table; numbered 'Table S21' when this ran)
# source file      : revision/text/_revision/build_table_s21.py  (mtime 2026-09-23 15:56)
# produced         : revision/text/_revision/Table_S21_rebuilt.csv, 244 rows x 17 columns
# run and inserted : execution-log cell f47df048-... (frame fe47a03f-..., 2026-09-23),
#                    archived as recovered/tables/table_S24__cell_f47df048.py
# note             : the sheet shipped in 290926Suppl.Table_FINAL.xlsx is this output after
#                    later edit passes in session b194cd74 (347 number-format rewrites logged
#                    in 04_figures/_recovered_session_b194cd74/tableS24_format_log.csv and 29
#                    substantive fixes in tableS24_fix_log_v2.csv, plus row-level rewrites);
#                    re-running this script does NOT reproduce the shipped sheet verbatim.
# ---------------------------------------------------------------------------

"""Rebuild Table S21 (Detailed statistical information) from the figure source
data, on the new figure numbering (Figs. 1-5, Supplementary Figs. S1-S27).

Every row carries the fields the reviewer asked for: sample size, unit of
observation, the error indicator actually drawn in the panel, the test with its
sidedness and pairing, the multiple-comparison correction, the exact test
statistic, its degrees of freedom, the exact P, the corrected P, an effect size
and its 95% CI, and the source data file.

    cd revision/text/_revision && python build_table_s21.py
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.abspath(os.path.join(HERE, '..'))
FG = os.path.join(TXT, 'figures')

COLS = ['figure', 'panel', 'quantity', 'n', 'unit', 'error_indicator', 'test',
        'sided', 'paired', 'correction', 'statistic', 'df', 'p_exact',
        'p_corrected', 'effect', 'ci95', 'source']

BOX = ('box: median and interquartile range, whiskers 1.5 x IQR; '
       'every individual observation plotted')
BAR_SD = 'bar: mean, error bar = 1 s.d. across participants'
CI95 = 'point estimate with 95% confidence interval'
NONE = 'not applicable (no error indicator in this panel)'

ROWS = []


def row(figure, panel, quantity, n, unit, err, test, sided, paired, corr,
        stat, df, p, pcorr='', effect='', ci='', source=''):
    ROWS.append(dict(zip(COLS, [figure, panel, quantity, n, unit, err, test,
                                sided, paired, corr, stat, df, p, pcorr,
                                effect, ci, source])))


def P(x, sig=3):
    """Exact P, never rounded to zero."""
    if x == '' or x is None or (isinstance(x, float) and np.isnan(x)):
        return ''
    x = float(x)
    if x >= 1e-4:
        return f'{x:.{sig}g}'
    return f'{x:.2e}'


# --------------------------------------------------------------- Figure 1 ----
row('Fig. 1', 'a-e', 'Analytical pipeline schematic: sample selection, circuit '
    'derivation, digital twin construction, virtual perturbation, validation',
    'see Table S1', 'not applicable', NONE,
    'no inferential statistics; the panel reproduces sample counts and '
    'previously reported estimates', '', '', 'not applicable', '', '', '', '',
    '', '', 'fig.1/fig1_data/fig1_sample_selection.csv')

# --------------------------------------------------------------- Figure 2 ----
row('Fig. 2', '2a', 'Cross-validated prediction of six DAWBA symptom bands from '
    'six task-specific connectomes (connectome-based predictive modelling)',
    'n = 1,050', 'participant', 'heat-map cell = Spearman rho; no error bar',
    'Spearman rank correlation between predicted and observed scores, 10-fold '
    'cross-validation', 'two-sided', 'unpaired',
    'NOT RECOVERABLE - see note', 'rho = 0.00 to 0.25 (per cell)', '',
    'NOT RECOVERABLE', '', '', '', 'fig.2/fig2_data/fig2a_cpm_rho.csv; '
    'rho values also in Table S3. The permutation P values quoted in the main '
    'text are not present in any source table or figure data file and could '
    'not be recomputed; the original CPM script output is required.')

row('Fig. 2', '2b', 'Anatomical composition of the positive and negative FC '
    'profiles', '29 negative and 34 positive edges', 'edge', NONE,
    'descriptive; edge selection reported in Table S4', '', '',
    'not applicable', '', '', '', '', '', '',
    'fig.2/fig2_data/fig2b_network_neg.csv, fig2b_network_pos.csv')

_led = pd.read_csv(os.path.join(HERE, 'numbers_ledger.csv'))


def from_ledger(fig_key, panel_key, err, figure_out=None, panel_out=None):
    """Emit every ledger row for one figure/panel, adding the error indicator."""
    sel = _led[(_led.figure == fig_key) & (_led.panel == panel_key)]
    assert len(sel), f'no ledger rows for {fig_key} / {panel_key}'
    for _, r in sel.iterrows():
        row(figure_out or fig_key, panel_out or r.panel, r.quantity, r.n,
            r.unit, err, r.test, r.sided, r.paired, r.correction, r.statistic,
            '' if pd.isna(r.df) else r.df, r.p_exact, r.p_corrected, r.effect,
            r.ci95, r.source if pd.isna(r.note) else f'{r.source} ({r.note})')


from_ledger('Fig. 2', '2c', BOX)

_e2 = pd.read_csv(os.path.join(FG, 'fig.2/fig2_data/fig2e_edge_group_difference.csv'))
row('Fig. 2', '2d', 'Chord diagram of the 12 NP-factor edges', '12 edges',
    'edge', NONE, 'descriptive; edge identities in Table S6', '', '',
    'not applicable', '', '', '', '', '', '',
    'fig.2/fig2_data/fig2d_circos_matrix.csv, fig2d_nodes.csv')

from_ledger('Fig. 2', '2e', BOX)
for _, r in _e2.iterrows():
    row('Fig. 2', '2e (edge level)',
        f'{r.edge} ({r.task}): healthy controls vs patients, STRATIFY',
        'HC 225, patients 202', 'participant', BOX,
        'independent-samples Student t (equal variance)', 'two-sided',
        'unpaired', 'Benjamini-Hochberg FDR across the 12 edges',
        f't = {r.t:.3f}', 425, P(r.p), P(r.p_fdr), f"Cohen's d = {r.d:.3f}",
        f'{r.ci_lo:.3f} to {r.ci_hi:.3f}',
        'fig.2/fig2_data/fig2e_edge_group_difference.csv')

from_ledger('Fig. 2', '2f', 'bar height = number of edges surviving FDR; no error bar')

# --------------------------------------------------------------- Figure 3 ----
from_ledger('Fig. 3', '3a', BOX)
row('Fig. 3', '3b', 'Whole-brain FC similarity between each build and the '
    'empirical connectome', '12 participants x 4 task conditions per build',
    'participant x condition', BAR_SD, 'descriptive summary of Pearson r; no '
    'inferential test is reported for this panel', 'not applicable', 'paired '
    'within participant', 'not applicable',
    'mean r = 0.076 (10M own-hyper) to 0.613 (voxel builds)', '', '', '', '',
    '', 'fig.3/fig3_data/fig3b_wholebrain_fc_crossscale.csv')
row('Fig. 3', '3c', 'Cross-build similarity of simulated NP connectivity',
    '12 participants x 12 edges = 144 cells per build pair',
    'participant x edge', 'heat-map cell = Spearman rho; no error bar',
    'Spearman rank correlation on raw NP values (Spearman chosen because the '
    '10M own-hyper build has excess kurtosis 10.56)', 'two-sided',
    'paired across builds', 'none (descriptive similarity matrix)',
    'rho = 0.933 (1B vs 100M), 0.905 (1B vs 10M); same-hyper block mean 0.90, '
    'cross-family mean 0.31', '', '', '', '', '',
    'fig.3/fig3_data/fig3c_cross_scale_similarity.csv')
from_ledger('Fig. 3', '3i', BOX)
from_ledger('Fig. 3', '3g', BOX)
row('Fig. 3', '3d', 'Run-to-run s.d. of summed NP connectivity across 5 repeat '
    'simulations', '12 participants per build (10M own-hyper: single run)',
    'participant', BOX, 'descriptive; no inferential test', 'not applicable',
    'repeated simulations of the same participant', 'not applicable',
    'mean s.d. = 0.125 (1B), 0.287 (100M), 0.316 (10M/268), 0.327 (10M), '
    '0.373 (3M/268), 0.448 (10M/1000)', '', '', '',
    '5-repeat reliability of the 1B build = 0.9915', '',
    'fig.3/fig3_data/fig3d_run_to_run_sd.csv')

# --------------------------------------------------------------- Figure 4 ----
_sl = pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4_subject_level_n288.csv'))
_ad = pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4ad_group_stats.csv'))
_PAN = {'fig4a': ('4a', 'empirical_resid', 'empirical NP factor'),
        'fig4b': ('4b', 'simulated_resid', 'simulated baseline NP factor'),
        'fig4c': ('4c', 'ampa_resid', 'NP factor after AMPA up-regulation'),
        'fig4d': ('4d', 'gaba_resid', 'NP factor after GABA-A up-regulation')}
_GRP = ['HC', 'High-symptom', 'Patient']


def _welch(a, b):
    from scipy import stats as st
    t, p = st.ttest_ind(a, b, equal_var=False)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    df = (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) +
                                     (vb / nb) ** 2 / (nb - 1))
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    return float(t), float(p), float(df), float((a.mean() - b.mean()) / sp)


for _, ar in _ad.iterrows():
    pan, col, what = _PAN[ar.panel]
    from_ledger('Fig. 4', pan, BOX)
    for i in range(3):
        for j in range(i + 1, 3):
            g1, g2 = _GRP[i], _GRP[j]
            a = _sl.loc[_sl.Group == g1, col].values
            b = _sl.loc[_sl.Group == g2, col].values
            t, p, dfw, d = _welch(a, b)
            q = ar[f'{g1}_vs_{g2}_q']
            row('Fig. 4', f'{pan} (post hoc)',
                f'{what}: {g1} vs {g2}', f'{g1} {len(a)}, {g2} {len(b)}',
                'participant', BOX,
                'Welch two-sample t test (unequal variance) on scores '
                'residualised on sex, site and mean framewise displacement '
                'across all 288 participants', 'two-sided', 'unpaired',
                'Benjamini-Hochberg FDR across the 3 pairwise contrasts',
                f't = {t:.3f}', f'{dfw:.1f}', P(p), P(q),
                f"Cohen's d = {d:.3f}", '',
                'fig.4/fig4_data/fig4_subject_level_n288.csv; '
                'fig4ad_group_stats.csv')

row('Fig. 4', '4e', 'Effect size of the control-patient difference in each of '
    'the four conditions', 'HC 69, patients 130', 'participant', CI95,
    "Cohen's d with 95% CI, from the Welch contrasts in 4a-4d", 'two-sided',
    'unpaired', 'as in 4a-4d', 'd = 0.618 (empirical), 0.531 (simulated), '
    '0.145 (AMPA), 0.116 (GABA-A)', '', '', '',
    'see the 4a-4d post hoc rows', 'empirical 0.320 to 0.916; simulated 0.234 '
    'to 0.827', 'fig.4/fig4_data/fig4e_effect_size.csv')

for _, r in pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4i_paired_stats.csv')).iterrows():
    row('Fig. 4', '4f/4i', f'{r.measure}: baseline vs {r.perturbation}',
        int(r.n), 'participant', BOX, 'paired two-sample t test (Wilcoxon '
        'signed-rank as a distribution-free check)', 'two-sided', 'paired',
        'none (two pre-registered perturbations)', f't = {r.t:.3f}',
        int(r.df), P(r.p_paired_t), '',
        f'mean change = {r.mean_diff:+.4f}, dz = {r.cohens_dz:.3f}, '
        f'{int(r.n_increased)}/{int(r.n)} increased ({r.pct_increased:.1f}%)',
        '', 'fig.4/fig4_data/fig4i_paired_stats.csv '
        f'(Wilcoxon P = {P(r.wilcoxon_p)})')

for _, r in pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4j_baseline_change_stats.csv')).iterrows():
    row('Fig. 4', '4j', f'{r.perturbation}: slope of the perturbed on the '
        'baseline score, tested against 1', int(r.n), 'participant',
        'regression line with 95% confidence band',
        'OLS slope, two-sided t test of H0: slope = 1', 'two-sided', 'paired',
        'none', f't = {r.t_slope_vs_1:.3f}', int(r.n) - 2, P(r.p_slope_vs_1),
        '', f'slope = {r.slope_post_on_pre:.4f}; Oldham r = {r.r_oldham:+.4f} '
        f'(P = {P(r.p_oldham)}); variance ratio = {r.var_ratio:.4f}',
        f'{r.slope_ci_lo:.4f} to {r.slope_ci_hi:.4f}',
        'fig.4/fig4_data/fig4j_baseline_change_stats.csv. The naive '
        f'baseline-change correlation (r = {r.r_naive:+.4f}) is inflated by '
        'the shared baseline term and is reported only for comparability with '
        'the previous version.')

for _, r in pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4h_dawba_pattern_stats.csv')).iterrows():
    row('Fig. 4', '4h', f'DAWBA {r.measure} band: {r.split}',
        f'both-up {int(r.n_up)}, any-down {int(r.n_down)}', 'participant', BOX,
        'Mann-Whitney U test', 'two-sided', 'unpaired',
        'Benjamini-Hochberg FDR across the 7 symptom measures',
        f'U = {r.U:,.1f}', '', P(r.p_mw), P(r.q_bh),
        f"Hedges' g = {r.hedges_g:+.3f}", f'{r.ci_lo:+.3f} to {r.ci_hi:+.3f}',
        'fig.4/fig4_data/fig4h_dawba_pattern_stats.csv')

from_ledger('Fig. 4', '4 (response pattern)',
            'stacked bar = proportion of participants per response pattern')

# --------------------------------------------------------------- Figure 5 ----
_P5 = pd.read_csv(os.path.join(FG, 'fig.5/fig5_data/fig5_panel_stats.csv'))
_H27 = pd.read_csv(os.path.join(FG, 'fig.5/fig5_data/fig5_healthy_n27.csv'))
_M36 = pd.read_csv(os.path.join(FG, 'fig.5/fig5_data/fig5_mdd_hc_n36.csv'))
_CIRC = {'b', 'c'}                      # subgroups defined by the sign tested


def _welch_df_only(a, b):
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    return (va / na + vb / nb) ** 2 / ((va / na) ** 2 / (na - 1) +
                                       (vb / nb) ** 2 / (nb - 1))


def _df5(pan, test, group, cond, n):
    """Residual df for a Fig. 5 row, recomputed rather than transcribed."""
    t, g = str(test), str(group)
    if 'OLS group coefficient' in t or 'group x drug' in t:
        return 30                                        # 36 - 6 parameters
    if 'one-sample' in t or 'paired' in t:
        return int(n) - 1
    if 'Welch' in t:
        if 'increasers vs decreasers' in g:
            inc = _H27[_H27.subgroup == 'increasers']
            dec = _H27[_H27.subgroup == 'decreasers']
            if pan == 'c':                               # placebo level
                a, b = inc['Placebo'].values, dec['Placebo'].values
            else:                                        # change from placebo
                a = (inc[cond] - inc['Placebo']).values
                b = (dec[cond] - dec['Placebo']).values
            return f'{_welch_df_only(a, b):.1f}'
        if 'MDD vs HC' in g:
            col = 'FC_p2' if cond == 'Placebo' else 'FC_delta'
            a = _M36.loc[_M36.group == 'MDD', col].values
            b = _M36.loc[_M36.group == 'HC', col].values
            return f'{_welch_df_only(a, b):.1f}'
        return ''
    if 'partial' in t:
        # df = n - (number of covariates partialled out) - 2, with the covariate
        # count read off the test description rather than assumed
        if 'adjusted for' in t:
            tail = t.split('adjusted for', 1)[1].split('(')[0]
            k = len([x for x in tail.replace(' and ', ',').split(',')
                     if x.strip()])
        elif 'baseline behaviour' in g or '4 baseline scores' in g:
            k = 4
        else:
            k = 1
        return int(n) - k - 2
    if 'Spearman' in t or 'Pearson' in t:
        return int(n) - 2
    if 'nested F' in t:
        return '1, 79' if 'baseline behaviour (4)' in g else '1, 82'
    return ''
_PANMAP = {'fig5h3': 'h (Supp. Results)', 'fig5h4': 'h (Supp. Results)',
           'fig5h5': 'h (Supp. Results)', 'fig5h6': 'h (Supp. Results)'}
for _, r in _P5.iterrows():
    pan = _PANMAP.get(str(r.panel), str(r.panel))
    sided = 'two-sided'
    paired = 'paired' if 'one-sample' in str(r.test) or 'paired' in str(r.test) \
        else 'unpaired'
    err = BOX if pan in list('abcde') or pan in ('d','e') else 'scatter with OLS fit and 95% band'
    note = ('fig.5/fig5_data/fig5_panel_stats.csv')
    if pan in _CIRC:
        note += ('. CIRCULAR: the two subgroups were defined by the sign of '
                 'the very change being tested; reported as a description of '
                 'the split, not as evidence for a drug effect.')
    if pan in ('d', 'e'):
        note += ('. Computed on the 11 unique NP edges represented in the '
                 'emotional face task (np_idx rows 9 and 12 are the same node '
                 'pair 233-15, so the 12 index rows contain 11 distinct '
                 'edges); raw edge sum, no Fisher transform. This is the '
                 'specification the main text reports.')
    row('Fig. 5', pan, f'{r.cohort}, {r.condition}: {r.group}', int(r.n),
        'participant', err, r.test, sided, paired,
        'none (each panel reports a single pre-specified contrast)',
        f'{r.stat:+.3f}' if pd.notna(r.stat) else '',
        _df5(pan, r.test, r.group, r.condition, r.n),
        P(r.p), '', f'estimate = {r.value:+.4f}', '', note)

# ------------------------------------------------- Supplementary figures ----
SUPP = {'Supp. STRATIFY': ('Supplementary Fig. S1', BOX),
        'Supp.': ('Supplementary Fig. S1', BOX),
        'Supp. PET': ('Supplementary Fig. S2', BOX),
        'Supp. Oldham': ('Supplementary Fig. S12',
                         'scatter with OLS fit and 95% band'),
        'Supp. paired MID': ('Supplementary Fig. S16', BOX)}
for key, (out, err) in SUPP.items():
    for pk in _led.loc[_led.figure == key, 'panel'].unique():
        from_ledger(key, pk, err, figure_out=out)

# S8, S17c and S19 are read from their own source tables: the ledger rows for
# these three carry their values as a JSON blob in the note field.
for _, r in pd.read_csv(os.path.join(FG, 'supp_empsim/data/'
                                         'empsim_paired_tests_n288.csv')).iterrows():
    row('Supplementary Fig. S8', 'a' if r.scores == 'raw' else 'b',
        f'{r.group}: simulated minus empirical NP factor ({r.scores} scores)',
        int(r.n), 'participant', BOX,
        'paired two-sample t test (Wilcoxon signed-rank as a check)',
        'two-sided', 'paired', 'none (three pre-specified groups)',
        f't = {r.t:.3f}', int(r.df), P(r.p_paired_t), '',
        f'mean difference = {r.mean_diff_sim_minus_emp:+.4f}, '
        f'dz = {r.cohens_dz:+.3f}', f'{r.ci95_lo:.4f} to {r.ci95_hi:.4f}',
        'supp_empsim/data/empsim_paired_tests_n288.csv'
        + ('. On the residualised scores the test is non-significant BY '
           'CONSTRUCTION: each measure is centred within cohort, so the '
           'paired difference has no group mean left to detect.'
           if r.scores != 'raw' else ''))

for _, r in pd.read_csv(os.path.join(FG, 'supp_wbdrug/data/'
                                         'wbdrug_direction_agreement_n288.csv')).iterrows():
    row('Supplementary Fig. S17', 'a-b',
        f'{r.drug} ({r.dtb_contrast}), {r.level}, {r.task_match}: edges '
        'changing in the direction predicted by the receptor-matched '
        'perturbation',
        f'{int(r.n_edges)} nominally drug-affected edges', 'edge',
        'bar with 95% binomial confidence interval',
        'node-level sign-flip permutation test against 50% agreement '
        '(binomial test reported alongside)', 'two-sided', 'unpaired',
        'none', f'{int(r.n_same)}/{int(r.n_edges)} agree '
        f'({r.pct_same:.1f}%)', '', P(r.p_signflip_node), '',
        f'binomial P = {P(r.p_binomial)}; null s.d. = {r.null_sd_pct:.1f}%',
        '', 'supp_wbdrug/data/wbdrug_direction_agreement_n288.csv '
        f'(pairing: {r.pairing})')

for _, r in pd.read_csv(os.path.join(FG, 'supp_wbdrug/data/'
                                         'wbdrug_map_reliability.csv')).iterrows():
    row('Supplementary Fig. S17', 'c',
        f'{r.drug}, {r.drug_condition}: split-half reliability of the '
        'edge-wise drug-effect map', 'see panel a-b', 'edge',
        'bar = reliability; no error bar',
        'Spearman-Brown split-half reliability; no inferential test',
        'not applicable', 'not applicable', 'not applicable',
        f'reliability = {r.spearman_brown_reliability:.3f}', '', '', '',
        f'maximum attainable correlation = {r.max_attainable_r:.3f}', '',
        'supp_wbdrug/data/wbdrug_map_reliability.csv')

for _, r in pd.read_csv(os.path.join(FG, 'supp_longitudinal/data/'
                                         'long_nested_increments_n85.csv')).iterrows():
    row('Supplementary Fig. S19', 'a-e',
        f'{r["index"]} restoration index added to a model containing '
        f'{r.covariates}', int(r.n), 'participant',
        'scatter with OLS fit and 95% band',
        'nested-model F test on the R-squared increment, with a matched '
        '5,000-permutation null', 'two-sided', 'unpaired',
        'none (two pre-specified indices x two covariate sets)',
        f'F = {r.F_change:.3f}', f'{int(r.df1)}, {int(r.df2)}',
        P(r.p_change), f'permutation P = {r.p_perm_deltaR2:.4f}',
        f'delta R-squared = {r.delta_R2:.4f} (reduced {r.R2_reduced:.4f} -> '
        f'full {r.R2_full:.4f}); partial r = {r.partial_r:+.3f} '
        f'(P = {P(r.p_partial)})', '',
        'supp_longitudinal/data/long_nested_increments_n85.csv')

for _, r in pd.read_csv(os.path.join(FG, 'supp_stratify/data/'
                                         'stratify_symptom_tests.csv')).iterrows():
    row('Supplementary Fig. S1', 'e',
        f'Summed DAWBA band score: healthy controls vs {r.group}',
        f'HC {int(r.n1)}, {r.group} {int(r.n2)}', 'participant', BOX,
        "Welch two-sample t test (unequal variance). Unlike panels a-d this "
        'panel does not use the equal-variance test: the summed band score is '
        'a right-skewed count whose variance scales with the mean, so the '
        f'variances are unequal (ratio {r.var_ratio:.2f}; '
        f"Levene F = {r.levene_F:.2f}, P = {P(r.levene_p)}), whereas in a-d "
        'the ratio is 1.1 to 1.3', 'two-sided',
        'unpaired', 'Bonferroni across the 3 contrasts in this panel',
        f't = {r.t:.3f}', f'{r.df:.1f}', P(r.p), P(r.p_bonf3),
        f"Hedges' g = {r.g:.3f}; means {r.mean1:.3f} (s.d. {r.sd1:.3f}) vs "
        f'{r.mean2:.3f} (s.d. {r.sd2:.3f})',
        f'{r.ci_lo:.3f} to {r.ci_hi:.3f}',
        'supp_stratify/data/stratify_symptom_subject_level.csv; '
        'stratify_symptom_tests.csv. Patient scores are from the STRATIFY '
        'self-report DAWBA and reproduce the archived means exactly. Controls '
        "are assigned to an assessment wave by the author's own lists "
        '(STARTIFT_HC_subject_list_fu2.txt, 54 IDs; '
        'STARTIFY_HC_subject_list_fu3.txt, 123 IDs; the lists do not overlap) '
        'and are scored at their designated wave only, with no substitution '
        'across waves: 46 STRATIFY-recruited controls, 46 scored at IMAGEN '
        'FU2 and 123 scored at IMAGEN FU3 = 215 controls, which is the n of '
        'the archived analysis and gives df = 412 for the pooled contrast, '
        'matching the main text. The 8 remaining FU2-list members have no FU2 '
        'score and are not carried over from FU3; 2 further controls are on '
        'neither list and have no DAWBA score in any available file. The '
        "archived control mean of 7.5395 (t(412) = 13.453, P = 1.87e-34, "
        "Hedges' g = 1.321, 95% CI 1.108 to 1.534) is not reproduced by the "
        'summed six-band score from any of these files under any wave '
        'assignment, so the statistics here are recomputed. The ADHD band can '
        'take negative values in both cohorts, which is why a few summed '
        'scores fall below zero.')

_wb = pd.read_csv(os.path.join(FG, 'supp_wholebrain/wb_data/'
                                   'SuppTable_WB1_wholebrain_modulation_n288.csv'))
for _, r in _wb.iterrows():
    row('Supplementary Fig. S13', 'a-c',
        f'{r.condition}, {r.contrast}: edges changed after perturbation',
        f'{int(r.n_subj)} participants x {int(r.n_edges):,} edges', 'edge',
        'bar = percentage of edges; no error bar',
        'paired t test per edge across participants', 'two-sided', 'paired',
        f'Benjamini-Hochberg FDR across the {int(r.n_edges):,} edges',
        f'{int(r.n_sig_FDR):,} edges significant ({r.pct_sig_FDR:.1f}%)', '',
        '', 'q < 0.05',
        f'{r.pct_up_of_sig:.1f}% of significant edges increased; median '
        f'|dz| = {r.median_absdz_sig:.3f}', '',
        'supp_wholebrain/wb_data/SuppTable_WB1_wholebrain_modulation_n288.csv')

for _, r in pd.read_csv(os.path.join(FG, 'supp_depnet/depnet_data/'
                                         'depnet_group_stats_n141.csv')).iterrows():
    row('Supplementary Fig. S14', 'a-d',
        f'Depression-specific network ({r.condition}): MDD vs controls',
        f'HC {int(r.n_hc)}, MDD {int(r.n_mdd)}', 'participant', BOX,
        'ANCOVA group coefficient, adjusted for sex, site and mean framewise '
        'displacement', 'two-sided', 'unpaired',
        'none (four pre-specified conditions)', f't = {r.t:.3f}', int(r.df),
        P(r.p), '', f'adjusted difference = {r.adj_diff_hc_minus_mdd:+.4f}; '
        f"unadjusted Cohen's d = {r.cohens_d_unadj:.3f}",
        f'{r.ci_lo:.4f} to {r.ci_hi:.4f}',
        'supp_depnet/depnet_data/depnet_group_stats_n141.csv')

for _, r in pd.read_csv(os.path.join(FG, 'supp_assimregion/data/'
                                         'assimregion_set_summary.csv')).iterrows():
    if r.set == 'prior':
        continue
    row('Supplementary Fig. S20', 'a-d',
        f'{r.task}: overlap of the {r.set} assimilation set with the '
        'meta-analytic set', f'{int(r.n_regions)} regions', 'region',
        'bar = Dice coefficient; no error bar',
        'descriptive spatial overlap (Dice); no inferential test',
        'not applicable', 'not applicable', 'not applicable',
        f'Dice = {r.dice_with_prior:.1f}%', '', '', '',
        f'{int(r.n_overlap_prior)} of {int(r.n_regions)} regions shared', '',
        'supp_assimregion/data/assimregion_set_summary.csv')

_as = pd.read_csv(os.path.join(FG, 'supp_assim/data/assim5_stats.csv'))
row('Supplementary Fig. S20', 'e', 'Repeat-assimilation stability of the NP '
    'edges', '5 repeat assimilations of the same participant',
    'simulation run', BOX, 'intraclass correlation', 'not applicable',
    'repeated runs', 'none',
    '; '.join(f'{r.statistic} = {r.value}' for _, r in _as.iterrows()), '',
    '', '', '', '', 'supp_assim/data/assim5_stats.csv')

for _, r in pd.read_csv(os.path.join(FG, 'supp_fingerprint/data/'
                                         'fingerprint_accuracy.csv')).iterrows():
    row('Supplementary Fig. S21', 'a-c',
        f'Individual fingerprinting from {r.data}',
        f'4 participants x {int(r.n_trials) // 4} held-out trials '
        f'= {int(r.n_trials)} trials', 'held-out trial',
        'bar = identification accuracy; no error bar',
        'nearest-neighbour identification accuracy against a chance level of '
        '25% (4 participants)', 'not applicable', 'not applicable', 'none',
        f'{int(r.n_correct)}/{int(r.n_trials)} correct '
        f'({r.accuracy_pct:.1f}%)', '', '', '',
        f'mean within-participant r = {r.mean_self_r:.4f} vs best other '
        f'{r.mean_best_other_r:.4f}; margin {r.mean_margin:.4f}', '',
        'supp_fingerprint/data/fingerprint_accuracy.csv')

for _, r in pd.read_csv(os.path.join(FG, 'supp_conductance/data/'
                                         'conductance_grid_summary_n288.csv')).iterrows():
    row('Supplementary Fig. S22', 'a-c',
        f'{r.knob} conductance {r.conductance} ({r.setting}): change in NP '
        'connectivity', int(r.n), 'participant', BOX,
        'paired two-sample t test against zero change', 'two-sided', 'paired',
        'none (a pre-specified +/-10% grid around the reported setting)',
        f't = {r.t:.3f}', int(r.df), P(r.p), '',
        f"mean change = {r.mean_delta:+.4f}, Cohen's dz = {r.cohens_d:.3f}; "
        f'{r.pct_same_sign:.1f}% of participants moved in the group direction',
        f'{r.ci_lo:.4f} to {r.ci_hi:.4f}',
        'supp_conductance/data/conductance_grid_summary_n288.csv')

_eft = pd.read_csv(os.path.join(FG, 'supp_eft/data/eft_3subs.csv'))
row('Supplementary Fig. S23', 'a-b', 'Bidirectional NP response to virtual '
    'AMPA and GABA-A modulation in the emotional face task',
    '3 illustrative participants x 2 perturbations', 'participant', NONE,
    'descriptive; n = 3 is too small for inference',
    'not applicable', 'paired within participant', 'not applicable',
    '; '.join(f'{r.subject} {r.perturbation} = {r.delta:+.4f}'
              for _, r in _eft.iterrows()), '', '', '', '', '',
    'supp_eft/data/eft_3subs.csv')

_mt = pd.read_csv(os.path.join(FG, 'supp_motion/data/motion_group_tests.csv'))
for _, r in _mt.iterrows():
    row('Supplementary Fig. S24', 'a', f'Head motion by group: {r.test}',
        288, 'participant', BOX, r.test, 'two-sided', 'unpaired', 'none',
        f'{r.statistic}', r.df, P(r.p), '', '', '',
        'supp_motion/data/motion_group_tests.csv')
_mc = pd.read_csv(os.path.join(FG, 'supp_motion/data/'
                                   'TableS25_motion_np_correlations_corrected_n288.csv'))
for _, r in _mc.iterrows():
    row('Supplementary Fig. S24', 'b-c',
        f'Correlation of {r.Measure} with mean framewise displacement',
        int(r.n), 'participant', 'scatter with OLS fit and 95% band',
        'Pearson correlation (Spearman as a distribution-free check)',
        'two-sided', 'unpaired', 'Bonferroni across the 6 NP measures (recomputed as min(1, 6P) '
        'because the source table stores one value rounded to 0)',
        f'r = {r.r:+.3f}', int(r.n) - 2, P(r.P_raw), P(min(1.0, 6 * r.P_raw)),
        f'variance explained = {100 * r.variance_explained:.2f}%; '
        f'Spearman rho = {r.spearman_rho:+.3f} (P = {P(r.P_spearman)})',
        r.CI95, 'supp_motion/data/'
        'TableS25_motion_np_correlations_corrected_n288.csv')

# Supplementary figures whose statistics are reported elsewhere in this table,
# or which carry no inferential test.  Listed so that every figure of the
# submission is accounted for.
XREF = [
    ('S3', 'Edge-level case-control differences in STRATIFY',
     'the 12 edge-level rows under Fig. 2e in this table'),
    ('S4', 'Construction of individualised task-state DTB models',
     'schematic; no inferential statistics'),
    ('S5', 'Single-participant calibration of neuronal scale',
     'Table S8; the cross-build contrasts are the Fig. 3a rows in this table'),
    ('S6', 'Concordance of edge-level and summed NP-factor changes (1 B build)',
     'fig.3/fig3_data/fig3h_claim_support_1b.csv'),
    ('S7', 'Prediction of task performance from empirical and simulated FC',
     'Table S16'),
    ('S9', 'Within-group perturbational changes in the NP factor',
     'the Fig. 4f/4i rows in this table'),
    ('S10', 'Behavioural symptoms of the two response groups',
     'the Fig. 4h rows in this table'),
    ('S11', 'Baseline dependence of individual perturbation responses',
     'the Fig. 4j rows in this table'),
    ('S15', 'Pharmacological crossover design',
     'schematic; no inferential statistics'),
    ('S18', 'Age-19 mapping from empirical NP connectivity to symptoms',
     'fig.5/fig5_data (n = 100, r-squared = 0.24, F = 2.3, P = 0.014)'),
    ('S25', 'Robustness of baseline-dependent responses in MID-specific NP '
            'connectivity', 'fig.4/fig4_data/fig4_mid_by_np_grouping_n288.csv'),
    ('S26', 'Within-group comparisons of baseline versus AMPA and GABA-A',
     'the Fig. 4f/4i rows in this table'),
    ('S27', 'Longitudinal restoration-index panels (AMPA alone, GABA-A)',
     'the Supplementary Fig. S19 rows in this table'),
]
for num, what, where in XREF:
    row(f'Supplementary Fig. {num}', 'all', what, 'see cross-reference',
        'see cross-reference', 'see cross-reference',
        f'reported in {where}', '', '', '', '', '', '', '', '', '', where)

# ------------------------------------------------------------------ write ----
TAB = pd.DataFrame(ROWS)[COLS]


def _order(f):
    if f.startswith('Fig. '):
        return (0, int(f.split()[1]))
    return (1, int(f.split('S')[-1].split()[0]))


TAB['_k'] = TAB.figure.map(_order)
TAB = TAB.sort_values('_k', kind='stable').drop(columns='_k').reset_index(drop=True)

HEAD = {
    'figure': 'Figure', 'panel': 'Panel',
    'quantity': 'Quantity tested', 'n': 'Sample size',
    'unit': 'Unit of observation',
    'error_indicator': 'Error indicator drawn in the panel',
    'test': 'Statistical test', 'sided': 'Sidedness', 'paired': 'Pairing',
    'correction': 'Multiple-comparison correction',
    'statistic': 'Test statistic', 'df': 'Degrees of freedom',
    'p_exact': 'Exact P', 'p_corrected': 'Corrected P',
    'effect': 'Effect size', 'ci95': '95% confidence interval',
    'source': 'Source data file and notes'}

OUT = os.path.join(HERE, 'Table_S21_rebuilt.csv')
TAB.rename(columns=HEAD).to_csv(OUT, index=False)
print(f'{len(TAB)} rows -> {OUT}')
print(TAB.figure.value_counts().reindex(TAB.figure.unique()).to_string())
