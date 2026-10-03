# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 35f2aef2-4a42-4acb-bbb7-45923b243e90
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-21 15:44:47 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3h_cumulative_share_1b.csv
# ===========================================================================

import numpy as np, pandas as pd
# per-subject cumulative share of the total absolute edge change (Lorenz-style)
cum_rows=[]
for drug,lab in [('ampa','AMPA'),('gaba','GABA-A')]:
    for sid in s.index:
        sub=long1b.xs(sid,level='sub_id').loc[EORD]
        de=(sub[drug]-sub['baseline']).abs().values
        d_sorted=np.sort(de)[::-1]; c=np.cumsum(d_sorted)/d_sorted.sum()
        for i,v in enumerate(c,1):
            cum_rows.append(dict(modulation=lab, sub_id=sid, n_edges=i, cum_share=round(float(v),4)))
cum=pd.DataFrame(cum_rows)
D3='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data'
cum.to_csv(f'{D3}/fig3h_cumulative_share_1b.csv',index=False)
m=cum.groupby(['modulation','n_edges']).cum_share.agg(['mean','std'])
print(m.round(3).unstack(0).to_string())
print('\nper-subject counts:')
print(psub.groupby('modulation').n_edges_concordant.agg(['min','median','max','mean']).round(2).to_string())