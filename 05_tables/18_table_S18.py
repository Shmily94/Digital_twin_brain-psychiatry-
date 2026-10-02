"""05_tables/18_table_S18.py

WHAT THIS SCRIPT COMPUTES
    Table S18 of the supplementary workbook, both sub-tables:
      S18a - frequencies and within-group percentages of the nine IMAGEN
             recruitment sites between the two response groups after virtual
             modulation (Increased n = 229, Decreased n = 59; n = 288 total);
      S18b - the same for sex.
    It also computes every test quoted in the two legends.

    Response groups follow the manuscript definition: "Increased" = negative-profile
    NP connectivity increased under both AMPA and GABA-A modulation (pattern
    "both up"); "Decreased" = a decrease under either modulation (pattern
    "any down").

INPUT FILES
    04_figures/fig.4/fig4_data/fig4_subject_level_n288.csv
        columns used: ID, Group, sex, site, pattern
    05_tables/mani_ampa_gaba_subs_diff_london_site.csv
        the IMAGEN recruitment-site record that separates the two London
        sub-sites (LONDON -> London-Invicro, LONDON2 -> London-CNS). Copied into
        this package from Figures/Figure4/ in the author's working tree; it is the
        only input of this script that does not live in the figure tree.

OUTPUT FILES
    $OUT_DIR/table_S18a_site_frequencies.csv
    $OUT_DIR/table_S18b_sex_frequencies.csv
    (OUT_DIR defaults to the system temp directory; the script never writes into
    04_figures/)

STATISTICAL TESTS PERFORMED
    Pearson chi-square test of independence between response group and recruitment
    site over the nine sites, two-sided, uncorrected (chi-square(8)); because 7 of
    18 expected counts fall below 5, a Monte-Carlo permutation test with 10,000
    random reassignments of response group is reported alongside it.
    The same chi-square test with the two London sub-sites collapsed
    (chi-square(7)), as stated in the legend.
    Pearson chi-square test of independence between response group and sex
    (chi-square(1)), two-sided, uncorrected, with Fisher's exact test, and a
    logistic regression of response group on sex and diagnostic group.

LAPTOP RUNNABLE
    yes - two CSV files, one 10,000-iteration permutation loop, a few seconds.

RECOVERED FROM
    execution-log cells in frame b194cd74-... (conda env python), archived verbatim
    under recovered/tables/:
      280fac11-...  loads fig4_subject_level_n288.csv          (table_S18__cell_280fac11.py)
      19bdc062-...  sex/site crosstabs, chi-square, Fisher     (table_S18__cell_19bdc062.py)
      1af34d03-...  logistic adjustment for diagnostic group   (table_S18__cell_1af34d03.py)
      63137639-...  cleans the recruitment-site strings        (table_S18__cell_63137639.py)
      693b42e0-...  nine-site crosstab                         (table_S18__cell_693b42e0.py)
      fce4c8ce-...  chi-square, permutation test, collapse     (table_S18__cell_fce4c8ce.py)
      5b272353-...  writes the shipped S18a/S18b blocks        (table_S18__cell_5b272353.py)
    Cell 8d54e0ef-... (table_S18__cell_8d54e0ef.py) is an earlier, superseded
    version of the same sheet that collapsed London into a single site.

REORGANISATION APPLIED
    Header added; the seven-cell chain above merged into one script; paths made
    explicit and repointed at this package; the openpyxl workbook writing and
    styling dropped in favour of two CSV outputs; the exploratory prints and the
    abandoned eight-site variant kept only where the legend quotes them. No
    computation, covariate or test was changed.

seed: fixed in the original run - numpy default_rng(0) for the permutation test,
      carried over unchanged, so the permutation P is exactly reproducible.
"""
import os
import tempfile

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, '..'))
FG = os.path.join(PKG, '04_figures')
OUT_DIR = os.environ.get('OUT_DIR', tempfile.gettempdir())

S = pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4_subject_level_n288.csv'))
L = pd.read_csv(os.path.join(HERE, 'mani_ampa_gaba_subs_diff_london_site.csv'))

