
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, statsmodels.api as sm
from scipy import stats
apply_figure_style(); apply_arial()
B='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/benchmark_predict_baseline_np/'
M=pd.read_csv(B+'np_beha_85subjects_all_quantities.csv')
y=M['beha_change_raw'].values.astype(float)
sim=[f'simbase_edge{i}' for i in range(1,13)]; emp=[f'emp_edge{i}' for i in range(1,13)]
def loo(cols):
    X=sm.add_constant(np.asarray(M[cols],float)); m=sm.OLS(y,X).fit()
    h=np.diag(X@np.linalg.pinv(X.T@X)@X.T)
    return y-m.resid/(1-h)
PAN=[('a','Age-19 symptoms',['beha19_sum'],0.0010),
     ('b','Symptoms + 12 simulated edges',['beha19_sum']+sim,0.0010),
     ('c','Symptoms + 12 empirical edges',['beha19_sum']+emp,0.0340),
     ('d','12 empirical edges',emp,0.1204)]
COL={'a':'#7F7F7F','b':'#2C6E9B','c':'#B0B0B0','d':'#B0B0B0'}
fig,axes=plt.subplots(2,2,figsize=(6.6,5.6))
STAT=[]
for (L,ttl,cols,pperm),ax in zip(PAN,axes.ravel()):
    p=loo(cols); r,pp=stats.pearsonr(p,y)
    ax.scatter(p,y,s=16,facecolor=COL[L],edgecolor='none',alpha=.85,zorder=3)
    xx=np.linspace(p.min(),p.max(),100)
    X1=sm.add_constant(p); f=sm.OLS(y,X1).fit()
    pr=f.get_prediction(sm.add_constant(xx)).summary_frame(alpha=.05)
    ax.plot(xx,pr['mean'],color='black',zorder=4)
    ax.fill_between(xx,pr['mean_ci_lower'],pr['mean_ci_upper'],color='0.85',alpha=.6,zorder=2)
    ax.axhline(0,color='0.85',zorder=1)
    ax.set_title(ttl,loc='left',fontsize=8)
    ax.text(.03,.97,'r = %.2f'%r,transform=ax.transAxes,va='top',ha='left',fontsize=7)
    ax.set_xlabel('Predicted \u0394 symptoms (leave-one-out)',fontsize=8)
    ax.set_ylabel('Observed \u0394 symptoms',fontsize=8)
    ax.margins(0.06)
    panel_letter(ax,L)
    STAT.append(dict(panel=L,model=ttl,n=len(y),loo_r=r,P_parametric=pp,P_permutation=pperm))
fig.tight_layout()
enforce_line_width(fig)
paths=save_figure_all(fig,'figS_longitudinal_model_scatters')
pd.DataFrame(STAT).to_csv('figS_longitudinal_model_scatters_values.csv',index=False)
print(pd.DataFrame(STAT).to_string(float_format=lambda v:'%.4g'%v)); print(paths)
print('fonts:',check_fonts(fig),'| lw:',check_line_widths(fig))
