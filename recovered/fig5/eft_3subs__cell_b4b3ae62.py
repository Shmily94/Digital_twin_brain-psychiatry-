# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/supp_eft/data/eft_3subs.csv
# cell id       : b4b3ae62-de2b-487f-9e6a-76fadf505293
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 522
# executed at   : 2026-09-21 21:29 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/50_eft_3subs.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted.
# ---------------------------------------------------------------------------
def eft_sheet(sh, pert):
    d=xl.parse(sh); d.columns=['subject','baseline','perturbed']
    d=d.assign(perturbation=pert, conductance=float(xl.parse(sh).columns[2]))
    return d
EFT=pd.concat([eft_sheet('ampa_eft','AMPA'), eft_sheet('gaba_eft','GABA-A')])
EFT=EFT[EFT.subject!='HC02'].reset_index(drop=True)
EFT['delta']=EFT.perturbed-EFT.baseline
EFT.to_csv(f"{dirs['eft']}/data/eft_3subs.csv", index=False)
print(EFT.to_string(index=False))
print('\ndirections  EFT  AMPA:', dict(zip(EFT[EFT.perturbation=='AMPA'].subject, np.sign(EFT[EFT.perturbation=='AMPA'].delta).astype(int))),
      ' GABA-A:', dict(zip(EFT[EFT.perturbation=='GABA-A'].subject, np.sign(EFT[EFT.perturbation=='GABA-A'].delta).astype(int))))
print('directions  NP   AMPA:', dict(zip(NPT[NPT.perturbation=='AMPA'].subject, np.sign(NPT[NPT.perturbation=='AMPA'].delta).astype(int))),
      ' GABA-A:', dict(zip(NPT[NPT.perturbation=='GABA-A'].subject, np.sign(NPT[NPT.perturbation=='GABA-A'].delta).astype(int))))
# ---- S5 data
MOTS=SL4[['ID','Group','sex','site','headmotion','empirical','simulated','ampa','gaba','d_ampa','d_gaba']].copy()
MOTS.to_csv(f"{dirs['motion']}/data/motion_subject_level_n288.csv", index=False)
grows=[dict(test='one-way ANOVA (3 groups)', statistic=round(float(f_),3), df='2, 285', p=float(f'{p_:.3g}')),
       dict(test='Kruskal-Wallis (3 groups)', statistic=round(float(kw[0]),3), df='2', p=float(f'{kw[1]:.3g}'))]
lev=stats.levene(*[MOTS.loc[MOTS.Group==g,'headmotion'] for g in ['HC','High-symptom','Patient']])
grows.append(dict(test='Levene (variance)', statistic=round(float(lev[0]),3), df='2, 285', p=float(f'{lev[1]:.3g}')))
a_=MOTS.loc[MOTS.Group=='HC','headmotion']; b_=MOTS.loc[MOTS.Group!='HC','headmotion']
tt=stats.ttest_ind(a_,b_,equal_var=False); uu=stats.mannwhitneyu(a_,b_)
sp=np.sqrt(((len(a_)-1)*a_.var(ddof=1)+(len(b_)-1)*b_.var(ddof=1))/(len(a_)+len(b_)-2))
grows += [dict(test='HC vs all others, Welch t', statistic=round(float(tt[0]),3),
               df=f'Cohen d = {(a_.mean()-b_.mean())/sp:+.2f}', p=float(f'{tt[1]:.3g}')),
          dict(test='HC vs all others, Mann-Whitney U', statistic=round(float(uu[0]),1), df='', p=float(f'{uu[1]:.3g}'))]
for g in ['HC','High-symptom','Patient']:
    v=MOTS.loc[MOTS.Group==g,'headmotion']
    grows.append(dict(test=f'{g}: mean (sd) FD, mm', statistic=round(float(v.mean()),4),
                      df=f'sd {v.std(ddof=1):.4f}; median {v.median():.4f}; n {len(v)}', p=np.nan))
pd.DataFrame(grows).to_csv(f"{dirs['motion']}/data/motion_group_tests.csv", index=False)
mrows2=[]
LABS={'empirical':'Empirical NP','simulated':'Simulated baseline NP','ampa':'NP after AMPA',
      'gaba':'NP after GABA-A','d_ampa':'Δ NP after AMPA','d_gaba':'Δ NP after GABA-A'}
for c,lab in LABS.items():
    r_,pr=stats.pearsonr(MOTS.headmotion, MOTS[c]); rh,ph=stats.spearmanr(MOTS.headmotion, MOTS[c])
    lo,hi=np.tanh(np.arctanh(r_)+np.array([-1,1])*1.959964/np.sqrt(len(MOTS)-3))
    mrows2.append(dict(outcome=lab, n=len(MOTS), r=round(float(r_),3), ci_low=round(float(lo),3),
                       ci_high=round(float(hi),3), p=float(f'{pr:.3g}'),
                       variance_pct=round(100*float(r_**2),2), rho=round(float(rh),3),
                       p_spearman=float(f'{ph:.3g}'), r_response_doc=THEIR[c]))
MOT2=pd.DataFrame(mrows2)
MOT2['q_fdr']=multipletests(MOT2.p, method='fdr_bh')[1].round(4)
MOT2.to_csv(f"{dirs['motion']}/data/motion_correlations.csv", index=False)
ed[['variable','n','r','p','q']].rename(columns={'q':'q_fdr'}).to_csv(
    f"{dirs['motion']}/data/motion_per_edge_correlations.csv", index=False)
print(); print(MOT2[['outcome','r','ci_low','ci_high','p','q_fdr','variance_pct','r_response_doc']].to_string(index=False))
