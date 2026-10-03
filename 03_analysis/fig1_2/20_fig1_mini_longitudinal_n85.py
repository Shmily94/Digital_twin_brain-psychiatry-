"""fig1_mini_longitudinal_n85

Computes : Fig. 1 longitudinal mini-panel: AMPA restoration index and four-year symptom change for the 85 IMAGEN participants with follow-up.
Inputs   : revision/text/figures/fig.5/fig5_data/fig5h_longitudinal_n85.csv
Output   : fig1_mini_longitudinal_n85.csv
Tests    : two-sided Pearson correlation (printed as a check; not stored in the file)
Local    : yes
Seed     : no random component

Recovered from execution-log cell 580428d6-95dc-4aad-9790-2ae4bfe22707
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 21:09:19 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig1_mini_longitudinal_n85__cell_580428d6.py
Reference copy : 04_figures/fig.1/fig1_data/fig1_mini_longitudinal_n85.csv  (read-only; never written by this script)
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
from scipy import stats

L85 = pd.read_csv(os.path.join(SUB, "revision", "text", "figures", "fig.5",
                               "fig5_data", "fig5h_longitudinal_n85.csv"))
print("corr(ampa index, fu3 change) =",
      round(stats.pearsonr(L85.ampa_restoration_index,
                           L85.fu3_symptom_change)[0], 4))
L85.to_csv(os.path.join(OUT, "fig1_mini_longitudinal_n85.csv"), index=False)
