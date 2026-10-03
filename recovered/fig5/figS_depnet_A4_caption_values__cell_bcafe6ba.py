# Verbatim execution-log cell archive - do not edit.
# data file     : 04_figures/supp_depnet/figS_depnet_A4_caption_values.csv
# cell id       : bcafe6ba-dcec-4f23-b21b-028ca9ddc191
# frame id      : 8d001885-f89b-4ca4-9e30-9866f1015ee6
# cell_index    : 539
# executed at   : 2026-09-24 22:22 UTC
# language      : bash
# organised as  : 03_analysis/fig5/49_figS_depnet_A4_caption_values.py
# This data file is a render-time by-product of 04_figures/supp_depnet/figS_depnet_A4.py.
# The cell below is the execution-log cell that produced the packaged copy
# (it runs, or last edits and runs, that figure script). The derivation itself
# is the figure script, which is already in the package.
# ---------------------------------------------------------------------------
cd /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/supp_depnet && python3 - <<'PY'
from pptx import Presentation
from pptx.util import Emu
for f in ("figS_depnet_A4.pptx","figS_depnet_A4_nocaption.pptx"):
    p=Presentation(f); sz=set(); n=0
    for sh in p.slides[0].shapes:
        if sh.has_text_frame:
            n+=1
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.size: sz.add(r.font.size.pt)
    print(f,"%.1f x %.1f"%(Emu(p.slide_width).mm,Emu(p.slide_height).mm),"| boxes",n,"| pt",sorted(sz))
PY
cp figS_depnet_A4.png figS_depnet_A4.pdf figS_depnet_A4.pptx figS_depnet_A4_nocaption.png figS_depnet_A4_nocaption.pdf figS_depnet_A4_nocaption.pptx figS_depnet_A4.py figS_depnet_A4_caption_values.csv "$OLDPWD"/ && echo staged