# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : ff182339-08d3-4312-b84b-5193f4aff47f
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-22 19:53:42 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3g_100m_three_subject_verification.csv
# ===========================================================================

V=[]
for s in SUB3:
    for dr in ['ampa','gaba']:
        st=float(g6[(g6.model=='100m')&(g6.drug==dr)&(g6.sub_id.astype(str)==s)].delta.iloc[0])
        V.append(dict(subject_id=int(s), sweep_alias={'112288':'HC01','113174215':'MDD','182136619':'AUD'}[s],
            drug=dr, perturbed_np_sum_recomputed=round(float(res[(s,dr)].sum()),4),
            baseline_100m_newflow=round(float(base100[s].sum()),4),
            delta_recomputed=round(float(res[(s,dr)].sum()-base100[s].sum()),4),
            delta_stored_fig3g=round(st,4),
            implied_baseline_of_stored=round(float(res[(s,dr)].sum()-st),4),
            baseline_3m_sweep=round(float(sw[{'112288':'HC01','113174215':'MDD','182136619':'AUD'}[s]]),4),
            conductance='ampa 0.0044' if dr=='ampa' else 'ampa 0.0044 + gaba 0.0040',
            n_repeats=5, source=f'orignial_3subs_perturb_100m_whole_brain_fc/{SUB3[s]}'))
VV=pd.DataFrame(V); VV.to_csv(f'{FD3}/fig3g_100m_three_subject_verification.csv', index=False)
print(VV[['subject_id','sweep_alias','drug','perturbed_np_sum_recomputed','baseline_100m_newflow',
          'delta_recomputed','delta_stored_fig3g','implied_baseline_of_stored','baseline_3m_sweep']].to_string(index=False))
