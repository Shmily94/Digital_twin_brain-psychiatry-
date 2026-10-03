# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_R2_permutation_null.csv; 04_figures/fig.5/fig5_data/fig5h_R2_permutation_null.csv
# cell id       : ab31e3b1-ddf0-4dee-b68d-97a80292f672
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 433
# executed at   : 2026-09-21 20:25 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/19_fig5h_R2_permutation_null.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
sc=lambda k: float(np.asarray(M[k]).ravel()[0])
pd.DataFrame([dict(R2_reduced=sc('R2_reduced'),R2_full=sc('R2_full'),
  delta_R2=sc('R2_full')-sc('R2_reduced'),F_change=sc('F_change'),p_change=sc('p_change'),
  p_perm_R2=sc('p_perm_R2'),beta=sc('beta_real'),p_perm_beta=sc('p_perm_beta'),
  n=int(sc('n')),n_perm=int(sc('Nperm')))]).to_csv(f'{O5}/fig5_data/fig5h_model_stats.csv',index=False)
np.savetxt(f'{O5}/fig5_data/fig5h_R2_permutation_null.csv',np.asarray(M['R2_perm']).ravel(),
           delimiter=',',header='R2_perm',comments='')
print(sorted(os.listdir(f'{O5}/fig5_data')))
print(pd.read_csv(f'{O5}/fig5_data/fig5h_model_stats.csv').round(4).to_string(index=False))