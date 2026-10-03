# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : b42ded68-ec4f-4c9e-8bee-77c2935547bf
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 17:01:07 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3c_similarity_pvalues.csv
# ===========================================================================

R.insert(1,'family_role',['within voxel family (100 M hyper)']*3+['within regional family (3 M-268 hyper)']+
         ['between families']*6)
R['n_participants']=12; R['n_cells_pooled']=144
R['p_block_perm_note']='5,000 participant-block permutations; 0 exceedances, so P is at the resolution floor 1/5001'
R.to_csv(D3+'fig3c_similarity_pvalues.csv',index=False)
shutil.copy(D3+'fig3c_similarity_pvalues.csv',WS+'fig3c_similarity_pvalues.csv')
for lab,sel in [('within voxel family',R.family_role.str.startswith('within voxel')),
                ('within regional family',R.family_role.str.startswith('within regional')),
                ('between families',R.family_role=='between families')]:
    s=R[sel]
    print('%-24s mean rho %.3f  range %.3f-%.3f | participant-level P range %.1e - %.1e'%(
        lab,s.rho_pooled.mean(),s.rho_pooled.min(),s.rho_pooled.max(),
        s.p_participant.min(),s.p_participant.max()))