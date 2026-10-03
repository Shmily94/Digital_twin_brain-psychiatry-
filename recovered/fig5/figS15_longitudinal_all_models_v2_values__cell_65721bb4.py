# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/supp_longitudinal/figS15_longitudinal_all_models_v2_values.csv
# cell id       : 65721bb4-c44f-4aa0-b1ed-7605716b56d1
# frame id      : b194cd74-5255-435a-9c1e-206638f9adae
# cell_index    : 685
# executed at   : 2026-09-29 12:51 UTC
# language      : python
# organised as  : 03_analysis/fig5/60_figS15_longitudinal_all_models_v2_values.py
# This data file is a render-time by-product of 04_figures/_recovered_session_b194cd74/figS15_models_all_v2.py.
# The cell below is the execution-log cell that produced the packaged copy
# (it runs, or last edits and runs, that figure script). The derivation itself
# is the figure script, which is already in the package.
# ---------------------------------------------------------------------------

code=open('figS15_models_all.py').read()
code=code.replace("""SPEC=[('a','Covariates only',COVC,'emp',0.6293),
      ('b','Age-19 symptoms',COVC+['beha19_sum'],'emp',0.0286),
      ('c','12 simulated NP edges',COVC+sim,'sim',0.0088),
      ('d','12 empirical NP edges',COVC+emp,'emp',0.2236),
      ('e','Summed simulated NP',COVC+['simbase_np_sum'],'sim',0.2735),
      ('f','Summed empirical NP',COVC+['emp_np_sum'],'emp',0.0372),
      ('g','Summed simulated + summed empirical',COVC+['simbase_np_sum','emp_np_sum'],'sim',0.0258),
      ('h','Symptoms + 12 simulated edges',COVC+['beha19_sum']+sim,'sim',0.0008),
      ('i','Symptoms + 12 empirical edges',COVC+['beha19_sum']+emp,'emp',0.0820)]""",
"""SPEC=[('a','Covariates only',COVC,'emp',0.6293),
      ('b','Age-19 symptoms',COVC+['beha19_sum'],'emp',0.0286),
      ('c','12 simulated\\nNP edges',COVC+sim,'sim',0.0088),
      ('d','12 empirical\\nNP edges',COVC+emp,'emp',0.2236),
      ('e','Summed\\nsimulated NP',COVC+['simbase_np_sum'],'sim',0.2735),
      ('f','Summed\\nempirical NP',COVC+['emp_np_sum'],'emp',0.0372),
      ('g','Summed simulated +\\nsummed empirical',COVC+['simbase_np_sum','emp_np_sum'],'sim',0.0258),
      ('h','Symptoms +\\n12 simulated edges',COVC+['beha19_sum']+sim,'sim',0.0008),
      ('i','Symptoms +\\n12 empirical edges',COVC+['beha19_sum']+emp,'emp',0.0820)]""")
code=code.replace("pw_mm=(PW-ML-MR-(NC-1)*K.GAPX)/NC; ph_mm=42.0",
                  "GAPX2=14.0\npw_mm=(PW-ML-MR-(NC-1)*GAPX2)/NC; ph_mm=40.0")
code=code.replace("x=ML+c_*(pw_mm+K.GAPX)","x=ML+c_*(pw_mm+GAPX2)")
code=code.replace("PH2=MT+3*(K.LETTER_BAND+ph_mm)+2*K.GAP+15.0+K.MB","PH2=MT+3*(K.LETTER_BAND+3.2+ph_mm)+2*K.GAP+15.0+K.MB")
code=code.replace("ytop=MT+K.LETTER_BAND+r_*(ph_mm+K.GAP+K.LETTER_BAND)","ytop=MT+K.LETTER_BAND+3.2+r_*(ph_mm+K.GAP+K.LETTER_BAND+3.2)")
code=code.replace("txt=K.letter(fig,x,ytop-1.0,L,ph=PH2)","txt=K.letter(fig,x,ytop-1.0,L,ph=PH2)")
code=code.replace("ax.set_title(ttl,fontsize=LABEL_PT,loc='left',pad=2.0)","ax.set_title(ttl,fontsize=LABEL_PT,loc='left',pad=1.6,linespacing=1.15)")
code=code.replace("figS15_longitudinal_all_models_A4","figS15_longitudinal_all_models_v2_A4").replace("figS15_longitudinal_all_models_values","figS15_longitudinal_all_models_v2_values")
CHECK='''
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
'''
code=code.replace("enforce(fig)\nfig.savefig", CHECK+"enforce(fig)\nfig.savefig")
open('figS15_models_all_v2.py','w').write(code)
p=subprocess.run([sys.executable,'figS15_models_all_v2.py'],capture_output=True,text=True,cwd=os.getcwd())
print(p.stdout[-1500:]); print('ERR:',p.stderr[-600:])
