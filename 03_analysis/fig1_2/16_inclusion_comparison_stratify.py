"""inclusion_comparison_stratify

Computes : Symptom-burden comparison between STRATIFY participants who entered the n = 288 population-twin analysis and those who did not, overall and within controls and patients.
Inputs   : 04_figures/supp_stratify/data/stratify_symptom_subject_level.csv; 04_figures/fig.4/fig4_data/fig4_subject_level_n288.csv
Output   : inclusion_comparison_stratify.csv
Tests    : Welch two-sample t test; Mann-Whitney U test; Hedges g; chi-square test of independence for group and diagnosis composition
Local    : yes
Seed     : no random component

Recovered from execution-log cell cdaf9702-be32-4d18-a33f-f8e815701be5
         frame b194cd74-5255-435a-9c1e-206638f9adae, 2026-09-29 11:18:35 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/inclusion_comparison_stratify__cell_cdaf9702.py
Reference copy : 04_figures/_recovered_session_b194cd74/inclusion_comparison_stratify.csv  (read-only; never written by this script)
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

ST = pd.read_csv(os.path.join(FIGT, "supp_stratify", "data",
                              "stratify_symptom_subject_level.csv"))
S288 = pd.read_csv(os.path.join(FIGT, "fig.4", "fig4_data",
                                "fig4_subject_level_n288.csv"))
ST["included"] = ST["ID"].isin(S288["ID"])

out = []
for lbl, sub in [("All STRATIFY", ST), ("HC", ST[ST.panel_group == "HC"]),
                 ("Patients", ST[ST.panel_group == "Patient"])]:
    a = sub.loc[sub.included, "sym6_sum"].dropna()
    b = sub.loc[~sub.included, "sym6_sum"].dropna()
    t, p = stats.ttest_ind(a, b, equal_var=False)
    u, pu = stats.mannwhitneyu(a, b)
    dof = ((a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)) ** 2 /
           ((a.var(ddof=1) / len(a)) ** 2 / (len(a) - 1) +
            (b.var(ddof=1) / len(b)) ** 2 / (len(b) - 1)))
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) /
                 (len(a) + len(b) - 2))
    g = (a.mean() - b.mean()) / sp
    out.append(dict(stratum=lbl, n_inc=len(a), n_exc=len(b), m_inc=a.mean(),
                    sd_inc=a.std(ddof=1), m_exc=b.mean(), sd_exc=b.std(ddof=1),
                    t=t, df=dof, P=p, U=u, P_MW=pu, g=g))

ct = pd.crosstab(ST["panel_group"], ST["included"])
c2, p2, _, _ = stats.chi2_contingency(ct.values)
print("group composition included vs not:\n", ct.to_string(),
      "\nchi2(1) = %.2f, P = %.3f" % (c2, p2))
ctd = pd.crosstab(ST.loc[ST.panel_group == "Patient", "diagnosis"],
                  ST.loc[ST.panel_group == "Patient", "included"])
c3, p3, _, _ = stats.chi2_contingency(ctd.values)
print("\ndiagnosis within patients:\n", ctd.to_string(),
      "\nchi2(1) = %.2f, P = %.3f" % (c3, p3))

pd.DataFrame(out).to_csv(
    os.path.join(OUT, "inclusion_comparison_stratify.csv"), index=False)
