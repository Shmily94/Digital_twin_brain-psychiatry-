# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 284588c4-c78f-4686-93d5-c6f98fe25907
#   frame id      : fe47a03f-2d43-4fe0-a1c3-e0544839d822
#   ran           : 2026-09-21 15:34:11 UTC
#   conda env     : python
#   cell kind     : py
#   produced      : 04_figures/fig.3/fig3_data/fig3h_subject_edge_counts_1b.csv
# ===========================================================================

D3='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3/fig3_data'
conc_tab.to_csv(f'{D3}/fig3h_edge_direction_1b.csv', index=False)
psub.to_csv(f'{D3}/fig3h_subject_edge_counts_1b.csv', index=False)
import subprocess
print(subprocess.run(['python','fig3h_edge_direction_1b.py'],cwd='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.3',capture_output=True,text=True).stdout[-600:])