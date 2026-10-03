"""Re-render selected figures with the deepened perturbation colours, as *_v2
files, WITHOUT touching the shared palette or the existing outputs.

The four tokens that move are the two perturbations and their in vivo
counterparts, which the palette deliberately pairs by colour:

    ampa / ketamine   #E1D09A -> #ECCB61      (saturation x1.45, lightness x0.88)
    gaba / midazolam  #96B9AD -> #80B4A2      (saturation x1.30, lightness x0.92)

For each target the script (1) patches np_dtb_style.USER_PALETTE in this
process and runs the figure script, (2) renames whatever that script just
wrote to <stem>_v2.<ext>, and (3) re-runs the script in a CLEAN subprocess so
the original files are restored byte-for-byte.

    python render_palette_v2.py
"""
import os, runpy, shutil, subprocess, sys

FIGDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(FIGDIR, "fig_color"))
sys.path.insert(0, FIGDIR)
import np_dtb_style as style

NEW = {"ampa": "#ECCB61", "ketamine": "#ECCB61",
       "gaba": "#80B4A2", "midazolam": "#80B4A2"}
EXT = (".png", ".pdf", ".pptx")

# (directory, script, stems it writes)
TARGETS = [
    ("fig.4", "fig4_main_A4.py", ["fig4_main_A4", "fig4_main_A4_nocaption"]),
    ("fig.5", "fig5_main_A4.py", ["fig5_main_A4", "fig5_main_A4_nocaption"]),
    ("supp_sensitivity", "figS_sensitivity_A4.py",
     ["figS_sensitivity_A4", "figS_sensitivity_A4_nocaption"]),
    ("supp_midpaired", "figS_midpaired_A4.py",
     ["figS_midpaired_A4", "figS_midpaired_A4_nocaption"]),
]


def run(here, script, argv):
    cwd = os.getcwd()
    os.chdir(here)
    old_argv = sys.argv[:]
    sys.argv = [script] + argv
    try:
        runpy.run_path(os.path.join(here, script), run_name="__main__")
    finally:
        sys.argv = old_argv
        os.chdir(cwd)


def main():
    style.USER_PALETTE.update(NEW)          # patched for this process only
    made = []
    for sub, script, stems in TARGETS:
        here = os.path.join(FIGDIR, sub)
        for argv in ([], ["--no-caption"]):
            run(here, script, argv)
        for stem in stems:                  # keep the v2 render
            for ext in EXT:
                src = os.path.join(here, stem + ext)
                if os.path.exists(src):
                    dst = os.path.join(here, stem + "_v2" + ext)
                    shutil.move(src, dst)
                    made.append(os.path.relpath(dst, FIGDIR))
        for argv in ([], ["--no-caption"]):  # restore the originals
            subprocess.run([sys.executable, script] + argv, cwd=here,
                           check=True, stdout=subprocess.DEVNULL)
    print("\n".join(made))
    print(f"{len(made)} v2 files written; originals re-rendered unpatched")


if __name__ == "__main__":
    main()
