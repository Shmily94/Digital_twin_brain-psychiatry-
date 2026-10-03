# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/fig.2/fig2_data/fig2c_profile_scores.csv
# cell id     : 223f88f4-9977-4a57-b95c-6fe4f8869585
# frame id    : fe47a03f-2d43-4fe0-a1c3-e0544839d822
# executed    : 2026-09-21 12:35:47 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

from scipy import stats
DD=OUT+"fig2_data/"

# --- 2a: CPM prediction (bubble) -- parse from the saved plot spec
spec=json.load(open(SUB+"figures_v2/fig2/cpm_predict_beha/bubblePlot.json"))
tsv=spec["originalData"]["mainDataArr"][0]["fileData"]
a=pd.DataFrame([r.split("\t") for r in tsv.split("\n")[1:]],
               columns=tsv.split("\n")[0].split("\t")).set_index("sample_id").astype(float)
a.index.name="symptom_domain"; a.to_csv(DD+"fig2a_cpm_rho.csv", float_format='%.12g')

# --- 2b: network affiliation of the two profiles
for sign,src in [("neg","figures_v2/fig2/np_regions/neg_np_factor_network_2.csv"),
                 ("pos","figures_v2/fig2/np_regions/pos_np_factor_network_2.csv")]:
    d=pd.read_csv(SUB+src, index_col=0); d.to_csv(DD+f"fig2b_network_{sign}.csv", float_format='%.12g')

# --- 2c: negative profile, HC vs Patient (residuals as published)
c=st[['ID','Group','Diseased','Neg_NP','Pos_NP','NP factor']].rename(columns={'NP factor':'NP_factor'})
c.to_csv(DD+"fig2c_profile_scores.csv", index=False, float_format='%.12g')
t,p=stats.ttest_ind(c.loc[c.Group=='HC','Neg_NP'], c.loc[c.Group=='Patient','Neg_NP'])
tn,pn=stats.ttest_ind(c.loc[c.Group=='HC','NP_factor'], c.loc[c.Group=='Patient','NP_factor'])
print(f"2c Neg_NP  HC(n={(c.Group=='HC').sum()}) vs Patient(n={(c.Group=='Patient').sum()}): t={t:.3f} p={p:.3g} | Bonf(x2)={min(1,p*2):.3g}")
print(f"2c NP12    t={tn:.3f} p={pn:.3g} | Bonf(x2)={min(1,pn*2):.3g}")

# --- 2d: 12-edge circos connectivity matrix
cir=pd.read_csv(SUB+"figures_v2/fig1/np_12_fcs_circos.csv", header=None)
cir.to_csv(DD+"fig2d_circos_matrix.csv", index=False, header=False, float_format='%.12g')
labels=['AntPFC','VentralPCC','ParaHipp','dlPFC_1','dlPFC_2','ITG_R','ParsOrbitalis_L','STG','FEF_R','AG',
        'FEF_L','PreMot+SuppMot','ParsOrbitalis_R','DorsalPCC','Caudate','Hippocampus','ITG_L','VisMotor','Fusiform']
nets=['DMN','DMN','DMN','FPN','FPN','FPN','SMF','SMF','SMF','SMF','Limbic','Limbic','Limbic','Limbic',
      'Sub','Sub','Motor','Visual Asso','Visual Asso']
pd.DataFrame({'node':labels,'network':nets}).to_csv(DD+"fig2d_nodes.csv", index=False)
print("\n2a", a.shape, "| 2b neg/pos 11x11 | 2c", c.shape, "| 2d matrix", cir.shape, "nodes", len(labels))
print("files:", sorted(os.listdir(DD)))
