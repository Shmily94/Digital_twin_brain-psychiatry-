# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/tableS24_audit_summary.csv
# cell id       : 258bd81e-6258-4c60-8b5c-69c980e89aa1
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 636
# executed at   : 2026-09-29 11:59 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/36_tableS24_audit_summary.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

S24TXT=' '.join(str(s24.cell(row=r,column=c).value or '') for r in range(1,s24.max_row+1) for c in range(1,18))
miss4=sorted({(re.sub(r'\s+',' ',m.group(1)).strip(' ,.('),m.group(2)) for t in acc4 for m in LABV.finditer(t)
              if '.' in m.group(2) and m.group(2) not in S24TXT})
print('main-text statistics absent from Table S24:', len(miss4), miss4)
summary=pd.DataFrame([dict(item='Table S24 data rows', value=231),
  dict(item='main-figure rows', value=51+11),
  dict(item='main-figure rows missing effect size', value=0),
  dict(item='main-figure rows missing 95% CI', value=0),
  dict(item='main-text statistics absent from Table S24', value=len(miss4)),
  dict(item='cells reformatted to the house number rules', value=len(L))])
summary.to_csv('tableS24_audit_summary.csv',index=False); print(summary.to_string(index=False))
