"""Supplementary figure | two-dimensional AMPA / GABA-A parameter sweep (A4 page).

Source data: data/coherence_results_tau_gamma.csv -- one simulation per cell of a
g_AMPA (10 levels, 0.0004-0.0040) x g_GABA-A (8 levels, 0.0005-0.0040) grid,
I_ext = 0, 80 cells.  Columns: Mean_firing_rate, Mean_Coherence and the coherence
of each of 217 regions.  The file carries NO BOLD-stability variable, so BOLD
stability is not plotted here.

The three operating points come from the Methods (not from this file): baseline
g_AMPA = 0.0008 / g_GABA-A = 0.0015; AMPA endpoint 0.0044 at baseline inhibition;
GABA-A endpoint 0.0040 with AMPA held at 0.0044.  g_AMPA = 0.0044-0.0052 was
explored in the four-participant 100-million-neuron calibration but is not in this
grid file, so those columns are drawn blank and hatched.

Regimes are read off the empirical gaps, not hand-thresholded: coherence is
bimodal (46 cells at 0.063-0.065, 34 cells at 0.34-0.76, none between) and the
floor cells split by rate with the same clean separation (38 cells <= 3.4 Hz,
8 cells >= 69.7 Hz, every synchronised cell between 5.3 and 39.9 Hz).

    cd revision/text/figures/supp_paramspace && python figS_paramspace_A4.py [--no-caption]
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle, Patch

FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
HERE = os.path.join(FIGDIR, "supp_paramspace")
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
from np_dtb_style import apply_np_style, C, LW, enforce            # noqa: E402
from supp_kit import fill, pt_edge                                 # noqa: E402
from fig_export import collect_text_records                        # noqa: E402
import figA4_kit as K                                              # noqa: E402
from figA4_kit import TICK_PT, ANNOT_PT, LABEL_PT, PW, PH, ML, MR, MT  # noqa: E402

DPI = 400
WITH_CAP = "--no-caption" not in sys.argv
STEM = "figS_paramspace_A4" if WITH_CAP else "figS_paramspace_A4_nocaption"
apply_np_style()
K.apply_page_style()
S = {}                                    # every number quoted in the caption


def dark(c, k=0.55):
    """Darken a hex colour for text and arrow ink (pt_edge returns 'none' for
    dark fills, which silently renders text invisible)."""
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02X%02X%02X" % (int(r * k), int(g * k), int(b * k))


d = pd.read_csv(os.path.join(HERE, "data", "coherence_results_tau_gamma.csv"))
FRp = d.pivot(index="GABA", columns="AMPA", values="Mean_firing_rate")
COp = d.pivot(index="GABA", columns="AMPA", values="Mean_Coherence")
GABA = FRp.index.values
AGRID = FRp.columns.values                       # 0.0004 .. 0.0040
AEXT = np.round(np.arange(AGRID[0], 0.00521, 0.0004), 6)   # .. 0.0052 for the marks
NSWEPT = len(AGRID)
S["n_cells"] = FRp.size
S["ampa_grid"] = f"{AGRID[0]:.4f}-{AGRID[-1]:.4f}"
S["gaba_grid"] = f"{GABA[0]:.4f}-{GABA[-1]:.4f}"

FR = np.full((len(GABA), len(AEXT)), np.nan); FR[:, :NSWEPT] = FRp.values
CO = np.full((len(GABA), len(AEXT)), np.nan); CO[:, :NSWEPT] = COp.values

# ---- regimes ---------------------------------------------------------------
SYNC_CUT, RATE_CUT = 0.20, 50.0          # both sit inside an empty interval
assert not ((COp.values > 0.08) & (COp.values < 0.30)).any()
REG = np.where(np.isnan(CO), 3,
               np.where(CO >= SYNC_CUT, 1, np.where(FR >= RATE_CUT, 2, 0)))
assert not ((REG == 0) & (FR > 4)).any()
assert not ((REG == 1) & ((FR < 5) | (FR > 40))).any()
for k, key in enumerate(["n_async", "n_sync", "n_excess"]):
    S[key] = int((REG == k).sum())
S["fr_range"] = f"{np.nanmin(FR):.2f}-{np.nanmax(FR):.2f}"
S["co_floor"] = f"{COp.values[COp.values < .08].min():.4f}-{COp.values[COp.values < .08].max():.4f}"
S["co_sync"] = f"{COp.values[COp.values >= .3].min():.3f}-{COp.values[COp.values >= .3].max():.3f}"
S["fr_async_max"] = f"{FR[REG == 0].max():.2f}"
S["fr_excess_min"] = f"{FR[REG == 2].min():.2f}"
S["fr_sync_range"] = f"{FR[REG == 1].min():.2f}-{FR[REG == 1].max():.2f}"

# ---- operating points (Methods values) -------------------------------------
BASE = (0.0008, 0.0015)
END_A = (0.0044, 0.0015)
END_G = (0.0044, 0.0040)
SWEEP_A0 = 0.0020                          # AMPA sweep started here
ib = (int(np.where(np.isclose(GABA, BASE[1]))[0][0]),
      int(np.where(np.isclose(AEXT, BASE[0]))[0][0]))
S["baseline_fr"] = f"{FR[ib]:.2f}"
S["baseline_co"] = f"{CO[ib]:.4f}"
S["baseline"] = f"g_AMPA = {BASE[0]:.4f}, g_GABA-A = {BASE[1]:.4f}"
CA, CG, CREF = C("ampa"), C("gaba"), C("baseline")
SCALE = 1e4


def xi(g_ampa):
    return float(np.where(np.isclose(AEXT, g_ampa))[0][0])


def yi(g_gaba):
    return float(np.where(np.isclose(GABA, g_gaba))[0][0])


# ---- page ------------------------------------------------------------------
fig = K.page()
AXW, AXH, CBW = 63.0, 43.0, 3.2
COL_X = (ML + 9.0, ML + 9.0 + 88.0)
ROW1_TOP, ROW2_TOP = MT + K.LETTER_BAND, MT + K.LETTER_BAND + AXH + 22.0 + K.LETTER_BAND


def heat(x_mm, y_mm, M, cmap, norm, title, cb_label, cb_ticks=None, w=AXW, h=AXH):
    ax = K.axes_mm(fig, x_mm, y_mm, w, h)
    cmap = plt.get_cmap(cmap).copy() if isinstance(cmap, str) else cmap
    cmap.set_bad("white")
    im = ax.imshow(np.ma.masked_invalid(M), origin="lower", aspect="auto",
                   cmap=cmap, norm=norm, interpolation="nearest")
    for j in range(NSWEPT, len(AEXT)):          # columns absent from this grid
        for i in range(len(GABA)):
            ax.add_patch(Rectangle((j - .5, i - .5), 1, 1, facecolor="white",
                                   edgecolor="0.62", linewidth=0, hatch="//",
                                   zorder=2))
    ax.set_xticks(range(len(AEXT)))
    ax.set_xticklabels([f"{v * SCALE:.0f}" for v in AEXT], fontsize=TICK_PT)
    ax.set_yticks(range(len(GABA)))
    ax.set_yticklabels([f"{v * SCALE:.0f}" for v in GABA], fontsize=TICK_PT)
    ax.set_xlabel("$g_{\\rm AMPA}$ ($10^{-4}$ S cm$^{-2}$)", fontsize=LABEL_PT)
    ax.set_ylabel("$g_{\\rm GABA}$-A ($10^{-4}$ S cm$^{-2}$)", fontsize=LABEL_PT)
    ax.set_title(title, fontsize=LABEL_PT, loc="left", pad=3)
    ax.tick_params(length=1.8, width=LW)
    for s in ax.spines.values():
        s.set_linewidth(LW)
    if cb_label is not None:
        cax = K.axes_mm(fig, x_mm + w + 2.0, y_mm, CBW, h)
        cb = fig.colorbar(im, cax=cax, ticks=cb_ticks)
        cb.set_label(cb_label, fontsize=LABEL_PT)
        cb.ax.tick_params(labelsize=TICK_PT, length=1.6, width=LW)
        cb.outline.set_linewidth(LW)
    return ax


def marks(ax, paths=True, labels=True):
    """Baseline point, the two perturbation endpoints and the protocol path."""
    if paths:
        ax.annotate("", xy=(xi(SWEEP_A0), yi(BASE[1])), xytext=(xi(BASE[0]), yi(BASE[1])),
                    arrowprops=dict(arrowstyle="-", lw=LW, color="0.35",
                                    linestyle=(0, (1.6, 1.6))), zorder=5)
        ax.annotate("", xy=(xi(END_A[0]), yi(END_A[1])), xytext=(xi(SWEEP_A0), yi(BASE[1])),
                    arrowprops=dict(arrowstyle="-|>", lw=LW * 1.5, color=dark(CA),
                                    mutation_scale=7), zorder=5)
        ax.annotate("", xy=(xi(END_G[0]), yi(END_G[1])), xytext=(xi(END_A[0]), yi(END_A[1])),
                    arrowprops=dict(arrowstyle="-|>", lw=LW * 1.5, color=dark(CG),
                                    mutation_scale=7), zorder=5)
    ax.plot(xi(BASE[0]), yi(BASE[1]), "o", ms=4.6, mfc="white", mec="black",
            mew=LW * 1.3, zorder=6)
    ax.plot(xi(END_A[0]), yi(END_A[1]), "s", ms=4.6, mfc=CA, mec=dark(CA),
            mew=LW * 1.3, zorder=6)
    ax.plot(xi(END_G[0]), yi(END_G[1]), "s", ms=4.6, mfc=CG, mec=dark(CG),
            mew=LW * 1.3, zorder=6)
    if labels:
        BB = dict(facecolor="white", edgecolor="none", pad=0.8)
        ax.text(xi(BASE[0]) - .2, yi(BASE[1]) + .60, "baseline", fontsize=ANNOT_PT,
                ha="left", va="bottom", color="black", zorder=6, bbox=BB)
        ax.text(xi(END_A[0]) + .60, yi(END_A[1]), "AMPA\n0.0044", fontsize=ANNOT_PT,
                ha="left", va="center", color=dark(CA), zorder=6, bbox=BB)
        ax.text(xi(END_G[0]) + .60, yi(END_G[1]), "GABA-A\n0.0040", fontsize=ANNOT_PT,
                ha="left", va="center", color=dark(CG), zorder=6, bbox=BB)
        ax.set_xlim(-.5, len(AEXT) + 3.6)


# a  mean firing rate
ax_a = heat(COL_X[0], ROW1_TOP, FR, "Greys",
            LogNorm(vmin=np.nanmin(FR), vmax=np.nanmax(FR)),
            "Mean firing rate", "Firing rate (Hz)", cb_ticks=[1, 3, 10, 30, 100])
marks(ax_a, labels=False)
# b  mean coherence
ax_b = heat(COL_X[1], ROW1_TOP, CO, "Greys", None, "Mean coherence", "Coherence")
marks(ax_b, labels=False)
# c  regime map
GREY = ["#E2E2E2", "#8C8C8C", "#F4F4F4", "white"]
ax_c = heat(COL_X[0], ROW2_TOP, REG, ListedColormap(GREY),
            BoundaryNorm([-.5, .5, 1.5, 2.5, 3.5], 4), "Dynamical regime", None)
for j in range(NSWEPT):
    for i in range(len(GABA)):
        if REG[i, j] == 2:
            ax_c.add_patch(Rectangle((j - .5, i - .5), 1, 1, facecolor="none",
                                     edgecolor="0.45", linewidth=0, hatch="\\\\\\\\",
                                     zorder=3))
marks(ax_c)
ax_c.legend(handles=[
    Patch(facecolor=GREY[0], edgecolor="0.6", lw=LW, label="Asynchronous, resting-like"),
    Patch(facecolor=GREY[1], edgecolor="0.6", lw=LW, label="Synchronised"),
    Patch(facecolor=GREY[2], edgecolor="0.45", lw=LW, hatch="\\\\\\\\",
          label="Excessive firing"),
    Patch(facecolor="white", edgecolor="0.62", lw=LW, hatch="//",
          label="Not in this grid")],
    fontsize=ANNOT_PT, frameon=False, loc="upper left", bbox_to_anchor=(-.13, -.30),
    ncol=2, handlelength=1.5, handleheight=1.0, labelspacing=.4, columnspacing=1.2)

# d  regional coherence along the AMPA axis at baseline inhibition
RCOLS = [c for c in d.columns if c.startswith("Region_")]
S["n_regions"] = len(RCOLS)
row = d[np.isclose(d.GABA, BASE[1])].sort_values("AMPA")
vals = [row[row.AMPA == a][RCOLS].values.ravel() for a in AGRID]
ax_d = K.axes_mm(fig, COL_X[1], ROW2_TOP, AXW, AXH)
bp = ax_d.boxplot(vals, positions=range(NSWEPT), widths=.62, patch_artist=True,
                  showfliers=False, whis=1.5)
for el in ("boxes", "whiskers", "caps", "medians"):
    for art in bp[el]:
        art.set_linewidth(LW); art.set_color("black")
rng = np.random.default_rng(0)
for i, (a, v) in enumerate(zip(AGRID, vals)):
    sync = COp.values[int(np.where(np.isclose(GABA, BASE[1]))[0][0]),
                      int(np.where(np.isclose(AGRID, a))[0][0])] >= SYNC_CUT
    bp["boxes"][i].set_facecolor(fill(CA) if sync else "#EDEDED")
    bp["boxes"][i].set_edgecolor("black")
    ax_d.scatter(i + rng.uniform(-.17, .17, len(v)), v, s=1.0, facecolor="0.45",
                 edgecolor="none", alpha=.35, zorder=3)
ax_d.axvline(xi(SWEEP_A0) - .5, color="0.5", lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax_d.text(xi(SWEEP_A0) - .70, ax_d.get_ylim()[1] * .99, "transition to\nsynchrony",
          fontsize=ANNOT_PT, ha="right", va="top", color="0.35",
          bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
ax_d.set_xticks(range(NSWEPT))
ax_d.set_xticklabels([f"{v * SCALE:.0f}" for v in AGRID], fontsize=TICK_PT)
ax_d.set_xlabel("$g_{\\rm AMPA}$ ($10^{-4}$ S cm$^{-2}$)", fontsize=LABEL_PT)
ax_d.set_ylabel("Regional coherence", fontsize=LABEL_PT)
ax_d.set_title(f"Across regions at $g_{{\\rm GABA}}$-A = {BASE[1]:.4f}",
               fontsize=LABEL_PT, loc="left", pad=3)
ax_d.tick_params(length=1.8, width=LW)
for s in ax_d.spines.values():
    s.set_linewidth(LW)
S["d_iqr_async"] = "%.4f" % np.median([np.subtract(*np.percentile(v, [75, 25]))
                                       for a, v in zip(AGRID, vals) if a < SWEEP_A0])
S["d_iqr_sync"] = "%.3f" % np.median([np.subtract(*np.percentile(v, [75, 25]))
                                      for a, v in zip(AGRID, vals) if a >= SWEEP_A0])

PANELS = [dict(ch="a", x=COL_X[0] - 6.0, axes=[ax_a], txt=K.letter(fig, COL_X[0] - 6.0, ROW1_TOP, "a")),
          dict(ch="b", x=COL_X[1] - 6.0, axes=[ax_b], txt=K.letter(fig, COL_X[1] - 6.0, ROW1_TOP, "b")),
          dict(ch="c", x=COL_X[0] - 6.0, axes=[ax_c], txt=K.letter(fig, COL_X[0] - 6.0, ROW2_TOP, "c")),
          dict(ch="d", x=COL_X[1] - 6.0, axes=[ax_d], txt=K.letter(fig, COL_X[1] - 6.0, ROW2_TOP, "d"))]
enforce(fig)
BOTTOM = ROW2_TOP + AXH + 22.0


def caption_runs():
    def R(s, bold=False):
        return [(w, bold) for w in s.split(" ")]
    r = []
    r += R("Supplementary Fig. S18 |", True)
    r += R("Two-dimensional AMPA/GABA-A conductance sweep used to place the baseline "
           f"and the perturbation endpoints. Each cell is one simulation of the digital "
           f"twin brain at a fixed pair of global conductances (n = {S['n_cells']} "
           f"simulations; unit of observation, one conductance pair; g_AMPA "
           f"{S['ampa_grid']} S cm-2 in steps of 0.0004 and g_GABA-A {S['gaba_grid']} "
           "S cm-2 in steps of 0.0005, external input 0). One run per cell, so no error "
           "indicator and no statistical test is shown; all four panels are descriptive "
           "maps of the model's dynamical regimes. Columns hatched in white were not "
           "simulated in this grid and are shown only so that the conductance settings "
           "used in the main analyses can be marked in place. ")
    r += R(" a,", True)
    r += R(f"Mean population firing rate (logarithmic colour scale, {S['fr_range']} Hz). ")
    r += R(" b,", True)
    r += R("Mean coherence across regions, which separates asynchronous from "
           "synchronised activity. ")
    r += R(" c,", True)
    r += R("Regime classification. Coherence is bimodal across the grid - "
           f"{S['n_async'] + S['n_excess']} cells lie at the {S['co_floor']} floor and "
           f"{S['n_sync']} cells at {S['co_sync']}, with no cell in between - and the "
           f"floor cells separate by rate just as cleanly, so the boundaries are read "
           f"off these gaps rather than set by hand: asynchronous (up to "
           f"{S['fr_async_max']} Hz, {S['n_async']} cells), synchronised "
           f"({S['fr_sync_range']} Hz, {S['n_sync']} cells) and excessive firing (from "
           f"{S['fr_excess_min']} Hz, {S['n_excess']} cells), the last excluded from use. "
           f"The open circle marks the baseline ({S['baseline']} S cm-2; "
           f"{S['baseline_fr']} Hz, coherence {S['baseline_co']}), chosen in the "
           "low-firing, low-coherence resting-like regime; the arrows trace the protocol "
           "actually used, AMPA raised first to 0.0044 S cm-2 (gold square) and GABA-A "
           "then raised to 0.0040 S cm-2 on top of it (teal square), each value having "
           "been selected as the one producing the largest increase in the summed NP "
           "factor over the calibrated range (Methods). ")
    r += R(" d,", True)
    r += R(f"Coherence of each of the {S['n_regions']} regions along the AMPA axis at "
           f"the baseline inhibition level (g_GABA-A = {BASE[1]:.4f} S cm-2), the line "
           f"along which AMPA was swept: boxes show the median and interquartile range "
           f"across regions with whiskers at 1.5x IQR and every region plotted "
           f"(n = {S['n_regions']} regions per box; unit of observation, one region). "
           "Regions move into synchrony together rather than one at a time, and the "
           "spread across regions widens once the network synchronises (median "
           f"interquartile range {S['d_iqr_async']} below the transition versus "
           f"{S['d_iqr_sync']} above it); gold fill marks the synchronised settings. "
           "Descriptive; no test.")
    return r


runs = caption_runs()
if WITH_CAP:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = K.draw_caption(
        fig, runs, ML, BOTTOM + K.CAP_GAP, PW - ML - MR)
else:
    cap_objs, cap_rect, n_lines, CAP_BOTTOM = [], None, 0, BOTTOM
assert CAP_BOTTOM <= PH - 0.5, f"content overruns A4: {CAP_BOTTOM:.1f} mm"

png, pdf, ppt = (os.path.join(HERE, STEM + e) for e in (".png", ".pdf", ".pptx"))
fig.savefig(png, dpi=DPI, bbox_inches=None, facecolor="white")
fig.savefig(pdf, bbox_inches=None, facecolor="white")
K.export_pptx(fig, ppt, cap_objs, runs, cap_rect, dpi=DPI,
              collect_text_records=collect_text_records)
pd.DataFrame([{"key": k, "value": str(v)} for k, v in S.items()]).to_csv(
    os.path.join(HERE, "figS_paramspace_caption_values.csv"), index=False)
# tidy source tables, one per panel
FRp.to_csv(os.path.join(HERE, "data", "paramspace_mean_firing_rate.csv"))
COp.to_csv(os.path.join(HERE, "data", "paramspace_mean_coherence.csv"))
pd.DataFrame(REG[:, :NSWEPT], index=GABA, columns=AGRID).to_csv(
    os.path.join(HERE, "data", "paramspace_regime.csv"))
pd.DataFrame({f"{a * SCALE:.0f}": v for a, v in zip(AGRID, vals)}).to_csv(
    os.path.join(HERE, "data", "paramspace_regional_coherence_ampa_axis.csv"), index=False)
bad = [t.get_text() for t in fig.findobj(matplotlib.text.Text)
       if t.get_text().strip() and t.get_fontname() != "Arial"]
print(f"[{STEM}] panels end at {BOTTOM:.1f} mm, caption {n_lines} lines -> "
      f"{CAP_BOTTOM:.1f} of {PH:.0f} mm | non-Arial: {bad[:3]}")
print(f"regimes async/sync/excess = {S['n_async']}/{S['n_sync']}/{S['n_excess']}; "
      f"baseline cell {S['baseline_fr']} Hz, coherence {S['baseline_co']}")
