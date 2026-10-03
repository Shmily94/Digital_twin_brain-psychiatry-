"""figS15_model_level_corrected

Computes : Model-level leave-one-out r for the six longitudinal specifications with multiplicity correction across the six models.
Inputs   : revision/benchmark_predict_baseline_np/np_beha_85subjects_all_quantities.csv
Output   : figS15_model_level_corrected.csv
Tests    : ordinary least squares with leave-one-out cross-validation; permutation P values carried over from the 2,000-shuffle null; Benjamini-Hochberg FDR and Bonferroni across the six models
Local    : yes
Seed     : the permutation P values are the literal values produced by the earlier null (numpy default_rng(1), 2,000 shuffles) and are hard-coded in the original cell; they are kept verbatim

Recovered from execution-log cell 2d6b646d-ef8c-4908-bae5-710175ddd67a
         frame b194cd74-5255-435a-9c1e-206638f9adae, 2026-09-29 12:22:51 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/figS15_model_level_corrected__cell_2d6b646d.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS15_model_level_corrected.csv  (read-only; never written by this script)
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
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests

B = os.path.join(SUB, "revision", "benchmark_predict_baseline_np")
M = pd.read_csv(os.path.join(B, "np_beha_85subjects_all_quantities.csv"))
sim = ["simbase_edge%d" % i for i in range(1, 13)]
emp = ["emp_edge%d" % i for i in range(1, 13)]
y = M["beha_change_raw"].values.astype(float)

def loo_pred(Xdf, y):
    X = sm.add_constant(np.asarray(Xdf, float))
    m = sm.OLS(y, X).fit()
    h = np.diag(X @ np.linalg.pinv(X.T @ X) @ X.T)
    return y - m.resid / (1 - h), m


def loo_r_fast(X, yv):
    m = sm.OLS(yv, X).fit()
    h = np.diag(X @ np.linalg.pinv(X.T @ X) @ X.T)
    p = yv - m.resid / (1 - h)
    return np.corrcoef(p, yv)[0, 1]

MODELS = {"symptoms": ["beha19_sum"], "sim12": sim, "emp12": emp,
          "symptoms+sim12": ["beha19_sum"] + sim,
          "symptoms+emp12": ["beha19_sum"] + emp,
          "sim12+empNPsum": sim + ["emp_np_sum"]}
res = {}
for k, cols in MODELS.items():
    p, m = loo_pred(M[cols], y)
    res[k] = dict(loo_r=np.corrcoef(p, y)[0, 1])

mods = ["symptoms", "sim12", "emp12", "symptoms+sim12", "symptoms+emp12",
        "sim12+empNPsum"]
# permutation P values as produced by the 2,000-shuffle null in the original run
pv = [0.0010, 0.0095, 0.1204, 0.0010, 0.0340, 0.0015]
q = multipletests(pv, method="fdr_bh")[1]
bonf = np.minimum(np.array(pv) * 6, 1)
MOD = pd.DataFrame(dict(model=mods, loo_r=[res[m]["loo_r"] for m in mods],
                        P_perm=pv, q_BH=q, P_bonf=bonf))
print(MOD.to_string(index=False, float_format=lambda v: "%.4g" % v))
MOD.to_csv(os.path.join(OUT, "figS15_model_level_corrected.csv"), index=False)
