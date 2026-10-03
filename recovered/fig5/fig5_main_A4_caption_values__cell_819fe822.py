# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/fig.5/fig5_main_A4_caption_values.csv
# cell id       : 819fe822-2337-4c92-b91a-25afde338a5d
# frame id      : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
# cell_index    : 162
# executed at   : 2026-09-26 12:09 UTC
# language      : bash
# organised as  : 03_analysis/fig5/42_fig5_main_A4_caption_values.py
# This data file is a render-time by-product of 04_figures/fig.5/fig5_main_A4.py.
# The cell below is the execution-log cell that produced the packaged copy
# (it runs, or last edits and runs, that figure script). The derivation itself
# is the figure script, which is already in the package.
# ---------------------------------------------------------------------------
cd "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5" && python - <<'PY'
s=open("fig5_main_A4.py").read()
probe = '''
print("row3 axes (mm from top): " + ", ".join(
    f"{ch} top {(1 - (_ax_of[ch].get_position().y0 + _ax_of[ch].get_position().height)) * PH:.2f}"
    f" bottom {(1 - _ax_of[ch].get_position().y0) * PH:.2f}"
    for ch in ("g", "h", "i")))
print("row3 xlabel/tick block: " + ", ".join(
    f"{ch} {(1 - _ax_of[ch].get_tightbbox(_r).y0 / fig.bbox.height) * PH:.2f}"
    for ch in ("g", "h", "i")))
'''
s = s.replace('K.place_letters(fig, PANELS, rows=[[ch for ch, *_ in row] for row in ROWS])',
              probe + 'K.place_letters(fig, PANELS, rows=[[ch for ch, *_ in row] for row in ROWS])', 1)
open("_probe3.py","w").write(s)
PY
python _probe3.py --no-caption 2>&1 | grep "row3"