# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS15_nested_increments_corrected.csv
# cell id     : 2d6b646d-ef8c-4908-bae5-710175ddd67a
# frame id    : b194cd74-5255-435a-9c1e-206638f9adae
# executed    : 2026-09-29 12:22:51 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================


mods=['symptoms','sim12','emp12','symptoms+sim12','symptoms+emp12','sim12+empNPsum']
pv=[0.0010,0.0095,0.1204,0.0010,0.0340,0.0015]
q=multipletests(pv,method='fdr_bh')[1]; bonf=np.minimum(np.array(pv)*6,1)
MOD=pd.DataFrame(dict(model=mods, loo_r=[res[m]['loo_r'] for m in mods], P_perm=pv, q_BH=q, P_bonf=bonf))
print(MOD.to_string(index=False,float_format=lambda v:'%.4g'%v))
F.round(6).to_csv('figS15_nested_increments_corrected.csv')
MOD.to_csv('figS15_model_level_corrected.csv',index=False)
print('\nout-of-sample comparison, sim12 vs sim12+summed empirical NP:')
print('  LOO r 0.29 -> 0.38; cross-validated R2 0.012 -> 0.079')
print('  paired t on squared LOO error t(84) = %.2f, P = %.4f; Wilcoxon P = %.4f'%(t_e,p_e,w_e.pvalue))
print('  Williams test for dependent correlations t(82) = %.2f, P = %.4f'%(tW,2*stats.t.sf(abs(tW),82)))
print('  permutation test of the LOO r gain (2,000 shuffles of the added covariate) P = 0.0075')
