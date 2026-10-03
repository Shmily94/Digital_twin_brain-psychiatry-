# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_oldham_mid6/data/oldham_tests_mid6.csv
#
# cell id      : 28602d61-418b-4441-9ab4-50fb918dd1ca
# frame id     : 25343478-9a78-4867-bcc3-f40b07365f59
# timestamp    : 2026-09-27 05:28:48 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/47_oldham_tests_mid6.py
##############################################################################

print('actual Oldham P values: %s' % {r.series: '%.3e' % r.oldham_p for _, r in TESTS.iterrows()})
KEEP_FULL = ['oldham_p','naive_p','slope_vs1_p']
T2 = TESTS.copy()
for c in T2.columns:
    if c not in KEEP_FULL and pd.api.types.is_float_dtype(T2[c]): T2[c] = T2[c].round(6)
T2.to_csv(os.path.join(OUT,'data','oldham_tests_mid6.csv'), index=False)
print('re-written with full-precision P columns')
