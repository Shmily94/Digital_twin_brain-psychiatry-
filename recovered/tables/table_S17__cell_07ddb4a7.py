# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S17
# cell id          : 07ddb4a7-bf55-4c8f-b431-8ce7d663b2fc
# frame id         : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# timestamp        : 2026-09-24 16:57:19 UTC (epoch-ms 1790269039376)
# conda env        : python
# produced         : rendering of Table S15 and Table S17 into the supplementary workbook (sheet titles and the collapsed chi-square quoted in the Table S17 legend)
# ----------------------------------------------------------------------------

from openpyxl.styles import Alignment,Font,PatternFill,Border,Side
wbF=openpyxl.load_workbook(OUTX)
HL=PatternFill('solid',fgColor='FFF2A8')
def rewrite(ws,header,data,title):
    ws.cell(row=1,column=1).value=title
    maxc=max(len(header),ws.max_column)
    for r in range(2,ws.max_row+1):
        for c in range(1,maxc+1): ws.cell(row=r,column=c).value=None
    for j,h in enumerate(header,1):
        c=ws.cell(row=2,column=j); c.value=h; c.font=Font(bold=True,size=9)
        c.fill=PatternFill('solid',fgColor='DDE6F0'); c.alignment=Alignment(wrap_text=True,vertical='center')
    for i,row in enumerate(data,3):
        for j,v in enumerate(row,1):
            c=ws.cell(row=i,column=j); c.value=v; c.font=Font(size=9); c.fill=HL
    ws.freeze_panes='A3'
rewrite(wbF['Table S15'],list(S15n.columns),S15n.values.tolist(),
 'Table S15. The perturbational responses across different-scales DTBs. Two-sided one-sample t tests against zero on the '
 'per-participant change in summed NP connectivity (n = 12 participants per build), Benjamini-Hochberg FDR across the seven '
 'builds within each modulation. The 3 M/268 rows are referenced to the plain baseline run of the corrected 3 M simulation.')
pat=['A+ G+','A+ G-','A- G+','A- G-']
lab=['AMPA increased, GABA-A increased','AMPA increased, GABA-A decreased',
     'AMPA decreased, GABA-A increased','AMPA decreased, GABA-A decreased']
d18=[]
for gp in ['HC','High-symptom','Patient']:
    tot=int(ctab.loc[gp].sum())
    d18.append([gp]+['%d (%.2f%%)'%(ctab.loc[gp,p],100*ctab.loc[gp,p]/tot) for p in pat]+['%d (100%%)'%tot])
tt=int(ctab.values.sum())
d18.append(['All']+['%d (%.2f%%)'%(ctab[p].sum(),100*ctab[p].sum()/tt) for p in pat]+['%d (100%%)'%tt])
rewrite(wbF['Table S18'],['Group']+lab+['Total'],d18,
 'Table S18. The distribution of different response individuals following AMPA and GABA-A manipulations (n = 288 digital twins). '
 'Collapsing to both-increased versus any-decreased, the proportions differ across groups: chi-square(2) = 14.17, P = 8.4 x 10^-4. '
 'The full four-category table gives chi-square(6) = 20.04, P = 0.0027, but three cells contain fewer than five participants, '
 'so the collapsed test is the one reported.')
wbF.save(OUTX); print('S15 and S18 rewritten')
print(pd.DataFrame(d18,columns=['Group']+['A+G+','A+G-','A-G+','A-G-']+['Total']).to_string(index=False))