# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/supp_pet/data/pet_permutation_39maps.csv
# cell id     : 07048c95-ce44-4f52-89e6-6ec9742a5a20
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-22 20:43:13 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

PD='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_pet'
os.makedirs(f'{PD}/data',exist_ok=True); os.makedirs(f'{PD}/panels',exist_ok=True)
def disp(s):
    p=s.split('_'); rec=p[0].replace('5HT','5-HT').replace('GABAa-bz','GABA-A (bz)').replace('GABAa','GABA-A')
    lig=p[1]; ds=p[-1]
    return f"{rec} · {lig} · {ds}"
PET.insert(1,'label',[disp(s) for s in short])
PET.insert(0,'map_index',range(1,40))
PET['n_np']=len(np_i); PET['n_non_np']=len(non_i); PET['n_permutations']=nperm
PET['fdr_significant']=PET.q_fdr<0.05
PET.to_csv(f'{PD}/data/pet_permutation_39maps.csv',index=False)
REG=pd.DataFrame(V,columns=short); REG.insert(0,'shen268_region',range(1,269))
REG.insert(1,'group',np.where(np.isin(np.arange(1,269),i32),'NP-related','non-NP'))
REG.to_csv(f'{PD}/data/pet_regional_values_268x39.csv',index=False)
print(PET.loc[PET.fdr_significant,['map_index','label','q_fdr']].to_string(index=False,float_format=lambda x:f'{x:.4g}'))
print('\nwritten', len(PET),'maps;', REG.group.value_counts().to_dict())