# --- recruitment site with the two London sub-sites separated ---------------
L['s2'] = L['recruitmentSite.2'].astype(str).str.replace("'", "").str.strip()
LAB = {'LONDON': 'London-Invicro', 'LONDON2': 'London-CNS'}
m = S.merge(L[['ID', 's2']], on='ID', how='left')
assert m['s2'].notna().all(), 'site record does not cover all 288 participants'
m['site9'] = m['s2'].map(lambda x: LAB.get(x, x.capitalize()))
m['grp'] = m['pattern'].map({'both up': 'Increased', 'any down': 'Decreased'})

ORD = ['Berlin', 'Dresden', 'Dublin', 'Hamburg', 'London-Invicro', 'London-CNS',
       'Mannheim', 'Nottingham', 'Paris']
GRP = ['Increased', 'Decreased']
ct = (pd.crosstab(m['grp'], m['site9'])
        .reindex(index=GRP, columns=ORD).fillna(0).astype(int))
sex_ct = pd.crosstab(m['grp'], m['sex']).reindex(index=GRP)
nI, nD = int(ct.loc['Increased'].sum()), int(ct.loc['Decreased'].sum())

# --- tests quoted in the S18a legend ---------------------------------------
chi2, p_site, dof, exp = stats.chi2_contingency(ct.values)

rng = np.random.default_rng(0)
g, s9 = m['grp'].values, m['site9'].values
cnt, N = 0, 10000
for _ in range(N):
    t = pd.crosstab(rng.permutation(g), s9).values
    cnt += stats.chi2_contingency(t)[0] >= chi2 - 1e-9
p_perm = (cnt + 1) / (N + 1)

ct8 = pd.crosstab(m['grp'], m['site']).reindex(index=GRP)
chi2_8, p_site8, dof8, _ = stats.chi2_contingency(ct8.values)

# --- tests quoted in the S18b legend ---------------------------------------
chi2_x, p_sex, dof_x, _ = stats.chi2_contingency(sex_ct.values)
odds, p_fisher = stats.fisher_exact(sex_ct.values)
dd = m.copy()
dd['y'] = (dd.grp == 'Decreased').astype(int)
m2 = smf.logit('y ~ C(sex) + C(Group)', data=dd).fit(disp=0)
z_sex, p_sex_adj = m2.tvalues['C(sex)[T.M]'], m2.pvalues['C(sex)[T.M]']

# --- the two sheet blocks ---------------------------------------------------
def block(tab, levels, level_name):
    rows = []
    for grp, n in ((GRP[0], nI), (GRP[1], nD)):
        first = True
        for lv in levels:
            f = int(tab.loc[grp, lv]) if lv in tab.columns else 0
            rows.append([grp if first else '', lv, f, f / n]); first = False
        rows.append(['', 'Missing', 0, 0.0])
        rows.append(['', 'Total', n, 1.0])
    return pd.DataFrame(rows, columns=['Group', level_name, 'Frequency', 'Percent'])

A = block(ct, ORD, 'Site')
B = block(sex_ct, ['F', 'M'], 'Sex')
OA = os.path.join(OUT_DIR, 'table_S18a_site_frequencies.csv')
OB = os.path.join(OUT_DIR, 'table_S18b_sex_frequencies.csv')
A.to_csv(OA, index=False); B.to_csv(OB, index=False)

print(A.to_string(index=False))
print('\nS18a legend: chi-squared(%d) = %.2f, P = %.3f (two-sided, uncorrected); '
      '%d of %d expected counts < 5, permutation P = %.3f; London collapsed: '
      'chi-squared(%d) = %.2f, P = %.3f'
      % (dof, chi2, p_site, (exp < 5).sum(), exp.size, p_perm, dof8, chi2_8, p_site8))
print('\n' + B.to_string(index=False))
print('\nS18b legend: chi-squared(%d) = %.2f, P = %.3f; Fisher exact P = %.3f; '
      'logistic regression on sex + diagnostic group: z = %.2f, P = %.3f'
      % (dof_x, chi2_x, p_sex, p_fisher, z_sex, p_sex_adj))
print('\n-> %s\n-> %s' % (OA, OB))
