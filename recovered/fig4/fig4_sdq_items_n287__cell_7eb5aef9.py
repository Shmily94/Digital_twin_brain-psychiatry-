# Verbatim archive of the execution-log cell that produced
#     04_figures/fig.4/fig4_data/fig4_sdq_items_n287.csv
#
# cell id      : 7eb5aef9-b7c8-4b6e-8b24-607618d2a160
# frame id     : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp    : 2026-09-21 16:05:41 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/08_fig4_sdq_items_n287.py
##############################################################################
M[['id','pattern','Group']+SDQ].rename(columns={'id':'ID'}).to_csv(
    f'{OUT}/fig4_data/fig4_sdq_items_n287.csv',index=False)
print(len(M), 'rows written')
