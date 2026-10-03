"""Vector synapse schematic for Fig. 1d, drawn in the registered manuscript palette.

Replaces the raster cartoon carried over from framework.pptx.  Shows both arms of
the perturbation the manuscript actually applies: AMPA conductance raised first,
then GABA-A raised on top of the AMPA-adjusted model.

Run directly to write fig1_assets/synapse_palette.{pdf,png}; import draw_synapse()
to place the same schematic inside another figure.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, C, LW       # noqa: E402
from supp_kit import fill, pt_edge                   # noqa: E402

INK, SOFT, FAINT = '#1A1A1A', '#4D4D4D', '#8C8C8C'
CELL, MEMB = '#F4F4F4', '#9A9A9A'
import matplotlib.colors as _mc


def dark(c, k=0.55):
    """a readable ink for text and arrows drawn in a palette colour.

    supp_kit.pt_edge() returns the string 'none' for colours darker than the
    luminance cut, which is right for marker edges but silently makes text and
    arrows invisible; this always returns a colour."""
    return tuple(np.array(_mc.to_rgb(c)) * k)


def _bouton(ax, cx, cy, w, h, rot, face, edge):
    """a presynaptic terminal: bell-shaped outline, rotated about (cx, cy)"""
    t = np.linspace(-np.pi / 2, np.pi / 2, 60)
    xs = np.concatenate([-w / 2 * np.ones(2), w / 2 * np.cos(t) * 1.0, -w / 2 * np.ones(2)])
    ys = np.concatenate([[-h / 2], [0.10 * h], h / 2 * np.sin(t) * 0 + 0, [0.10 * h], [-h / 2]])
    # simple bell: neck at the bottom, dome at the top
    th = np.linspace(np.pi, 0, 80)
    dome_x, dome_y = w / 2 * np.cos(th), h * .42 * np.sin(th) + h * .10
    pts = np.array([[-w * .18, -h * .50], [-w * .22, -h * .10], *zip(dome_x, dome_y),
                    [w * .22, -h * .10], [w * .18, -h * .50]])
    R = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
    pts = pts @ R.T + np.array([cx, cy])
    ax.add_patch(Polygon(pts, closed=True, facecolor=face, edgecolor=edge,
                         linewidth=LW * 1.2, zorder=3, joinstyle='round'))
    return pts


def draw_synapse(ax, x0, y0, w, h, fs=5.0, ampa_note='0.0044', gaba_note='0.0040'):
    """draw into an existing axes, inside the rectangle (x0, y0, w, h) of its data space"""
    AMP, GAB = C('ampa'), C('gaba')
    AMPD, GABD = dark(AMP), dark(GAB)
    xc = x0 + w * .46
    # ---- postsynaptic neuron: dendritic shaft with two receptor patches ------
    ax.add_patch(FancyBboxPatch((xc - w * .07, y0 + h * .06), w * .14, h * .56,
                                boxstyle='round,pad=0,rounding_size=0.25',
                                facecolor=CELL, edgecolor=MEMB, linewidth=LW * 1.2, zorder=3))
    ax.text(xc, y0 + h * .015, 'postsynaptic neuron', fontsize=fs * .86, color=SOFT,
            ha='center', va='bottom', zorder=6)
    # ---- excitatory (AMPA) terminal, above -----------------------------------
    _bouton(ax, xc, y0 + h * .80, w * .30, h * .30, 0.0, fill(AMP), AMPD)
    for dx, dy in [(-.055, .80), (.055, .80), (0.0, .87)]:
        ax.add_patch(Circle((xc + w * dx, y0 + h * dy), w * .022, facecolor=AMP,
                            edgecolor=AMPD, linewidth=LW * .7, zorder=5))
    ax.add_patch(FancyArrowPatch((xc, y0 + h * .655), (xc, y0 + h * .585), arrowstyle='-|>',
                                 mutation_scale=5.0, lw=LW * 1.3, color=AMPD, zorder=5))
    ax.add_patch(FancyBboxPatch((xc - w * .055, y0 + h * .545), w * .11, h * .045,
                                boxstyle='round,pad=0,rounding_size=0.12',
                                facecolor=AMP, edgecolor=AMPD, linewidth=LW, zorder=5))
    ax.text(xc + w * .085, y0 + h * .83, 'glutamate', fontsize=fs * .9, color=AMPD,
            ha='left', va='center', zorder=6)
    ax.text(xc + w * .085, y0 + h * .565, 'AMPA receptor', fontsize=fs * .9, color=AMPD,
            ha='left', va='center', zorder=6)
    ax.add_patch(FancyArrowPatch((xc + w * .085, y0 + h * .50), (xc + w * .30, y0 + h * .50),
                                 arrowstyle='-|>', mutation_scale=5.4, lw=LW * 1.5,
                                 color=AMPD, zorder=5))
    ax.text(xc + w * .32, y0 + h * .50, f'excitatory conductance \u2191\n$g_{{\\rm AMPA}}$ = {ampa_note}',
            fontsize=fs * .9, color=AMPD, ha='left', va='center', linespacing=1.35, zorder=6)
    # ---- inhibitory (GABA-A) terminal, from the left -------------------------
    _bouton(ax, x0 + w * .17, y0 + h * .30, w * .24, h * .26, np.pi / 2, fill(GAB), GABD)
    for dx, dy in [(.13, .30), (.17, .345), (.17, .255)]:
        ax.add_patch(Circle((x0 + w * dx, y0 + h * dy), w * .020, facecolor=GAB,
                            edgecolor=GABD, linewidth=LW * .7, zorder=5))
    ax.add_patch(FancyArrowPatch((x0 + w * .28, y0 + h * .30), (xc - w * .085, y0 + h * .30),
                                 arrowstyle='-|>', mutation_scale=5.0, lw=LW * 1.3,
                                 color=GABD, zorder=5))
    ax.add_patch(FancyBboxPatch((xc - w * .085, y0 + h * .275), w * .045, h * .055,
                                boxstyle='round,pad=0,rounding_size=0.10',
                                facecolor=GAB, edgecolor=GABD, linewidth=LW, zorder=5))
    ax.text(x0 + w * .17, y0 + h * .445, 'GABA', fontsize=fs * .9, color=GABD,
            ha='center', va='bottom', zorder=6)
    ax.text(xc + w * .085, y0 + h * .275, 'GABA-A receptor', fontsize=fs * .9, color=GABD,
            ha='left', va='center', zorder=6)
    ax.add_patch(FancyArrowPatch((xc + w * .085, y0 + h * .175), (xc + w * .30, y0 + h * .175),
                                 arrowstyle='-|>', mutation_scale=5.4, lw=LW * 1.5,
                                 color=GABD, zorder=5))
    ax.text(xc + w * .32, y0 + h * .175,
            f'inhibitory conductance \u2191\n$g_{{\\rm GABA}}$-A = {gaba_note}, on raised AMPA',
            fontsize=fs * .9, color=GABD, ha='left', va='center', linespacing=1.35, zorder=6)


if __name__ == '__main__':
    apply_np_style()
    W_MM, H_MM = 56.0, 30.0
    fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
    draw_synapse(ax, 0, 0, 100, 100, fs=5.6)
    out = os.path.join(HERE, 'fig1_assets', 'synapse_palette')
    fig.savefig(out + '.pdf', transparent=True)
    fig.savefig(out + '.png', dpi=900, transparent=True)
    print('wrote', out + '.pdf/.png', f'{W_MM} x {H_MM} mm')
