# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/supp_longitudinal/figS14_longscatter_A4_caption_values.csv
# cell id       : 1344c602-0326-4ea0-abe2-e4a2e3b4e4c4
# frame id      : 8d001885-f89b-4ca4-9e30-9866f1015ee6
# cell_index    : 590
# executed at   : 2026-09-24 23:29 UTC
# language      : bash
# organised as  : 03_analysis/fig5/59_figS14_longscatter_A4_caption_values.py
# This data file is a render-time by-product of 04_figures/supp_longitudinal/figS14_longscatter_A4.py.
# The cell below is the execution-log cell that produced the packaged copy
# (it runs, or last edits and runs, that figure script). The derivation itself
# is the figure script, which is already in the package.
# ---------------------------------------------------------------------------
cd /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_longitudinal && python3 figS14_longscatter_A4.py 2>&1|tail -3 && python3 figS14_longscatter_A4.py --no-caption 2>&1|head -1 && cp figS14_longscatter_A4.png figS14_longscatter_A4.pdf figS14_longscatter_A4.pptx figS14_longscatter_A4_nocaption.png figS14_longscatter_A4_nocaption.pdf figS14_longscatter_A4_nocaption.pptx figS14_longscatter_A4.py figS14_longscatter_A4_caption_values.csv "$OLDPWD"/ && echo staged