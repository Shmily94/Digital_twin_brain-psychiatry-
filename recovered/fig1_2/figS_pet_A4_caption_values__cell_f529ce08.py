# ======================================================================
# VERBATIM ARCHIVE of the execution-log cell that produced
#   04_figures/supp_pet/figS_pet_A4_caption_values.csv
# cell id     : f529ce08-4fb0-47d2-bbd5-ea31eb78cb46
# frame id    : 8d001885-f89b-4ca4-9e30-9866f1015ee6
# executed    : 2026-09-24 20:08:06 UTC
# conda env   : (shell cell)
# Nothing below this banner has been removed or reformatted.
# ======================================================================

# [edit_file] created /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_pet/figS_pet_A4.py
+++ /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_pet/figS_pet_A4.py
+"""The 39-map PET panel as a captioned supplementary figure on A4.
+
+Same plot as panels/figS_pet_l (effect size of the negative-profile region set
+against the rest of the Shen-268 parcellation, in each of 39 PET maps), but
+laid out under the frozen rules of figA4_kit: 8 / 9 / 10 pt type, the exact
+permutation statistics in a rich-text caption instead of a declarative title,
+and both variants (with caption and --no-caption).
+
+    python figS_pet_A4.py [--no-caption]
+"""
+import os, sys
+import numpy as np
+import pandas as pd
+import matplotlib
+matplotlib.use("Agg")
+import matplotlib.pyplot as plt
+
+FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
+HERE = os.path.join(FIGDIR, "supp_pet")
+sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
+sys.path.insert(0, FIGDIR)
+from np_dtb_style import apply_np_style, panel, C, LW, enforce
+from fig_export import collect_text_records
+import figA4_kit as K
+from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT
+
+DPI = 400
+WITH_CAP = "--no-caption" not in sys.argv
+STEM = "figS_pet_A4" if WITH_CAP else "figS_pet_A4_nocaption"
+SUPP_NO = "S10"                    # next free number in FIGURE_LEGENDS.md
+apply_np_style()
+K.apply_page_style()
+
+ST = pd.read_csv(os.path.join(HERE, "data", "pet_permutation_39maps.csv"))
+S = ST.sort_values(["receptor", "map_index"]).reset_index(drop=True)
+C_NP, C_OT = C("neg_profile"), C("non_np")
+
+# ------------------------------------------------------------------ the panel
+COL_W = 120.0                      # the plot keeps its own width; the caption
+XB = 11.0                          # runs the full text width below it
+LAB_L = 46.0                       # the widest map name is 44.4 mm at 8 pt
+S_PT = 26.0
+
+
+def forest(ax):
+    y = np.arange(len(S))[::-1]
+    for yy, (_, r) in zip(y, S.iterrows()):
+        sig = bool(r.fdr_significant)
+        ax.plot([0, r.hedges_g], [yy, yy], color="0.75", lw=LW * .8, zorder=1)
+        ax.scatter([r.hedges_g], [yy], s=S_PT,
+                   facecolor=C_NP if sig else "none",
+                   edgecolor=C_NP if sig else "0.45", linewidth=LW, zorder=3)
+    ax.axvline(0, color="0.35", lw=LW, zorder=2)
+    ax.set_yticks(y)
+    ax.set_yticklabels(S.label.values, fontsize=TICK_PT)
+    for t, s in zip(ax.get_yticklabels(), S.fdr_significant.values):
+        t.set_color("0.15" if s else "0.45")
+    ax.tick_params(axis="both", labelsize=TICK_PT)
+    ax.set_ylim(-1, len(S))
+    ax.set_xlabel("Hedges' $g$ (negative profile \u2212 other regions)",
+                  fontsize=LABEL_PT)
+    ax.scatter([], [], s=S_PT, facecolor=C_NP, edgecolor=C_NP, linewidth=LW,
+               label="$q$ < 0.05")
+    ax.scatter([], [], s=S_PT, facecolor="none", edgecolor="0.45",
+               linewidth=LW, label="n.s.")
+    ax.legend(loc="upper left", frameon=False, fontsize=ANNOT_PT,
+              handletextpad=.3, bbox_to_anchor=(.01, .995))
+
+
+def build(plot_h):
+    f = plt.figure(figsize=panel(PW, PH))
+    ax = K.axes_mm(f, ML + LAB_L, MT, COL_W - LAB_L, plot_h)
+    forest(ax)
+    enforce(f)
+    return f, [dict(ch="", x=ML, axes=[ax], txt=None)], MT + plot_h + XB
+
+
+# ------------------------------------------------------------------- caption
+CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Receptor and transporter "
+             "availability in the negative-profile regions, across 39 PET "
+             "maps.")
+
+
+def caption_runs():
+    sig = S[S.fdr_significant].sort_values("q_fdr")
+    names = ", ".join(f"{r.label.replace(' · ', ' ')} (g = {r.hedges_g:.2f}, "
+                      f"q = {r.q_fdr:.3f})" for _, r in sig.iterrows())
+    n_np, n_ot = int(S.n_np.iloc[0]), int(S.n_non_np.iloc[0])
+    n_perm = int(S.n_permutations.iloc[0])
+    cap = [
+        ("", f"Each row is one PET map from the neuromaps collection. The unit "
+             f"of observation is one Shen-268 region: the {n_np} regions "
+             f"plotted as the negative profile are the nodes of its 29 edges, "
+             f"a superset of the {19} nodes of the 12-edge NP factor, and are "
+             f"compared with the remaining {n_ot} regions. x, Hedges' g for "
+             f"the difference in mean regional value (negative profile minus "
+             f"other regions); a filled marker marks a map that survives "
+             f"correction, an open one a map that does not; the map name is "
+             f"printed in black or grey to match. The test is a permutation "
+             f"test on the difference in means: the region labels are "
+             f"reassigned at random {n_perm:,} times with the group sizes "
+             f"held at {n_np} and {n_ot}, and the two-sided P value is "
+             f"(#|null| >= |observed| + 1) / ({n_perm:,} + 1). P values are "
+             f"corrected across all {len(S)} maps with the "
+             f"Benjamini-Hochberg FDR, and {int(S.fdr_significant.sum())} "
+             f"maps reach q < 0.05, all of them in the direction of higher "
+             f"availability in the negative-profile regions: {names}. Every "
+             f"map is shown, so the selection is visible: the effect sizes "
+             f"of the maps that do not survive run from "
+             f"{S.loc[~S.fdr_significant, 'hedges_g'].min():+.2f} to "
+             f"{S.loc[~S.fdr_significant, 'hedges_g'].max():+.2f}. The region "
+             f"set carries the negative-profile colour rather than the "
+             f"NP-factor blue of the main figures because it is defined on "
+             f"the 29-edge profile; repeating the test on the 19 NP-factor "
+             f"nodes alone leaves 6 maps below q = 0.05. "),
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
+_f0, _p0, _ = build(150.0)
+_runs0 = caption_runs()
+_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
+               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
+plt.close(_f0)
+
+CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
+PLOT_H = PH - K.MB - CAP_H - MT - XB
+fig, PANELS, BOTTOM = build(PLOT_H)
+
+runs = caption_runs()
+if WITH_CAP:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
+        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
+else:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
+
+assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
+_ax = PANELS[0]["axes"][0]
+_pitch = _ax.get_position().height * PH / (len(S) - 1)
+print(f"[{STEM}] axes {COL_W - LAB_L:.0f} x {PLOT_H:.1f} mm; row pitch "
+      f"{_pitch:.2f} mm; caption {n_lines} lines -> {CAP_BOTTOM:.1f} mm of "
+      f"{PH:.0f} mm")
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
+S.to_csv(os.path.join(HERE, "figS_pet_A4_caption_values.csv"), index=False)
+plt.close(fig)
+