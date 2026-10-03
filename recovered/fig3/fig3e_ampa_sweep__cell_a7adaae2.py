# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : a7adaae2-30a2-4b07-bd07-3ce69a594847
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-21 14:02:59 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3e_ampa_sweep.csv
#                   (written under its pre-rename name fig3d_ampa_sweep.csv)
# ===========================================================================

amp=pd.read_csv(SUB+"figures_v2/fig3/manipulated_fcs_4subs/plot_mani_AMPA.csv")
gab=pd.read_excel(SUB+"figures_v2/fig3/manipulated_fcs_4subs/plot_mani_gaba.xlsx")
amp.columns=['subject']+[str(c) for c in amp.columns[1:]]
gab.columns=['subject']+[f"{float(c):.4f}" if str(c).replace('.','').isdigit() else str(c) for c in gab.columns[1:]]
amp=amp[amp.subject!='HC02']; gab=gab[gab.subject!='HC02']
amp.to_csv(D3+"fig3d_ampa_sweep.csv", index=False, float_format='%.12g')
gab.to_csv(D3+"fig3e_gaba_sweep.csv", index=False, float_format='%.12g')
print("3d", amp.shape, amp.subject.tolist(), "\n cols:", amp.columns.tolist())
print("3e", gab.shape, gab.subject.tolist(), "\n cols:", gab.columns.tolist())
