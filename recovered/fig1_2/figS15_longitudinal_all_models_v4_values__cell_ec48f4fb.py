# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS15_longitudinal_all_models_v4_values.csv
# cell id     : ec48f4fb-4f44-4c1c-a00c-aa5929c2ea28
# frame id    : b194cd74-5255-435a-9c1e-206638f9adae
# executed    : 2026-09-29 14:36:59 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================


s=open('figS15_models_all_v3.py').read()
s=s.replace('"""Supplementary Fig. S15 | all nine longitudinal model specifications (n = 85)."""',
            '"""Extended Data Fig. 6 | all nine longitudinal model specifications (n = 85).\nAsterisks mark the permutation P of each specification\'s leave-one-out r."""')
s=s.replace("""    ax.text(.03,.965,'r = %.2f'%r,transform=ax.transAxes,va='top',ha='left',fontsize=ANNOT_PT)""",
"""    star=('***' if pperm<0.001 else '**' if pperm<0.01 else '*' if pperm<0.05 else 'n.s.')
    ax.text(.03,.965,'r = %.2f %s'%(r,star),transform=ax.transAxes,va='top',ha='left',fontsize=ANNOT_PT)""")
s=s.replace("_v3_A4.png","_v4_A4.png").replace("_v3_A4.pdf","_v4_A4.pdf").replace("_v3_A4.pptx","_v4_A4.pptx").replace("_v3_values.csv","_v4_values.csv")
s=s.replace("S.append(dict(panel=L,model=ttl,n=len(y),loo_r=round(r,4),P_permutation=pperm,",
            "S.append(dict(panel=L,model=ttl,n=len(y),loo_r=round(r,4),P_permutation=pperm,significance=star,")
open('figS15_models_all_v4.py','w').write(s)
print('star' in s, s.count('_v4_A4'))
