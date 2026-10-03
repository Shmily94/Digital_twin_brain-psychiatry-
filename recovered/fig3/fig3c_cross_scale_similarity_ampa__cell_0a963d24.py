# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 0a963d24-557e-4396-96a0-dd059559cdd8
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 19:01:49 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3c_cross_scale_similarity_ampa.csv
# ===========================================================================

def sp_mat(dr):
    M_=np.full((7,7),np.nan); N_=np.zeros((7,7),int)
    for i,x in enumerate(ORDER):
        for j,y in enumerate(ORDER):
            a,b2=PERT[(x,dr)].ravel(),PERT[(y,dr)].ravel()
            ok=np.isfinite(a)&np.isfinite(b2); N_[i,j]=ok.sum()
            M_[i,j]=1.0 if i==j else float(stats.spearmanr(a[ok],b2[ok])[0])
    return pd.DataFrame(M_,index=ORDER,columns=ORDER), pd.DataFrame(N_,index=ORDER,columns=ORDER)
SA,NA=sp_mat('ampa'); SG,NG=sp_mat('gaba')
SA.to_csv(f'{FD3}/fig3c_cross_scale_similarity_ampa.csv'); SG.to_csv(f'{FD3}/fig3c_cross_scale_similarity_gaba.csv')
NA.to_csv(f'{FD3}/fig3c_cross_scale_n_cells_ampa.csv');    NG.to_csv(f'{FD3}/fig3c_cross_scale_n_cells_gaba.csv')
print('AMPA-perturbed state (Spearman, 144 cells; 108 where 100 M is involved)'); print(SA.round(2).to_string())
print('\nGABA-A-perturbed state'); print(SG.round(2).to_string())
def blocks(Mx):
    o=[(i,j) for i in range(7) for j in range(i+1,7)]
    sh=[Mx.iloc[i,j] for i,j in o if HYP[ORDER[i]]==HYP[ORDER[j]]]
    cr=[Mx.iloc[i,j] for i,j in o if HYP[ORDER[i]]!=HYP[ORDER[j]]]
    return round(float(np.mean(sh)),3), round(float(min(sh)),3), round(float(max(sh)),3), round(float(np.mean(cr)),3)
print('\n           same-hyper mean/min/max | cross mean')
for nm,Mx in [('baseline',SP),('AMPA    ',SA),('GABA-A  ',SG)]: print(f'{nm}  {blocks(Mx)}')
