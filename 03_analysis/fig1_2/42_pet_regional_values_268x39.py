"""pet_regional_values_268x39

Computes : Regional PET values for the 268 Shen parcels across the 39 receptor and transporter maps, labelled by NP-related versus non-NP membership.
Inputs   : figures_v2/fig4/corr_neuromaps_np_regions/np_32_regions_permutation_test.mat; figures_v2/fig4/corr_neuromaps_np_regions/p_permutation_test.mat
Output   : pet_regional_values_268x39.csv
Tests    : none — regional value table with the NP grouping applied
Local    : yes
Seed     : no random component

Recovered from execution-log cell 07048c95-ce44-4f52-89e6-6ec9742a5a20
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 20:43:13 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/pet_regional_values_268x39__cell_07048c95.py
Reference copy : 04_figures/supp_pet/data/pet_regional_values_268x39.csv  (read-only; never written by this script)
"""

import os
import sys

# ---------------------------------------------------------------- paths
# SUBMISSION_ROOT is the author's working tree; every upstream input below
# lives under it.  Override with the environment variable of the same name.
SUB = os.environ.get("SUBMISSION_ROOT", "/Users/yunman/Desktop/submission")
PKG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   os.pardir, os.pardir))
FIGT = os.path.join(PKG, "04_figures")          # read-only reference tree
# Outputs are written to OUT_DIR (default: the current directory).  They are
# NEVER written into 04_figures/, whose copies are the verification reference.
OUT = os.environ.get("OUT_DIR", os.getcwd())
os.makedirs(OUT, exist_ok=True)

import numpy as np
import pandas as pd
import scipy.io as sio
from statsmodels.stats.multitest import multipletests

NM = os.path.join(SUB, "figures_v2", "fig4", "corr_neuromaps_np_regions")
M32 = sio.loadmat(os.path.join(NM, "np_32_regions_permutation_test.mat"))
M19 = sio.loadmat(os.path.join(NM, "p_permutation_test.mat"))
mapn = [str(x[0][0]) for x in M19["map_name"]]
i32 = M32["np_idx"].ravel().astype(int)
V = M32["values"]
np_i = np.array(sorted(i32)) - 1
all_i = np.arange(268)
non_i = np.setdiff1d(all_i, np_i)
short = [m.replace(".nii.gz", "").replace(".nii", "") for m in mapn]

REG = pd.DataFrame(V, columns=short)
REG.insert(0, "shen268_region", range(1, 269))
REG.insert(1, "group",
           np.where(np.isin(np.arange(1, 269), i32), "NP-related", "non-NP"))
print(REG.group.value_counts().to_dict())
REG.to_csv(os.path.join(OUT, "pet_regional_values_268x39.csv"), index=False)
