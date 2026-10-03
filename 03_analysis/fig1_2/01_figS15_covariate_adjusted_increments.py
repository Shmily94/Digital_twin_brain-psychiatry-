"""figS15_covariate_adjusted_increments

Computes : Covariate-adjusted nested-model increments for the 85-participant longitudinal analysis: the extra variance each predictor block explains over sex, recruitment site and mean framewise displacement.
Inputs   : revision/benchmark_predict_baseline_np/np_beha_85subjects_all_quantities.csv; revision/benchmark_predict_baseline_np/np85_12edges_repetitions_wide.csv
Output   : figS15_covariate_adjusted_increments.csv
Tests    : nested ordinary-least-squares model comparison (partial F test on the R2 increment); Benjamini-Hochberg FDR across the ten increments
Local    : yes
Seed     : no random component

Recovered from execution-log cell 7cb0f84d-b703-4c6e-9dd7-cb2240f1a89e
         frame b194cd74-5255-435a-9c1e-206638f9adae, 2026-09-29 12:26:42 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/figS15_covariate_adjusted_increments__cell_7cb0f84d.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS15_covariate_adjusted_increments.csv  (read-only; never written by this script)
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


def nested2(cov, add, base=COVC):
    X0 = sm.add_constant(np.asarray(MM[base + cov], float))
    X1 = sm.add_constant(np.asarray(MM[base + cov + add], float))
    m0 = sm.OLS(y, X0).fit()
    m1 = sm.OLS(y, X1).fit()
    k = len(add)
    df2 = int(m1.df_resid)
    dR2 = m1.rsquared - m0.rsquared
    F = (dR2 / k) / ((1 - m1.rsquared) / df2)
    return dict(dR2=dR2, F=F, df1=k, df2=df2, P=stats.f.sf(F, k, df2))


ADJ = {
    "summed simulated NP beyond covariates": nested2([], ["simbase_np_sum"]),
    "summed empirical NP beyond covariates": nested2([], ["emp_np_sum"]),
    "summed simulated beyond summed empirical": nested2(["emp_np_sum"], ["simbase_np_sum"]),
    "summed empirical beyond summed simulated": nested2(["simbase_np_sum"], ["emp_np_sum"]),
    "12 simulated edges beyond covariates": nested2([], sim),
    "12 empirical edges beyond covariates": nested2([], emp),
    "12 simulated edges beyond the 12 empirical edges": nested2(emp, sim),
    "12 empirical edges beyond the 12 simulated edges": nested2(sim, emp),
    "12 simulated edges beyond symptoms": nested2(["beha19_sum"], sim),
    "12 empirical edges beyond symptoms": nested2(["beha19_sum"], emp),
}
Z2 = pd.DataFrame(ADJ).T
Z2["q_BH"] = multipletests(Z2.P, method="fdr_bh")[1]
print(Z2[["dR2", "F", "df1", "df2", "P", "q_BH"]].to_string(
    float_format=lambda v: "%.4g" % v))
Z2.round(6).to_csv(os.path.join(OUT, "figS15_covariate_adjusted_increments.csv"))
