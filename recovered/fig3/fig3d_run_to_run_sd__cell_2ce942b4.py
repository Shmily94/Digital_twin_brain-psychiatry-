# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 2ce942b4-8c5c-419c-a7f3-20d6e843b2ae
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 17:19:32 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3d_run_to_run_sd.csv
# ===========================================================================

agg=(D4.dropna(subset=['np_sd']).groupby('model').np_sd.agg(['mean','std','count'])
     .rename(columns={'mean':'run_sd_mean','std':'run_sd_sd','count':'n_subjects'}))
agg=agg.reindex(ORDER).reset_index()
agg['n_repeats']=agg.model.map({**{k:v.shape[1] for k,v in REPS.items()},'10m_own':1})
agg.to_csv(f'{FD3}/fig3d_run_to_run_sd.csv', index=False)
D4.to_csv(f'{FD3}/fig3d_run_to_run_sd_per_subject.csv', index=False)
print(agg.round(4).to_string(index=False))
