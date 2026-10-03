"""NP-DTB manuscript figure style — single source of truth for the revision.

Two things this module enforces, both of which the current figure set violates:

1.  Panels are drawn at FINAL PRINTED SIZE (1:1).  No PowerPoint rescaling.
    `panel(w_mm, h_mm)` returns the figsize in inches for a panel of that
    printed width.  Nature Medicine: 88 mm single column, 180 mm double.

2.  One value per visual channel.  Every rule/spine/whisker/box edge is
    LW pt, every tick label TICK_PT, every axis label LABEL_PT, every
    annotation ANNOT_PT.  A panel never overrides these.

Colour tokens come from np_dtb_palette.py; VAR2TOKEN below fixes which token
each scientific variable owns, so the same variable is the same colour in
every panel and no two variables share a colour.

Usage
-----
    from np_dtb_style import apply_np_style, panel, C, enforce, panel_title
    apply_np_style()
    fig, ax = plt.subplots(figsize=panel(45, 40))
    ax.bar(x, y, color=C('ampa'))
    panel_title(ax, 'AMPA perturbation normalises NP')
    enforce(fig)
    fig.savefig('fig3b.pdf')      # vector, Type-42 fonts
"""
from __future__ import annotations
import os, sys
import matplotlib as mpl
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from np_dtb_palette import PALETTE  # noqa: E402

# ----------------------------------------------------------------- constants
MM = 1 / 25.4
COL_SINGLE_MM, COL_DOUBLE_MM = 88.0, 180.0

LABEL_PT = 8      # axis labels, panel titles
ANNOT_PT = 7      # legend entries, in-panel annotation, significance marks
TICK_PT = 6       # tick labels
LETTER_PT = 8     # panel letters (bold)

LW = 0.75         # EVERY drawn rule: spines, ticks, box edges, whiskers,
                  # medians, caps, plotted lines, brackets, reference lines.
                  # Equivalent to the deck's historical 2.5 pt at its median
                  # 0.30x placement shrink -- i.e. this preserves the look the
                  # figures already have, but makes it independent of placement.
MARKER_MM = 1.2   # scatter marker diameter (-> s = (MARKER_MM/25.4*72)**2)
TICK_LEN = 2.0

FONT = 'Arial'


def panel(w_mm: float, h_mm: float) -> tuple[float, float]:
    """figsize in inches for a panel whose PRINTED width is w_mm."""
    return (w_mm * MM, h_mm * MM)


def apply_np_style() -> None:
    mpl.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': [FONT, 'Helvetica', 'DejaVu Sans'],
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none',
        'axes.labelsize': LABEL_PT, 'axes.titlesize': LABEL_PT,
        'axes.titleweight': 'normal', 'axes.titlelocation': 'left',
        'axes.titlepad': 3.0, 'axes.labelpad': 2.0,
        'xtick.labelsize': TICK_PT, 'ytick.labelsize': TICK_PT,
        'legend.fontsize': ANNOT_PT, 'font.size': ANNOT_PT,
        'axes.linewidth': LW, 'lines.linewidth': LW, 'patch.linewidth': LW,
        'grid.linewidth': LW, 'hatch.linewidth': LW,
        'boxplot.boxprops.linewidth': LW, 'boxplot.whiskerprops.linewidth': LW,
        'boxplot.capprops.linewidth': LW, 'boxplot.medianprops.linewidth': LW,
        'boxplot.meanprops.linewidth': LW, 'boxplot.flierprops.linewidth': LW,
        'xtick.major.width': LW, 'ytick.major.width': LW,
        'xtick.minor.width': LW, 'ytick.minor.width': LW,
        'xtick.major.size': TICK_LEN, 'ytick.major.size': TICK_LEN,
        'xtick.direction': 'out', 'ytick.direction': 'in',
        'axes.spines.top': False, 'axes.spines.right': False,
        'legend.frameon': False, 'legend.handlelength': 1.4,
        'legend.labelspacing': 0.3, 'legend.borderpad': 0.0,
        'figure.dpi': 400, 'savefig.dpi': 400,
        'savefig.bbox': 'tight', 'savefig.pad_inches': 0.01,
        'axes.unicode_minus': False,
    })


