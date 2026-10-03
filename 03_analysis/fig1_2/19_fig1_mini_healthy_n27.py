"""fig1_mini_healthy_n27

Computes : Fig. 1 healthy-crossover mini-panel: summed MID reward-network FC per condition (placebo, ketamine, midazolam) for the 27 healthy volunteers.
Inputs   : revision/whole_brain_fc_compare/pharma_data/summed_MID_FCs_3conditions.csv
Output   : fig1_mini_healthy_n27.csv
Tests    : none — subject x condition pivot of the raw summed score
Local    : yes
Seed     : no random component

Recovered from execution-log cell 580428d6-95dc-4aad-9790-2ae4bfe22707
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 21:09:19 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig1_mini_healthy_n27__cell_580428d6.py
Reference copy : 04_figures/fig.1/fig1_data/fig1_mini_healthy_n27.csv  (read-only; never written by this script)
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

d3 = pd.read_csv(os.path.join(SUB, "revision", "whole_brain_fc_compare",
                              "pharma_data", "summed_MID_FCs_3conditions.csv"))
R27 = d3.pivot(index="Subject", columns="Condition", values="raw_score")
print("conditions:", list(R27.columns), "| n =", len(R27))
R27.reset_index().to_csv(os.path.join(OUT, "fig1_mini_healthy_n27.csv"), index=False)
