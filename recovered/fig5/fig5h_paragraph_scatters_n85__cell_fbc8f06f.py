# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_paragraph_scatters_n85.csv; 04_figures/fig.5/fig5_data/fig5h_paragraph_scatters_n85.csv
# cell id       : fbc8f06f-ac73-47ae-8f2b-683d1ce7b349
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 498
# executed at   : 2026-09-21 21:19 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/29_fig5h_paragraph_scatters_n85.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
Z1 = emp_sum.reshape(-1,1)
xr2, yr2 = resid(idx, Z1), resid(y, Z1)
rp2, pp2_ = stats.pearsonr(xr2, yr2)
print('added-variable over empirical baseline NP: partial r = %.4f, P = %.4g (nested F P = 0.0259)' % (rp2, pp2_))
SC = pd.DataFrame(dict(
    ampa_index=idx, fu3_symptom_change=y,
    empirical_baseline_np_sum=emp_sum, baseline_symptom_sum=X1.sum(1),
    index_resid_on_empNP=xr2, fu3change_resid_on_empNP=yr2))
SC.to_csv(f'{D5}/fig5h_paragraph_scatters_n85.csv', index=False)
rows=[]
for xn, yn, lab, kind in [
    ('index_resid_on_empNP','fu3change_resid_on_empNP','AMPA index vs FU3 symptom change, adjusted for baseline empirical NP','partial Pearson r'),
    ('ampa_index','fu3_symptom_change','AMPA index vs FU3 symptom change, unadjusted','Pearson r'),
    ('ampa_index','empirical_baseline_np_sum','AMPA index vs baseline empirical NP connectivity','Pearson r'),
    ('ampa_index','baseline_symptom_sum','AMPA index vs baseline symptoms','Pearson r')]:
    r_, p_ = stats.pearsonr(SC[xn], SC[yn])
    lo, hi = np.tanh(np.arctanh(r_) + np.array([-1,1])*1.959964/np.sqrt(len(SC)-3))
    rows.append(dict(relationship=lab, n=len(SC), test=kind, r=round(float(r_),3),
                     ci_low=round(float(lo),3), ci_high=round(float(hi),3),
                     p=float(f'{p_:.3g}')))
ST=pd.DataFrame(rows); ST.to_csv(f'{D5}/fig5h_paragraph_scatter_stats.csv', index=False)
print(ST.to_string(index=False))
