# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 4f1219ba-ee06-45f1-adc4-bf6e8ed25294
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-21 21:29:24 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/supp_assim/data/assim5_stats.csv
# ===========================================================================

FIG=f'{B}/revision/text/figures'
dirs={k: f'{FIG}/supp_{k}' for k in ['assim','fingerprint','conductance','eft','motion']}
for k,v in dirs.items():
    os.makedirs(f'{v}/data', exist_ok=True); os.makedirs(f'{v}/panels', exist_ok=True)

# ---- S1 data
A5.to_csv(f"{dirs['assim']}/data/assim5_edges_mid.csv", index=False)
pd.DataFrame([dict(statistic='ICC(3,1), runs fixed', value=round(float(icc31),4)),
              dict(statistic='ICC(2,1), runs random', value=round(float(icc21),4)),
              dict(statistic='mean between-run profile r', value=round(float(np.mean(pair_r)),4)),
              dict(statistic='min between-run profile r', value=round(float(min(pair_r)),4)),
              dict(statistic='max between-run profile r', value=round(float(max(pair_r)),4)),
              dict(statistic='SD between edges (signal)', value=round(float(R.mean(1).std(ddof=1)),4)),
              dict(statistic='mean SD between runs (noise)', value=round(float(R.std(1,ddof=1).mean()),4)),
              dict(statistic='signal/noise SD ratio', value=round(float(R.mean(1).std(ddof=1)/R.std(1,ddof=1).mean()),2)),
              dict(statistic='n runs', value=5), dict(statistic='n reward-task edges', value=6),
              ]).to_csv(f"{dirs['assim']}/data/assim5_stats.csv", index=False)

# ---- S2 data
for nm,F,path in [('empirical',FE,'fingerprint_similarity_empirical.csv'),
                  ('simulated',FS,'fingerprint_similarity_simulated.csv')]:
    pd.DataFrame(F[2], index=F[1], columns=F[0]).to_csv(f"{dirs['fingerprint']}/data/{path}")
fp=[]
for nm,F in [('empirical BOLD',FE),('simulated (no re-assimilation)',FS)]:
    corr=np.array([t==p for t,p in zip(F[3],F[4])])
    fp.append(dict(data=nm, n_trials=len(corr), n_correct=int(corr.sum()),
                   accuracy_pct=round(100*float(corr.mean()),1),
                   mean_self_r=round(float(F[5].mean()),4),
                   mean_best_other_r=round(float(F[6].mean()),4),
                   mean_margin=round(float((F[5]-F[6]).mean()),4),
                   misidentified=';'.join([F[1][i] for i in np.where(~corr)[0]]) or 'none'))
FPA=pd.DataFrame(fp); FPA.to_csv(f"{dirs['fingerprint']}/data/fingerprint_accuracy.csv", index=False)
pd.DataFrame(dict(trial=FE[1], subject=FE[3],
                  self_r_empirical=FE[5], best_other_r_empirical=FE[6],
                  self_r_simulated=FS[5], best_other_r_simulated=FS[6])).to_csv(
    f"{dirs['fingerprint']}/data/fingerprint_margins.csv", index=False)
print(FPA.to_string(index=False))

# ---- S3 data
CG.to_csv(f"{dirs['conductance']}/data/conductance_grid_summary_n288.csv", index=False)
STRAT.to_csv(f"{dirs['conductance']}/data/conductance_responder_by_group_n288.csv", index=False)
IND.drop(columns=['ID']).to_csv(f"{dirs['conductance']}/data/conductance_subject_level_n288.csv", index=False)
IRC.to_csv(f"{dirs['conductance']}/data/conductance_across_setting_correlations.csv", index=False)

# ---- S4 data
EFT=pd.concat([xl.parse('ampa_eft').rename(columns={'Unnamed: 0':'subject','0.0044':'perturbed'}).assign(perturbation='AMPA'),
               xl.parse('gaba_eft').rename(columns={'Unnamed: 0':'subject','0.0040':'perturbed'}).assign(perturbation='GABA-A')])
EFT=EFT[EFT.subject!='HC02'].reset_index(drop=True)     # HC02 excluded, as in the model sweeps
EFT['delta']=EFT.perturbed-EFT.baseline
NPT=pd.concat([xl.parse('Sheet3').rename(columns={'Unnamed: 0':'subject','simulation_np':'baseline','mani_ampa_np':'perturbed'}).assign(perturbation='AMPA'),
               xl.parse('Sheet4').rename(columns={'Unnamed: 0':'subject','simulation_np':'baseline','mani_gaba_np':'perturbed'}).assign(perturbation='GABA-A')])
NPT=NPT[NPT.subject!='HC02'].reset_index(drop=True); NPT['delta']=NPT.perturbed-NPT.baseline
EFT.to_csv(f"{dirs['eft']}/data/eft_3subs.csv", index=False)
NPT.to_csv(f"{dirs['eft']}/data/np_task_3subs.csv", index=False)
print(); print(EFT.to_string(index=False)); print(); print(NPT.to_string(index=False))
