"""stratify_group_tests

Computes : Supplementary Fig. S1 group comparisons: healthy controls versus MDD, AUD and all patients on the negative profile, the positive profile and the 12-edge NP factor.
Inputs   : figures_v2/fig1/pos_neg_np_stratify_resi_without_ed.csv
Output   : stratify_group_tests.csv
Tests    : two-sided independent-samples Student t test (equal variance); Hedges g with a 95% confidence interval; Bonferroni correction over three tests
Local    : yes
Seed     : no random component

Recovered from execution-log cell ce74bfcc-9a4f-4961-a8dc-5475eaf1d40a
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 20:51:51 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/stratify_group_tests__cell_ce74bfcc.py
Reference copy : 04_figures/supp_stratify/data/stratify_group_tests.csv  (read-only; never written by this script)
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
from scipy import stats

ST = pd.read_csv(os.path.join(SUB, "figures_v2", "fig1",
                              "pos_neg_np_stratify_resi_without_ed.csv"))
ST.columns = [c.strip().lstrip("\ufeff") for c in ST.columns]
ST["Diag"] = np.where(ST.Diseased.isin(["MDD", "AUD"]), ST.Diseased,
                      np.where(ST.Group == "HC", "HC", "Other patient"))

hc = ST[ST.Group == "HC"]
mdd = ST[ST.Diag == "MDD"]
aud = ST[ST.Diag == "AUD"]

SL = ST[["ID", "Group", "Diseased", "Pos_NP", "Neg_NP", "NP factor"]].copy()
SL["panel_group"] = np.where(
    SL.Group == "HC", "HC",
    np.where(SL.Diseased.isin(["MDD", "AUD"]), SL.Diseased, "Other patient"))
# panel b duplicates the patient rows under the label "Patient"; the packaged
# file restricts that duplicate to the MDD and AUD patients (amendment 620aea28)
keep = SL[SL.Group == "Patient"].copy()
keep = keep[keep.Diseased.isin(["MDD", "AUD"])]
keep["panel_group"] = "Patient"
SL2 = pd.concat([SL, keep], ignore_index=True)
pat = SL2[SL2.panel_group == "Patient"]

rows = []
for pan, meas, pairs in [("a", "Neg_NP", [("MDD", mdd), ("AUD", aud)]),
                         ("b", "Pos_NP", [("Patient", pat)]),
                         ("c", "Pos_NP", [("MDD", mdd), ("AUD", aud)]),
                         ("d", "NP factor", [("MDD", mdd), ("AUD", aud)])]:
    for nm, g in pairs:
        t = stats.ttest_ind(hc[meas], g[meas], equal_var=True)
        n1, n2 = len(hc), len(g)
        sp = np.sqrt(((n1 - 1) * hc[meas].var(ddof=1) +
                      (n2 - 1) * g[meas].var(ddof=1)) / (n1 + n2 - 2))
        dd = hc[meas].mean() - g[meas].mean()
        se = sp * np.sqrt(1 / n1 + 1 / n2)
        ci = stats.t.interval(.95, n1 + n2 - 2, dd, se)
        rows.append(dict(panel=pan, measure=meas, group=nm, n_hc=n1, n_group=n2,
                         hc_mean=round(hc[meas].mean(), 4),
                         group_mean=round(g[meas].mean(), 4),
                         diff_hc_minus_group=round(dd, 4),
                         ci95_lo=round(ci[0], 4), ci95_hi=round(ci[1], 4),
                         hedges_g=round(dd / sp * (1 - 3 / (4 * (n1 + n2) - 9)), 4),
                         t=round(t.statistic, 4), df=n1 + n2 - 2,
                         p_uncorrected=float(t.pvalue),
                         p_bonf3=min(float(t.pvalue) * 3, 1.0),
                         test="two-sided independent-samples Student t "
                              "(equal variance)",
                         correction="Bonferroni, 3 tests"))
GT = pd.DataFrame(rows)
print(GT[["panel", "group", "t", "df", "p_bonf3", "hedges_g"]].to_string(
    index=False, float_format=lambda x: "%.4g" % x))
GT.to_csv(os.path.join(OUT, "stratify_group_tests.csv"), index=False)
