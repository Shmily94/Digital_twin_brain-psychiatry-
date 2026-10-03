# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/tableS24_fix_log_v2.csv
# cell id       : e360f742-07c8-4b6a-9295-dcc3e8896c52
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 758
# executed at   : 2026-09-29 14:24 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/37_tableS24_fix_log_v2.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

setc(59,11,'leave-one-out r = 0.32; nested F(12,63) = 3.02 over the covariates; whole-model F(21,63) = 2.15','item 13: whole-model F added to match the Fig. 5h legend')
setc(59,13,'0.0088 (leave-one-out r, 5,000 permutations); 0.0022 (nested F test over the covariates); 0.0103 (whole-model F test)','item 13: whole-model P added to match the Fig. 5h legend')
wb.save('290926Suppl.Table_ED_v2.xlsx')
LOG=pd.DataFrame(log); LOG.to_csv('tableS24_fix_log_v2.csv',index=False)
print(len(LOG),'cell changes'); print(LOG.groupby('reason').size().to_string())
