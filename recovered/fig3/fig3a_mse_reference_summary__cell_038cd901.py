# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 038cd901-1757-432f-bb8d-3abc2bb7a0cf
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-23 15:13:19 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3a_mse_reference_summary.csv
# ===========================================================================

out=piv.reset_index().rename(columns={'model':'build','empirical_model_voxels':'mse_under_empirical_model_voxels',
    'empirical_original_3m':'mse_under_empirical_original_3m'})
out['note']=['Table S10 takes the designated reference for each build; the designation is not constant across builds']*len(out)
out.to_csv(D3+'fig3a_mse_reference_dependence.csv',index=False)
summ=pd.DataFrame([
 dict(reference='empirical_original_3m (common)',voxel_family_mean=0.1024,regional_family_mean=0.0960,
      winner='regional',gap=0.0065,best_single_build='3m_268 (0.0888)'),
 dict(reference='empirical_model_voxels (common)',voxel_family_mean=0.0581,regional_family_mean=0.0784,
      winner='voxel',gap=0.0204,best_single_build='10m voxel (0.0498)'),
 dict(reference='mixed, as in Table S10',voxel_family_mean=0.0581,regional_family_mean=0.0960,
      winner='voxel',gap=0.0379,best_single_build='10m voxel (0.0498)')])
summ.to_csv(D3+'fig3a_mse_reference_summary.csv',index=False)
print(summ.to_string(index=False))