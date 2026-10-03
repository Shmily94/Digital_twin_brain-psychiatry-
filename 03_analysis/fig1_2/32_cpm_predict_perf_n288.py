"""cpm_predict_perf_n288

Computes : Connectome-based predictive modelling performance for every task-behaviour target, from simulated and from empirical functional connectivity, in each MID task state.
Inputs   : figures_v2/fig4/cpm_task_perf_results/predict_perf_simulated_empirical_fc_matrix.mat; figures_v2/fig4/cpm_task_perf_results/task_perf_300subs.csv
Output   : cpm_predict_perf_n288.csv
Tests    : the r and P per target come from the CPM pipeline stored in the .mat file; this script additionally reports a Wilcoxon signed-rank test and a paired t test comparing simulated with empirical FC across the six reaction-time targets (printed, not stored)
Local    : yes
Seed     : no random component

Recovered from execution-log cell f5dee225-2f16-4504-8ba5-aa7453c89999
         frame c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f, 2026-09-26 17:13:44 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/cpm_predict_perf_n288__cell_f5dee225.py
Reference copy : 04_figures/supp_cpm/data/cpm_predict_perf_n288.csv  (read-only; never written by this script)
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
import scipy.io as sio
from scipy import stats

SRC = os.path.join(SUB, "figures_v2", "fig4", "cpm_task_perf_results")
m = sio.loadmat(os.path.join(SRC, "predict_perf_simulated_empirical_fc_matrix.mat"),
                squeeze_me=True, struct_as_record=False)
names = [r.name for r in np.atleast_1d(m["results"])]
rows = []
for f, r, p in zip(names, np.atleast_1d(m["predict_perf"]),
                   np.atleast_1d(m["predict_p_value"])):
    tgt, rest = f.split("_CPM")
    rows.append(dict(target=tgt,
                     fc_source="simulated" if rest.startswith("simulated") else "empirical",
                     task_state="anticipation" if "antici" in rest else "feedback",
                     r=float(r), p=float(p), file=f))
d = pd.DataFrame(rows).sort_values(["target", "fc_source", "task_state"])
d["n"] = len(pd.read_csv(os.path.join(SRC, "task_perf_300subs.csv")))

rt = d[d.target.str.endswith("_RT")]
piv = rt.pivot_table(index=["target", "task_state"], columns="fc_source", values="r")
w = stats.wilcoxon(piv["simulated"], piv["empirical"])
t = stats.ttest_rel(piv["simulated"], piv["empirical"])
print("sim %.3f emp %.3f diff %+.3f | Wilcoxon P=%.4f | t(%d)=%.3f P=%.4f"
      % (piv["simulated"].mean(), piv["empirical"].mean(),
         (piv["simulated"] - piv["empirical"]).mean(), w.pvalue,
         len(piv) - 1, t.statistic, t.pvalue))
print("n rows saved:", len(d))
d.to_csv(os.path.join(OUT, "cpm_predict_perf_n288.csv"), index=False)
