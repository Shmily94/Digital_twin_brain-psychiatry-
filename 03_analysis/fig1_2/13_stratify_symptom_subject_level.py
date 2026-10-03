"""stratify_symptom_subject_level

Computes : Subject-level six-band DAWBA symptom sum for the STRATIFY patients and the 215 controls, with the source cohort each control score came from.  (byte-identical copy of supp_stratify/data/stratify_symptom_subject_level.csv, staged into the figS1_k2 working directory by cell 409f1acb before the Supplementary Fig. S1 render.)
Inputs   : revision/edge_level/STRA_self_dawba.mat; revision/edge_level/Self_FU2_inter_exter.mat; revision/edge_level/STRTIFY_dawba_sumscore.xlsx; figures_v2/fig4/DAWBA_beha_symptoms_fu3.xlsx; revision/STARTIFT_HC_subject_list_fu2.txt; revision/STARTIFY_HC_subject_list_fu3.txt; 04_figures/supp_stratify/data/stratify_subject_level_n434.csv
Output   : stratify_symptom_subject_level.csv
Tests    : none — subject-level symptom table
Local    : yes
Seed     : no random component

Recovered from execution-log cell 2671891f-151c-446c-86fe-cbbec44af875
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-23 13:44:26 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/stratify_symptom_subject_level__cell_2671891f.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS1_k2/data/stratify_symptom_subject_level.csv  (read-only; never written by this script)
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

print(sym.groupby(["panel_group", "symptom_source"]).size().to_string())
sym.to_csv(os.path.join(OUT, "stratify_symptom_subject_level.csv"), index=False)
