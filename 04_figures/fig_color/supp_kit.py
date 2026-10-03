"""Shared drawing helpers for the supplementary figures.

Imported alongside np_dtb_style so every supplementary panel uses the same
grammar as the main figures: box + all individual points, pale fills for pale
colours, point outlines where the fill is light, one panel per file.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats
from PIL import Image
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from np_dtb_style import LW, TICK_PT, ANNOT_PT, enforce
from fig_export import fig_to_pptx

DPI = 400


def lum(c):
    r, g, b = mcolors.to_rgb(c)
    return .2126 * r + .7152 * g + .0722 * b


def fill(c):
    rgb = np.array(mcolors.to_rgb(c))
    return tuple(1 - (.35 if lum(c) > .70 else .45) * (1 - rgb))


def pt_edge(c):
    return tuple(np.array(mcolors.to_rgb(c)) * .55) if lum(c) > .70 else 'none'


def saver(outd, manifest):
    os.makedirs(outd, exist_ok=True)

    def save(fig, stem, w_mm, h_mm, note, pptx=True):
        fig.savefig(f'{outd}/{stem}.png', dpi=DPI, bbox_inches='tight')
        fig.savefig(f'{outd}/{stem}.pdf', bbox_inches='tight')
        if pptx:
            fig_to_pptx(fig, f'{outd}/{stem}.pptx', dpi=DPI)
        px = Image.open(f'{outd}/{stem}.png').size
        manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                             png_px=f'{px[0]}x{px[1]}',
                             dpi=round(px[0] / (w_mm / 25.4)), source=note))
        plt.close(fig)
    return save


def boxes(ax, positions, values, colours, width=.62, jitter=.15, seed=0, s=13.0):
    bp = ax.boxplot(values, positions=positions, widths=width, showfliers=False,
                    patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
    rng = np.random.default_rng(seed)
    for i, v in enumerate(values):
        bp['boxes'][i].set_facecolor(fill(colours[i]))
        bp['boxes'][i].set_edgecolor('black')
        ax.scatter(positions[i] + rng.uniform(-jitter, jitter, len(v)), v, s=s,
                   facecolor=colours[i], edgecolor=pt_edge(colours[i]),
                   linewidth=LW * .55, alpha=.9, zorder=3)
    return bp


def forest(ax, labels, est, lo, hi, colours, xlabel, zero=0.0, s=22.0):
    """Horizontal estimate + 95% CI plot, newest row at the top."""
    yy = np.arange(len(labels))[::-1]
    ax.axvline(zero, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
    for y, e, l, h, c in zip(yy, est, lo, hi, colours):
        ax.plot([l, h], [y, y], color=c, lw=LW * 1.8, solid_capstyle='round', zorder=2)
        ax.scatter([e], [y], s=s, facecolor=c, edgecolor=pt_edge(c),
                   linewidth=LW * .55, zorder=3)
    ax.set_yticks(yy); ax.set_yticklabels(labels, fontsize=TICK_PT)
    ax.set_ylim(-.7, len(labels) - .3)
    ax.set_xlabel(xlabel)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    return yy


def scatter_fit(ax, x, y, col, s=22.0, spearman=False, line=True):
    ax.scatter(x, y, s=s, facecolor=col, edgecolor=pt_edge(col), linewidth=LW * .55,
               alpha=.9, zorder=3)
    if line:
        b = np.polyfit(x, y, 1)
        xx = np.linspace(min(x), max(x), 50)
        ax.plot(xx, np.polyval(b, xx), color='black', lw=LW, zorder=4)
    return stats.spearmanr(x, y) if spearman else stats.pearsonr(x, y)
