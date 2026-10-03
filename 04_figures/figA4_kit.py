"""Shared A4 page kit for the assembled main figures (Fig. 3, Fig. 4, ...).

Holds the three things every assembled figure needs and nothing else:
  * the type scheme  (8 pt ticks / 9 pt annotation / 10 pt axis labels /
    11 pt bold panel letters / 8 pt caption), pushed into rcParams
  * a word-wrapped rich-text caption (bold panel letters inline)
  * the pptx exporter: 400 dpi raster graphics layer, one native PowerPoint
    text box per label, and the caption as ONE editable word-wrapped box.

IMPORTANT: np_dtb_style.apply_np_style() sets rcParam savefig.bbox='tight'.
fig_export.fig_to_pptx() then saves its background layer through that rcParam,
which crops the graphics to the axes box while the text boxes keep full-canvas
coordinates -- that is why every panels/*.pptx in this project has an offset
text layer.  apply_page_style() below resets savefig.bbox to None.
"""
import os
import matplotlib
import matplotlib.pyplot as plt

TICK_PT, ANNOT_PT, LABEL_PT, LETTER_PT, CAP_PT = 8, 9, 10, 11, 8
FONT = "Arial"
PW, PH = 210.0, 297.0          # A4 portrait, mm
ML, MR, MT = 15.0, 15.0, 12.0  # page margins, mm
MM = 1 / 25.4


def apply_page_style():
    """Call AFTER np_dtb_style.apply_np_style()."""
    matplotlib.rcParams.update({
        "savefig.bbox": None,                       # keep the A4 canvas exact
        "axes.labelsize": LABEL_PT, "axes.titlesize": LABEL_PT,
        "xtick.labelsize": TICK_PT, "ytick.labelsize": TICK_PT,
        "legend.fontsize": ANNOT_PT, "font.size": ANNOT_PT,
    })


def page(pw=PW, ph=PH):
    return plt.figure(figsize=(pw * MM, ph * MM))


def axes_mm(fig, x_mm, y_mm, w_mm, h_mm, pw=PW, ph=PH):
    """Axes placed by its top-left corner in page millimetres."""
    return fig.add_axes([x_mm / pw, 1 - (y_mm + h_mm) / ph, w_mm / pw, h_mm / ph])


def letter(fig, x_mm, y_mm, ch, pw=PW, ph=PH):
    """Panel letter, bold, baseline y_mm above the axes top."""
    return fig.text(x_mm / pw, 1 - y_mm / ph, ch, fontsize=LETTER_PT,
                    fontweight="bold", va="bottom", ha="left")


# --------------------------------------------------------------- layout rules
# Frozen internal distribution, shared by every assembled main figure.
# Everything is measured off what is actually drawn, never assumed:
#   * a row's panels are pushed down so their CONTENT tops (axes + ticks +
#     legend + brackets) sit on one line -> the row reads flush,
#   * each bold letter is then seated LETTER_PAD above and LETTER_PADX left of
#     its OWN panel's content -> equal letter-to-plot distance everywhere,
#     never closer to a neighbour than to its own panel.
LETTER_BAND = 6.0      # white band above each row that holds the letters
LETTER_PAD = 0.9       # letter bottom above its own panel's topmost ink
LETTER_PADX = 1.0      # letter right edge left of its own panel's leftmost ink
LETTER_W = LETTER_PT / 72 * 25.4 * .75      # nominal width of one bold letter
GAP = 6.0              # between rows
GAPX = 5.0             # between columns
MB = 4.0               # bottom margin
CAP_GAP = 2.0          # panels -> caption
CAP_LH = 2.95          # caption line height, mm


def _mm(fig, px):
    return px / fig.dpi * 25.4


def content_box(fig, panels, ph=PH):
    """{ch: (content_top_mm, content_left_mm, axes_top_mm)} for each panel.

    `panels` are dicts with keys ch, x (column left bound, mm) and axes (list).
    """
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    h_px = fig.get_size_inches()[1] * fig.dpi
    out = {}
    for p in panels:
        bb = [a.get_tightbbox(rend) for a in p["axes"]]
        out[p["ch"]] = (_mm(fig, h_px - max(b.y1 for b in bb)),
                        _mm(fig, min(b.x0 for b in bb)),
                        _mm(fig, h_px - max(a.get_window_extent().y1
                                            for a in p["axes"])))
    return out


def overhangs(fig, panels):
    """{ch: mm by which the panel's content rises above its own axes top}."""
    return {ch: max(ax_top - top, 0.0)
            for ch, (top, _left, ax_top) in content_box(fig, panels).items()}


def place_letters(fig, panels, pw=PW, ph=PH, rows=None):
    """Seat every panel letter against its own panel's measured content.

    Pass `rows` (a list of letter groups) to level the letters of each row on
    one line -- the row's highest content top.  Do that whenever the row's x
    axes are also meant to line up; leave it None to keep each letter as close
    as possible to its own panel.
    """
    box = content_box(fig, panels)
    line = {}
    for grp in (rows or []):
        chs = [c for c in grp if c in box]
        for c in chs:
            line[c] = min(box[c2][0] for c2 in chs)
    for p in panels:
        top, left, _ = box[p["ch"]]
        top = line.get(p["ch"], top)
        x = max(p.get("x", 0.0), left - LETTER_PADX - LETTER_W)
        p["txt"].set_position((x / pw, 1 - (top - LETTER_PAD) / ph))
    return {ch: v[0] for ch, v in box.items()}


