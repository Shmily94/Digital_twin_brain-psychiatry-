"""fig1_mini_clinical_n36

Computes : Fig. 1 clinical-ketamine mini-panel: placebo and ketamine reward-network FC for the 36 participants with a complete session pair.
Inputs   : revision/text/figures/fig.5/fig5_data/fig5_mdd_hc_n36.csv
Output   : fig1_mini_clinical_n36.csv
Tests    : none — subject-level extract for plotting
Local    : yes
Seed     : no random component

Recovered from execution-log cell 580428d6-95dc-4aad-9790-2ae4bfe22707
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 21:09:19 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig1_mini_clinical_n36__cell_580428d6.py
Reference copy : 04_figures/fig.1/fig1_data/fig1_mini_clinical_n36.csv  (read-only; never written by this script)
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

import pandas as pd

M36 = pd.read_csv(os.path.join(SUB, "revision", "text", "figures", "fig.5",
                               "fig5_data", "fig5_mdd_hc_n36.csv"))
# The recovered cell read FC_p2 / FC_d2 straight off fig5_mdd_hc_n36.csv.  A
# later cell (040b58f5) renamed those two columns to FC_p2_12row / FC_d2_12row
# in that file and re-used the old names for an 11-edge recomputation.  The
# packaged fig1 file holds the 12-row values, so they are read under their
# current names and restored to the column names the packaged file carries.
out = M36[["SubID", "group", "FC_p2_12row", "FC_d2_12row"]].rename(
    columns={"FC_p2_12row": "FC_p2", "FC_d2_12row": "FC_d2"})
print(out.shape, out.group.value_counts().to_dict())
out.to_csv(os.path.join(OUT, "fig1_mini_clinical_n36.csv"), index=False)
