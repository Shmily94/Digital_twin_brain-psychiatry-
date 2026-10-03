# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 0163c09f-c9cf-47ae-961c-d962f84d30fe
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 18:14:50 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3c_metric_comparison.csv
# ===========================================================================

SP.to_csv(f'{FD3}/fig3c_cross_scale_similarity.csv')
PE.to_csv(f'{FD3}/fig3c_cross_scale_similarity_pearson.csv')
d.round(4).to_csv(f'{FD3}/fig3c_metric_comparison.csv', index=False)
print(open(f'{FD3}/fig3c_cross_scale_similarity.csv').read()[:200])
