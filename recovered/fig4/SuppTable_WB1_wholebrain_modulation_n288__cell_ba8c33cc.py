# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_wholebrain/wb_data/SuppTable_WB1_wholebrain_modulation_n288.csv
#
# cell id      : ba8c33cc-5568-4fc6-8be4-37a8230fcf10
# frame id     : 97872b81-5061-4c82-a255-9ab25db6e3f8
# timestamp    : 2026-09-07 14:17:32 UTC
# conda env    : python
# language     : python
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/53_SuppTable_WB1_wholebrain_modulation_n288.py
##############################################################################
KEEP=S288
def edges288(d, cond, subkey_ids):
    M=d[cond]; out={}
    for sid in set(subkey_ids):
        s0=strip0(sid)
        if s0 not in KEEP: continue
        sel=np.where(subkey_ids==sid)[0]
        out[s0]=np.nanmean(M[:,:,sel][iu[0],iu[1],:], axis=1)
    return out

def loadids(fn, subkey):
    d=loadmat(p+fn)
    return d, np.array([str(x[0][0]).strip() if len(x[0])>0 else "" for x in d[subkey]])

def paired(E1,E0):
    common=sorted(set(E1)&set(E0))
    A=np.vstack([E0[s] for s in common]); B=np.vstack([E1[s] for s in common])
    diff=B-A
    t,pv=stats.ttest_rel(B,A,axis=0,nan_policy='omit'); t=np.asarray(t); pv=np.asarray(pv)
    ok=np.isfinite(pv); rej=np.zeros_like(pv,bool)
    rej[ok]=multipletests(pv[ok],alpha=0.05,method='fdr_bh')[0]
    dz=np.nanmean(diff,axis=0)/np.nanstd(diff,axis=0,ddof=1)
    return len(common),t,pv,rej,dz

store={}
rows=[]
for mod,subkey,conds in [("sst","sst_subject",["sst_stop_suces","sst_stop_failure"]),
                         ("mid","mid_subject",["mid_feed_hit","mid_antici_hit"])]:
    dB,iB=loadids(f"{mod}_data_baseline_217.mat",subkey)
    dA,iA=loadids(f"{mod}_data_mani_ampa_217.mat",subkey)
    dG,iG=loadids(f"{mod}_data_mani_gaba_217.mat",subkey)
    for c in conds:
        EB=edges288(dB,c,iB); EA=edges288(dA,c,iA); EG=edges288(dG,c,iG)
        for label,E1,E0 in [("AMPA vs baseline",EA,EB),
                            ("AMPA+GABA-A vs baseline",EG,EB),
                            ("AMPA+GABA-A vs AMPA (incremental)",EG,EA)]:
            n,t,pv,rej,dz=paired(E1,E0)
            store[(c,label)]=(t,pv,rej,dz)
            rows.append(dict(condition=c, contrast=label, n_subj=n, n_edges=len(t),
                n_sig_FDR=int(rej.sum()), pct_sig_FDR=round(100*rej.sum()/len(t),1),
                n_up=int(((t>0)&rej).sum()), n_down=int(((t<0)&rej).sum()),
                pct_up_of_sig=round(100*((t>0)&rej).sum()/max(rej.sum(),1),1),
                median_absdz_sig=round(float(np.nanmedian(np.abs(dz[rej]))),3),
                pct_absdz_gt0p5=round(100*np.nanmean(np.abs(dz)>0.5),1),
                pct_absdz_gt0p8=round(100*np.nanmean(np.abs(dz)>0.8),1)))
t288=pd.DataFrame(rows)
t288.to_csv("SuppTable_WB1_wholebrain_modulation_n288.csv", index=False)
print(t288.to_string(index=False))
