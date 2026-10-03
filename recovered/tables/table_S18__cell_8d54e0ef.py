# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : 8d54e0ef-8c1e-4e04-b1f7-0d6498e3255a
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:13:29 UTC (epoch-ms 1790676809691)
# conda env        : python
# produced         : writes the Table S18a/S18b frequency blocks, percentages and legends into the supplementary workbook
# ----------------------------------------------------------------------------


m3=smf.ols('y ~ C(sex) + C(Group)', data=dd).fit()
print('OLS (linear probability) sex coefficient: beta=%.4f t=%.2f P=%.4f'%(m3.params['C(sex)[T.M]'], m3.tvalues['C(sex)[T.M]'], m3.pvalues['C(sex)[T.M]']))
m4=smf.ols('y ~ C(sex)', data=dd).fit()
print('OLS sex only: t=%.2f P=%.4f'%(m4.tvalues['C(sex)[T.M]'], m4.pvalues['C(sex)[T.M]']))
SITES=['BERLIN','DRESDEN','DUBLIN','HAMBURG','LONDON','MANNHEIM','NOTTINGHAM','PARIS']
NAME={'BERLIN':'Berlin','DRESDEN':'Dresden','DUBLIN':'Dublin','HAMBURG':'Hamburg','LONDON':'London','MANNHEIM':'Mannheim','NOTTINGHAM':'Nottingham','PARIS':'Paris'}
tot={'Increased':229,'Decreased':59}
ws=wb['Table S18']
for r in range(1, ws.max_row+1):
    for c in range(1, ws.max_column+1): ws.cell(row=r,column=c).value=None
def put(r, vals):
    for c,v in enumerate(vals, start=1):
        if v is not None: ws.cell(row=r, column=c).value=v
put(1,['Table S18a. Frequencies for recruitment site between response groups after virtual perturbation (n = 288 digital twins; Increased = NP increased under both perturbations, n = 229; Decreased = NP decreased under at least one perturbation, n = 59)'])
put(2,['Group','Site','Frequency','Percent'])
row=3
for g in ['Increased','Decreased']:
    first=True
    for s in SITES:
        f=int(site_ct.loc[g,s]) if s in site_ct.columns else 0
        put(row,[g if first else None, NAME[s], f, f/tot[g]]); first=False; row+=1
    put(row,[None,'Missing',0,0.0]); row+=1
    put(row,[None,'Total',tot[g],1.0]); row+=1
put(row,['Chi-squared test of independence across the eight sites: χ²(7) = %.2f, P = %.3f (two-sided; no correction). One expected count was below 5, so the test is reported as approximate.'%(chi2_s,p_s)]); row+=2
put(row,['Table S18b. Frequencies for sex between response groups after virtual perturbation (same sample as S18a)']); row+=1
put(row,['Group','Sex','Frequency','Percent']); row+=1
for g in ['Increased','Decreased']:
    first=True
    for s in ['F','M']:
        f=int(sex_ct.loc[g,s]); put(row,[g if first else None, s, f, f/tot[g]]); first=False; row+=1
    put(row,[None,'Missing',0,0.0]); row+=1
    put(row,[None,'Total',tot[g],1.0]); row+=1
put(row,['Chi-squared test of independence: χ²(1) = %.2f, P = %.3f; Fisher exact P = %.3f (two-sided; no correction). Adjusting for diagnostic group, the sex effect persists in this sample (logistic regression, z = %.2f, P = %.3f; linear model t = %.2f, P = %.3f).'%(chi2_x,p_x,pf,m2.tvalues['C(sex)[T.M]'],m2.pvalues['C(sex)[T.M]'],m3.tvalues['C(sex)[T.M]'],m3.pvalues['C(sex)[T.M]'])]); row+=1
put(row,['Source: revision/text/figures/fig.4/fig4_data/fig4_subject_level_n288.csv (response pattern, sex and recruitment site for the 288 twins), recomputed 29 Sep. London is a single recruitment site in this analysis file; the earlier version of this table split it into London-Invicro and London-CNS and was based on 290 participants (251 increased / 39 decreased).'])
for r in range(3, ws.max_row+1):
    c=ws.cell(row=r, column=4)
    if isinstance(c.value,(int,float)): c.number_format='0.0%'
OUT2='290926Suppl.Table_v3.xlsx'; wb.save(OUT2); shutil.copy(OUT2, dest+OUT2)
ck=openpyxl.load_workbook(dest+OUT2)['Table S18']
for r in ck.iter_rows(min_row=1, max_row=ck.max_row, values_only=True):
    cells=[('' if c is None else (f'{c:.1%}' if isinstance(c,float) else str(c))) for c in r]
    while cells and not cells[-1]: cells.pop()
    if cells: print(' | '.join(x[:95] for x in cells))
