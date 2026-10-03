# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S7b
# cell id          : d154baf0-347a-48d5-a32e-105dd8b71370
# frame id         : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
# timestamp        : 2026-09-29 12:55:59 UTC (epoch-ms 1790686559827)
# conda env        : python
# produced         : the four-participant demographics block reproduced in the Table S7b sub-table (sub13-sub16)
# ----------------------------------------------------------------------------

cd /Users/yunman/Desktop/submission && python - <<'PY'
import pandas as pd, numpy as np, warnings
warnings.filterwarnings("ignore")
ids = [6502630, 60334165, 136295480, 141253295]
LONG = {6502630: "sub-000006502630", 60334165: "sub-000060334165",
        136295480: "sub-000136295480", 141253295: "sub-000141253295"}

S = pd.ExcelFile("Figures/table/select_subjects_for validation.xlsx").parse("Sheet1")
S.columns = [str(c).strip() for c in S.columns]
sel = S[S.ID.isin(ids)][["ID", "sex", "recruitmentSite", "Age", "headmotion",
                         "Group", "TIMEPOINT"]].copy()

keep = pd.read_csv("revision/corr_hd_np/empirical_fc_headmotion_excl_fd05.csv")
fd = keep.headmotion.to_numpy(float)
mu, sd = fd.mean(), fd.std(ddof=1)
sel["fd_z_n288"] = (sel.headmotion - mu) / sd
sel["fd_pctile_n288"] = [100.0 * (fd < v).mean() for v in sel.headmotion]
sel["in_n288_sample"] = sel.ID.isin(keep.ID)

hd = pd.read_csv("revision/corr_hd_np/empirical_fc_headmotion_290subs.csv")
chk = hd.set_index("ID").headmotion
assert np.allclose(sel.set_index("ID").headmotion.sort_index(),
                   chk.loc[sel.ID].sort_index()), "motion values disagree"
# group label from the independent motion table too
sel["group_check"] = sel.ID.map(hd.set_index("ID").Group2)

sel.insert(0, "subject", sel.ID.map(LONG))
sel = sel.rename(columns={"sex": "sex", "recruitmentSite": "recruitment_site",
                          "Age": "age_years", "headmotion": "mean_fd_mm",
                          "Group": "diagnostic_group", "group_check": "subgroup"})
sel = sel.drop(columns=["ID"]).sort_values("subject").reset_index(drop=True)
sel.to_csv("/tmp/four_subjects_demographics.csv", index=False)
print(sel.to_string(index=False))
print()
print("n=288 reference: mean FD %.4f mm, s.d. %.4f, median %.4f, range %.4f-%.4f"
      % (mu, sd, np.median(fd), fd.min(), fd.max()))
PY