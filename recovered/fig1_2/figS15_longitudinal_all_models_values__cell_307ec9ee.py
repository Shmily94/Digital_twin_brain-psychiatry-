# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/_recovered_session_b194cd74/figS15_longitudinal_all_models_values.csv
# cell id     : 307ec9ee-080c-475a-b1af-8ef24fa16465
# frame id    : b194cd74-5255-435a-9c1e-206638f9adae
# executed    : 2026-09-29 12:48:00 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================


code=open('figS15_models_adj.py').read()
NEWSPEC = '''SPEC=[('a','Covariates only',COVC,'emp',0.6293),
      ('b','Age-19 symptoms',COVC+['beha19_sum'],'emp',0.0286),
      ('c','12 simulated NP edges',COVC+sim,'sim',0.0088),
      ('d','12 empirical NP edges',COVC+emp,'emp',0.2236),
      ('e','Summed simulated NP',COVC+['simbase_np_sum'],'sim',0.2735),
      ('f','Summed empirical NP',COVC+['emp_np_sum'],'emp',0.0372),
      ('g','Summed simulated + summed empirical',COVC+['simbase_np_sum','emp_np_sum'],'sim',0.0258),
      ('h','Symptoms + 12 simulated edges',COVC+['beha19_sum']+sim,'sim',0.0008),
      ('i','Symptoms + 12 empirical edges',COVC+['beha19_sum']+emp,'emp',0.0820)]'''
i0=code.find("SPEC=[('a'"); i1=code.find("COL={'sim'")
code2=code[:i0]+NEWSPEC+"\n"+code[i1:]
code2=code2.replace("NC,NR=3,2","NC,NR=3,3")
code2=code2.replace("PH2=MT+2*(K.LETTER_BAND+ph_mm)+K.GAP+15.0+K.MB","PH2=MT+3*(K.LETTER_BAND+ph_mm)+2*K.GAP+15.0+K.MB")
code2=code2.replace("K.align_left_ink(fig,panels,[['a','d'],['b','e'],['c','f']])","K.align_left_ink(fig,panels,[['a','d','g'],['b','e','h'],['c','f','i']])")
code2=code2.replace("K.place_letters(fig,panels,ph=PH2,rows=[['a','b','c'],['d','e','f']])","K.place_letters(fig,panels,ph=PH2,rows=[['a','b','c'],['d','e','f'],['g','h','i']])")
code2=code2.replace("figS15_longitudinal_models_adj_A4","figS15_longitudinal_all_models_A4").replace("figS15_longitudinal_models_adj_values","figS15_longitudinal_all_models_values")
open('figS15_models_all.py','w').write(code2)
p=subprocess.run([sys.executable,'figS15_models_all.py'],capture_output=True,text=True,cwd=os.getcwd())
print(p.stdout[-1500:]); print('ERR:',p.stderr[-600:])
