"""figS15_covariate_adjusted_models

Computes : Covariate-adjusted model-level summary for the 85-participant longitudinal analysis: in-sample R2, leave-one-out r, cross-validated R2 and a permutation P for eight nested specifications.
Inputs   : revision/benchmark_predict_baseline_np/np_beha_85subjects_all_quantities.csv; revision/benchmark_predict_baseline_np/np85_12edges_repetitions_wide.csv
Output   : figS15_covariate_adjusted_models.csv
Tests    : ordinary least squares with leave-one-out cross-validation; permutation test of the leave-one-out r (2,000 shuffles of the outcome); Benjamini-Hochberg FDR across the eight models
Local    : yes
Seed     : numpy default_rng(23) for the permutation null, as in the original cell

Recovered from execution-log cell 7cb0f84d-b703-4c6e-9dd7-cb2240f1a89e
         frame b194cd74-5255-435a-9c1e-206638f9adae, 2026-09-29 12:26:42 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/figS15_covariate_adjusted_models__cell_7cb0f84d.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS15_covariate_adjusted_models.csv  (read-only; never written by this script)
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

W85 = pd.read_csv(os.path.join(B, "np85_12edges_repetitions_wide.csv"))
MM = M.merge(W85[["sub_id", "sex", "site", "headmotion", "age_baseline"]],
             on="sub_id", how="left")
assert MM[["sex", "site", "headmotion"]].notna().all().all()
COV = pd.get_dummies(MM[["sex", "site"]], drop_first=True).astype(float)
COV["headmotion"] = MM["headmotion"].values
COVC = list(COV.columns)
MM = pd.concat([MM, COV], axis=1)

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

SPEC2 = {
    "covariates only": COVC,
    "+ summed simulated": COVC + ["simbase_np_sum"],
    "+ summed empirical": COVC + ["emp_np_sum"],
    "+ 12 simulated edges": COVC + sim,
    "+ 12 empirical edges": COVC + emp,
    "+ symptoms": COVC + ["beha19_sum"],
    "+ symptoms + 12 simulated": COVC + ["beha19_sum"] + sim,
    "+ symptoms + 12 empirical": COVC + ["beha19_sum"] + emp,
}
rng = np.random.default_rng(23)
rows = []
for k, cols in SPEC2.items():
    p, m = loo_pred(MM[cols], y)
    r = np.corrcoef(p, y)[0, 1]
    X = sm.add_constant(np.asarray(MM[cols], float))
    null = np.array([loo_r_fast(X, rng.permutation(y)) for _ in range(2000)])
    rows.append(dict(model=k, R2=m.rsquared, adjR2=m.rsquared_adj, loo_r=r,
                     cvR2=1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2),
                     perm_P=((null >= r).sum() + 1) / 2001))
A = pd.DataFrame(rows)
A["q_BH"] = multipletests(A.perm_P, method="fdr_bh")[1]
print(A.to_string(index=False, float_format=lambda v: "%.4g" % v))
A.to_csv(os.path.join(OUT, "figS15_covariate_adjusted_models.csv"), index=False)
