"""figS15_nested_increments_corrected

Computes : Nested-model increments for the six-member family of longitudinal comparisons, with FDR and Bonferroni correction across that family.
Inputs   : revision/benchmark_predict_baseline_np/np_beha_85subjects_all_quantities.csv
Output   : figS15_nested_increments_corrected.csv
Tests    : nested ordinary-least-squares model comparison (partial F test on the R2 increment); Benjamini-Hochberg FDR and Bonferroni across the six increments
Local    : yes
Seed     : no random component

Recovered from execution-log cell 2d6b646d-ef8c-4908-bae5-710175ddd67a
         frame b194cd74-5255-435a-9c1e-206638f9adae, 2026-09-29 12:22:51 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/figS15_nested_increments_corrected__cell_2d6b646d.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS15_nested_increments_corrected.csv  (read-only; never written by this script)
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


def nested(cov, add, y=y):
    X0 = sm.add_constant(np.asarray(M[cov], float)) if cov else np.ones((len(y), 1))
    X1 = sm.add_constant(np.asarray(M[cov + add], float))
    m0 = sm.OLS(y, X0).fit()
    m1 = sm.OLS(y, X1).fit()
    k = len(add)
    df2 = int(m1.df_resid)
    dR2 = m1.rsquared - m0.rsquared
    F = (dR2 / k) / ((1 - m1.rsquared) / df2)
    return dict(dR2=dR2, F=F, df1=k, df2=df2, P=stats.f.sf(F, k, df2))


FAM = {
    "12 simulated edges beyond age-19 symptoms": nested(["beha19_sum"], sim),
    "12 empirical edges beyond age-19 symptoms": nested(["beha19_sum"], emp),
    "summed empirical NP beyond the 12 simulated edges": nested(sim, ["emp_np_sum"]),
    "12 simulated edges beyond the summed empirical NP": nested(["emp_np_sum"], sim),
    "12 simulated edges beyond symptoms + summed empirical NP":
        nested(["beha19_sum", "emp_np_sum"], sim),
    "summed empirical NP beyond age-19 symptoms": nested(["beha19_sum"], ["emp_np_sum"]),
}
F = pd.DataFrame(FAM).T
F["q_BH"] = multipletests(F.P, method="fdr_bh")[1]
F["P_bonf"] = np.minimum(F.P * len(F), 1)
print(F[["dR2", "F", "df1", "df2", "P", "q_BH", "P_bonf"]].to_string(
    float_format=lambda v: "%.4g" % v))
F.round(6).to_csv(os.path.join(OUT, "figS15_nested_increments_corrected.csv"))
