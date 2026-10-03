# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/fig.2/fig2_data/fig2e_edge_group_difference.csv
# cell id     : e2c4fdf2-d737-4ae5-9f7d-2a754679db40
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-21 12:56:45 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

from statsmodels.stats.multitest import multipletests
import statsmodels.api as sm
hc2=hc.rename(columns={hc.columns[0]:'ID'})
print("site completeness:", hc2.recruitmentSite.notna().sum(), hc2.scanningSite.notna().sum(),
      "| headmotion NaN:", hc2.headmotion.isna().sum(), "| sex NaN:", hc2.sex.isna().sum())
mrg = st[['ID','Group']].merge(edges, on='ID').merge(hc2[['ID','sex','recruitmentSite','headmotion']], on='ID')
mrg = mrg.dropna(subset=['sex','recruitmentSite','headmotion'])
print("Fig2e analysis n:", mrg.Group.value_counts().to_dict())
Xd = pd.get_dummies(mrg[['sex','recruitmentSite']], drop_first=True).astype(float)
Xd['headmotion']=mrg.headmotion.values
X = sm.add_constant(Xd.values)
rows=[]
for i in range(1,13):
    y=mrg[f'edge{i}'].values
    r = y - sm.OLS(y, X).fit().predict(X)
    g1=r[(mrg.Group=='HC').values]; g2=r[(mrg.Group=='Patient').values]
    tt=stats.ttest_ind(g1,g2)
    d=(g1.mean()-g2.mean())/np.sqrt(((len(g1)-1)*g1.var(ddof=1)+(len(g2)-1)*g2.var(ddof=1))/(len(g1)+len(g2)-2))
    se=np.sqrt(1/len(g1)+1/len(g2)+d**2/(2*(len(g1)+len(g2))))
    rows.append(dict(edge=f'Edge {i}', task='SST' if i<=6 else 'MID',
                     t=tt.statistic, p=tt.pvalue, d=d, ci_lo=d-1.96*se, ci_hi=d+1.96*se))
e2=pd.DataFrame(rows)
e2['p_fdr']=multipletests(e2.p, method='fdr_bh')[1]
e2.to_csv(DD+"fig2e_edge_group_difference.csv", index=False, float_format='%.12g')
print(e2.round(4).to_string(index=False))
print("\nedges passing FDR q<0.05:", int((e2.p_fdr<0.05).sum()))
