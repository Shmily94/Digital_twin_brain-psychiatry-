"""fig2e_edge_group_difference

Computes : Fig. 2e per-edge group difference: HC versus patients on each of the twelve NP edges after regressing out sex, recruitment site and mean framewise displacement.
Inputs   : figures_v2/fig1/pos_neg_np_stratify_resi_without_ed.csv; Figures/table/stratify_np_fcs12.mat; figures_v2/fig2/NP_covari_info_STRATIFY.xlsx
Output   : fig2e_edge_group_difference.csv
Tests    : two-sided independent-samples t test on covariate-residualised edges; Cohen's d with a 95% confidence interval; Benjamini-Hochberg FDR across the twelve edges
Local    : yes
Seed     : no random component

Recovered from execution-log cell e2c4fdf2-d737-4ae5-9f7d-2a754679db40
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 12:56:45 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig2e_edge_group_difference__cell_e2c4fdf2.py
Reference copy : 04_figures/fig.2/fig2_data/fig2e_edge_group_difference.csv  (read-only; never written by this script)
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

STRATIFY_RESI = os.path.join(SUB, "figures_v2", "fig1",
                             "pos_neg_np_stratify_resi_without_ed.csv")
st = pd.read_csv(STRATIFY_RESI)
st.columns = [c.strip().lstrip("\ufeff") for c in st.columns]
st = st[st.Diseased.isin(["HC", "MDD", "AUD"])].copy()
st["Group"] = np.where(st.Diseased == "HC", "HC", "Patient")
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

m = sio.loadmat(os.path.join(SUB, "Figures", "table", "stratify_np_fcs12.mat"))
edges = pd.DataFrame(m["NP_fcs_no_cere"],
                     columns=["edge%d" % i for i in range(1, 13)])
edges.insert(0, "ID", m["id_sub"][:, 0].astype(np.int64))

xl = pd.ExcelFile(os.path.join(SUB, "figures_v2", "fig2",
                               "NP_covari_info_STRATIFY.xlsx"))
hc = xl.parse("HC_info")
hc2 = hc.rename(columns={hc.columns[0]: "ID"})

mrg = st[["ID", "Group"]].merge(edges, on="ID").merge(
    hc2[["ID", "sex", "recruitmentSite", "headmotion"]], on="ID")
mrg = mrg.dropna(subset=["sex", "recruitmentSite", "headmotion"])
print("Fig2e analysis n:", mrg.Group.value_counts().to_dict())

Xd = pd.get_dummies(mrg[["sex", "recruitmentSite"]], drop_first=True).astype(float)
Xd["headmotion"] = mrg.headmotion.values
X = sm.add_constant(Xd.values)

rows = []
for i in range(1, 13):
    yv = mrg["edge%d" % i].values
    r = yv - sm.OLS(yv, X).fit().predict(X)
    g1 = r[(mrg.Group == "HC").values]
    g2 = r[(mrg.Group == "Patient").values]
    tt = stats.ttest_ind(g1, g2)
    d = (g1.mean() - g2.mean()) / np.sqrt(
        ((len(g1) - 1) * g1.var(ddof=1) + (len(g2) - 1) * g2.var(ddof=1)) /
        (len(g1) + len(g2) - 2))
    se = np.sqrt(1 / len(g1) + 1 / len(g2) + d ** 2 / (2 * (len(g1) + len(g2))))
    rows.append(dict(edge="Edge %d" % i, task="SST" if i <= 6 else "MID",
                     t=tt.statistic, p=tt.pvalue, d=d,
                     ci_lo=d - 1.96 * se, ci_hi=d + 1.96 * se))
e2 = pd.DataFrame(rows)
e2["p_fdr"] = multipletests(e2.p, method="fdr_bh")[1]
print(e2.round(4).to_string(index=False))
print("edges passing FDR q<0.05:", int((e2.p_fdr < 0.05).sum()))
e2.to_csv(os.path.join(OUT, "fig2e_edge_group_difference.csv"), index=False,
          float_format="%.12g")
