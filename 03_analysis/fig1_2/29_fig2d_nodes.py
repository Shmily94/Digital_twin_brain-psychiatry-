"""fig2d_nodes

Computes : Fig. 2d node table: the nineteen circos nodes and the canonical network each belongs to.
Inputs   : none — the node/network assignment is written out literally
Output   : fig2d_nodes.csv
Tests    : none — definition table
Local    : yes
Seed     : no random component

Recovered from execution-log cell 223f88f4-9977-4a57-b95c-6fe4f8869585
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 12:35:47 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig2d_nodes__cell_223f88f4.py
Reference copy : 04_figures/fig.2/fig2_data/fig2d_nodes.csv  (read-only; never written by this script)
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

labels = ["AntPFC", "VentralPCC", "ParaHipp", "dlPFC_1", "dlPFC_2", "ITG_R",
          "ParsOrbitalis_L", "STG", "FEF_R", "AG", "FEF_L", "PreMot+SuppMot",
          "ParsOrbitalis_R", "DorsalPCC", "Caudate", "Hippocampus", "ITG_L",
          "VisMotor", "Fusiform"]
nets = ["DMN", "DMN", "DMN", "FPN", "FPN", "FPN", "SMF", "SMF", "SMF", "SMF",
        "Limbic", "Limbic", "Limbic", "Limbic", "Sub", "Sub", "Motor",
        "Visual Asso", "Visual Asso"]
nodes = pd.DataFrame({"node": labels, "network": nets})
print(nodes.to_string(index=False))
nodes.to_csv(os.path.join(OUT, "fig2d_nodes.csv"), index=False)
