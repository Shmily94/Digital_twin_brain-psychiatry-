# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/ED_renumbering_map.csv
# cell id       : 22ca620c-f728-4fbd-bd5f-caf8b66c31bf
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 703
# executed at   : 2026-09-29 13:56 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/01_ED_renumbering_map.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

rows=[]
for old,n in sorted(ED.items(), key=lambda kv: kv[1]):
    rows.append(dict(old_label='Fig. %s'%old, new_label='Extended Data Fig. %d'%n, destination='Extended Data',
                     first_cited_main_text_para=[i for t,i in order if t==old][0] if old in [t for t,_ in order] else ''))
for old,n in sorted(SINEW.items(), key=lambda kv: kv[1]):
    rows.append(dict(old_label='Fig. %s'%old, new_label='Fig. S%d'%n, destination='Supplementary Information',
                     first_cited_main_text_para=[i for t,i in order if t==old][0] if old in [t for t,_ in order] else 'Methods only'))
MAP=pd.DataFrame(rows); MAP.to_csv('ED_renumbering_map.csv',index=False)
print(MAP.to_string(index=False))