def align_left_ink(fig, panels, columns, pw=PW):
    """Make every panel of a vertical column start its ink on one line, so the
    panel LETTERS line up as well as the frames.  Tick labels differ in width
    between panels; the panel whose label block is widest sets the line and the
    y label of every other panel in the column is moved out to it (a little
    white between a y label and its ticks is invisible, a letter that does not
    line up is not).  Call it before place_letters.  Returns the line per
    column, in mm."""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    by = {p["ch"]: p for p in panels}
    out = {}
    for col in columns:
        axs = [by[ch]["axes"][0] for ch in col if ch in by]
        if not axs:
            continue
        t = min(_mm(fig, a.get_tightbbox(rend).x0) for a in axs)
        for a in axs:
            for _ in range(3):              # the anchor of a rotated label is
                d = _mm(fig, a.get_tightbbox(rend).x0) - t   # not its bbox
                if abs(d) < .03:            # centre, so close the loop on the
                    break                   # measured edge instead
                lab, pos = a.yaxis.label, a.get_position()
                px, py = lab.get_position()          # x in px after the draw
                a.yaxis.set_label_coords(
                    (px - d / 25.4 * fig.dpi - pos.x0 * fig.bbox.width)
                    / (pos.width * fig.bbox.width), py)
                fig.canvas.draw()
        out[tuple(col)] = t
    return out


def legend_above(ax, *args, ncol=2, **kw):
    """Legend in the white band above the axes -- never covered by the data."""
    kw.setdefault("fontsize", ANNOT_PT)
    kw.setdefault("handletextpad", .4)
    kw.setdefault("columnspacing", 1.2)
    return ax.legend(*args, loc="lower center", bbox_to_anchor=(.5, 1.0),
                     ncol=ncol, borderpad=0, frameon=False, **kw)


def _wrap(fig, runs, width_mm, size_pt, renderer):
    """Greedy word wrap over (text, bold) runs -> lines of (word, bold, w_mm)."""
    words = [(w, b) for txt, b in runs for w in txt.split(" ") if w]

    def wpx(s, bold):
        t = fig.text(0, 0, s, fontsize=size_pt,
                     fontweight="bold" if bold else "normal")
        w = t.get_window_extent(renderer=renderer).width
        t.remove()
        return w / fig.dpi * 25.4

    space = wpx(" ", False)
    lines, cur, cw = [], [], 0.0
    for w, bold in words:
        ww = wpx(w, bold)
        if cur and cw + space + ww > width_mm:
            lines.append(cur); cur, cw = [], 0.0
        cur.append((w, bold, ww))
        cw += ww + (space if len(cur) > 1 else 0)
    if cur:
        lines.append(cur)
    return lines, space


def draw_caption(fig, runs, x_mm, top_mm, w_mm, lh=2.95, pw=PW, ph=PH):
    """Draw the caption; returns (text objects, rect_mm, n_lines, bottom_mm)."""
    renderer = fig.canvas.get_renderer()
    lines, space = _wrap(fig, runs, w_mm, CAP_PT, renderer)
    objs = []
    for i, line in enumerate(lines):
        x, y = x_mm, top_mm + i * lh
        for word, bold, ww in line:
            objs.append(fig.text(x / pw, 1 - (y + lh * .78) / ph, word,
                                 fontsize=CAP_PT, va="baseline", ha="left",
                                 fontweight="bold" if bold else "normal"))
            x += ww + space
    bottom = top_mm + len(lines) * lh
    return objs, (x_mm, top_mm - .5, w_mm, bottom - top_mm + 2), len(lines), bottom


def export_pptx(fig, path, caption_objs=(), caption_runs=(), cap_rect=None,
                dpi=400, collect_text_records=None):
    """Raster graphics layer + native text boxes; caption as one editable box."""
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
    from matplotlib import colors as mcolors
    import matplotlib.text as mtext

    caption_objs = set(caption_objs)
    recs = [r for r in collect_text_records(fig) if r["obj"] not in caption_objs]
    fw, fh = [float(v) for v in fig.get_size_inches()]
    fdpi = float(fig.dpi)
    vis = [(t, t.get_visible()) for t in fig.findobj(mtext.Text)]
    for t, _ in vis:
        t.set_visible(False)
    bg = os.path.splitext(path)[0] + "_bg.png"
    fig.savefig(bg, dpi=dpi, bbox_inches=None, facecolor=fig.get_facecolor())
    for t, v in vis:
        t.set_visible(v)

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(fw), Inches(fh)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(bg, 0, 0, width=Inches(fw), height=Inches(fh))
    align = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
    pad = 1.25
    for r in recs:
        w, h = r["w"] * pad / fdpi, r["h"] * pad / fdpi
        left, top = r["cx"] / fdpi - w / 2.0, (fh - r["cy"] / fdpi) - h / 2.0
        box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = align.get(r["ha"], PP_ALIGN.CENTER)
        run = p.add_run()
        run.text = (r["text"].replace("$", "").replace("\\Delta", "Δ")
                    .replace("\\chi", "χ").replace("\\rho", "ρ")
                    .replace("\\", ""))
        f = run.font
        f.name = FONT; f.size = Pt(r["size"])
        f.bold = r["weight"] in ("bold", "semibold", "heavy", "black")
        f.italic = r["style"] in ("italic", "oblique")
        f.color.rgb = RGBColor(*[int(round(255 * c)) for c in mcolors.to_rgb(r["color"])])
        if r["rot"]:
            box.rotation = (-r["rot"]) % 360.0
    if cap_rect is not None:
        x_mm, y_mm, w_mm, h_mm = cap_rect
        box = slide.shapes.add_textbox(Inches(x_mm * MM), Inches(y_mm * MM),
                                       Inches(w_mm * MM), Inches(h_mm * MM))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        for text, bold in caption_runs:
            run = p.add_run()
            run.text = text
            run.font.name = FONT; run.font.size = Pt(CAP_PT); run.font.bold = bold
    prs.save(path)
    os.remove(bg)
    return path
