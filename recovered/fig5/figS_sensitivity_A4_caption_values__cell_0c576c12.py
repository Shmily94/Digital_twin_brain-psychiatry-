# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/supp_sensitivity/figS_sensitivity_A4_caption_values.csv
# cell id       : 0c576c12-8872-4f63-ae9c-8fb074bc842b
# frame id      : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
# cell_index    : 76
# executed at   : 2026-09-24 23:21 UTC
# language      : bash
# organised as  : 03_analysis/fig5/62_figS_sensitivity_A4_caption_values.py
# This data file is a render-time by-product of 04_figures/supp_sensitivity/figS_sensitivity_A4.py.
# The cell below is the execution-log cell that produced the packaged copy
# (it runs, or last edits and runs, that figure script). The derivation itself
# is the figure script, which is already in the package.
# ---------------------------------------------------------------------------
cd "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_sensitivity" && python - <<'PY'
p = "figS_sensitivity_A4.py"
s = open(p).read()

# 1. drop every panel sub-title
for t in ['    panel_title(ax, "Mean \\u0394 NP at every conductance setting")\n    ax.title.set_fontsize(LABEL_PT)\n',
          '    panel_title(ax, "Responders by diagnostic group")\n    ax.title.set_fontsize(LABEL_PT)\n',
          '    panel_title(ax, "Per-twin stability")\n    ax.title.set_fontsize(LABEL_PT)\n',
          '    panel_title(ax, head)\n    ax.title.set_fontsize(LABEL_PT)\n',
          '    panel_title(ax, "Baseline versus change")\n    ax.title.set_fontsize(LABEL_PT)\n']:
    assert t in s, t[:40]
    s = s.replace(t, "")

# 2. drop panel f from the layout
s = s.replace('PANEL_FN = {"a": p_a, "b": p_b, "c": p_c, "d": p_d, "e": p_e, "f": p_f}',
              'PANEL_FN = {"a": p_a, "b": p_b, "c": p_c, "d": p_d, "e": p_e}\n'
              '# p_f (baseline versus change) is kept above but no longer placed')
s = s.replace('ROWS = [(["a", "b"], 12.0), (["c", "d", "e", "f"], 12.0)]   # (letters, x band)',
              'ROWS = [(["a", "b"], 12.0), (["c", "d", "e"], 12.0)]        # (letters, x band)')
s = s.replace('BLOCK = {"a": 88.0, "b": 87.0,                             # 175 + 1 gap = 180\n'
              '         "c": 40.0, "d": 43.0, "e": 43.0, "f": 39.0}       # 165 + 3 gaps = 180',
              'BLOCK = {"a": 88.0, "b": 87.0,                             # 175 + 1 gap = 180\n'
              '         "c": 54.0, "d": 58.0, "e": 58.0}                  # 170 + 2 gaps = 180')

# 3. caption: d-f -> d-e, and remove the f entry
s = s.replace('d-f  INDIVIDUAL level', 'd-e  INDIVIDUAL level')
s = s.replace('"d-f test the TASK CONTEXT', '"d-e test the TASK CONTEXT')
s = s.replace('"of the reward and inhibition tasks. HC02 is excluded from d-f "',
              '"of the reward and inhibition tasks. HC02 is excluded from d-e "')
s = s.replace('"artefact of the conductance chosen, in the full sample; d-f "',
              '"artefact of the conductance chosen, in the full sample; d-e "')
f_entry = '''        ("f", ", change against baseline for both tasks and both "
              "perturbations, 12 twin-by-perturbation observations in all; "
              "the twins that start lowest gain most, in either task. "),
'''
assert f_entry in s
s = s.replace(f_entry, "")
s = s.replace('# -------------------------------------------- d-f  EFT validation, 3 twins',
              '# -------------------------------------------- d-e  EFT validation, 3 twins')
open(p, "w").write(s)
print("panel_title left:", s.count("panel_title("), "| f in ROWS:", '"f"' in s.split("ROWS = ")[1].split("\n")[0])
PY
python figS_sensitivity_A4.py && python figS_sensitivity_A4.py --no-caption