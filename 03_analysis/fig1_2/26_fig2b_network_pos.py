"""fig2b_network_pos

Computes : Fig. 2b network affiliation of the posative NP profile: edge counts between canonical resting-state networks.
Inputs   : figures_v2/fig2/np_regions/pos_np_factor_network_2.csv
Output   : fig2b_network_pos.csv
Tests    : none in this script — the network affiliation matrix is transcribed
Local    : yes
Seed     : no random component

Recovered from execution-log cell 223f88f4-9977-4a57-b95c-6fe4f8869585
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 12:35:47 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig2b_network_pos__cell_223f88f4.py
Reference copy : 04_figures/fig.2/fig2_data/fig2b_network_pos.csv  (read-only; never written by this script)
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

src = os.path.join(SUB, "figures_v2", "fig2", "np_regions", 'pos_np_factor_network_2.csv')
d = pd.read_csv(src, index_col=0)
print(d.shape, list(d.columns))
d.to_csv(os.path.join(OUT, "fig2b_network_pos.csv"), float_format="%.12g")