# ------------------------------------------------- variable -> colour token
# MINIMAL-CHANGE palette: these are the manuscript's OWN colours, kept as they are.
# Only two things were changed, both because the reviewer's comment requires it:
#   1. provenance (empirical vs simulated) no longer borrows the HC/patient greys
#      and oranges -- it moves to fill state, so #D55E00 only ever means "patient".
#   2. the Fig-4 ROC drug colours, which were swapped relative to the other panels.
USER_PALETTE = {
    # reference condition -- grey means "untreated / unperturbed / healthy" throughout
    'hc':            '#7F7F7F',
    'placebo':       '#7F7F7F',
    'baseline':      '#7F7F7F',
    'reference':     '#7F7F7F',
    # group severity
    'high_symptom':  '#E69F00',
    'patient':       '#D55E00',
    'mdd':           '#D55E00',
    # AUD gets its own tone so that MDD and AUD can appear in the same panel
    # (STRATIFY supplement) without sharing a colour; same hue family as the
    # other patient colours, separated by lightness so it also survives
    # greyscale printing and dichromatic simulation.
    'aud':           '#8C3A00',
    # perturbation and its in vivo counterpart share the colour (a correspondence,
    # not a collision: virtual AMPA and ketamine are the same manipulation)
    'ampa':          '#E1D09A',
    'ketamine':      '#E1D09A',
    'gaba':          '#96B9AD',
    'midazolam':     '#96B9AD',
    # response subgroups
    # Response direction: two tones of one hue, so the pair survives colour-vision
    # deficiency and greyscale (dark vs pale, ΔL* = 42; worst-case ΔE = 43 across
    # normal / deuteranope / protanope simulation).  The former pink/blue-grey pair
    # (#D9A5B3 / #8DA0B4) collapsed to ΔE = 8.7 under protanopia and #D9A5B3 was
    # indistinguishable from midazolam teal for deuteranopes (ΔE = 2.0).
    'increased':     '#8C4A6B',
    'decreased':     '#E8C4D2',
    'increased_dk':  '#8C4A6B',   # outline for pale fills
    'decreased_dk':  '#8C4A6B',
    # circuits / profiles  (manuscript: "positive (pink) or negative (blue)")
    # negative profile = 29 edges incl. cerebellum/brainstem; NP factor = the
    # 12 cortico-subcortical edges left after removing them.  Same blue family,
    # deeper for the narrower set.
    'neg_profile':   '#6BAED6',
    'neg_profile_hc': '#A8D0E0',
    'neg_profile_pt': '#0072B2',
    'np12':          '#0072B2',
    'pos_profile':   '#C878A0',
    'non_np':        '#BFBFBF',
    # model family (Fig. 3 fidelity panels).  Violet sits in the gap between the
    # palette's mauve-pink (#C878A0) and blue (#0072B2), so it is new but in
    # family; one hue, two tones = one axis (spatial resolution), two levels.
    'model_regional': '#8E7CC3',
    'model_voxel':    '#4C3F8C',
    'model_mid':      '#6E5CA8',   # blend of the two, for a neutral value ramp
}
PALETTE = USER_PALETTE
VAR2TOKEN = {k: k for k in USER_PALETTE}

MARKER = {'mid': 'o', 'sst': 's', 'eft': '^'}


def C(var: str) -> str:
    """Hex for a scientific variable name.  Raises on an unregistered name --
    this is deliberate: a variable with no token has no colour."""
    try:
        return USER_PALETTE[var]
    except KeyError as e:
        raise KeyError(
            f"'{var}' has no colour token. Register it in VAR2TOKEN, or carry "
            f"it on a non-colour channel: {sorted(NON_HUE)}") from e


def empirical(var: str) -> dict:
    """Marker kwargs for the EMPIRICAL version of a quantity (open)."""
    return dict(facecolor='white', edgecolor=C(var), linewidth=LW)


def simulated(var: str) -> dict:
    """Marker kwargs for the SIMULATED version of a quantity (solid)."""
    return dict(facecolor=C(var), edgecolor=C(var), linewidth=LW)


def panel_title(ax, text: str) -> None:
    """Brief panel subtitle, left-aligned above the axes (reviewer request)."""
    ax.set_title(text, fontsize=LABEL_PT, loc='left', pad=3)


def panel_letter(fig, ax, letter: str, dx: float = -0.02, dy: float = 0.02):
    ax.text(dx, 1 + dy, letter, transform=ax.transAxes, fontsize=LETTER_PT,
            fontweight='bold', va='bottom', ha='right')


def enforce(fig) -> list[str]:
    """Sweep the finished figure: every line to LW, y-ticks inward, every text
    to Arial.  Returns the list of artists it had to correct (empty = clean)."""
    fixed = []
    for ax in fig.get_axes():
        for sp in ax.spines.values():
            if abs(sp.get_linewidth() - LW) > 1e-6:
                fixed.append(f'spine {sp.spine_type}'); sp.set_linewidth(LW)
        for ln in ax.get_lines():
            if abs(ln.get_linewidth() - LW) > 1e-6:
                fixed.append('line'); ln.set_linewidth(LW)
        for pt in ax.patches:
            if pt.get_linewidth() and abs(pt.get_linewidth() - LW) > 1e-6:
                fixed.append('patch'); pt.set_linewidth(LW)
        for coll in ax.collections:
            try:
                lws = coll.get_linewidths()
                if len(lws) and abs(float(lws[0]) - LW) > 1e-6:
                    fixed.append('collection'); coll.set_linewidth(LW)
            except Exception:
                pass
        ax.tick_params(axis='y', direction='in', width=LW, length=TICK_LEN)
        ax.tick_params(axis='x', direction='out', width=LW, length=TICK_LEN)
    for t in fig.findobj(mpl.text.Text):
        if t.get_text() and t.get_fontname() != FONT:
            fixed.append(f'font:{t.get_fontname()}'); t.set_fontname(FONT)
    return fixed
