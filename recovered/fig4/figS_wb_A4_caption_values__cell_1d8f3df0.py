# Verbatim archive of the execution-log cell that produced
#     04_figures/supp_wholebrain/figS_wb_A4_caption_values.csv
#
# cell id      : 1d8f3df0-c037-40bf-ba5e-506b8baf91cf
# frame id     : 8d001885-f89b-4ca4-9e30-9866f1015ee6
# timestamp    : 2026-09-24 21:58:11 UTC
# conda env    : python
# language     : diff
# exit status  : ok
#
# Nothing below this line has been removed, reordered or reformatted.
# The organised script is 03_analysis/fig4/52_figS_wb_A4_caption_values.py
##############################################################################
# [edit_file] created /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_wholebrain/figS_wb_A4.py
+++ /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_wholebrain/figS_wb_A4.py
+"""Supplementary figure: whole-brain extent of the virtual perturbations, all
+three panels on ONE A4 page.
+
+The panels are those of wb_supp.py, rebuilt under the frozen rules of figA4_kit
+(8 / 9 / 10 / 11 pt type, no declarative titles, every statistic in the
+caption, both variants):
+
+  a  how the proportion of the 23,436 edges falls once an effect-size floor is
+     imposed (FDR q < 0.05 -> |d_z| > 0.5 -> |d_z| > 0.8)
+  b  median |d_z| among the significant edges, by task condition
+  c  net signed change per canonical network pair, 9 x 9, for two task
+     conditions x two contrasts, on one shared colour scale
+
+Nothing is recomputed: both tables are the stored n = 288 whole-brain summaries
+    wb_data/SuppTable_WB1_wholebrain_modulation_n288.csv
+    wb_data/SuppTable_WB_network_pair_summary_n288.csv
+
+    python figS_wb_A4.py [--no-caption]
+"""
+import os, sys
+import numpy as np
+import pandas as pd
+import matplotlib
+matplotlib.use("Agg")
+import matplotlib.pyplot as plt
+from matplotlib.lines import Line2D
+
+FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
+HERE = os.path.join(FIGDIR, "supp_wholebrain")
+sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
+sys.path.insert(0, FIGDIR)
+from np_dtb_style import apply_np_style, panel, C, LW, enforce
+from fig_export import collect_text_records
+import figA4_kit as K
+from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT
+
+D = os.path.join(HERE, "wb_data")
+DPI = 400
+WITH_CAP = "--no-caption" not in sys.argv
+STEM = "figS_wb_A4" if WITH_CAP else "figS_wb_A4_nocaption"
+SUPP_NO = "S7"
+apply_np_style()
+K.apply_page_style()
+
+WB = pd.read_csv(os.path.join(D, "SuppTable_WB1_wholebrain_modulation_n288.csv"))
+NPP = pd.read_csv(os.path.join(D, "SuppTable_WB_network_pair_summary_n288.csv"))
+COND = ["sst_stop_suces", "sst_stop_failure", "mid_feed_hit", "mid_antici_hit"]
+CLAB = {"sst_stop_suces": "SST stop-success",
+        "sst_stop_failure": "SST stop-failure",
+        "mid_feed_hit": "MID feedback", "mid_antici_hit": "MID anticipation"}
+CMK = dict(zip(COND, ["o", "s", "^", "D"]))
+CONTR = [("AMPA vs baseline", "AMPA", C("ampa")),
+         ("AMPA+GABA-A vs baseline", "AMPA+GABA-A", C("gaba"))]
+NETS = ["DMN", "FPN", "Limbic", "Motor", "SMF", "Sub", "Visual Asso",
+        "Visual I", "Visual II"]
+SHOW = [("sst_stop_suces", "AMPA vs baseline"),
+        ("sst_stop_suces", "AMPA+GABA-A vs baseline"),
+        ("mid_feed_hit", "AMPA vs baseline"),
+        ("mid_feed_hit", "AMPA+GABA-A vs baseline")]
+S = {}
+
+
+def row(cond, contrast):
+    return WB[(WB.condition == cond) & (WB.contrast == contrast)].iloc[0]
+
+
+def pair_matrix(cond, contrast):
+    Mx = np.full((len(NETS), len(NETS)), np.nan)
+    sub = NPP[(NPP.condition == cond) & (NPP.contrast == contrast)]
+    for _, r in sub.iterrows():
+        lab = r.net_pair
+        if "(within)" in lab:
+            a = b = lab.split(" (")[0]
+        else:
+            a, b = [s.strip() for s in lab.replace("\u2013", "-").split("-")]
+        i, j = NETS.index(a), NETS.index(b)
+        Mx[i, j] = Mx[j, i] = r.net_signed_pct
+    return Mx
+
+
+ALLM = np.array([pair_matrix(*s) for s in SHOW])
+VMAX = float(np.nanmax(np.abs(ALLM)))
+
+# ------------------------------------------------------------------- panels
+def p_a(ax):
+    xs = [0, 1, 2]
+    for contrast, clab, col in CONTR:
+        for cond in COND:
+            r = row(cond, contrast)
+            ax.plot(xs, [r.pct_sig_FDR, r.pct_absdz_gt0p5, r.pct_absdz_gt0p8],
+                    color=col, lw=LW, marker=CMK[cond], markersize=3.4,
+                    markerfacecolor=col, markeredgecolor=col,
+                    markeredgewidth=LW, zorder=3)
+    ax.set_xticks(xs)
+    ax.set_xticklabels(["FDR\n$q$ < 0.05", "$|d_z|$ > 0.5", "$|d_z|$ > 0.8"],
+                       fontsize=LABEL_PT)
+    ax.tick_params(axis="y", labelsize=TICK_PT)
+    ax.set_xlim(-.3, 2.3); ax.set_ylim(0, 100)
+    ax.set_ylabel("Edges of 23,436 (%)", fontsize=LABEL_PT)
+    h1 = [Line2D([], [], color=col, lw=LW * 1.6) for _, _, col in CONTR]
+    h2 = [Line2D([], [], color="0.4", lw=0, marker=CMK[c], markersize=3.4,
+                 markerfacecolor="0.4", markeredgecolor="0.4") for c in COND]
+    ax.legend(h1 + h2, [l for _, l, _ in CONTR] + [CLAB[c] for c in COND],
+              loc="upper right", ncol=2, fontsize=ANNOT_PT, handletextpad=.4,
+              columnspacing=1.0, labelspacing=.25, borderaxespad=.2,
+              frameon=False)
+    S["a"] = {f"{c}|{k}": dict(fdr=float(row(c, k).pct_sig_FDR),
+                               gt05=float(row(c, k).pct_absdz_gt0p5),
+                               gt08=float(row(c, k).pct_absdz_gt0p8),
+                               n_sig=int(row(c, k).n_sig_FDR),
+                               up=float(row(c, k).pct_up_of_sig))
+              for c in COND for k, _, _ in CONTR}
+
+
+def p_b(ax):
+    xw = np.arange(len(COND))
+    for k, (contrast, clab, col) in enumerate(CONTR):
+        v = [row(c, contrast).median_absdz_sig for c in COND]
+        ax.bar(xw + (k - .5) * .34, v, width=.32, facecolor=col,
+               edgecolor="black", linewidth=LW, zorder=2, label=clab)
+    for y_, lab in [(.5, "medium"), (.8, "large")]:
+        ax.axhline(y_, color="0.6", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
+        ax.text(len(COND) - .45, y_ + .01, lab, ha="right", va="bottom",
+                fontsize=ANNOT_PT, color="0.5")
+    ax.set_xticks(xw)
+    ax.set_xticklabels([CLAB[c].replace(" ", "\n") for c in COND],
+                       fontsize=TICK_PT)
+    ax.tick_params(axis="y", labelsize=TICK_PT)
+    ax.set_xlim(-.6, len(COND) - .4); ax.set_ylim(0, .95)
+    ax.set_ylabel("Median $|d_z|$\n(significant edges)", fontsize=LABEL_PT)
+    ax.legend(loc="upper left", fontsize=ANNOT_PT, handletextpad=.4,
+              borderaxespad=.2, frameon=False)
+    S["b"] = {f"{c}|{k}": float(row(c, k).median_absdz_sig)
+              for c in COND for k, _, _ in CONTR}
+
+
+def p_c(axes):
+    for k, (ax, (cond, contrast)) in enumerate(zip(axes, SHOW)):
+        im = ax.imshow(pair_matrix(cond, contrast), cmap="coolwarm",
+                       vmin=-VMAX, vmax=VMAX)
+        ax.set_xticks(range(len(NETS))); ax.set_yticks(range(len(NETS)))
+        ax.set_xticklabels(NETS, fontsize=TICK_PT, rotation=90)
+        ax.set_yticklabels(NETS if k == 0 else [""] * len(NETS),
+                           fontsize=TICK_PT)
+        ax.set_xticks(np.arange(-.5, len(NETS), 1), minor=True)
+        ax.set_yticks(np.arange(-.5, len(NETS), 1), minor=True)
+        ax.grid(which="minor", color="0.85", linewidth=LW)
+        ax.tick_params(which="both", length=0)
+        for sp in ax.spines.values():
+            sp.set_visible(True); sp.set_linewidth(LW); sp.set_color("0.40")
+        ax.set_title(f"{CLAB[cond]}\n{contrast.split(' vs')[0]}",
+                     fontsize=ANNOT_PT, pad=2)
+    S["c"] = dict(vmax=VMAX, lo=float(np.nanmin(ALLM)),
+                  hi=float(np.nanmax(ALLM)), n_pairs=45,
+                  shown=[f"{c}|{k}" for c, k in SHOW])
+    return im
+
+
+# --------------------------------------------------------------- page geometry
+GUT = K.LETTER_W + K.LETTER_PADX
+GAPX, GAP = 8.5, K.GAP
+LETTER_BAND, MB = K.LETTER_BAND, K.MB
+LAB_A, LAB_B, LAB_C = 17.0, 20.0, 17.0     # y label + y ticks per panel
+XB1, XB2 = 9.0, 21.0                       # 2-line x ticks / rotated net names
+COL_A = 102.0                              # row 1: a wider than b
+COL_B = PW - ML - MR - COL_A - GAPX
+CB_W, CB_GAP, SUB_GAP = 3.2, 3.0, 2.2      # colour bar and sub-matrix gaps
+MAX_H1 = 44.0
+
+
+def build(plot_h1, plot_h2):
+    f = plt.figure(figsize=panel(PW, PH))
+    out = []
+    top = MT + LETTER_BAND
+    ax_a = K.axes_mm(f, ML + GUT + LAB_A, top, COL_A - GUT - LAB_A, plot_h1)
+    p_a(ax_a)
+    out.append(dict(ch="a", x=ML, axes=[ax_a],
+                    txt=K.letter(f, ML, top - 1.2, "a")))
+    xb = ML + COL_A + GAPX
+    ax_b = K.axes_mm(f, xb + GUT + LAB_B, top, COL_B - GUT - LAB_B, plot_h1)
+    p_b(ax_b)
+    out.append(dict(ch="b", x=xb, axes=[ax_b],
+                    txt=K.letter(f, xb, top - 1.2, "b")))
+
+    top2 = top + plot_h1 + XB1 + GAP + LETTER_BAND
+    x0 = ML + GUT + LAB_C
+    wid = (PW - MR - CB_W - CB_GAP - x0 - 3 * SUB_GAP) / 4
+    sub = [K.axes_mm(f, x0 + k * (wid + SUB_GAP), top2, wid, plot_h2)
+           for k in range(4)]
+    im = p_c(sub)
+    cax = K.axes_mm(f, PW - MR - CB_W, top2, CB_W, plot_h2)
+    cb = f.colorbar(im, cax=cax)
+    cb.set_label("Net signed change (%)", fontsize=ANNOT_PT, labelpad=2)
+    cb.ax.tick_params(labelsize=TICK_PT, width=LW, length=1.6)
+    cb.outline.set_linewidth(LW)
+    out.append(dict(ch="c", x=ML, axes=sub,
+                    txt=K.letter(f, ML, top2 - 1.2, "c")))
+    enforce(f)
+    for ax in sub:
+        ax.tick_params(which="both", length=0)
+    return f, out, top2 + plot_h2 + XB2
+
+
+# ------------------------------------------------------------------- caption
+CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Whole-brain extent of the "
+             "virtual perturbations at n = 288.")
+
+
+def caption_runs():
+    a, b, c = S["a"], S["b"], S["c"]
+    fdr = [a[f"{k}|AMPA vs baseline"]["fdr"] for k in COND]
+    fdr2 = [a[f"{k}|AMPA+GABA-A vs baseline"]["fdr"] for k in COND]
+    g05 = [a[f"{k}|AMPA vs baseline"]["gt05"] for k in COND]
+    g08 = [a[f"{k}|AMPA vs baseline"]["gt08"] for k in COND]
+    g05b = [a[f"{k}|AMPA+GABA-A vs baseline"]["gt05"] for k in COND]
+    m1 = [b[f"{k}|AMPA vs baseline"] for k in COND]
+    m2 = [b[f"{k}|AMPA+GABA-A vs baseline"] for k in COND]
+    up2 = [a[f"{k}|AMPA+GABA-A vs baseline"]["up"] for k in COND]
+    cap = [
+        ("", "All three panels are computed on the same edge set: the 23,436 "
+             "upper-triangular edges among 217 nodes, in each of four task "
+             "conditions (SST stop-success, SST stop-failure, MID feedback, "
+             "MID anticipation), for the 288 digital twins of the Fig. 4 "
+             "cohort. Unit of observation is one subject; every edge is tested "
+             "with a two-sided paired t test (df = 287) and the 23,436 tests "
+             "of a condition are corrected together by Benjamini-Hochberg "
+             "FDR. Colour separates the two contrasts throughout: AMPA versus "
+             "baseline and AMPA + GABA-A versus baseline. "),
+        ("a", f", the proportion of edges that survives as the criterion is "
+              f"tightened from FDR significance alone to an effect-size floor. "
+              f"Marker shape gives the task condition. Under AMPA, "
+              f"{min(fdr):.1f}-{max(fdr):.1f}% of edges pass FDR, but only "
+              f"{min(g05):.1f}-{max(g05):.1f}% reach |d_z| > 0.5 and "
+              f"{min(g08):.1f}-{max(g08):.1f}% reach |d_z| > 0.8; under "
+              f"AMPA + GABA-A, {min(fdr2):.1f}-{max(fdr2):.1f}% pass FDR and "
+              f"{min(g05b):.1f}-{max(g05b):.1f}% reach |d_z| > 0.5. The large "
+              f"number of significant edges therefore reflects the power "
+              f"available at n = 288 rather than a large per-edge effect, and "
+              f"an effect-size floor should be stated whenever the extent is "
+              f"described in words. "),
+        ("b", f", the median |d_z| among the significant edges of each "
+              f"condition; the dashed lines mark the conventional medium "
+              f"(0.5) and large (0.8) benchmarks. AMPA: "
+              f"{min(m1):.3f}-{max(m1):.3f}. AMPA + GABA-A: "
+              f"{min(m2):.3f}-{max(m2):.3f}. The typical significant edge is "
+              f"thus a small-to-medium effect, and no condition reaches the "
+              f"large benchmark on the median. "),
+        ("c", f", spatial organisation of the response: the net signed "
+              f"percentage of significantly changed edges for each of the "
+              f"{c['n_pairs']} canonical network pairs (9 networks, within "
+              f"and between), for two of the four conditions x the two "
+              f"contrasts. All four matrices share one colour scale, "
+              f"symmetric about zero at +/-{c['vmax']:.1f}%, and the values "
+              f"shown run from {c['lo']:.1f}% to {c['hi']:.1f}%; the matrices "
+              f"are symmetric by construction. Red is a net increase in "
+              f"connectivity, blue a net decrease. This panel is descriptive "
+              f"and carries no test; the per-pair counts for all four "
+              f"conditions and all three contrasts (540 rows) are tabulated "
+              f"in SuppTable_WB_network_pair_summary_n288.csv. "),
+        ("", f"The direction of the response is also asymmetric between the "
+             f"two contrasts: of the significant edges under "
+             f"AMPA + GABA-A, {min(up2):.1f}-{max(up2):.1f}% increase, "
+             f"against {min(a[f'{k}|AMPA vs baseline']['up'] for k in COND):.1f}"
+             f"-{max(a[f'{k}|AMPA vs baseline']['up'] for k in COND):.1f}% "
+             f"under AMPA alone. The incremental AMPA + GABA-A versus AMPA "
+             f"contrast is not plotted here and is given in "
+             f"SuppTable_WB1_wholebrain_modulation_n288.csv. "),
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
+# pass 1 -- caption height and the content overhang of each row
+_f0, _p0, _ = build(30.0, 30.0)
+_over = K.overhangs(_f0, _p0)
+_runs0 = caption_runs()
+_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
+               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
+plt.close(_f0)
+
+CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
+FIXED = (MT + 2 * LETTER_BAND + XB1 + XB2 + GAP + _over["c"]
+         + max(_over["a"], _over["b"]))
+FREE = PH - MB - CAP_H - FIXED
+PLOT_H1 = min(MAX_H1, FREE * .45)
+x0 = ML + GUT + LAB_C
+SUB_W = (PW - MR - CB_W - CB_GAP - x0 - 3 * SUB_GAP) / 4
+PLOT_H2 = min(FREE - PLOT_H1, SUB_W)        # keep the 9 x 9 cells square
+
+fig, PANELS, BOTTOM = build(PLOT_H1, PLOT_H2)
+K.align_left_ink(fig, PANELS, [["a", "c"]])
+K.place_letters(fig, PANELS, rows=[["a", "b"], ["c"]])
+
+runs = caption_runs()
+if WITH_CAP:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
+        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
+else:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
+
+assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
+print(f"[{STEM}] row1 {PLOT_H1:.1f} mm, matrices {PLOT_H2:.1f} x {SUB_W:.1f} mm "
+      f"(cell {PLOT_H2 / 9:.2f} mm); panels end at {BOTTOM:.1f} mm; caption "
+      f"{n_lines} lines -> {CAP_BOTTOM:.1f} mm of {PH:.0f} mm")
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
+    os.path.join(HERE, "figS_wb_A4_caption_values.csv"), index=False)
+plt.close(fig)
+
