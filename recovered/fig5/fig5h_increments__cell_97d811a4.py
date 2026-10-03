# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_increments.csv; 04_figures/fig.5/fig5_data/fig5h_increments.csv
# cell id       : 97d811a4-384e-40b3-96ad-ba3552f8f339
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 496
# executed at   : 2026-09-21 21:18 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/23_fig5h_increments.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
INC2 = pd.read_csv(f'{D5}/fig5h_increments.csv')
INC2.insert(2, 'n', len(y))
INC2['p_full_predictors'] = INC2.df2.apply(lambda d: len(y) - int(d) - 1)
INC2.to_csv(f'{D5}/fig5h_increments.csv', index=False)
print(INC2[['index','covariates','n','p_full_predictors','df2','delta_R2','p_change']].to_string(index=False))
