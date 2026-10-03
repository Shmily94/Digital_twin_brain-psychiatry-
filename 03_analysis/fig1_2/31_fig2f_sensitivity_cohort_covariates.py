"""fig2f_sensitivity_cohort_covariates

Computes : Fig. 2f cohort and covariate sensitivity: how many of the twelve NP edges survive FDR when the cohort definition (427 / 434 / 513) and the covariate set (adjusted / raw) are varied.
Inputs   : figures_v2/fig1/pos_neg_np_stratify_resi.csv; Figures/table/stratify_np_fcs12.mat; figures_v2/fig2/NP_covari_info_STRATIFY.xlsx
Output   : fig2f_sensitivity_cohort_covariates.csv
Tests    : two-sided independent-samples t test per edge, with and without sex, recruitment site and mean framewise displacement as covariates; Benjamini-Hochberg FDR across the twelve edges within each specification
Local    : yes
Seed     : no random component

Recovered from execution-log cell 3be95f4f-5095-4838-a544-3174bbfabd61
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 13:17:15 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig2f_sensitivity_cohort_covariates__cell_3be95f4f.py
Reference copy : 04_figures/fig.2/fig2_data/fig2f_sensitivity_cohort_covariates.csv  (read-only; never written by this script)
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
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests

m = sio.loadmat(os.path.join(SUB, "Figures", "table", "stratify_np_fcs12.mat"))
edges = pd.DataFrame(m["NP_fcs_no_cere"],
                     columns=["edge%d" % i for i in range(1, 13)])
edges.insert(0, "ID", m["id_sub"][:, 0].astype(np.int64))

xl = pd.ExcelFile(os.path.join(SUB, "figures_v2", "fig2",
                               "NP_covari_info_STRATIFY.xlsx"))
hc = xl.parse("HC_info")
hc2 = hc.rename(columns={hc.columns[0]: "ID"})

full = pd.read_csv(os.path.join(SUB, "figures_v2", "fig1",
                                "pos_neg_np_stratify_resi.csv"))
full.columns = [c.strip().lstrip("\ufeff") for c in full.columns]
cohorts = {
    "427 HC+MDD+AUD (current)": full[full.Diseased.isin(["HC", "MDD", "AUD"])],
    "434 all patients, no ED":
        full[full.Diseased.isin(["HC", "MDD", "AUD", "Psychosis", "ADHD"])],
    "513 all incl. ED": full,
}


def run(sub, adjust):
    d = sub[["ID", "Diseased"]].merge(edges, on="ID").merge(
        hc2[["ID", "sex", "recruitmentSite", "headmotion"]], on="ID").dropna(
        subset=["sex", "recruitmentSite", "headmotion"])
    g = np.where(d.Diseased == "HC", "HC", "Patient")
    if adjust:
        Xd = pd.get_dummies(d[["sex", "recruitmentSite"]],
                            drop_first=True).astype(float)
        Xd["hd"] = d.headmotion.values
        X = sm.add_constant(Xd.values)
    out = []
    for i in range(1, 13):
        yv = d["edge%d" % i].values
        r = yv - sm.OLS(yv, X).fit().predict(X) if adjust else yv
        out.append(stats.ttest_ind(r[g == "HC"], r[g == "Patient"]))
    p = np.array([o.pvalue for o in out])
    t = np.array([o.statistic for o in out])
    q = multipletests(p, method="fdr_bh")[1]
    return len(d), int((q < .05).sum()), int((p < .05).sum()), np.where(q < .05)[0] + 1, t


rows = []
for name, sub in cohorts.items():
    for adj in (True, False):
        n, nq, np_, which, t = run(sub, adj)
        rows.append(dict(cohort=name,
                         covariates="sex + site + meanFD" if adj else "none (raw edges)",
                         n=n, n_patients=int((sub.Diseased != "HC").sum()),
                         n_edges_FDR=nq, n_edges_p05=np_,
                         edges_FDR=" ".join("E%d" % i for i in which)))
sens = pd.DataFrame(rows)
print(sens.to_string(index=False))
sens.to_csv(os.path.join(OUT, "fig2f_sensitivity_cohort_covariates.csv"),
            index=False)
