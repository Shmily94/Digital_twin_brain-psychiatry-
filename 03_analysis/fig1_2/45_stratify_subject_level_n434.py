"""stratify_subject_level_n434

Computes : Subject-level negative profile, positive profile and 12-edge NP factor for the STRATIFY cohort, in the panel grouping Supplementary Fig. S1 plots (HC, MDD, AUD, Other patient, plus a duplicated Patient stratum).
Inputs   : figures_v2/fig1/pos_neg_np_stratify_resi_without_ed.csv
Output   : stratify_subject_level_n434.csv
Tests    : none — subject-level extract with the panel grouping applied
Local    : yes
Seed     : no random component

Recovered from execution-log cell ce74bfcc-9a4f-4961-a8dc-5475eaf1d40a
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 20:51:51 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/stratify_subject_level_n434__cell_ce74bfcc.py
Reference copy : 04_figures/supp_stratify/data/stratify_subject_level_n434.csv  (read-only; never written by this script)
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
from scipy import stats

ST = pd.read_csv(os.path.join(SUB, "figures_v2", "fig1",
                              "pos_neg_np_stratify_resi_without_ed.csv"))
ST.columns = [c.strip().lstrip("\ufeff") for c in ST.columns]
ST["Diag"] = np.where(ST.Diseased.isin(["MDD", "AUD"]), ST.Diseased,
                      np.where(ST.Group == "HC", "HC", "Other patient"))

hc = ST[ST.Group == "HC"]
mdd = ST[ST.Diag == "MDD"]
aud = ST[ST.Diag == "AUD"]

SL = ST[["ID", "Group", "Diseased", "Pos_NP", "Neg_NP", "NP factor"]].copy()
SL["panel_group"] = np.where(
    SL.Group == "HC", "HC",
    np.where(SL.Diseased.isin(["MDD", "AUD"]), SL.Diseased, "Other patient"))
# panel b duplicates the patient rows under the label "Patient"; the packaged
# file restricts that duplicate to the MDD and AUD patients (amendment 620aea28)
keep = SL[SL.Group == "Patient"].copy()
keep = keep[keep.Diseased.isin(["MDD", "AUD"])]
keep["panel_group"] = "Patient"
SL2 = pd.concat([SL, keep], ignore_index=True)
pat = SL2[SL2.panel_group == "Patient"]

print("panel_group counts:", SL2.panel_group.value_counts().to_dict())
SL2.to_csv(os.path.join(OUT, "stratify_subject_level_n434.csv"), index=False)
