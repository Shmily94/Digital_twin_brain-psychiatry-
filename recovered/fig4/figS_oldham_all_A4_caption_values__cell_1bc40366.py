# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_oldham_all/figS_oldham_all_A4_caption_values.csv
#
# cell id      : 1bc40366-1cb9-4e77-8657-6f41c4367cc7
# frame id     : 25343478-9a78-4867-bcc3-f40b07365f59
# timestamp    : 2026-09-27 05:41:05 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/45_figS_oldham_all_A4_caption_values.py
##############################################################################

src = open(os.path.join(FG,'supp_oldham','figS_oldham_A4.py')).read()
new_doc = '''"""Supplementary figure: Oldham's test for baseline dependence, all seven
scatter panels on ONE A4 page.

Panel order requested by the author: the simulation with the full 12-edge NP
factor, the simulation with the six MID-specific NP edges, the healthy
pharmacology cohort, then the clinical pharmacology cohort.

  a  DTB model, full NP factor, baseline -> AMPA
  b  DTB model, full NP factor, baseline -> GABA-A
  c  DTB model, six MID edges, baseline -> AMPA
  d  DTB model, six MID edges, baseline -> GABA-A
  e  Healthy cohort, placebo -> ketamine
  f  Healthy cohort, placebo -> midazolam
  g  Clinical cohort, placebo -> ketamine

Oldham's test regresses the change (post - pre) on the AVERAGE of the two
measurements rather than on the baseline, which removes the mathematical
coupling of the naive baseline-versus-change correlation.

    python figS_oldham_all_A4.py [--no-caption]
"""'''
src = src[src.index('"""')+3:]
src = src[src.index('"""')+3:]
src = new_doc + src
src = src.replace('HERE = os.path.join(FIGDIR, "supp_oldham")', 'HERE = os.path.join(FIGDIR, "supp_oldham_all")')
src = src.replace('STEM = "figS_oldham_A4" if WITH_CAP else "figS_oldham_A4_nocaption"',
                  'STEM = "figS_oldham_all_A4" if WITH_CAP else "figS_oldham_all_A4_nocaption"')
src = src.replace('"oldham_tests.csv"', '"oldham_tests_all.csv"').replace('"oldham_subject_level.csv"', '"oldham_subject_level_all.csv"')
src = src.replace('figS_oldham_A4_caption_values.csv', 'figS_oldham_all_A4_caption_values.csv')
old_spec = src[src.index('SPEC = ['):src.index(']\nS = {}')+1]
new_spec = '''SPEC = [
    ("a", "model_ampa", "ampa", "Simulation, full NP",
     "Mean of baseline\\nand AMPA state", "AMPA state \\u2212 baseline"),
    ("b", "model_gaba", "gaba", "Simulation, full NP",
     "Mean of baseline\\nand GABA-A state", "GABA-A state \\u2212 baseline"),
    ("c", "mid6_ampa", "ampa", "Simulation, six MID edges",
     "Mean of baseline\\nand AMPA state", "AMPA state \\u2212 baseline"),
    ("d", "mid6_gaba", "gaba", "Simulation, six MID edges",
     "Mean of baseline\\nand GABA-A state", "GABA-A state \\u2212 baseline"),
    ("e", "healthy_ket", "ketamine", "Healthy",
     "Mean of placebo\\nand ketamine", "Ketamine \\u2212 placebo"),
    ("f", "healthy_mid", "midazolam", "Healthy",
     "Mean of placebo\\nand midazolam", "Midazolam \\u2212 placebo"),
    ("g", "clinical_ket", "ketamine", "Clinical",
     "Mean of placebo\\nand ketamine", "Ketamine \\u2212 placebo"),
]'''
src = src.replace(old_spec, new_spec)
src = src.replace('ROWS = [["a", "b", "c"], ["d", "e"]]\nCOLS = [["a", "d"], ["b", "e"], ["c"]]\nNCOL, NROW = 3, len(ROWS)',
                  'ROWS = [["a", "b", "c", "d"], ["e", "f", "g"]]\nCOLS = [["a", "e"], ["b", "f"], ["c", "g"], ["d"]]\nNCOL, NROW = 4, len(ROWS)')
src = src.replace('SUPP_NO = "S12"', 'SUPP_NO = "S12"')
open(os.path.join(ALLD,'figS_oldham_all_A4.py'),'w').write(src)
print('SPEC replaced: %s | ROWS replaced: %s' % (new_spec in src, 'ROWS = [["a", "b", "c", "d"]' in src))
print('remaining references to the old data files: %d' % (src.count('oldham_tests.csv')+src.count('oldham_subject_level.csv')))
