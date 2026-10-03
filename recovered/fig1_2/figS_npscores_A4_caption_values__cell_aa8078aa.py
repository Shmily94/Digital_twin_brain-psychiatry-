# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/supp_npscores/figS_npscores_A4_caption_values.csv
# cell id     : aa8078aa-16ed-4fa2-841e-b905b126066b
# frame id    : c60c0dc4-003a-4667-bb4f-e50a2f4c1e5f
# executed    : 2026-09-24 23:52:15 UTC
# conda env   : (shell cell)
# Nothing below this banner has been removed or reformatted.
# ======================================================================

# [edit_file] created /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_npscores/figS_npscores_A4.py
+++ /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_npscores/figS_npscores_A4.py
+"""Supplementary figure: the NP factor score within each diagnostic group,
+compared twice - model against data, and baseline against perturbation.
+
+  a  simulated versus EMPIRICAL scores, residualised (age, sex, site, mean FD
+     regressed out, each measure centred separately) - the specification
+     behind the manuscript sentence
+  b  the same comparison on the RAW scores, shown because the two measures
+     carry a constant offset that residualisation removes by construction
+  c  simulated BASELINE versus the AMPA-perturbed state
+  d  simulated BASELINE versus the GABA-A-perturbed state
+
+n = 288 twins throughout (HC 69, high-symptom 89, patients 130).  Every panel
+holds one box per condition per group with all individual observations; the
+open box is the reference condition (empirical in a and b, simulated baseline
+in c and d) and the filled box the model state being compared to it.  Each
+comparison is within subject, so every bracket carries a paired t test.
+
+Sources: supp_empsim/data (a, b) and fig.4/fig4_data/fig4_paired_np_mid_n288.csv
+(c, d); the within-group paired tests for c and d are computed from the
+subject-level file into data/npscores_baseline_vs_perturbed_by_group_n288.csv.
+
+    python figS_npscores_A4.py [--no-caption]
+"""
+import os, sys
+import numpy as np
+import pandas as pd
+import matplotlib
+matplotlib.use("Agg")
+import matplotlib.pyplot as plt
+
+FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
+HERE = os.path.join(FIGDIR, "supp_npscores")
+EMPSIM = os.path.join(FIGDIR, "supp_empsim", "data")
+FIG4 = os.path.join(FIGDIR, "fig.4", "fig4_data")
+sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
+sys.path.insert(0, FIGDIR)
+from np_dtb_style import apply_np_style, panel, C, LW, enforce
+from fig_export import collect_text_records
+from supp_kit import fill, pt_edge
+import figA4_kit as K
+from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT
+
+DPI = 400
+WITH_CAP = "--no-caption" not in sys.argv
+STEM = "figS_npscores_A4" if WITH_CAP else "figS_npscores_A4_nocaption"
+SUPP_NO = "S14"                    # occupied: S1-S8 (FIGURE_LEGENDS.md, with
+                                   # S3 now the merged sensitivity figure),
+                                   # S9 stratify, S10 pet, S11 midpaired,
+                                   # S12 oldham, S13 wbdrug
+apply_np_style()
+K.apply_page_style()
+
+SL = pd.read_csv(os.path.join(EMPSIM, "empsim_subject_level_n288.csv"))
+ES = pd.read_csv(os.path.join(EMPSIM, "empsim_paired_tests_n288.csv"))
+P4 = pd.read_csv(os.path.join(FIG4, "fig4_paired_np_mid_n288.csv"))
+BP = pd.read_csv(os.path.join(
+    HERE, "data", "npscores_baseline_vs_perturbed_by_group_n288.csv"))
+
+GRPS = ["HC", "High-symptom", "Patient"]
+GLAB = {"HC": "Healthy controls", "High-symptom": "High-symptom",
+        "Patient": "Patients"}
+GCOL = {"HC": C("hc"), "High-symptom": C("high_symptom"),
+        "Patient": C("patient")}
+S = {}                             # every caption number
+
+
+def two_condition_panel(ax, frame, cols, labels, ylab, tests, key):
+    """Six boxes: one pair per group, open = reference, filled = model state.
+
+    `tests` maps group -> dict(t, p, n) for the bracket over that group's pair.
+    """
+    rng = np.random.default_rng(0)
+    pos, vals, cols_, filled = [], [], [], []
+    for gi, g in enumerate(GRPS):
+        sub = frame[frame.Group == g]
+        for mi, c in enumerate(cols):
+            pos.append(gi * 2.6 + mi * .95)
+            vals.append(sub[c].values)
+            cols_.append(GCOL[g]); filled.append(mi == 1)
+    bp = ax.boxplot(vals, positions=pos, widths=.62, showfliers=False,
+                    patch_artist=True)
+    for el in ("boxes", "whiskers", "caps", "medians"):
+        for art in bp[el]:
+            art.set_linewidth(LW); art.set_color("black")
+    for i, v in enumerate(vals):
+        bp["boxes"][i].set_facecolor(fill(cols_[i]) if filled[i] else "white")
+        bp["boxes"][i].set_edgecolor("black")
+        ax.scatter(pos[i] + rng.uniform(-.15, .15, len(v)), v, s=4.5,
+                   facecolor=cols_[i] if filled[i] else "none",
+                   edgecolor=pt_edge(cols_[i]) if filled[i] else cols_[i],
+                   linewidth=LW * (.4 if filled[i] else .6), alpha=.85,
+                   zorder=3)
+    lo = float(min(v.min() for v in vals))
+    hi = float(max(v.max() for v in vals))
+    span = hi - lo
+    for gi, g in enumerate(GRPS):
+        r = tests[g]
+        x0, x1 = gi * 2.6, gi * 2.6 + .95
+        ax.plot([x0, x1], [hi + span * .04] * 2, color="0.45", zorder=3)
+        p_ = r["p"]
+        ptxt = f"$P$ = {p_:.3f}" if p_ >= .001 else f"$P$ = {p_:.0e}"
+        ax.text((x0 + x1) / 2, hi + span * .06,
+                f"$t$ = {r['t']:+.2f}\n{ptxt}", ha="center", va="bottom",
+                fontsize=TICK_PT, linespacing=1.15,
+                color="0.35" if p_ >= .05 else C("patient"))
+        S[f"{key}|{g}"] = dict(r)
+    ax.set_xticks(pos)
+    ax.set_xticklabels(labels * len(GRPS), fontsize=TICK_PT)
+    ax.set_ylabel(ylab, fontsize=LABEL_PT)
+    ax.tick_params(axis="both", labelsize=TICK_PT)
+    ax.set_ylim(lo - span * .06, hi + span * .30)
+    ax.set_xlim(-.7, (len(GRPS) - 1) * 2.6 + 1.65)
+    ax.axhline(0, color="0.85", zorder=0)
+    tr = ax.get_xaxis_transform()
+    for gi, g in enumerate(GRPS):      # group identity under its own pair
+        ax.text(gi * 2.6 + .475, -.155, f"{GLAB[g]}\nn = {tests[g]['n']}",
+                transform=tr, ha="center", va="top", fontsize=TICK_PT,
+                color=GCOL[g], clip_on=False)
+
+
+def emp_tests(scored):
+    out = {}
+    for g in GRPS:
+        r = ES[(ES.group == g) & (ES.scores == scored)].iloc[0]
+        out[g] = dict(t=float(r["t"]), p=float(r["p_paired_t"]),
+                      n=int(r["n"]), diff=float(r["mean_diff_sim_minus_emp"]),
+                      lo=float(r["ci95_lo"]), hi=float(r["ci95_hi"]),
+                      dz=float(r["cohens_dz"]), r=float(r["pearson_r_emp_sim"]),
+                      emp=float(r["empirical_mean"]),
+                      sim=float(r["simulated_mean"]))
+    return out
+
+
+def pert_tests(pert):
+    out = {}
+    for g in GRPS:
+        r = BP[(BP.perturbation == pert) & (BP.group == g)].iloc[0]
+        out[g] = dict(t=float(r["t"]), p=float(r["p_paired_t"]),
+                      n=int(r["n"]), diff=float(r["mean_diff"]),
+                      lo=float(r["ci95_lo"]), hi=float(r["ci95_hi"]),
+                      dz=float(r["cohens_dz"]),
+                      pct=float(r["pct_increased"]),
+                      n_up=int(r["n_increased"]),
+                      base=float(r["baseline_mean"]),
+                      pertm=float(r["perturbed_mean"]))
+    return out
+
+
+def p_a(ax):
+    two_condition_panel(ax, SL, ["empirical_resid", "simulated_resid"],
+                        ["emp.", "sim."], "NP factor (residualised)",
+                        emp_tests("residualised"), "a")
+
+
+def p_b(ax):
+    two_condition_panel(ax, SL, ["empirical", "simulated"],
+                        ["emp.", "sim."], "NP factor (raw)",
+                        emp_tests("raw"), "b")
+
+
+def p_c(ax):
+    two_condition_panel(ax, P4, ["np_baseline", "np_ampa"],
+                        ["base.", "AMPA"], "NP factor (simulated)",
+                        pert_tests("AMPA"), "c")
+
+
+def p_d(ax):
+    two_condition_panel(ax, P4, ["np_baseline", "np_gaba"],
+                        ["base.", "GABA-A"], "NP factor (simulated)",
+                        pert_tests("GABA-A"), "d")
+
+
+PANEL_FN = {"a": p_a, "b": p_b, "c": p_c, "d": p_d}
+
+# --------------------------------------------------------------- page geometry
+GUT = K.LETTER_W + K.LETTER_PADX
+GAPX, GAP = 6.0, K.GAP
+LETTER_BAND, MB = K.LETTER_BAND, K.MB
+XB = 12.0                          # condition ticks + the group block label
+MAX_H = 46.0
+ROWS = [["a", "b"], ["c", "d"]]
+BLOCK = {"a": 87.0, "b": 87.0, "c": 87.0, "d": 87.0}   # 174 + 6 gap = 180
+
+
+def col_geom(fig, panels):
+    rend = fig.canvas.get_renderer()
+    mm = lambda px: px / fig.dpi * 25.4
+    by = {p["ch"]: p for p in panels}
+    geom = {}
+    for row in ROWS:
+        x = ML
+        for ch in row:
+            ax = by[ch]["axes"][0]
+            bb, pos = ax.get_tightbbox(rend), ax.get_position()
+            L = min(max(pos.x0 * PW - mm(bb.x0), 0.0), 15.0)
+            R_ = min(max(mm(bb.x1) - (pos.x0 + pos.width) * PW, 0.0), 4.0)
+            geom[ch] = (x, x + GUT + L,
+                        max(BLOCK[ch] - GUT - L - R_, BLOCK[ch] * .5))
+            x += BLOCK[ch] + GAPX
+    return geom
+
+
+def build(plot_h, geom=None):
+    f = plt.figure(figsize=panel(PW, PH))
+    out, y = [], MT
+    for row in ROWS:
+        top = y + LETTER_BAND
+        x = ML
+        for ch in row:
+            slot, ax_x, ax_w = (geom[ch] if geom else
+                                (x, x + GUT + 13.0, BLOCK[ch] - GUT - 15.0))
+            ax = K.axes_mm(f, ax_x, top, ax_w, plot_h)
+            PANEL_FN[ch](ax)
+            out.append(dict(ch=ch, x=slot, axes=[ax],
+                            txt=K.letter(f, slot, top - 1.2, ch)))
+            x += BLOCK[ch] + GAPX
+        y = top + plot_h + XB + GAP
+    enforce(f)
+    return f, out, y - GAP
+
+
+# ------------------------------------------------------------------- caption
+CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | The NP factor score within each "
+             "diagnostic group: simulated against empirical, and simulated "
+             "baseline against the perturbed state.")
+
+
+def pf(p):
+    return (f"P = {p:.3f}" if p >= 1e-3 else
+            f"P = {p:.2g}" if p >= 1e-4 else f"P = {p:.1e}")
+
+
+def emp_line(key):
+    out = []
+    for g in GRPS:
+        d = S[f"{key}|{g}"]
+        out.append(f"{GLAB[g].lower()} (n = {d['n']}) empirical "
+                   f"{d['emp']:+.3f} versus simulated {d['sim']:+.3f}, "
+                   f"difference {d['diff']:+.3f} (95% CI {d['lo']:+.3f} to "
+                   f"{d['hi']:+.3f}), t({d['n'] - 1}) = {d['t']:.3f}, "
+                   f"{pf(d['p'])}, dz = {d['dz']:+.3f}")
+    return "; ".join(out)
+
+
+def pert_line(key):
+    out = []
+    for g in GRPS:
+        d = S[f"{key}|{g}"]
+        out.append(f"{GLAB[g].lower()} (n = {d['n']}) {d['base']:+.3f} to "
+                   f"{d['pertm']:+.3f}, change {d['diff']:+.3f} (95% CI "
+                   f"{d['lo']:+.3f} to {d['hi']:+.3f}), "
+                   f"t({d['n'] - 1}) = {d['t']:.3f}, {pf(d['p'])}, "
+                   f"dz = {d['dz']:+.3f}, {d['n_up']} of {d['n']} twins "
+                   f"({d['pct']:.1f}%) increased")
+    return "; ".join(out)
+
+
+def caption_runs():
+    cap = [
+        ("", "All panels show the same n = 288 twins (69 healthy controls, "
+             "89 high-symptom participants, 130 patients), one box per "
+             "condition per diagnostic group with every individual "
+             "observation plotted beside it; boxes give the median and "
+             "interquartile range with whiskers at 1.5 times that range. The "
+             "open box is the reference condition and the filled box the "
+             "model state compared against it, group identity is carried by "
+             "colour, and because every comparison is within subject each "
+             "bracket carries a two-sided paired t test. a and b ask whether "
+             "the model reproduces the observed score; c and d ask whether "
+             "the virtual perturbation moves that score. "),
+        ("a", ", empirical against simulated scores after residualisation "
+              "(age, sex, site and mean framewise displacement regressed out, "
+              "each measure centred separately) - the specification used in "
+              "the manuscript: " + emp_line("a") + ". Simulated and empirical "
+              "scores do not differ in any group. "),
+        ("b", ", the same comparison on the raw scores: " + emp_line("b")
+              + ". Before residualisation the simulated scores carry a "
+                "downward offset in healthy controls and in patients, which "
+                "is a constant of the measure rather than a group effect and "
+                "is removed by construction in a. The subject-wise "
+                "correlation between the two measures is weak throughout "
+                "(Pearson r = "
+              + ", ".join(f"{S[f'b|{g}']['r']:+.2f}" for g in GRPS)
+              + " for the three groups on the raw scores), so agreement of "
+                "the group distributions should not be read as agreement "
+                "twin by twin. "),
+        ("c", ", simulated baseline against the AMPA-perturbed state: "
+              + pert_line("c") + ". "),
+        ("d", ", simulated baseline against the GABA-A-perturbed state: "
+              + pert_line("d") + ". "),
+        ("", "Read together: the model's resting score is statistically "
+             "indistinguishable from the measured one within every group "
+             "once nuisance variables are removed (a), while both virtual "
+             "perturbations raise the score in every group (c, d) - the "
+             "AMPA effect is largest in patients and the GABA-A effect is "
+             "large and near-universal everywhere. No multiple-comparison "
+             "correction is applied across the panels. Source values are in "
+             "empsim_subject_level_n288.csv and empsim_paired_tests_n288.csv "
+             "(a, b) and in fig4_paired_np_mid_n288.csv (c, d); the "
+             "within-group paired tests for c and d are tabulated in "
+             "npscores_baseline_vs_perturbed_by_group_n288.csv. "),
+    ]
+    runs = [(CAP_TITLE + " ", True)]
+    for lab, seg in cap:
+        if lab:
+            runs.append((lab + ",", True))
+            seg = seg[1:] if seg.startswith(",") else seg
+        runs.append((seg, False))
+    return runs
+
+
+# pass 1 -- caption height at a provisional plot height
+_f0, _p0, _ = build(34.0)
+_runs0 = caption_runs()
+_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
+               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
+plt.close(_f0)
+
+CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
+NROW = len(ROWS)
+FIXED = MT + NROW * (LETTER_BAND + XB) + (NROW - 1) * GAP
+PLOT_H = min((PH - MB - CAP_H - FIXED) / NROW, MAX_H)
+assert PLOT_H > 20.0, f"no room for the panels: {PLOT_H:.1f} mm"
+
+# pass 2 -- solve the column geometry at the fitted height
+_f1, _p1, _ = build(PLOT_H)
+_geom = col_geom(_f1, _p1)
+plt.close(_f1)
+for _ in range(3):
+    _f2, _p2, _ = build(PLOT_H, geom=_geom)
+    _geom = col_geom(_f2, _p2)
+    plt.close(_f2)
+fig, PANELS, BOTTOM = build(PLOT_H, geom=_geom)
+K.place_letters(fig, PANELS, rows=ROWS)
+
+runs = caption_runs()
+if WITH_CAP:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
+        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
+else:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
+
+assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
+print(f"[{STEM}] axes height {PLOT_H:.1f} mm; panels end at {BOTTOM:.1f} mm; "
+      f"caption {n_lines} lines -> {CAP_BOTTOM:.1f} mm of {PH:.0f} mm")
+
+# ----------------------------------------------------------------------- export
+png, pdf, ppt = (os.path.join(HERE, STEM + ext) for ext in (".png", ".pdf", ".pptx"))
+fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
+fig.savefig(pdf, bbox_inches=None, facecolor="white")
+K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
+              collect_text_records=collect_text_records)
+bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
+       if t.get_text().strip() and t.get_fontname() != "Arial"]
+print("non-Arial text:", bad[:5], "| files:",
+      [os.path.basename(p) for p in (png, pdf, ppt)])
+pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
+    os.path.join(HERE, "figS_npscores_A4_caption_values.csv"), index=False)
+plt.close(fig)
+