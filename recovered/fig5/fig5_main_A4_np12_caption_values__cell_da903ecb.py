# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/fig.5/fig5_main_A4_np12_caption_values.csv
# cell id       : da903ecb-7665-4217-81f7-eb52ee5af3ea
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 152
# executed at   : 2026-09-26 21:42 UTC
# language      : python
# organised as  : 03_analysis/fig5/43_fig5_main_A4_np12_caption_values.py
# This data file is a render-time by-product of 04_figures/fig.5/fig5_main_A4_np12.py.
# The cell below is the execution-log cell that produced the packaged copy
# (it runs, or last edits and runs, that figure script). The derivation itself
# is the figure script, which is already in the package.
# ---------------------------------------------------------------------------

for f in ['fig5_main_A4_np12.png','fig5_main_A4_np12.pdf','fig5_main_A4_np12.pptx','fig5_main_A4_np12_nocaption.png','fig5_main_A4_np12_nocaption.pdf','fig5_main_A4_np12_nocaption.pptx','fig5_main_A4_np12.py','fig5_main_A4_np12_caption_values.csv']:
    shutil.copy(os.path.join(HERE5,f), f)
shutil.copy(os.path.join(D5,'fig5h_np12_loo_n85.csv'),'fig5h_np12_loo_n85.csv')
shutil.copy(os.path.join(D5,'fig5i_np12_loo_accuracy.csv'),'fig5i_np12_loo_accuracy.csv')
print(open('fig5_main_A4_np12_caption_values.csv').read()[-700:])
