#!/usr/bin/env python3
"""figS_longitudinal_model_scatters_values.csv

Computes
    Panel values of the four-model leave-one-out scatter figure (model, n, LOO
    r, parametric and permutation P), emitted by the figure script at render
    time.

Inputs
    - 04_figures/_recovered_session_b194cd74/np_beha_85subjects_all_quantities.csv

Output
    04_figures/_recovered_session_b194cd74/figS_longitudinal_model_scatters_values.csv

Statistical tests
    recomputed by the producing script while rendering:
      - Pearson correlation
      - ordinary least squares GLM with covariates
      - leave-one-out cross-validation

Local runnability
    yes (local_runnable = yes).  Verification: match.
    4 rows x 6 cols identical (max rel dev 0.00e+00)
Producing script (already in the package)
    04_figures/_recovered_session_b194cd74/figS_long_models.py

Recovered from
    execution-log cell 33c224e5-71e5-4e81-9d7b-af28875477be
    frame b194cd74-5255-435a-9c1e-206638f9adae, cell_index 549, 2026-09-29 11:20 UTC
    - the run of that figure script from which the packaged copy of this table
      came.

Random seed
    not applicable - the producing script recomputes caption values deterministically
    from the packaged data tables

Notes
    This table is a render-time by-product: no separate statistical cell ever
    produced it.  Re-running it means re-running the figure script, which is what
    this wrapper does - into a scratch mirror, so that nothing under 04_figures
    is touched.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", ".."))
FIGROOT = os.path.join(PKG, "04_figures")
OUT_DIR = os.environ.get("RECOVERY_OUT_DIR", os.path.join(HERE, "_scratch"))

FIGDIR = '_recovered_session_b194cd74'          # directory of the producing script, relative to 04_figures
SCRIPT = '_recovered_session_b194cd74/figS_long_models.py'          # the producing script itself, relative to 04_figures
TARGET = 'figS_longitudinal_model_scatters_values.csv'          # the data file this script is here to reproduce

MIRROR = os.path.join(OUT_DIR, "figmirror")
SUPPORT = ["fig_color", "figA4_kit.py", "render_palette_v2.py"]


def mirror():
    """copy the producing figure directory and its shared support modules into
    OUT_DIR, so the figure script runs against a writable copy"""
    os.makedirs(MIRROR, exist_ok=True)
    for name in SUPPORT:
        src = os.path.join(FIGROOT, name)
        dst = os.path.join(MIRROR, name)
        if not os.path.exists(src) or os.path.exists(dst):
            continue
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    src = os.path.join(FIGROOT, FIGDIR)
    dst = os.path.join(MIRROR, FIGDIR)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return dst


AUTHOR_FIGROOT = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"


def neutralise_absolute_paths(root):
    """Several A4 assembly scripts hard-code the author's figure tree as an
    absolute constant (FIGDIR = "<author tree>") and write their renders there
    rather than next to themselves.  The figure tree of this package is
    read-only and the author's working tree must not be touched, so in the
    scratch mirror that constant is repointed at the mirror.  This changes no
    computation: only where the outputs land."""
    for base, _dirs, files in os.walk(root):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(base, name)
            try:
                src = open(path, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            if AUTHOR_FIGROOT not in src:
                continue
            open(path, "w", encoding="utf-8").write(src.replace(AUTHOR_FIGROOT, root))


def main():
    figdir = mirror()
    neutralise_absolute_paths(MIRROR)
    script = os.path.join(MIRROR, SCRIPT)
    proc = subprocess.run([sys.executable, os.path.basename(script)],
                          cwd=os.path.dirname(script), capture_output=True, text=True)
    sys.stdout.write(proc.stdout[-4000:])
    sys.stderr.write(proc.stderr[-4000:])
    produced = None
    for root, _dirs, files in os.walk(figdir):
        if TARGET in files:
            produced = os.path.join(root, TARGET)
            break
    if produced is None:
        raise SystemExit("figure script did not write %s (exit %d)" % (TARGET, proc.returncode))
    final = os.path.join(OUT_DIR, TARGET)
    shutil.copy2(produced, final)
    print("wrote", final)


if __name__ == "__main__":
    main()
