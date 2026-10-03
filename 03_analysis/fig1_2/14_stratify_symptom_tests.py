"""stratify_symptom_tests

Computes : Supplementary Fig. S1e symptom-burden comparison: controls versus MDD, AUD and all patients on the six-band DAWBA sum.  (byte-identical copy of supp_stratify/data/stratify_symptom_tests.csv, staged into the figS1_k2 working directory by cell 409f1acb before the Supplementary Fig. S1 render.)
Inputs   : revision/edge_level/STRA_self_dawba.mat; revision/edge_level/Self_FU2_inter_exter.mat; revision/edge_level/STRTIFY_dawba_sumscore.xlsx; figures_v2/fig4/DAWBA_beha_symptoms_fu3.xlsx; revision/STARTIFT_HC_subject_list_fu2.txt; revision/STARTIFY_HC_subject_list_fu3.txt; 04_figures/supp_stratify/data/stratify_subject_level_n434.csv
Output   : stratify_symptom_tests.csv
Tests    : Welch two-sample t test (unequal variance); Hedges g with a 95% confidence interval; Levene's test of equality of variance; Bonferroni over three tests
Local    : yes
Seed     : no random component

Recovered from execution-log cell 04e1fc40-24bc-49e2-bf84-08baad5e4501
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-23 13:55:32 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/stratify_symptom_tests__cell_04e1fc40.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS1_k2/data/stratify_symptom_tests.csv  (read-only; never written by this script)
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
from scipy import stats as st

EL = os.path.join(SUB, "revision", "edge_level")
RV = os.path.join(SUB, "revision")

# --- subject list and panel grouping (the file produced by the sibling script)
sub = pd.read_csv(os.path.join(FIGT, "supp_stratify", "data",
                               "stratify_subject_level_n434.csv"))
hc = sub[sub.panel_group == "HC"].copy()

# --- STRATIFY self-report DAWBA (six symptom bands)
S = sio.loadmat(os.path.join(EL, "STRA_self_dawba.mat"),
                simplify_cells=True)["STRA_self"]
smat = pd.DataFrame(np.asarray(S["STRA_psy_match"]),
                    columns=["adhd", "cd", "eating", "depre", "anxiety", "phobia"])
smat["ID"] = np.asarray(S["psy_match_sub"])
smat["sum6"] = smat[["adhd", "cd", "eating", "depre", "anxiety",
                     "phobia"]].sum(axis=1)
sx = smat.set_index("ID")

# --- IMAGEN FU2 self-report DAWBA
F = sio.loadmat(os.path.join(EL, "Self_FU2_inter_exter.mat"),
                simplify_cells=True)["FU2_self"]
fud = pd.DataFrame(np.asarray(F["FU2_psy_match"]),
                   columns=["adhd", "cd", "eating", "depre", "anxiety", "phobia"])
fud["ID"] = np.asarray(F["FU2_psy_match_sub"])
fud["sym6_sum"] = fud[["adhd", "cd", "eating", "depre", "anxiety",
                       "phobia"]].sum(axis=1)

# --- IMAGEN FU3 self-report DAWBA
d3 = pd.read_excel(os.path.join(SUB, "figures_v2", "fig4",
                                "DAWBA_beha_symptoms_fu3.xlsx"))
B3 = ["adhd", "cd", "eat", "dep", "gad", "sp"]
d3s = d3.dropna(subset=B3).copy()
d3s["sum6"] = d3s[B3].sum(axis=1)
fu3 = pd.Series(d3s.sum6.values, index=d3s.ID.values)
fu3 = fu3[~fu3.index.duplicated()]

# --- patients: STRATIFY sum-score workbook fixes who has a usable score
dw = pd.read_excel(os.path.join(EL, "STRTIFY_dawba_sumscore.xlsx"))
dw["sym6_sum"] = dw[["ADHD", "CD", "GAD", "DEP", "SP", "ED"]].sum(axis=1)
stra = dw[["PSC2", "sym6_sum"]].rename(columns={"PSC2": "ID"})
patm = sub[sub.panel_group == "Patient"].merge(stra, on="ID", how="inner")
pid = patm.ID.values
pm = sx.loc[[i for i in pid if i in sx.index], "sum6"]

# --- controls: STRATIFY-recruited, then the designated FU2 and FU3 lists
hc_stra = sx.reindex(hc.ID.values).sum6.dropna()
f2 = [l.strip() for l in open(os.path.join(RV, "STARTIFT_HC_subject_list_fu2.txt"))
      if l.strip()]
f3 = [l.strip() for l in open(os.path.join(RV, "STARTIFY_HC_subject_list_fu3.txt"))
      if l.strip()]
i2 = set(int(x) for x in f2)
i3 = set(int(x) for x in f3)
hc_from_f2 = fud.set_index("ID").sym6_sum.reindex(sorted(i2)).dropna()
hc_from_f3 = fu3.reindex(sorted(i3)).dropna()

HC215 = pd.concat([hc_stra, hc_from_f2, hc_from_f3])
assert len(HC215) == 215 and HC215.index.is_unique
src215 = {**{i: "STRATIFY-recruited HC (STRA_self_dawba.mat)" for i in hc_stra.index},
          **{i: "IMAGEN FU2 (STARTIFT_HC_subject_list_fu2.txt)" for i in hc_from_f2.index},
          **{i: "IMAGEN FU3 (STARTIFY_HC_subject_list_fu3.txt)" for i in hc_from_f3.index}}

diag = sub[sub.panel_group.isin(["MDD", "AUD"])][["ID", "panel_group"]].rename(
    columns={"panel_group": "diagnosis"})
sym = pd.DataFrame({"ID": list(pm.index) + list(HC215.index),
                    "panel_group": ["Patient"] * len(pm) + ["HC"] * len(HC215),
                    "sym6_sum": list(pm.values) + list(HC215.values)}).merge(
    diag, on="ID", how="left")
sym["symptom_source"] = [src215.get(i,
                                    "STRATIFY patient self-report (STRA_self_dawba.mat)")
                         for i in sym.ID]
H = sym.loc[sym.panel_group == "HC", "sym6_sum"].values


def welch(a, b):
    t, p = st.ttest_ind(a, b, equal_var=False)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    dfw = ((va / na + vb / nb) ** 2 /
           ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)))
    sp = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    d = (a.mean() - b.mean()) / sp
    g = d * (1 - 3 / (4 * (na + nb) - 9))
    se = np.sqrt((na + nb) / (na * nb) + g ** 2 / (2 * (na + nb - 2)))
    lev = st.levene(a, b)
    return dict(n1=nb, n2=na, df=round(float(dfw), 1), t=float(t), p=float(p),
                g=float(g), ci_lo=float(g - 1.96 * se), ci_hi=float(g + 1.96 * se),
                mean1=float(b.mean()), sd1=float(b.std(ddof=1)),
                mean2=float(a.mean()), sd2=float(a.std(ddof=1)),
                var_ratio=float(va / vb), levene_F=float(lev.statistic),
                levene_p=float(lev.pvalue),
                test="Welch two-sample t test (unequal variance)")


rows = []
for lab, vv in [("MDD", sym.loc[sym.diagnosis == "MDD", "sym6_sum"].values),
                ("AUD", sym.loc[sym.diagnosis == "AUD", "sym6_sum"].values),
                ("Patient", sym.loc[sym.panel_group == "Patient", "sym6_sum"].values)]:
    r = welch(vv, H)
    r.update(panel="e", group=lab, measure="sym6_sum")
    rows.append(r)
STW = pd.DataFrame(rows)
STW["p_bonf3"] = np.minimum(1, STW.p * 3)
print(STW[["group", "n1", "n2", "df", "t", "p", "p_bonf3", "g",
           "var_ratio", "levene_F", "levene_p"]].to_string(index=False))
STW.to_csv(os.path.join(OUT, "stratify_symptom_tests.csv"), index=False)
