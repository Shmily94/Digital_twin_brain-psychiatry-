"""pet_permutation_39maps

Computes : Spatial-permutation test of NP-related versus non-NP regions for each of 39 PET receptor and transporter maps.
Inputs   : figures_v2/fig4/corr_neuromaps_np_regions/np_32_regions_permutation_test.mat; figures_v2/fig4/corr_neuromaps_np_regions/p_permutation_test.mat
Output   : pet_permutation_39maps.csv
Tests    : two-sided permutation test on the NP-minus-non-NP regional mean difference (10,000 random region reassignments); Hedges g; Benjamini-Hochberg FDR across the 39 maps; the MATLAB-stored P and q are carried alongside for comparison
Local    : yes
Seed     : numpy default_rng(0) for the 10,000-permutation null, as in the original cell

Recovered from execution-log cell 07048c95-ce44-4f52-89e6-6ec9742a5a20
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 20:43:13 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/pet_permutation_39maps__cell_07048c95.py
Reference copy : 04_figures/supp_pet/data/pet_permutation_39maps.csv  (read-only; never written by this script)
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


def disp(s):
    p = s.split("_")
    rec = (p[0].replace("5HT", "5-HT").replace("GABAa-bz", "GABA-A (bz)")
             .replace("GABAa", "GABA-A"))
    return "%s \u00b7 %s \u00b7 %s" % (rec, p[1], p[-1])


real = V[np_i].mean(0) - V[non_i].mean(0)
rng = np.random.default_rng(0)
nperm = 10000
cnt = np.zeros(39)
for b in range(nperm):
    pi = rng.choice(268, len(np_i), replace=False)
    qi = np.setdiff1d(all_i, pi)
    cnt += (np.abs(V[pi].mean(0) - V[qi].mean(0)) >= np.abs(real))
pperm = (cnt + 1) / (nperm + 1)
q_bh = multipletests(pperm, method="fdr_bh")[1]
st_p = M32["p_value_39"].ravel()
st_q = M32["fdr_pvals"].ravel()

PET = pd.DataFrame(dict(
    map_file=mapn, receptor=[s.split("_")[0] for s in short],
    np_mean=V[np_i].mean(0), non_np_mean=V[non_i].mean(0), diff=real,
    hedges_g=[(V[np_i, j].mean() - V[non_i, j].mean()) /
              np.sqrt(((len(np_i) - 1) * V[np_i, j].var(ddof=1) +
                       (len(non_i) - 1) * V[non_i, j].var(ddof=1)) / 266)
              for j in range(39)],
    p_perm=pperm, q_fdr=q_bh, p_perm_stored=st_p, q_fdr_stored=st_q))
PET.insert(1, "label", [disp(s) for s in short])
PET.insert(0, "map_index", range(1, 40))
PET["n_np"] = len(np_i)
PET["n_non_np"] = len(non_i)
PET["n_permutations"] = nperm
PET["fdr_significant"] = PET.q_fdr < 0.05
# two VAChT map names end in "_sum", which the generic label rule mis-parses;
# the follow-up cell 2f0441f5 corrected them in the file
for _k, _v in {"VAChT_feobv_hc18_aghourian_sum.nii": "VAChT \u00b7 feobv \u00b7 aghourian",
               "VAChT_feobv_hc5_bedard_sum.nii": "VAChT \u00b7 feobv \u00b7 bedard"}.items():
    PET.loc[PET.map_file.str.contains(_k.split(".nii")[0]), "label"] = _v
print("recomputed vs stored: p max|d| = %.4f, q max|d| = %.4f"
      % (np.abs(pperm - st_p).max(), np.abs(q_bh - st_q).max()))
print(PET.loc[PET.fdr_significant, ["map_index", "label", "q_fdr"]].to_string(
    index=False, float_format=lambda x: "%.4g" % x))
PET.to_csv(os.path.join(OUT, "pet_permutation_39maps.csv"), index=False)
