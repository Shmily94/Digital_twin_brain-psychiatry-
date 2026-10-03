# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/_recovered_session_b194cd74/fig5_data_adj/fig5h_np12_loo_n85.csv
# cell id       : 546b6257-75cd-4dba-8c89-0a1168fb9ea5
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 652
# executed at   : 2026-09-29 12:37 UTC
# language      : python    conda env: python
# organised as  : 03_analysis/fig5/27_fig5h_np12_loo_n85_adj.py
# This is the terminal cell exactly as it ran, with nothing removed and nothing
# reformatted. It is a fragment of an interactive session and is not standalone;
# the organised script carries the full dependency chain from the same session.
# ---------------------------------------------------------------------------

import os, shutil, glob
ADJ='fig5_data_adj'; os.makedirs(ADJ, exist_ok=True)
for f in glob.glob(F5+'*.csv'): shutil.copy(f, ADJ)
obs=y
pd.DataFrame(dict(observed=obs, predicted_sim=PRED3['covariates + 12 simulated NP edges'],
                  predicted_emp=PRED3['covariates + 12 empirical NP edges'])).to_csv(ADJ+'/fig5h_np12_loo_n85.csv',index=False)
sel=[('age-19 symptoms only','covariates + age-19 symptoms',1,0,0),
     ('12 simulated NP edges','covariates + 12 simulated NP edges',12,1,0),
     ('12 empirical NP edges','covariates + 12 empirical NP edges',12,0,1),
     ('symptoms + 12 simulated edges','covariates + symptoms + 12 simulated NP edges',13,1,0),
     ('symptoms + 12 empirical edges','covariates + symptoms + 12 empirical NP edges',13,0,1)]
rows=[]
for label,key,k,si_,em in sel:
    m=MOD3[MOD3.model==key].iloc[0]
    rows.append(dict(model=label,k=k,r_LOO=round(m.loo_r,4),P=round(m.perm_P,5),R2_LOO=round(m.cv_R2,4),
                     short=label.replace('age-19 symptoms only','symptoms').replace('12 simulated NP edges','simulated\nedges')
                            .replace('12 empirical NP edges','empirical\nedges').replace('symptoms + 12 simulated edges','symptoms +\nsimulated')
                            .replace('symptoms + 12 empirical edges','symptoms +\nempirical'),
                     simulated=si_,empirical=em,null_p95=round(m.null_p95,4),perm_P=round(m.perm_P,5),n=85,n_perm=5000))
ACCADJ=pd.DataFrame(rows); ACCADJ.to_csv(ADJ+'/fig5i_np12_loo_accuracy.csv',index=False)
print(ACCADJ[['model','r_LOO','P','R2_LOO','null_p95']].to_string(index=False))
s=src.replace('D = os.path.join(HERE, "fig5_data")', 'D = os.path.join(os.getcwd(), "fig5_data_adj")')
s=s.replace('STEM = "fig5_main_A4_np12" if WITH_CAP else "fig5_main_A4_np12_nocaption"',
            'STEM = "fig5_main_A4_np12_adj" if WITH_CAP else "fig5_main_A4_np12_adj_nocaption"')
OLDTHR='''    thr = float(ACC.null_p95.iloc[0])
    ax.plot([-.6, len(ACC) - .4], [thr] * 2, ls=(0, (2.2, 1.6)), color="0.35",
            lw=LW, zorder=3, solid_capstyle="butt")
    ax.text(len(ACC) - .45, thr, " null 95th", ha="left", va="center",
            fontsize=ANNOT_PT, color="0.35")'''
NEWTHR='''    thr = float(ACC.null_p95.mean())
    for i, row in ACC.iterrows():          # each model has its own null
        ax.plot([i - .33, i + .33], [row.null_p95] * 2, ls=(0, (2.2, 1.6)),
                color="0.35", lw=LW, zorder=3, solid_capstyle="butt")
    ax.text(len(ACC) - .45, thr, " null 95th", ha="left", va="center",
            fontsize=ANNOT_PT, color="0.35")'''
assert OLDTHR in s; s=s.replace(OLDTHR,NEWTHR)
open('fig5_main_A4_np12_adj.py','w').write(s)
p=subprocess.run([sys.executable,'fig5_main_A4_np12_adj.py'],capture_output=True,text=True,cwd=os.getcwd())
print(p.stdout[-1200:]); print('ERR:',p.stderr[-1500:])
