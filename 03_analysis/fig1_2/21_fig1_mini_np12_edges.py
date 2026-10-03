"""fig1_mini_np12_edges

Computes : Fig. 1 edge-definition table: the twelve negative-psychopathology edges, their task condition and their parcel pair in the 217-region space.
Inputs   : revision/model_scale_consistent/edge_definitions.csv
Output   : fig1_mini_np12_edges.csv
Tests    : none — definition table
Local    : yes
Seed     : no random component

Recovered from execution-log cell 580428d6-95dc-4aad-9790-2ae4bfe22707
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 21:09:19 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig1_mini_np12_edges__cell_580428d6.py
Reference copy : 04_figures/fig.1/fig1_data/fig1_mini_np12_edges.csv  (read-only; never written by this script)
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

edges = pd.read_csv(os.path.join(SUB, "revision", "model_scale_consistent",
                                 "edge_definitions.csv"))
print(edges.shape, list(edges.columns))
edges.to_csv(os.path.join(OUT, "fig1_mini_np12_edges.csv"), index=False)
