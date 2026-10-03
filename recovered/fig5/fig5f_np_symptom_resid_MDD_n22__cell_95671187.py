# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5f_np_symptom_resid_MDD_n22.csv; 04_figures/fig.5/fig5_data/fig5f_np_symptom_resid_MDD_n22.csv
# cell id       : 95671187-f972-4268-a5e1-129878ec285a
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 1149
# executed at   : 2026-09-23 08:31 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/17_fig5f_np_symptom_resid_MDD_n22.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
import numpy as np
def resid(v,Z):
    v=np.asarray(v,float); A=np.column_stack([np.ones(len(v)),Z]); return v-A@np.linalg.lstsq(A,v,rcond=None)[0]
q2=q.copy()   # patients n=22, has symp_b0_pca, symp_delta_pca, delta(11-edge), age, sexM, drug_first, fd_p2
Z=np.column_stack([q2.symp_b0_pca.values,q2.age.values,q2.drug_first.values,q2.fd_p2.values])
F=pd.DataFrame(dict(SubID=q2.SubID,group='MDD',symp_b0_pca=q2.symp_b0_pca,
    symp_delta_pca=q2.symp_delta_pca,FC_p2=q2.baseline_fc,FC_delta=q2.delta,
    x_NPchange_resid=resid(q2.delta.values,Z), y_sympPC1change_resid=resid(q2.symp_delta_pca.values,Z)))
from scipy import stats as st
r=np.corrcoef(F.x_NPchange_resid,F.y_sympPC1change_resid)[0,1]; dfr=len(F)-4-2
tt=r*np.sqrt(dfr/(1-r**2)); pp=2*st.t.sf(abs(tt),dfr)
print('partial r = %.4f  P = %.4f  df = %d  (target -0.558 / 0.016 / 16)'%(r,pp,dfr))
assert abs(r+0.5576)<0.001
F.to_csv(FG+'fig.5/fig5_data/fig5f_np_symptom_resid_MDD_n22.csv',index=False)