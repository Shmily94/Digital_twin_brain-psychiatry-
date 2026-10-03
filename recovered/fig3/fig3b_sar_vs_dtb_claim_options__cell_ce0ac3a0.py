# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : ce0ac3a0-7019-4666-b760-e945da67ce43
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 16:06:56 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3b_sar_vs_dtb_claim_options.csv
# ===========================================================================

P=P[~((P.panel=='3b')&(P.df==3))].copy(); P.to_csv(D3+'fig3_results_paragraph_contrasts.csv',index=False)
pd.DataFrame([dict(status='RESOLVED in v4',note=(
 'The SAR-versus-3M/268 problem no longer exists. With the 3M build re-scored on the corrected '
 'task-FC pipeline, 3M/268 = 0.3485 +- 0.0565 exceeds SAR = 0.2342 +- 0.0317 in 12 of 12 '
 'participants (diff +0.1143, 95% CI +0.0888 to +0.1397, paired t(11) = 9.891, P = 8.24e-07) and '
 'rWW = 0.1486 +- 0.0235 (diff +0.1999, t(11) = 16.143, P = 5.25e-09). The options previously '
 'listed in this file - all of which assumed SAR > 3M/268 - are withdrawn, including the '
 'Bonferroni family-size calculation (576,555 tests) and the TOST equivalence analysis.'),
 superseded_claim='SAR > 3M/268 by +0.0831, t(11) = 12.35, P = 8.67e-08 (computed from the superseded 3M run)')
 ]).to_csv(D3+'fig3b_sar_vs_dtb_claim_options.csv',index=False)
print('paragraph contrasts now %d rows; 3b rows: %d'%(len(P),(P.panel=='3b').sum()))
for fn in ['fig3b_wholebrain_fc_crossscale.csv','fig3b_wholebrain_fc_by_condition.csv',
           'fig3b_common_reference_tests.csv','fig3_results_paragraph_contrasts.csv',
           'fig3b_sar_vs_dtb_claim_options.csv','fig3_3m_run_provenance.csv']:
    shutil.copy(D3+fn,WS+fn)
shutil.copy(F3+'panels/fig3b.png',WS+'fig3b.png')
shutil.copy(SUB+'revision/text/_revision/results_calibration_draft.md',WS+'results_calibration_draft.md')
shutil.copy(SUB+'revision/text/_revision/main_figure_legends.md',WS+'main_figure_legends.md')
shutil.copy(XL,WS+'Suppl.Table_revision_updated.xlsx')
print('staged')