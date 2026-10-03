# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S17
# cell id          : 674db32f-4ef2-4e02-863f-0dfe6e4db227
# frame id         : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp        : 2026-09-24 16:56:51 UTC (epoch-ms 1790269011257)
# conda env        : python
# produced         : Table S17 four-category response-pattern crosstab (n=288) and its chi-square test; also the Table S15 reformat of fig3g_delta_np_stats_by_model.csv
# ----------------------------------------------------------------------------

GS=pd.read_csv(art('fig3g_delta_np_stats_by_model.csv'))
BN={'3m_268':'3m_268','10m_268':'10m_268','10m_1000':'10m_1000','10m_own':'10m_voxel (own 10m hyper)',
    '10m':'10m_voxel','100m':'100m_voxel','1b':'1b_voxel'}
S15n=[]
for mod in ['AMPA','GABA-A']:
    for b in ['3m_268','10m_268','10m_1000','10m_own','10m','100m','1b']:
        r=GS[(GS.modulation==mod)&(GS.model==b)].iloc[0]
        S15n.append([mod,BN[b],int(r.n),int(r.n_increased),round(r.mean_delta,4),round(r.sd_delta,4),
                     round(r.t,3),float('%.3g'%r.p),float('%.3g'%r.q_bh)])
S15n=pd.DataFrame(S15n,columns=['modulation','model','n','Increased (n)','mean_delta_np','sd_delta','t','p','q (BH across 7 models)'])
print(S15n.to_string(index=False))
F4['pat2']=np.where(F4.d_ampa>0,'A+','A-')+np.where(F4.d_gaba>0,' G+',' G-')
ctab=pd.crosstab(F4.Group,F4.pat2)
print('\ncurrent pattern distribution (n = %d):'%len(F4)); print(ctab.to_string())
c2=st.chi2_contingency(ctab[[c for c in ctab.columns if ctab[c].sum()>0]])
print('chi2(%d) = %.3f, P = %.4g'%(c2.dof,c2.statistic,c2.pvalue))