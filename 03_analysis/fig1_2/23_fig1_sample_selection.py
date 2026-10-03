"""fig1_sample_selection

Computes : Fig. 1 sample-selection table: screened, analysed and excluded counts with the exclusion reason for each of the seven cohorts entering the study.
Inputs   : none — the table is written out literally, each row citing the data file that carries the count
Output   : fig1_sample_selection.csv
Tests    : none — bookkeeping table
Local    : yes
Seed     : no random component

Recovered from execution-log cell 6cb740f2-6c20-471f-bce9-283abd39f368
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-22 21:09:09 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fig1_sample_selection__cell_6cb740f2.py
Reference copy : 04_figures/fig.1/fig1_data/fig1_sample_selection.csv  (read-only; never written by this script)
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

import pandas as pd

SEL = pd.DataFrame([
    dict(stage=1, cohort="IMAGEN discovery", screened=1050, analysed=1050,
         excluded=0, reason="",
         source="fig2a_cpm_rho.csv (edge selection cohort)"),
    dict(stage=1, cohort="STRATIFY validation", screened=513, analysed=427,
         excluded=86, reason="eating disorder 79; psychosis 6; ADHD 1",
         source="fig2f_sensitivity_cohort_covariates.csv (513 / 434 / 427)"),
    dict(stage=2, cohort="Cross-scale twins", screened=12, analysed=12,
         excluded=0, reason="", source="fig3a_mse_per_subject.csv"),
    dict(stage=3, cohort="Population twins", screened=290, analysed=288,
         excluded=2, reason="mean framewise displacement > 0.5 mm",
         source="group_empir_simu_manipu_np_Resi3.csv (290) \u2192 "
                "fig4_subject_level_n288.csv"),
    dict(stage=4, cohort="Healthy crossover", screened=27, analysed=27,
         excluded=0, reason="",
         source="summed_MID_FCs_3conditions.csv (27 \u00d7 3 conditions)"),
    dict(stage=4, cohort="Clinical ketamine", screened=41, analysed=36,
         excluded=5,
         reason="incomplete placebo + ketamine session pair (MDD 3, HC 2)",
         source="age_demographics_placebo_np_n41.csv \u2192 "
                "age_demographics_n36.csv"),
    dict(stage=5, cohort="IMAGEN follow-up", screened=288, analysed=85,
         excluded=203, reason="no usable four-year follow-up symptom data",
         source="fig5h_longitudinal_n85.csv"),
])
# reason_short was added to the file by the follow-up cell a63db222, which
# supplied the shortened wording used in the Fig. 1 flow diagram explicitly.
SEL["reason_short"] = SEL.reason.replace({
    "eating disorder 79; psychosis 6; ADHD 1":
        "eating disorder 79, psychosis 6, ADHD 1",
    "incomplete placebo + ketamine session pair (MDD 3, HC 2)":
        "incomplete session pair (MDD 3, HC 2)",
    "no usable four-year follow-up symptom data":
        "no four-year follow-up symptoms",
    "mean framewise displacement > 0.5 mm":
        "mean framewise displacement > 0.5 mm"})
SEL.loc[SEL.reason == "", "reason"] = float("nan")
SEL.loc[SEL.reason.isna(), "reason_short"] = float("nan")
print(SEL.to_string(index=False))
SEL.to_csv(os.path.join(OUT, "fig1_sample_selection.csv"), index=False)
