"""fig2a_cpm_rho

Computes : Fig. 2a connectome-based predictive modelling: Spearman rho between predicted and observed score for each symptom domain x task state, parsed from the saved bubble-plot specification.
Inputs   : figures_v2/fig2/cpm_predict_beha/bubblePlot.json
Output   : fig2a_cpm_rho.csv
Tests    : none in this script — the rho values were produced by the CPM pipeline and are transcribed here
Local    : yes
Seed     : no random component

Recovered from execution-log cell 223f88f4-9977-4a57-b95c-6fe4f8869585
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 12:35:47 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig2a_cpm_rho__cell_223f88f4.py
Reference copy : 04_figures/fig.2/fig2_data/fig2a_cpm_rho.csv  (read-only; never written by this script)
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

import json
import pandas as pd

spec_path = os.path.join(SUB, "figures_v2", "fig2", "cpm_predict_beha",
                         "bubblePlot.json")
spec = json.load(open(spec_path))
tsv = spec["originalData"]["mainDataArr"][0]["fileData"]
a = pd.DataFrame([r.split("\t") for r in tsv.split("\n")[1:]],
                 columns=tsv.split("\n")[0].split("\t")).set_index(
                     "sample_id").astype(float)
a.index.name = "symptom_domain"
print(a.shape)
a.to_csv(os.path.join(OUT, "fig2a_cpm_rho.csv"), float_format="%.12g")
