# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : 63137639-4047-44a0-933b-fd5fa6bde094
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:22:00 UTC (epoch-ms 1790677320653)
# conda env        : python
# produced         : cleans the IMAGEN recruitment-site strings that separate the two London sub-sites
# ----------------------------------------------------------------------------


L['s2']=L['recruitmentSite.2'].astype(str).str.replace("'","").str.strip()
L['s1']=L['recruitmentSite.1'].astype(str).str.replace("'","").str.strip()
print(pd.crosstab(L['recruitmentSite'], L['s2']))
print('\nID.1 vs ID ordering aligned?', (L['ID']==L['ID.2']).all(), (L['ID'].head(203)==L['ID.1'].head(203)).all() if L['ID.1'].notna().sum()==203 else 'n/a')
print('\ns1 counts (first 203 rows):'); print(L['s1'].head(203).value_counts().to_dict())
