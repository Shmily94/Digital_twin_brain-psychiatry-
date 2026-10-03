# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/supp_cpm/data/cpm_predict_perf_n288.csv
# cell id     : f5dee225-2f16-4504-8ba5-aa7453c89999
# frame id    : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
# executed    : 2026-09-26 17:13:44 UTC
# conda env   : python
# Nothing below this banner has been removed or reformatted.
# ======================================================================

cd "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_cpm" && python - <<'PY'
import scipy.io as sio, numpy as np, pandas as pd
SRC = "/Users/yunman/Desktop/submission/figures_v2/fig4/cpm_task_perf_results"
m = sio.loadmat(f"{SRC}/predict_perf_simulated_empirical_fc_matrix.mat",
                squeeze_me=True, struct_as_record=False)
names = [r.name for r in np.atleast_1d(m["results"])]
rows = []
for f, r, p in zip(names, np.atleast_1d(m["predict_perf"]),
                   np.atleast_1d(m["predict_p_value"])):
    tgt, rest = f.split("_CPM")
    rows.append(dict(target=tgt,
                     fc_source="simulated" if rest.startswith("simulated") else "empirical",
                     task_state="anticipation" if "antici" in rest else "feedback",
                     r=float(r), p=float(p), file=f))
d = pd.DataFrame(rows).sort_values(["target", "fc_source", "task_state"])
d["n"] = len(pd.read_csv(f"{SRC}/task_perf_300subs.csv"))
d.to_csv("data/cpm_predict_perf_n288.csv", index=False)
rt = d[d.target.str.endswith("_RT")]
print(rt.pivot_table(index="target", columns=["fc_source", "task_state"], values="r").round(3).to_string())
from scipy import stats
piv = rt.pivot_table(index=["target", "task_state"], columns="fc_source", values="r")
w = stats.wilcoxon(piv["simulated"], piv["empirical"]); t = stats.ttest_rel(piv["simulated"], piv["empirical"])
print("sim %.3f emp %.3f diff %+.3f | Wilcoxon P=%.4f | t(%d)=%.3f P=%.4f"
      % (piv["simulated"].mean(), piv["empirical"].mean(),
         (piv["simulated"]-piv["empirical"]).mean(), w.pvalue, len(piv)-1, t.statistic, t.pvalue))
print("n rows saved:", len(d))
PY