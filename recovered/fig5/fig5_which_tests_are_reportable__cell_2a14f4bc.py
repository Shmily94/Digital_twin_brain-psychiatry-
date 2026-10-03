# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5_which_tests_are_reportable.csv; 04_figures/fig.5/fig5_data/fig5_which_tests_are_reportable.csv
# cell id       : 2a14f4bc-596a-4225-b1c7-1d83b34f0e20
# frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# cell_index    : 480
# executed at   : 2026-09-21 21:04 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/16_fig5_which_tests_are_reportable.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------
rows=[]
def add(**k): rows.append(k)
for post in ['Ketamine','Midazolam']:
    X = sm.add_constant(Hp.Placebo.values); mod = sm.OLS(Hp[post].values, X).fit()
    b, se = mod.params[1], mod.bse[1]; ci = mod.conf_int()[1]; t=(b-1)/se; df=len(Hp)-2
    add(cohort='healthy n=27', quantity=f'{post} on placebo, OLS slope', estimate=round(b,3),
        ci_low=round(ci[0],3), ci_high=round(ci[1],3), test='t vs slope = 1',
        stat=round(t,3), p=float(f'{2*(1-stats.t.cdf(abs(t),df)):.3g}'), circular='no',
        note='uses only placebo and post-drug values; no grouping by the sign of the change')
    add(cohort='healthy n=27', quantity=f'var({post}) / var(placebo)',
        estimate=round(Hp[post].var(ddof=1)/Hp.Placebo.var(ddof=1),3), ci_low=np.nan,
        ci_high=np.nan, test='descriptive', stat=np.nan, p=np.nan, circular='no',
        note='>1 means the drug increased between-subject spread')
    rn,pn = stats.pearsonr(Hp.Placebo, Hp[post]-Hp.Placebo)
    add(cohort='healthy n=27', quantity=f'placebo vs change under {post}, Pearson r',
        estimate=round(rn,3), ci_low=np.nan, ci_high=np.nan, test='Pearson', stat=round(rn,3),
        p=float(f'{pn:.3g}'), circular='partly',
        note='inflated by the shared placebo term; report the slope above instead')
add(cohort='healthy n=27', quantity='Delta ketamine vs Delta midazolam, Pearson r',
    estimate=round(r_raw,3), ci_low=np.nan, ci_high=np.nan, test='Pearson', stat=round(r_raw,3),
    p=float(f'{p_raw:.3g}'), circular='partly', note='both changes share the -placebo term')
add(cohort='healthy n=27', quantity='Ketamine vs Midazolam, partial r | placebo',
    estimate=round(r_pc,3), ci_low=np.nan, ci_high=np.nan, test='partial Pearson',
    stat=round(r_pc,3), p=float(f'{p_pc:.3g}'), circular='no',
    note='the non-circular test of cross-drug consistency of the individual response')
for col,nm in [('d_ket','change under ketamine'),('d_mid','change under midazolam'),
               ('Placebo','placebo level')]:
    a=Hp.loc[Hp.pattern=='both up',col]; b=Hp.loc[Hp.pattern=='any down',col]
    t_,p_=stats.ttest_ind(a,b,equal_var=False)
    add(cohort='healthy n=27', quantity=f'both-up vs any-down, {nm}',
        estimate=round(float(a.mean()-b.mean()),3), ci_low=np.nan, ci_high=np.nan,
        test='Welch t', stat=round(float(t_),3), p=float(f'{p_:.3g}'),
        circular='YES - do not report' if col!='Placebo' else 'partly',
        note='group defined by the sign of these same changes (8/8 forced)' if col!='Placebo'
             else 'not definitional, but coupled through change = post - placebo')
for col,nm in [('FC_p2','placebo (p2)'),('FC_d2','ketamine (d2)'),('FC_delta','change d2 - p2')]:
    a=PH.loc[PH.group=='HC',col]; b=PH.loc[PH.group=='MDD',col]
    t_,p_=stats.ttest_ind(a,b,equal_var=False); _,pu=stats.mannwhitneyu(a,b)
    sp=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(a)+len(b)-2))
    add(cohort='MDD 22 / HC 14', quantity=f'HC vs MDD, {nm}', estimate=round(float(a.mean()-b.mean()),3),
        ci_low=np.nan, ci_high=np.nan, test=f'Welch t (Hedges g = {(a.mean()-b.mean())/sp:+.2f}; MW P = {pu:.3g})',
        stat=round(float(t_),3), p=float(f'{p_:.3g}'), circular='no',
        note='grouping variable is diagnosis, external to the FC measurement')
V=pd.DataFrame(rows)
V.to_csv('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data/fig5_which_tests_are_reportable.csv', index=False)
import shutil; shutil.copy('/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.5/fig5_data/fig5_which_tests_are_reportable.csv','fig5_which_tests_are_reportable.csv')
print(V[['cohort','quantity','estimate','test','p','circular']].to_string(index=False))
