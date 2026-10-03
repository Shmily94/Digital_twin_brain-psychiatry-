# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_added_variable_n85.csv; 04_figures/fig.5/fig5_data/fig5h_added_variable_n85.csv
# cell id       : d04f2aa4-9fe4-4442-b3e8-91a60dce08ff
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 459
# executed at   : 2026-09-21 20:46 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/20_fig5h_added_variable_n85.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
D5='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data'
pd.DataFrame(dict(ampa_index_resid=xr, fu3_change_resid=yr)).to_csv(f'{D5}/fig5h_added_variable_n85.csv', index=False)
T.to_csv(f'{D5}/fig5h_nested_models.csv', index=False)
pd.DataFrame(dict(deltaR2_null_ampa=ampa_null, deltaR2_null_gaba=gaba_null)).to_csv(f'{D5}/fig5h_deltaR2_null.csv', index=False)
print(T[['predictor','delta_R2','F_change','p_change','p_perm_deltaR2','partial_r','cvR2_reduced','cvR2_full']].round(4).to_string(index=False))
