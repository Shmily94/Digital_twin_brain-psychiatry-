"""fig3i_assimilated_bold_r.csv | main Fig. 3 (04_figures/fig.3/fig3_main_A4_v2.py)

Recovered statistical-analysis script | reproducibility package | Fig. 3 track.

WHAT THIS SCRIPT COMPUTES
    This code builds a long-format table of BOLD correlation values from a
    wide table T that has one row per subject-task combination and one
    column per assimilation-plus-simulation configuration. It filters to
    rows whose subject id starts with sub-, coerces the relevant
    simulation columns to numeric, and then melts each subject-task row
    into one output row per configuration column, mapping the original
    Chinese column labels to short model codes and attaching metadata
    (family, simulation neuron count, assimilation hyperparameters,
    resolution, and number of repeats averaged) looked up from fixed
    dictionaries keyed on that model code. One row of the output therefore
    represents a single subject, task, and model configuration, with
    bold_r holding that configuration's BOLD correlation value rounded to
    five decimal places and the accompanying columns describing the fixed
    properties of that configuration rather than anything computed per
    row.

INPUT FILES
    /Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/manuscript_numbers_newflow/3m_model_new_run/baseline同化区域BOLD_r总表.xlsx

OUTPUT FILE
    fig3i_assimilated_bold_r.csv
    written to OUT_DIR (default /tmp/recovery_scratch/fig3)
    reference copy in this package: 04_figures/fig.3/fig3_data/fig3i_assimilated_bold_r.csv

STATISTICAL TESTS
    descriptive summary only (no inferential test in the recovered cell)

RUNNABLE ON A LAPTOP
    conditional on the input files above being present on this machine

SEED
    not applicable (deterministic computation)

PROVENANCE
    execution-log cell : 3c7e0c72-9ebb-4721-a3d5-f131cda7ec4f
    frame              : fe47a03f-2d43-4fe0-a1c3-e0544839d822
    ran                : 2026-09-22 17:49:04 UTC
    conda environment  : python
    verbatim archive   : recovered/fig3/fig3i_assimilated_bold_r__cell_3c7e0c72.py
    candidates found   : 1

REORGANISATION APPLIED
    A header was added; the imports, the input paths and the constants the
    interactive cell inherited from earlier cells in its session were made
    explicit; exploratory prints and abandoned branches were dropped; all file
    writes were redirected to OUT_DIR.  No computation, test, covariate,
    correction or seed was changed.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Output redirection.  The reference data file lives under 04_figures/, which
# this package treats as read-only evidence.  Every file write performed below
# is therefore redirected into OUT_DIR under its own basename.  Set the
# RECOVERY_OUT_DIR environment variable to choose a different scratch folder.
# ---------------------------------------------------------------------------
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures")
sys.path.insert(0, "/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/Code/reproducibility_package/04_figures/fig_color")
OUT_DIR = os.environ.get("RECOVERY_OUT_DIR", os.path.join("/tmp", "recovery_scratch", "fig3"))
os.makedirs(OUT_DIR, exist_ok=True)


def _install_write_guard():
    import pandas as _pd

    def _redirect(p):
        if isinstance(p, (str, bytes, os.PathLike)):
            p = os.fspath(p)
            if os.path.abspath(os.path.dirname(p) or ".") != os.path.abspath(OUT_DIR):
                return os.path.join(OUT_DIR, os.path.basename(p))
        return p

    for _cls, _name in ((_pd.DataFrame, "to_csv"), (_pd.Series, "to_csv"),
                        (_pd.DataFrame, "to_excel"), (_pd.Series, "to_excel")):
        _orig = getattr(_cls, _name)

        def _w(self, path_or_buf=None, *a, __o=_orig, **k):
            return __o(self, _redirect(path_or_buf), *a, **k)
        setattr(_cls, _name, _w)
    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib.figure import Figure as _F
        _sf = _F.savefig

        def _sfw(self, fname, *a, **k):
            return _sf(self, _redirect(fname), *a, **k)
        _F.savefig = _sfw
    except Exception:
        pass
    try:
        import scipy.io as _sio
        _sm = _sio.savemat

        def _smw(fn, *a, **k):
            return _sm(_redirect(fn), *a, **k)
        _sio.savemat = _smw
    except Exception:
        pass


_install_write_guard()

import pandas as pd

# ---- inputs and constants recovered from earlier cells of the same session
#      (cells 2303b194, 3d91af14, 5233e78b, b74f5fe0)
B='/Users/yunman/Desktop/submission'
FD3=f'{B}/revision/text/figures/fig.3/fig3_data'
FAMILY={**{k:'regional' for k in ['3m_268','10m_268','10m_1000']},
        **{k:'voxel' for k in ['10m_own','10m','100m','1b']},'SAR':'benchmark','RWW':'benchmark'}
HYP={'3m_268':'3 M','10m_268':'3 M','10m_1000':'10 M / 1000','10m_own':'10 M voxel',
     '10m':'100 M','100m':'100 M','1b':'100 M','SAR':'—','RWW':'—'}
RES={'3m_268':'268 regions','10m_268':'268 regions','10m_1000':'1000 regions',
     '10m_own':'voxel','10m':'voxel','100m':'voxel','1b':'voxel','SAR':'—','RWW':'—'}
SIMN={'3m_268':'3 M','10m_268':'10 M','10m_1000':'10 M','10m_own':'10 M','10m':'10 M',
      '100m':'100 M','1b':'1 B','SAR':'—','RWW':'—'}
XL='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/06_upstream_inputs/model_scale_consistent/manuscript_numbers_newflow/3m_model_new_run/baseline同化区域BOLD_r总表.xlsx'
xf=pd.ExcelFile(XL)
raw=xf.parse('总表', header=None)
hi=raw.index[raw[0].astype(str).str.contains('被试',na=False)][0]
T=raw.iloc[hi+1:].copy()
T.columns=[str(x).replace('\n','') for x in raw.iloc[hi]]
T=T[T['被试'].astype(str).str.startswith('sub-')].reset_index(drop=True)
BCOL=[c for c in T.columns if '模拟' in c]
raw=xf.parse('总表', header=None)
hi=raw.index[raw[0].astype(str).str.contains('被试',na=False)][0]
T=raw.iloc[hi+1:].copy()
T.columns=[str(x).replace('\n','') for x in raw.iloc[hi]]
T=T[T['被试'].astype(str).str.startswith('sub-')].reset_index(drop=True)
BCOL=[c for c in T.columns if '模拟' in c]
T[BCOL]=T[BCOL].apply(pd.to_numeric, errors='coerce')
XLMAP={'3m同化+3m模拟':'3m_268','3m同化+10m268模拟':'10m_268','10m1000同化+模拟':'10m_1000',
       '10m同化+模拟':'10m_own','100m同化+10m模拟':'10m','100m同化+模拟':'100m','100m同化+1b模拟':'1b'}

# ---- computation: recovered from execution-log cell 3c7e0c72
rows=[]
NREP={'3m_268':5,'10m_268':5,'10m_1000':5,'10m':5,'100m':5,'1b':5,'10m_own':1}
for _,r in T.iterrows():
    for c in BCOL:
        k=XLMAP[c]
        rows.append(dict(subject_id=str(r['被试']).replace('sub-','').lstrip('0'), task=r['任务'], model=k,
                         family=FAMILY[k], sim_neurons=SIMN[k], assimilation_hyperparams=HYP[k],
                         resolution=RES[k], n_repeats_averaged=NREP[k], bold_r=round(float(r[c]),5)))
BR=pd.DataFrame(rows)
BR.to_csv(f'{FD3}/fig3i_assimilated_bold_r.csv', index=False)
