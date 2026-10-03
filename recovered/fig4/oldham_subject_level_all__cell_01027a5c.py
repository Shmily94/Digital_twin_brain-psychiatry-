# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_oldham_all/data/oldham_subject_level_all.csv
#
# cell id      : 01027a5c-247d-4fe8-9735-13a80ad2e877
# frame id     : 25343478-9a78-4867-bcc3-f40b07365f59
# timestamp    : 2026-09-27 05:40:36 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/43_oldham_subject_level_all.py
##############################################################################

FG = '/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures'
ALLD = os.path.join(FG, 'supp_oldham_all')
os.makedirs(os.path.join(ALLD,'data'), exist_ok=True); os.makedirs(os.path.join(ALLD,'panels'), exist_ok=True)
T_old = pd.read_csv(os.path.join(FG,'supp_oldham','data','oldham_tests.csv'))
S_old = pd.read_csv(os.path.join(FG,'supp_oldham','data','oldham_subject_level.csv'))
T_new = pd.read_csv(os.path.join(FG,'supp_oldham_mid6','data','oldham_tests_mid6.csv'))
S_new = pd.read_csv(os.path.join(FG,'supp_oldham_mid6','data','oldham_subject_level_mid6.csv'))
T_new['note'] = T_new['note'].fillna('')
Tc = pd.concat([T_old, T_new[T_new.series.str.startswith('mid6')]], ignore_index=True)
Sc = pd.concat([S_old, S_new], ignore_index=True)
Tc.to_csv(os.path.join(ALLD,'data','oldham_tests_all.csv'), index=False)
Sc.to_csv(os.path.join(ALLD,'data','oldham_subject_level_all.csv'), index=False)
need = ['model_ampa','model_gaba','mid6_ampa','mid6_gaba','healthy_ket','healthy_mid','clinical_ket']
print('series present in combined tests: %s' % [s for s in need if s in set(Tc.series)])
print('subject-level counts: %s' % {s: int((Sc.series==s).sum()) for s in need})
print('\nOldham r / P for the seven panels:')
print(Tc.set_index('series').loc[need, ['n','oldham_r','oldham_p','variance_ratio_post_pre','naive_baseline_change_r']].to_string(float_format=lambda v:'%.4g'%v))
