# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/supp_npscores/data/npscores_baseline_vs_perturbed_by_group_n288.csv
# cell id     : 52acc453-7941-4f55-b079-4fb602dd73d5
# frame id    : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
# executed    : 2026-09-24 23:51:02 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

cd "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_npscores" && python - <<'PY'
import pandas as pd, numpy as np
from scipy import stats
src = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data/fig4_paired_np_mid_n288.csv"
df = pd.read_csv(src)
rows = []
for pert, col in [("AMPA", "np_ampa"), ("GABA-A", "np_gaba")]:
    for g in ["HC", "High-symptom", "Patient"]:
        s = df[df.Group == g]
        b, p_ = s.np_baseline.values, s[col].values
        d = p_ - b
        t, pv = stats.ttest_rel(p_, b)
        w = stats.wilcoxon(p_, b)
        n = len(d); se = d.std(ddof=1) / np.sqrt(n)
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
out.to_csv("data/npscores_baseline_vs_perturbed_by_group_n288.csv", index=False)
print(out.drop(columns=["wilcoxon_p"]).to_string(index=False))
PY