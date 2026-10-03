# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_increment_nulls.csv; 04_figures/fig.5/fig5_data/fig5h_increment_nulls.csv
# cell id       : 8e731932-ef49-4e32-964a-1b667fa55dd9
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 490
# executed at   : 2026-09-21 21:12 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/22_fig5h_increment_nulls.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
def nested_full(pred, red, name, cov):
    Xfu = np.column_stack([pred, red]); n = len(y)
    R2r,_ = r2(red, y); R2fu, bfu = r2(Xfu, y)
    p1_, p2_ = red.shape[1], Xfu.shape[1]
    F = ((R2fu-R2r)/(p2_-p1_))/((1-R2fu)/(n-p2_-1)); p = stats.f.sf(F, p2_-p1_, n-p2_-1)
    rng = np.random.default_rng(1); null = np.empty(5000)
    for i in range(5000):
        yp = rng.permutation(y); null[i] = r2(Xfu, yp)[0] - r2(red, yp)[0]
    t = np.sqrt(F)
    return dict(index=name, covariates=cov, R2_reduced=round(R2r,4), R2_full=round(R2fu,4),
                delta_R2=round(R2fu-R2r,4), F_change=round(F,3), df2=n-p2_-1,
                p_change=float(f'{p:.3g}'),
                p_perm_deltaR2=float(f'{(null>=R2fu-R2r).mean():.3g}'),
                partial_r=round(float(np.sign(bfu[1])*t/np.sqrt(t**2+n-p2_-1)),3),
                null_p95=round(float(np.percentile(null,95)),4)), null

COMBOS = [(idx,'AMPA',X1,'baseline behaviour (4)'), (gab,'GABA-A',X1,'baseline behaviour (4)'),
          (idx,'AMPA',emp_sum.reshape(-1,1),'baseline empirical NP (1)'),
          (gab,'GABA-A',emp_sum.reshape(-1,1),'baseline empirical NP (1)')]
INC, NULLS = [], {}
for pred, nm, red, cov in COMBOS:
    row, nl = nested_full(pred, red, nm, cov); INC.append(row)
    NULLS[f'{nm}|{cov}'] = nl
INC = pd.DataFrame(INC)
INC.to_csv(f'{D5}/fig5h_increments.csv', index=False)
pd.DataFrame(NULLS).to_csv(f'{D5}/fig5h_increment_nulls.csv', index=False)
print(INC.to_string(index=False))
