"""05_tables/17_table_S17.py

WHAT THIS SCRIPT COMPUTES
    Table S17 of the supplementary workbook: "The distribution of different response
    individuals following AMPA and GABA-A manipulations (n = 288 digital twins)".
    Each digital twin is classified by the sign of its NP-factor change under the two
    virtual modulations, giving four response categories (AMPA up/down x GABA-A
    up/down); the table reports the count and within-group percentage of each
    category for healthy controls, high-symptom participants and patients, and for
    the pooled sample, together with the chi-square tests quoted in the table legend.

INPUT FILES
    04_figures/fig.4/fig4_data/fig4_subject_level_n288.csv
        columns used: Group, d_ampa (NP change after AMPA modulation),
        d_gaba (NP change after GABA-A modulation on the high-AMPA state)

OUTPUT FILE
    $OUT_DIR/table_S17_response_distribution.csv   (OUT_DIR defaults to the system
    temp directory; the script never writes into 04_figures/)

STATISTICAL TESTS PERFORMED
    Chi-square test of independence on the full four-category x three-group table
    (chi-square(6)), two-sided, no multiple-comparison correction.
    Chi-square test of independence on the collapsed two-category table
    (both-increased versus any-decreased) x three groups (chi-square(2)), two-sided.
    The collapsed test is the one reported in the manuscript, because the
    four-category table is too sparse for the asymptotic chi-square: 6 of its 12
    cells hold fewer than five participants (observed 1, 1, 3 in the "AMPA
    increased, GABA-A decreased" column and 1, 0, 0 in the "AMPA decreased, GABA-A
    decreased" column), and the same 6 cells have expected counts below five
    (1.198, 1.545, 2.257 and 0.240, 0.309, 0.451). NOTE FOR THE AUTHOR: the legend
    shipped in the workbook states "three cells contain fewer than five
    participants"; the count is 6 of 12 on both the observed and the expected
    counts, verified from fig4_subject_level_n288.csv. The test statistics
    themselves are unaffected - this is the sparsity justification quoted in the
    legend, not an input to any computation.

LAPTOP RUNNABLE
    yes - single 288-row CSV, runs in under a second.

RECOVERED FROM
    execution-log cell 674db32f-... (frame fe47a03f-..., conda env python), which
    computed the crosstab and the four-category chi-square, archived verbatim as
    recovered/tables/table_S17__cell_674db32f.py. The counts and percentages were
    written into the workbook by cell 07ddb4a7-... (same frame), archived as
    recovered/tables/table_S17__cell_07ddb4a7.py, which also carries the collapsed
    chi-square quoted in the legend.

REORGANISATION APPLIED
    Header added; the input path made explicit (the original cell used a DataFrame
    `F4` already in the kernel and an artefact-store helper); the category labels and
    the workbook row assembly of cell 07ddb4a7 merged into this one script; the
    workbook-writing and openpyxl styling dropped. No computation changed.

seed: not applicable (no resampling in this script)
"""
import os
import tempfile

import numpy as np
import pandas as pd
from scipy import stats as st

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, '..'))
FG = os.path.join(PKG, '04_figures')
OUT_DIR = os.environ.get('OUT_DIR', tempfile.gettempdir())

F4 = pd.read_csv(os.path.join(FG, 'fig.4/fig4_data/fig4_subject_level_n288.csv'))

# --- four response categories, exactly as in the recovered cell -------------
F4['pat2'] = np.where(F4.d_ampa > 0, 'A+', 'A-') + np.where(F4.d_gaba > 0, ' G+', ' G-')
ctab = pd.crosstab(F4.Group, F4.pat2)

PAT = ['A+ G+', 'A+ G-', 'A- G+', 'A- G-']
LAB = ['AMPA increased, GABA-A increased', 'AMPA increased, GABA-A decreased',
       'AMPA decreased, GABA-A increased', 'AMPA decreased, GABA-A decreased']

rows = []
for gp in ['HC', 'High-symptom', 'Patient']:
    tot = int(ctab.loc[gp].sum())
    rows.append([gp] + ['%d (%.2f%%)' % (ctab.loc[gp, p], 100 * ctab.loc[gp, p] / tot)
                        for p in PAT] + ['%d (100%%)' % tot])
tt = int(ctab.values.sum())
rows.append(['All'] + ['%d (%.2f%%)' % (ctab[p].sum(), 100 * ctab[p].sum() / tt)
                       for p in PAT] + ['%d (100%%)' % tt])
TAB = pd.DataFrame(rows, columns=['Group'] + LAB + ['Total'])

# --- the two chi-square tests quoted in the table legend --------------------
full = ctab[[c for c in ctab.columns if ctab[c].sum() > 0]]
c_full = st.chi2_contingency(full)

coll = pd.DataFrame({'both increased': ctab['A+ G+'],
                     'any decreased': ctab[[p for p in PAT if p != 'A+ G+']].sum(axis=1)})
c_coll = st.chi2_contingency(coll.values)

OUT = os.path.join(OUT_DIR, 'table_S17_response_distribution.csv')
TAB.to_csv(OUT, index=False)
print(TAB.to_string(index=False))
print('\nfour-category test : chi-square(%d) = %.3f, P = %.4g'
      % (c_full.dof, c_full.statistic, c_full.pvalue))
print('collapsed test     : chi-square(%d) = %.2f, P = %.2g'
      % (c_coll[2], c_coll[0], c_coll[1]))
print('\n%d rows -> %s' % (len(TAB), OUT))
