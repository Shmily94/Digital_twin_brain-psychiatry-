"""fingerprint_accuracy

Computes : Identification ("fingerprinting") accuracy for empirical and for simulated reward-network connectivity: how often a trial is matched to its own subject, and the self-versus-best-other similarity margin.
Inputs   : figures_v2/fig4/cross_validation/fingerprint_empirical_data.xlsx; figures_v2/fig4/cross_validation/fingerprint_simulated_data.xlsx
Output   : fingerprint_accuracy.csv
Tests    : nearest-neighbour identification accuracy (descriptive); mean self and best-other similarity and their margin
Local    : yes
Seed     : no random component

Recovered from execution-log cell 4f1219ba-ee06-45f1-adc4-bf6e8ed25294
         frame fe47a03f-2d43-4fe0-a1c3-e0544839d822, 2026-09-21 21:29:24 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/fingerprint_accuracy__cell_4f1219ba.py
Reference copy : 04_figures/supp_fingerprint/data/fingerprint_accuracy.csv  (read-only; never written by this script)
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

CV = os.path.join(SUB, "figures_v2", "fig4", "cross_validation")


def acc(path):
    """Identification accuracy from a subject x trial similarity matrix."""
    d = pd.read_excel(path, header=None)
    subs = list(d.iloc[0, 1:].values)
    rows = d.iloc[1:, 0].values
    Mx = d.iloc[1:, 1:].astype(float).values
    truth = [r.split("_")[0] for r in rows]
    pred = [subs[i] for i in Mx.argmax(1)]
    self_r = np.array([Mx[i, subs.index(truth[i])] for i in range(len(rows))])
    other = np.array([np.delete(Mx[i], subs.index(truth[i])).max()
                      for i in range(len(rows))])
    return subs, rows, Mx, truth, pred, self_r, other


FE = acc(os.path.join(CV, "fingerprint_empirical_data.xlsx"))
FS = acc(os.path.join(CV, "fingerprint_simulated_data.xlsx"))

fp = []
for nm, F in [("empirical BOLD", FE), ("simulated (no re-assimilation)", FS)]:
    corr = np.array([t == p for t, p in zip(F[3], F[4])])
    fp.append(dict(data=nm, n_trials=len(corr), n_correct=int(corr.sum()),
                   accuracy_pct=round(100 * float(corr.mean()), 1),
                   mean_self_r=round(float(F[5].mean()), 4),
                   mean_best_other_r=round(float(F[6].mean()), 4),
                   mean_margin=round(float((F[5] - F[6]).mean()), 4),
                   misidentified=";".join([F[1][i] for i in np.where(~corr)[0]])
                                 or "none"))
FPA = pd.DataFrame(fp)
print(FPA.to_string(index=False))
FPA.to_csv(os.path.join(OUT, "fingerprint_accuracy.csv"), index=False)
