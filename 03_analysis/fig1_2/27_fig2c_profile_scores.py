"""fig2c_profile_scores

Computes : Fig. 2c subject-level negative and positive NP profile scores and the 12-edge NP factor for the 427-participant STRATIFY cohort (HC, MDD, AUD).
Inputs   : figures_v2/fig1/pos_neg_np_stratify_resi_without_ed.csv
Output   : fig2c_profile_scores.csv
Tests    : two-sided independent-samples t test, HC versus patients, on the negative profile and on the 12-edge NP factor; Bonferroni across the two measures (printed; the CSV holds the subject-level scores)
Local    : yes
Seed     : no random component

Recovered from execution-log cell 223f88f4-9977-4a57-b95c-6fe4f8869585
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 12:35:47 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig2c_profile_scores__cell_223f88f4.py
Reference copy : 04_figures/fig.2/fig2_data/fig2c_profile_scores.csv  (read-only; never written by this script)
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

STRATIFY_RESI = os.path.join(SUB, "figures_v2", "fig1",
                             "pos_neg_np_stratify_resi_without_ed.csv")
st = pd.read_csv(STRATIFY_RESI)
st.columns = [c.strip().lstrip("\ufeff") for c in st.columns]
st = st[st.Diseased.isin(["HC", "MDD", "AUD"])].copy()
st["Group"] = np.where(st.Diseased == "HC", "HC", "Patient")
from scipy import stats

c = st[["ID", "Group", "Diseased", "Neg_NP", "Pos_NP", "NP factor"]].rename(
    columns={"NP factor": "NP_factor"})
t, p = stats.ttest_ind(c.loc[c.Group == "HC", "Neg_NP"],
                       c.loc[c.Group == "Patient", "Neg_NP"])
tn, pn = stats.ttest_ind(c.loc[c.Group == "HC", "NP_factor"],
                         c.loc[c.Group == "Patient", "NP_factor"])
print("2c Neg_NP  HC(n=%d) vs Patient(n=%d): t=%.3f p=%.3g | Bonf(x2)=%.3g"
      % ((c.Group == "HC").sum(), (c.Group == "Patient").sum(), t, p, min(1, p * 2)))
print("2c NP12    t=%.3f p=%.3g | Bonf(x2)=%.3g" % (tn, pn, min(1, pn * 2)))
c.to_csv(os.path.join(OUT, "fig2c_profile_scores.csv"), index=False,
         float_format="%.12g")
