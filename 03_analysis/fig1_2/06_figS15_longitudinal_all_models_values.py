"""figS15_longitudinal_all_models_values

Computes : Leave-one-out prediction of four-year symptom change under nine model specifications (n = 85).  The CSV is emitted as a side output of the in-package figure script named below; this script re-runs that figure script in a scratch directory and collects the CSV.
Inputs   : 04_figures/_recovered_session_b194cd74/figS15_models_all.py and the data it reads
Output   : figS15_longitudinal_all_models_values.csv
Tests    : ordinary least squares with leave-one-out cross-validation; two-sided Pearson correlation between predicted and observed change; in-sample model F test; permutation null for the leave-one-out r
Local    : yes
Seed     : set inside the in-package figure script; not re-fixed here

Recovered from execution-log cell 307ec9ee-080c-475a-b1af-8ef24fa16465
         frame b194cd74-5255-435a-9c1e-206638f9adae, 2026-09-29 12:48:00 UTC, conda env 'python'
Verbatim archive: recovered/fig1_2/figS15_longitudinal_all_models_values__cell_307ec9ee.py
Reference copy : 04_figures/_recovered_session_b194cd74/figS15_longitudinal_all_models_values.csv  (read-only; never written by this script)
"""

import os
import sys

# ---------------------------------------------------------------- paths
# SUBMISSION_ROOT is the author's working tree; every upstream input below
# lives under it.  Override with the environment variable of the same name.
SUB = os.environ.get("SUBMISSION_ROOT", "/Users/yunman/Desktop/submission")
PKG = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   os.pardir, os.pardir))
FIGT = os.path.join(PKG, "04_figures")          # read-only reference tree
# Outputs are written to OUT_DIR (default: the current directory).  They are
# NEVER written into 04_figures/, whose copies are the verification reference.
OUT = os.environ.get("OUT_DIR", os.getcwd())
os.makedirs(OUT, exist_ok=True)

import shutil
import subprocess
import tempfile

SCRIPT_REL = '_recovered_session_b194cd74/figS15_models_all.py'          # path of the figure script inside 04_figures/
VALUES = 'figS15_longitudinal_all_models_values.csv'              # file name it emits
SCRIPT = os.path.join(FIGT, SCRIPT_REL)
SRCDIR = os.path.dirname(SCRIPT)
SUBDIR = os.path.dirname(SCRIPT_REL)

# copy the figure directory to scratch so 04_figures stays untouched
# The whole figure subdirectory is copied into a scratch tree that MIRRORS the
# layout of 04_figures/, so that the script's own HERE = <figure tree>/<subdir>
# resolves inside the scratch tree once the two absolute path literals it was
# written with are retargeted.  Nothing outside the scratch tree is written.
work = tempfile.mkdtemp(prefix="fig12_")
dest = os.path.join(work, SUBDIR)
shutil.copytree(SRCDIR, dest)
for kit in ("figA4_kit.py", "render_palette_v2.py"):
    p = os.path.join(FIGT, kit)
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(work, kit))
        shutil.copy2(p, os.path.join(dest, kit))

# Retarget the two absolute path literals in the SCRATCH COPY only -- the same
# two literals tools/retarget_paths.py rewrites.  No statistic, no parameter and
# no plotting instruction is touched.
OLD_FIGDIR = "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures"
OLD_SESSION = ("/Users/yunman/.claude-science/orgs/"
               "226b8dbb-95c8-4e4b-90ab-d5a7406d7ce4/workspaces/"
               "b194cd74-5255-435a-9c1e-206638f9adae")
target = os.path.join(dest, os.path.basename(SCRIPT))
_s = open(target).read()
_s = _s.replace(OLD_SESSION, dest).replace(OLD_FIGDIR, work)
assert OLD_FIGDIR not in _s and OLD_SESSION not in _s, \
    "an absolute path outside the scratch tree survived retargeting"
open(target, "w").write(_s)

r = subprocess.run([sys.executable, os.path.basename(SCRIPT)],
                   cwd=dest, capture_output=True, text=True)
sys.stdout.write(r.stdout[-2000:])
sys.stderr.write(r.stderr[-2000:])

produced = None
for root, _d, files in os.walk(work):
    if VALUES in files:
        produced = os.path.join(root, VALUES)
        break
if produced is None:
    raise SystemExit("figure script did not emit %s (exit %d)" % (VALUES, r.returncode))
shutil.copy2(produced, os.path.join(OUT, VALUES))
print("wrote", os.path.join(OUT, VALUES))
