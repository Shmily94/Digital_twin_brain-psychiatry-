
"""Supplementary Fig. S15 | leave-one-out prediction of four-year symptom change,
covariate-adjusted model specifications (n = 85; sex, recruitment site and mean
framewise displacement in every model)."""
import os, sys, json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
FIGDIR="/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
sys.path.insert(0, os.path.join(FIGDIR,"fig_color")); sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, C, LW, LABEL_PT, ANNOT_PT, TICK_PT, enforce
from fig_export import collect_text_records
import figA4_kit as K
from figA4_kit import PW, PH, ML, MR, MT
apply_np_style(); K.apply_page_style()

B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/'
M=pd.read_csv(B+'np_beha_85subjects_all_quantities.csv')
W=pd.read_csv(B+'np85_12edges_repetitions_wide.csv')[['sub_id','sex','site','headmotion']]
M=M.merge(W,on='sub_id',how='left')
COV=pd.get_dummies(M[['sex','site']],drop_first=True).astype(float); COV['headmotion']=M['headmotion'].values
COVC=list(COV.columns); M=pd.concat([M,COV],axis=1)
y=M['beha_change_raw'].values.astype(float)
sim=[f'simbase_edge{i}' for i in range(1,13)]; emp=[f'emp_edge{i}' for i in range(1,13)]
SPEC=[('a','Covariates only',COVC,'emp',0.6293),
      ('b','Age-19 symptoms',COVC+['beha19_sum'],'emp',0.0286),
      ('c','12 simulated\nNP edges',COVC+sim,'sim',0.0088),
      ('d','12 empirical\nNP edges',COVC+emp,'emp',0.2236),
      ('e','Summed\nsimulated NP',COVC+['simbase_np_sum'],'sim',0.2735),
      ('f','Summed\nempirical NP',COVC+['emp_np_sum'],'emp',0.0372),
      ('g','Summed simulated +\nsummed empirical',COVC+['simbase_np_sum','emp_np_sum'],'sim',0.0258),
      ('h','Symptoms +\n12 simulated edges',COVC+['beha19_sum']+sim,'sim',0.0008),
      ('i','Symptoms +\n12 empirical edges',COVC+['beha19_sum']+emp,'emp',0.0820)]
COL={'sim':C('np12'),'emp':C('baseline')}
def loo(cols):
    X=sm.add_constant(np.asarray(M[cols],float)); m=sm.OLS(y,X).fit()
    h=np.diag(X@np.linalg.pinv(X.T@X)@X.T)
    return y-m.resid/(1-h), m
NC,NR=3,3
GAPX2=14.0
pw_mm=(PW-ML-MR-(NC-1)*GAPX2)/NC; ph_mm=40.0
PH2=MT+3*(K.LETTER_BAND+3.2+ph_mm)+2*K.GAP+15.0+K.MB
fig=K.page(ph=PH2); panels=[]; S=[]
for i,(L,ttl,cols,tok,pperm) in enumerate(SPEC):
    r_,c_=divmod(i,NC)
    x=ML+c_*(pw_mm+GAPX2); ytop=MT+K.LETTER_BAND+3.2+r_*(ph_mm+K.GAP+K.LETTER_BAND+3.2)
    ax=K.axes_mm(fig,x,ytop,pw_mm,ph_mm,ph=PH2)
    p,m=loo(cols); r,_=stats.pearsonr(p,y)
    ax.scatter(p,y,s=6.0,facecolor=COL[tok],edgecolor='none',alpha=.85,zorder=3)
    X1=sm.add_constant(p); f=sm.OLS(y,X1).fit()
    xx=np.linspace(p.min(),p.max(),100); pr=f.get_prediction(sm.add_constant(xx)).summary_frame(alpha=.05)
    ax.fill_between(xx,pr['mean_ci_lower'],pr['mean_ci_upper'],color='0.90',zorder=2,lw=0)
    ax.plot(xx,pr['mean'],color='black',lw=LW,zorder=4)
    ax.axhline(0,color='0.85',lw=LW,zorder=1)
    ax.set_title(ttl,fontsize=LABEL_PT,loc='left',pad=1.6,linespacing=1.15)
    ax.text(.03,.965,'r = %.2f'%r,transform=ax.transAxes,va='top',ha='left',fontsize=ANNOT_PT)
    if r_==NR-1: ax.set_xlabel('Predicted \u0394 symptoms\n(leave-one-out)',fontsize=LABEL_PT)
    if c_==0: ax.set_ylabel('Observed \u0394 symptoms',fontsize=LABEL_PT)
    ax.margins(.07)
    panels.append(dict(ch=L,x=x,axes=[ax],txt=K.letter(fig,x,ytop-1.0,L,ph=PH2)))
    S.append(dict(panel=L,model=ttl,n=len(y),loo_r=round(r,4),P_permutation=pperm,R2=round(m.rsquared,4),
                  adj_R2=round(m.rsquared_adj,4),F=round(m.fvalue,3),df1=int(m.df_model),df2=int(m.df_resid),
                  P_model=m.f_pvalue))
K.align_left_ink(fig,panels,[['a','d','g'],['b','e','h'],['c','f','i']])
K.place_letters(fig,panels,ph=PH2,rows=[['a','b','c'],['d','e','f'],['g','h','i']])

# --- geometry check: every title inside its own column, and closer to its own
#     axes than to the neighbouring panel
fig.canvas.draw(); rend=fig.canvas.get_renderer()
px_mm=fig.get_size_inches()[0]*fig.dpi/PW
bad=[]
cols={}
for i,(L,ttl,cols_,tok,pp) in enumerate(SPEC):
    r_,c_=divmod(i,NC); ax=panels[i]['axes'][0]
    tb=ax.title.get_window_extent(rend); ab=ax.get_window_extent()
    col_x0=(ML+c_*(pw_mm+GAPX2))*px_mm; col_x1=col_x0+pw_mm*px_mm
    over=max(0.0,(tb.x1-col_x1)/px_mm)
    gap_to_neighbour=(col_x1+GAPX2*px_mm-tb.x1)/px_mm
    pad_to_own=(ab.y1-tb.y0)/px_mm
    if over>0.2 or gap_to_neighbour<abs(pad_to_own):
        bad.append((L,round(over,2),round(gap_to_neighbour,2),round(abs(pad_to_own),2)))
print('title overflow / gap check (panel, overflow_mm, gap_to_neighbour_mm, pad_to_own_mm):', bad)
enforce(fig)
fig.savefig('figS15_longitudinal_all_models_v2_A4.png',dpi=400)
fig.savefig('figS15_longitudinal_all_models_v2_A4.pdf')
K.export_pptx(fig,'figS15_longitudinal_all_models_v2_A4.pptx',collect_text_records=collect_text_records)
pd.DataFrame(S).to_csv('figS15_longitudinal_all_models_v2_values.csv',index=False)
print(pd.DataFrame(S).to_string(index=False,float_format=lambda v:'%.4g'%v))
