
"""Supplementary Fig. S15 | all nine longitudinal model specifications (n = 85)."""
import os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
FIGDIR="/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
sys.path.insert(0, os.path.join(FIGDIR,"fig_color")); sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, C, LW, LABEL_PT, ANNOT_PT, TICK_PT, LETTER_PT, enforce
from fig_export import collect_text_records
import figA4_kit as K
from figA4_kit import PW, ML, MR, MT
apply_np_style(); K.apply_page_style()

B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/'
M=pd.read_csv(B+'np_beha_85subjects_all_quantities.csv')
Wc=pd.read_csv(B+'np85_12edges_repetitions_wide.csv')[['sub_id','sex','site','headmotion']]
M=M.merge(Wc,on='sub_id',how='left')
COV=pd.get_dummies(M[['sex','site']],drop_first=True).astype(float); COV['headmotion']=M['headmotion'].values
COVC=list(COV.columns); M=pd.concat([M,COV],axis=1)
y=M['beha_change_raw'].values.astype(float)
sim=[f'simbase_edge{i}' for i in range(1,13)]; emp=[f'emp_edge{i}' for i in range(1,13)]
SPEC=[('a','Covariates only',COVC,'emp',0.6293),
      ('b','Age-19 symptoms',COVC+['beha19_sum'],'emp',0.0286),
      ('c','12 simulated edges',COVC+sim,'sim',0.0088),
      ('d','12 empirical edges',COVC+emp,'emp',0.2236),
      ('e','Summed simulated NP',COVC+['simbase_np_sum'],'sim',0.2735),
      ('f','Summed empirical NP',COVC+['emp_np_sum'],'emp',0.0372),
      ('g','Both summed read-outs',COVC+['simbase_np_sum','emp_np_sum'],'sim',0.0258),
      ('h','Symptoms + simulated',COVC+['beha19_sum']+sim,'sim',0.0008),
      ('i','Symptoms + empirical',COVC+['beha19_sum']+emp,'emp',0.0820)]
COL={'sim':C('np12'),'emp':C('baseline')}
def loo(cols):
    X=sm.add_constant(np.asarray(M[cols],float)); m=sm.OLS(y,X).fit()
    h=np.diag(X@np.linalg.pinv(X.T@X)@X.T)
    return y-m.resid/(1-h), m

NC,NR=3,3
GAPX=14.0; GAPY=11.0                 # visible gaps inside a row and between rows
TITLE_BAND=3.6                       # measured band that holds the one-line title
LETTER_GAP=0.6                       # letter sits this far above the title
pw_mm=(PW-ML-MR-(NC-1)*GAPX)/NC; ph_mm=38.0
PH2=MT+NR*(ph_mm+TITLE_BAND+3.0)+(NR-1)*GAPY+14.0+K.MB
fig=K.page(ph=PH2); panels=[]; S=[]
for i,(L,ttl,cols,tok,pperm) in enumerate(SPEC):
    r_,c_=divmod(i,NC)
    x=ML+c_*(pw_mm+GAPX)
    ytop=MT+TITLE_BAND+3.0+r_*(ph_mm+TITLE_BAND+3.0+GAPY)
    ax=K.axes_mm(fig,x,ytop,pw_mm,ph_mm,ph=PH2)
    p,m=loo(cols); r,_=stats.pearsonr(p,y)
    ax.scatter(p,y,s=6.0,facecolor=COL[tok],edgecolor='none',alpha=.85,zorder=3)
    X1=sm.add_constant(p); f=sm.OLS(y,X1).fit()
    xx=np.linspace(p.min(),p.max(),100); pr=f.get_prediction(sm.add_constant(xx)).summary_frame(alpha=.05)
    ax.fill_between(xx,pr['mean_ci_lower'],pr['mean_ci_upper'],color='0.90',zorder=2,lw=0)
    ax.plot(xx,pr['mean'],color='black',lw=LW,zorder=4)
    ax.axhline(0,color='0.85',lw=LW,zorder=1)
    ax.set_title(ttl,fontsize=LABEL_PT,loc='left',pad=1.2)
    ax.text(.03,.965,'r = %.2f'%r,transform=ax.transAxes,va='top',ha='left',fontsize=ANNOT_PT)
    if r_==NR-1: ax.set_xlabel('Predicted \u0394 symptoms\n(leave-one-out)',fontsize=LABEL_PT)
    if c_==0: ax.set_ylabel('Observed \u0394 symptoms',fontsize=LABEL_PT)
    ax.margins(.07)
    panels.append(dict(ch=L,x=x,ytop=ytop,col=c_,axes=[ax]))
    S.append(dict(panel=L,model=ttl,n=len(y),loo_r=round(r,4),P_permutation=pperm,R2=round(m.rsquared,4),
                  adj_R2=round(m.rsquared_adj,4),F=round(m.fvalue,3),df1=int(m.df_model),df2=int(m.df_resid),
                  P_model=m.f_pvalue))
# letters: seated just above each panel's own title, left of its own y-axis ink
fig.canvas.draw(); rend=fig.canvas.get_renderer()
px=fig.get_size_inches()[0]*fig.dpi/PW; h_px=fig.get_size_inches()[1]*fig.dpi
for d in panels:
    ax=d['axes'][0]
    tb=ax.title.get_window_extent(rend); bb=ax.get_tightbbox(rend)
    top_mm=(h_px-tb.y1)/px                     # top of the title, in page mm
    left_mm=min(bb.x0, tb.x0)/px               # leftmost ink of this panel
    d['txt']=K.letter(fig, max(0.0,left_mm-1.0-K.LETTER_W), top_mm-LETTER_GAP, d['ch'], ph=PH2)
fig.canvas.draw(); rend=fig.canvas.get_renderer()
bad=[]
for i,d in enumerate(panels):
    ax=d['axes'][0]; tb=ax.title.get_window_extent(rend); ab=ax.get_window_extent()
    col_x1=(d['x']+pw_mm)*px
    over=max(0.0,(tb.x1-col_x1)/px)
    to_neighbour=(col_x1+GAPX*px-tb.x1)/px
    to_own=(ab.y1-tb.y0)/px
    lb=d['txt'].get_window_extent(rend)
    bad.append((d['ch'],round(over,2),round(to_neighbour,2),round(abs(to_own),2),round((h_px-lb.y0)/px-(h_px-tb.y1)/px,2)))
print('panel, title_overflow_mm, title_to_neighbour_mm, title_to_own_axes_mm, letter_above_title_mm')
for b_ in bad: print('  ',b_)
enforce(fig)
fig.savefig('figS15_longitudinal_all_models_v3_A4.png',dpi=400)
fig.savefig('figS15_longitudinal_all_models_v3_A4.pdf')
K.export_pptx(fig,'figS15_longitudinal_all_models_v3_A4.pptx',collect_text_records=collect_text_records)
pd.DataFrame(S).to_csv('figS15_longitudinal_all_models_v3_values.csv',index=False)
print('page %.1f x %.1f mm | panel %.1f x %.1f mm | row gap %.1f | col gap %.1f'%(PW,PH2,pw_mm,ph_mm,GAPY,GAPX))
