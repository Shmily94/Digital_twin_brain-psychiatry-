# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 8ce04524-f306-482a-81ab-a1176ee284c3
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 20:01:32 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3c_cross_scale_n_cells_ampa.csv
# ===========================================================================

DL[('100m','ampa')]=FIN['ampa'].values; DL[('100m','gaba')]=FIN['gaba'].values
rows=[]
for (m_,dr),v in DL.items():
    v=np.asarray(v,float); t=stats.ttest_1samp(v,0); w=stats.wilcoxon(v); ci=stats.t.interval(.95,len(v)-1,v.mean(),stats.sem(v))
    rows.append(dict(modulation='AMPA' if dr=='ampa' else 'GABA-A', model=m_, family=FAMILY[m_], n=len(v),
        n_increased=int((v>0).sum()), pct_increased=round(100*float((v>0).mean()),1),
        mean_delta=round(float(v.mean()),4), sd_delta=round(float(v.std(ddof=1)),4), sem=round(float(stats.sem(v)),4),
        t=round(float(t.statistic),3), df=len(v)-1, p=float(t.pvalue),
        cohens_dz=round(float(v.mean()/v.std(ddof=1)),3), ci95_lo=round(float(ci[0]),4),
        ci95_hi=round(float(ci[1]),4), wilcoxon_p=float(w.pvalue)))
G=pd.DataFrame(rows); G['q_bh']=multipletests(G.p,method='fdr_bh')[1]
G=G.sort_values(['modulation','model'], key=lambda s: s.map({m:i for i,m in enumerate(ORDER)}) if s.name=='model' else s)
G.to_csv(f'{FD3}/fig3g_delta_np_stats_by_model.csv', index=False)
SRC={'3m_268':'Mani_simulated_3m_NP_12edges_and_factor.mat (new run; manipu/manipu_gaba minus manipu_gaba_baseline, 5-repeat mean)',
     '10m_own':'np_edges_simulated_baseline_mani.xlsx sheet simulate_np (single run)',
     '100m':'perturbed: simulation_results_wide_12subs.csv for 9 twins + orignial_3subs_perturb_100m_whole_brain_fc/ for HC01, MDD, AUD (ampa 0.0044; gaba 0.0040 on ampa 0.0044; 5 repeats); baseline: newflow 100m'}
pd.DataFrame([dict(model=m_, family=FAMILY[m_], drug=dr, sub_id=int(s), delta=round(float(x),5),
                   source=SRC.get(m_,'newflow six-model tables; regional builds use the _r style, voxel builds the plain conditions'))
              for (m_,dr),v in DL.items() for s,x in zip(sid,np.asarray(v,float))]).to_csv(f'{FD3}/fig3g_delta_np_seven_models.csv', index=False)
SA,NA=sp_mat('ampa'); SG,NG=sp_mat('gaba')
for X,f_ in [(SA,'ampa'),(SG,'gaba')]: X.to_csv(f'{FD3}/fig3c_cross_scale_similarity_{f_}.csv')
NA.to_csv(f'{FD3}/fig3c_cross_scale_n_cells_ampa.csv'); NG.to_csv(f'{FD3}/fig3c_cross_scale_n_cells_gaba.csv')
print(G[G.model=='100m'][['modulation','n','n_increased','mean_delta','t','df','p','q_bh']].to_string(index=False, float_format=lambda x:f'{x:.4g}'))
print('\n100m 行现在全部 144 单元:', int(NA.loc["100m"].min()), int(NG.loc["100m"].min()))
print('AMPA  q<0.05:', G[(G.modulation=="AMPA")&(G.q_bh<.05)].model.tolist(),
      '| GABA-A q<0.05:', G[(G.modulation=="GABA-A")&(G.q_bh<.05)].model.tolist())
