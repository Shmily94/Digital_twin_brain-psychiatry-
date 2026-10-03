"""npscores_baseline_vs_perturbed_by_group_n288

Computes : Baseline versus perturbed NP score by diagnostic group in the 288 population twins, separately for the AMPA and the GABA-A perturbation.
Inputs   : 04_figures/fig.4/fig4_data/fig4_paired_np_mid_n288.csv
Output   : npscores_baseline_vs_perturbed_by_group_n288.csv
Tests    : paired two-sided t test; Wilcoxon signed-rank test; 95% confidence interval of the mean within-subject difference; Cohen's dz
Local    : yes
Seed     : no random component

Recovered from execution-log cell 52acc453-7941-4f55-b079-4fb602dd73d5
         frame c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f, 2026-09-24 23:51:02 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/npscores_baseline_vs_perturbed_by_group_n288__cell_52acc453.py
Reference copy : 04_figures/supp_npscores/data/npscores_baseline_vs_perturbed_by_group_n288.csv  (read-only; never written by this script)
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

src = os.path.join(FIGT, "fig.4", "fig4_data", "fig4_paired_np_mid_n288.csv")
df = pd.read_csv(src)
rows = []
for pert, col in [("AMPA", "np_ampa"), ("GABA-A", "np_gaba")]:
    for g in ["HC", "High-symptom", "Patient"]:
        s = df[df.Group == g]
        b, p_ = s.np_baseline.values, s[col].values
        d = p_ - b
        t, pv = stats.ttest_rel(p_, b)
        w = stats.wilcoxon(p_, b)
        n = len(d)
        se = d.std(ddof=1) / np.sqrt(n)
        ci = stats.t.ppf(.975, n - 1) * se
        rows.append(dict(perturbation=pert, group=g, n=n,
                         baseline_mean=round(b.mean(), 4),
                         perturbed_mean=round(p_.mean(), 4),
                         mean_diff=round(d.mean(), 4),
                         ci95_lo=round(d.mean() - ci, 4),
                         ci95_hi=round(d.mean() + ci, 4),
                         n_increased=int((d > 0).sum()),
                         pct_increased=round(100 * (d > 0).mean(), 1),
                         t=round(float(t), 3), df=n - 1, p_paired_t=float(pv),
                         wilcoxon_p=float(w.pvalue),
                         cohens_dz=round(float(d.mean() / d.std(ddof=1)), 3)))
out = pd.DataFrame(rows)
print(out.drop(columns=["wilcoxon_p"]).to_string(index=False))
out.to_csv(os.path.join(OUT,
                        "npscores_baseline_vs_perturbed_by_group_n288.csv"),
           index=False)
