# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_wholebrain/wb_data/SuppTable_WB_network_pair_summary_n288.csv
#
# cell id      : 09110be8-1f30-4f28-9d8f-1b5a1e214f70
# frame id     : 97872b81-5061-4c82-a255-9ab25db6e3f8
# timestamp    : 2026-09-07 14:17:54 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/54_SuppTable_WB_network_pair_summary_n288.py
##############################################################################
shen_ids=pd.read_excel(rev+"whole_brain_fc_compare/model_data/remain_id_217.xlsx", header=0).iloc[:,0].astype(int).values
assert len(shen_ids)==217, len(shen_ids)
lab=shen.set_index("NodeNo")["Network2"].to_dict()
net=np.array([str(lab[s]).strip() for s in shen_ids])
ni, nj = net[iu[0]], net[iu[1]]
pair=np.array([" – ".join(sorted([a,b])) if a!=b else f"{a} (within)" for a,b in zip(ni,nj)])
print(pd.Series(net).value_counts().to_dict())

nprows=[]
for (c,label),(t,pv,rej,dz) in store.items():
    for pr in np.unique(pair):
        m=(pair==pr)
        tot=int((m&rej).sum())
        if tot==0: continue
        up=int((m&rej&(t>0)).sum()); dn=tot-up
        nprows.append(dict(condition=c, contrast=label, net_pair=pr,
            n_total=int(m.sum()), n_sig=tot, n_increase=up, n_decrease=dn,
            net_signed_pct=round(100*(up-dn)/m.sum(),2)))
npdf=pd.DataFrame(nprows)
npdf.to_csv("SuppTable_WB_network_pair_summary_n288.csv", index=False)

a=npdf[npdf.contrast=="AMPA vs baseline"]
for c in ["sst_stop_suces","sst_stop_failure"]:
    g=a[a.condition==c].sort_values("net_signed_pct")
    print("==",c,"neg:",[(r.net_pair,round(r.net_signed_pct,1)) for r in g.head(4).itertuples()])
    print("   pos:",[(r.net_pair,round(r.net_signed_pct,1)) for r in g.tail(3).itertuples()])
for c in ["mid_feed_hit","mid_antici_hit"]:
    g=a[a.condition==c]
    print("==",c,"| net-positive frac:",round((g.net_signed_pct>0).mean(),3),"| max:",round(g.net_signed_pct.max(),1))
gb=npdf[npdf.contrast=="AMPA+GABA-A vs baseline"]
print("GABA vs baseline: net-pos frac", round((gb.net_signed_pct>0).mean(),3), "range", round(gb.net_signed_pct.min(),1), round(gb.net_signed_pct.max(),1))
gi=npdf[npdf.contrast=="AMPA+GABA-A vs AMPA (incremental)"]
print("incremental: net-pos frac", round((gi.net_signed_pct>0).mean(),3), "range", round(gi.net_signed_pct.min(),1), round(gi.net_signed_pct.max(),1))
