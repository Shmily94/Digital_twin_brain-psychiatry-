# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5_mdd_hc_n36.csv; 04_figures/fig.5/fig5_data/fig5_mdd_hc_n36.csv
# cell id       : 040b58f5-5246-4b17-ba2d-4a7b245c1dbf
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 1086
# executed at   : 2026-09-23 08:17 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/14_fig5_mdd_hc_n36.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
F5=R+'figures/fig.5/fig5_data/'
old=pd.read_csv(F5+'fig5_mdd_hc_n36.csv')
new=old.rename(columns={'FC_p2':'FC_p2_12row','FC_d2':'FC_d2_12row','FC_delta':'FC_delta_12row'})
m11=t11.set_index('SubID')
new['FC_p2']  = m11.loc[new.SubID,'fp'].values
new['FC_d2']  = m11.loc[new.SubID,'fd_'].values
new['FC_delta']= m11.loc[new.SubID,'delta'].values
for c in ['age','sexM','drug_first','fd_p2']: new[c]=m11.loc[new.SubID,c].values
# verify the two main-text statistics off the file itself
chk=new.assign(grp=(new.group=='MDD').astype(int))
mb=smf.ols('FC_p2 ~ grp + age + sexM + fd_p2 + drug_first',data=chk).fit()
mi=smf.ols('FC_delta ~ grp + age + sexM + fd_p2 + drug_first',data=chk).fit()
print('from new file: baseline t(%d)=%.3f P=%.4f | interaction t(%d)=%.3f P=%.4f'%(
    mi.df_resid,mb.tvalues['grp'],mb.pvalues['grp'],mi.df_resid,mi.tvalues['grp'],mi.pvalues['grp']))
assert abs(mb.tvalues['grp']+2.766)<0.001 and abs(mi.tvalues['grp']-3.429)<0.001
new.to_csv(F5+'fig5_mdd_hc_n36.csv',index=False)
print('cols:',new.columns.tolist())
print('corr 11-edge vs 12-row delta = %.4f'%np.corrcoef(new.FC_delta,new.FC_delta_12row)[0,1])