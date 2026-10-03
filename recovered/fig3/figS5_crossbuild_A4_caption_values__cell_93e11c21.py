# ===========================================================================
# VERBATIM ARCHIVE -- execution-log cell source, exactly as it ran.
# Nothing has been removed, added or reformatted below the header.
#
#   cell id       : 93e11c21-bc01-4590-ad89-e15f36d5c2a0
#   frame id      : 8d001885-f89b-4ca4-9e30-9866f1015ee6
#   ran           : 2026-09-24 20:35:33 UTC
#   conda env     : (not recorded)
#   cell kind     : edit_file
#   produced      : 04_figures/supp_crossbuild/figS5_crossbuild_A4_caption_values.csv
# ===========================================================================

# [edit_file] created /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_crossbuild/figS5_crossbuild_A4.py
+++ /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_crossbuild/figS5_crossbuild_A4.py
+"""Supplementary figure: cross-build agreement of the 12-edge NP profile, at
+baseline and after each perturbation.
+
+The three panels are the fig.3 panels fig3c, fig3c_ampa and fig3c_gaba, rebuilt
+from the same matrices under the frozen rules of figA4_kit: 8 / 9 / 10 / 11 pt
+type, no declarative panel titles (their statements move into the caption), one
+shared colour bar, and both variants (with caption and --no-caption).
+
+Data (read in place, not copied, so there is one source of truth):
+    ../fig.3/fig3_data/fig3c_cross_scale_similarity.csv        baseline
+    ../fig.3/fig3_data/fig3c_cross_scale_similarity_ampa.csv   + AMPA
+    ../fig.3/fig3_data/fig3c_cross_scale_similarity_gaba.csv   + AMPA + GABA-A
+
+    python figS5_crossbuild_A4.py [--no-caption]
+"""
+import os, sys, itertools
+import numpy as np
+import pandas as pd
+import matplotlib
+matplotlib.use("Agg")
+import matplotlib.pyplot as plt
+from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
+
+FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
+HERE = os.path.join(FIGDIR, "supp_crossbuild")
+sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
+sys.path.insert(0, FIGDIR)
+from np_dtb_style import apply_np_style, panel, C, LW, enforce
+from fig_export import collect_text_records
+import figA4_kit as K
+from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, CAP_PT, PW, PH, ML, MR, MT
+
+D = os.path.join(FIGDIR, "fig.3", "fig3_data")
+DPI = 400
+WITH_CAP = "--no-caption" not in sys.argv
+STEM = "figS5_crossbuild_A4" if WITH_CAP else "figS5_crossbuild_A4_nocaption"
+SUPP_NO = "S5"
+apply_np_style()
+K.apply_page_style()
+
+MAT = {k: pd.read_csv(os.path.join(D, f), index_col=0) for k, f in
+       [("base", "fig3c_cross_scale_similarity.csv"),
+        ("ampa", "fig3c_cross_scale_similarity_ampa.csv"),
+        ("gaba", "fig3c_cross_scale_similarity_gaba.csv")]}
+NCELL = pd.read_csv(os.path.join(D, "fig3c_cross_scale_n_cells_ampa.csv"),
+                    index_col=0)
+
+CLAB = {"3m_268": "3 M | 268", "10m_268": "10 M | 268",
+        "10m_1000": "10 M | 1000", "10m_own": "10 M | voxel",
+        "10m": "10 M | voxel", "100m": "100 M | voxel", "1b": "1 B | voxel"}
+CHYP = {"3m_268": "3 M", "10m_268": "3 M", "10m_1000": "10 M/1000",
+        "10m_own": "10 M vox", "10m": "100 M", "100m": "100 M", "1b": "100 M"}
+FAMC = {**{k: C("model_reg") for k in ("3m_268", "10m_268", "10m_1000")},
+        **{k: C("model_vox") for k in ("10m_own", "10m", "100m", "1b")}}
+REG = ["3m_268", "10m_268", "10m_1000"]
+VOX = ["10m", "100m", "1b"]
+OWN = "10m_own"
+
+# negatives are real and are the point of the perturbed states, so the scale
+# runs to the global minimum with white AT zero instead of clipping them
+VMIN = np.floor(min(m.values.min() for m in MAT.values()) * 10) / 10
+CMAP = LinearSegmentedColormap.from_list(
+    "fidelity", ["0.55", "#FFFFFF", C("model_mid")])
+NORM = TwoSlopeNorm(vmin=VMIN, vcenter=0.0, vmax=1.0)
+S = {}                                  # every caption number -> CSV
+
+
+def block(m, keys_a, keys_b=None):
+    v = ([m.loc[a, b] for a, b in itertools.combinations(keys_a, 2)]
+         if keys_b is None else [m.loc[a, b] for a in keys_a for b in keys_b])
+    return float(min(v)), float(max(v))
+
+
+for k, m in MAT.items():
+    S[k] = dict(pair_268=float(m.loc["3m_268", "10m_268"]),
+                regional=block(m, REG), vox100=block(m, VOX),
+                reg_vox=block(m, REG, VOX),
+                own=(float(min(m.loc[OWN, c] for c in m.columns if c != OWN)),
+                     float(max(m.loc[OWN, c] for c in m.columns if c != OWN))),
+                gmin=float(m.values.min()))
+S["n_cells"] = int(NCELL.values.min())
+
+
+def heat(ax, key):
+    m = MAT[key]
+    M = m.values.astype(float)
+    n = M.shape[0]
+    im = ax.imshow(M, cmap=CMAP, norm=NORM)
+    for i in range(n):
+        for j in range(n):
+            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
+                    fontsize=TICK_PT,
+                    color="white" if M[i, j] > .62 else "black")
+    labs = [f"{CLAB[c]}\nhyper {CHYP[c]}" for c in m.columns]
+    ax.set_xticks(range(n)); ax.set_yticks(range(n))
+    ax.set_xticklabels(labs, fontsize=TICK_PT, rotation=90)
+    ax.set_yticklabels(labs, fontsize=TICK_PT)
+    for t, c in zip(ax.get_xticklabels(), m.columns):
+        t.set_color(FAMC[c])
+    for t, c in zip(ax.get_yticklabels(), m.columns):
+        t.set_color(FAMC[c])
+    ax.set_xticks(np.arange(-.5, n, 1), minor=True)
+    ax.set_yticks(np.arange(-.5, n, 1), minor=True)
+    ax.grid(which="minor", color="0.40", linewidth=LW)
+    for sp in ax.spines.values():
+        sp.set_visible(True); sp.set_linewidth(LW); sp.set_color("0.40")
+    ax.tick_params(length=0, which="both")
+    return im
+
+
+def p_a(ax):
+    ax._im = heat(ax, "base")
+
+
+def p_b(ax):
+    ax._im = heat(ax, "ampa")
+
+
+def p_c(ax):
+    ax._im = heat(ax, "gaba")
+
+
+# --------------------------------------------------------------- page geometry
+GUT = K.LETTER_W + K.LETTER_PADX
+GAPX, GAP = 8.5, K.GAP
+LETTER_BAND, MB = K.LETTER_BAND, K.MB
+LAB_L = 25.0                       # two-line y labels, horizontal
+XB = 25.0                          # two-line x labels, rotated 90 degrees
+COL_W = (PW - ML - MR - GAPX) / 2
+ROWS = [[("a", p_a), ("b", p_b)], [("c", p_c)]]
+CB_W, CB_H = 52.0, 3.4             # shared colour bar, in the empty 4th slot
+
+
+def build(plot_h):
+    f = plt.figure(figsize=panel(PW, PH))
+    out, y, im = [], MT, None
+    for row in ROWS:
+        top = y + LETTER_BAND
+        for j, (ch, fn) in enumerate(row):
+            slot = ML + j * (COL_W + GAPX)
+            ax = K.axes_mm(f, slot + GUT + LAB_L, top,
+                           COL_W - GUT - LAB_L, plot_h)
+            fn(ax)
+            im = ax._im
+            out.append(dict(ch=ch, x=slot, axes=[ax],
+                            txt=K.letter(f, slot, top - 1.2, ch)))
+        y = top + plot_h + XB + GAP
+    # the shared key sits in the slot panel d would have used
+    cx = ML + COL_W + GAPX + GUT + LAB_L
+    cy = MT + 2 * LETTER_BAND + plot_h + XB + GAP + plot_h * .25
+    cax = K.axes_mm(f, cx, cy, CB_W, CB_H)
+    cb = f.colorbar(im, cax=cax, orientation="horizontal",
+                    ticks=[VMIN, 0, .5, 1])
+    cb.set_label("Spearman $\\rho$ over the 12 subjects x 12 edges\n"
+                 "(144 cells) of the raw NP profile",
+                 fontsize=ANNOT_PT, labelpad=2)
+    cb.ax.tick_params(labelsize=TICK_PT, width=LW, length=1.6)
+    cb.outline.set_linewidth(LW)
+    enforce(f)
+    return f, out, y - GAP
+
+
+# ------------------------------------------------------------------- caption
+CAP_TITLE = (f"Supplementary Fig. {SUPP_NO} | Cross-build agreement of the "
+             "12-edge NP profile follows the assimilated hyperparameters, and "
+             "loosens under perturbation.")
+
+
+def caption_runs():
+    b, a, g = S["base"], S["ampa"], S["gaba"]
+    cap = [
+        ("", f"Each matrix is the agreement between every pair of the seven "
+             f"digital-twin-brain builds in the same quantity: one Spearman "
+             f"rho over all 12 subjects x 12 edges = {S['n_cells']} cells of "
+             f"the raw NP profile, with no per-subject averaging, no Fisher "
+             f"transform and no standardisation. Rows and columns give the "
+             f"build (simulated neurons | parcellation) above the "
+             f"hyperparameter set it was assimilated with; regional builds are "
+             f"printed in light purple and voxel builds in dark purple. The "
+             f"colour bar is shared by the three panels and is white at zero, "
+             f"so the negative entries that appear after perturbation are grey "
+             f"rather than clipped; the matrices are symmetric and the "
+             f"diagonal is 1 by construction. Rank correlation is used because "
+             f"the builds have very different tail behaviour: the 10 M voxel "
+             f"build assimilated with its own hyperparameters has excess "
+             f"kurtosis 10.6, and its Pearson agreement with the 100 M "
+             f"hyperparameter voxel builds falls from 0.21 to -0.04 when the "
+             f"five most extreme of the 144 cells are dropped, whereas "
+             f"Spearman moves only from 0.07 to -0.02; over the 21 "
+             f"off-diagonal pairs the two metrics rank almost identically "
+             f"(rho = 0.96, largest shift 0.14) and the Pearson matrix is "
+             f"kept in fig3c_cross_scale_similarity_pearson.csv. "
+             f"Repeat-averaged profiles are used wherever repeats exist (the "
+             f"3 M, 10 M | 268 and archive voxel builds, five runs each); the "
+             f"10 M voxel own-hyperparameter build is a single run. "),
+        ("a", f", baseline. Agreement tracks the hyperparameter set, not the "
+              f"model scale: the two builds that share the 3 M hyperparameters "
+              f"agree at rho = {b['pair_268']:.2f} although one is a 3 M and "
+              f"the other a 10 M model, and the three voxel builds that share "
+              f"the 100 M hyperparameters agree at "
+              f"{b['vox100'][0]:.2f}-{b['vox100'][1]:.2f}, while agreement "
+              f"across the two families is only "
+              f"{b['reg_vox'][0]:.2f}-{b['reg_vox'][1]:.2f}. The 10 M voxel "
+              f"build assimilated with its own hyperparameters agrees with no "
+              f"other build ({b['own'][0]:+.2f} to {b['own'][1]:+.2f}). "),
+        ("b", f", after the AMPA perturbation. The regional block tightens "
+              f"({a['regional'][0]:.2f}-{a['regional'][1]:.2f} against "
+              f"{b['regional'][0]:.2f}-{b['regional'][1]:.2f} at baseline) "
+              f"while the voxel block loosens "
+              f"({a['vox100'][0]:.2f}-{a['vox100'][1]:.2f} against "
+              f"{b['vox100'][0]:.2f}-{b['vox100'][1]:.2f}), and the first "
+              f"negative entries appear (minimum {a['gmin']:+.2f}). "),
+        ("c", f", after AMPA plus GABA-A. The two 268-region builds become "
+              f"nearly interchangeable (rho = {g['pair_268']:.2f}), the voxel "
+              f"block stays together "
+              f"({g['vox100'][0]:.2f}-{g['vox100'][1]:.2f}) but its agreement "
+              f"with the regional builds drops to "
+              f"{g['reg_vox'][0]:.2f}-{g['reg_vox'][1]:.2f}, and the "
+              f"own-hyperparameter build turns negative against every voxel "
+              f"build ({g['own'][0]:+.2f} to {g['own'][1]:+.2f}). All entries "
+              f"in b and c use the full {S['n_cells']} cells; the counts are "
+              f"tabulated in fig3c_cross_scale_n_cells_ampa.csv and "
+              f"fig3c_cross_scale_n_cells_gaba.csv. "),
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
+# pass 1 -- caption height at a provisional panel height
+_f0, _p0, _ = build(60.0)
+_runs0 = caption_runs()
+_l0 = (K._wrap(_f0, _runs0, PW - ML - MR, CAP_PT,
+               _f0.canvas.get_renderer())[0] if WITH_CAP else [])
+plt.close(_f0)
+
+CAP_H = (K.CAP_GAP + len(_l0) * K.CAP_LH + 1.0) if WITH_CAP else 0.0
+NROW = len(ROWS)
+FIXED = MT + NROW * (LETTER_BAND + XB) + (NROW - 1) * GAP
+PLOT_H = min((PH - MB - CAP_H - FIXED) / NROW, COL_W - GUT - LAB_L)
+fig, PANELS, BOTTOM = build(PLOT_H)
+K.align_left_ink(fig, PANELS, [["a", "c"]])
+K.place_letters(fig, PANELS, rows=[[ch for ch, _ in row] for row in ROWS])
+
+runs = caption_runs()
+if WITH_CAP:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
+        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
+else:
+    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
+
+assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"
+print(f"[{STEM}] cell {PLOT_H / 7:.2f} mm; panels end at {BOTTOM:.1f} mm; "
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
+    os.path.join(HERE, "figS5_crossbuild_A4_caption_values.csv"), index=False)
+plt.close(fig)
+