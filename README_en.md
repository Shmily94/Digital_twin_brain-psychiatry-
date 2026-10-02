# Reproducibility package

Every figure and every statistic in the paper, traced from the submitted
deliverable back to the code that produced it.

The reference is the submitted material, not any intermediate draft:

| submitted file | contents |
|---|---|
| `290926NatMed_Manuscript_FINAL.docx` | main text, with Fig. 1–5 embedded |
| `290926Supplementary_Information_FINAL.docx` | Supplementary Information, Fig. S1–S14 |
| `ExtendedData/Extended_Data_Fig_1–9` | Extended Data figures |
| `290926Suppl.Table_FINAL.xlsx` | Supplementary Tables S1–S24 |

Copies are in `04_figures/_final_deliverables/` and serve as the reference of
record: every comparison in this package is made against them.

## Two invariants

1. **Everything here is a copy.** Building this package modified, moved and
   deleted nothing in the author's working tree. `MANIFEST.csv` records the
   source path, size and SHA256 of all 1,190 files so the claim is checkable.
   One breach occurred during verification and was repaired;
   `VERIFICATION_REPORT.md` section 5 documents it in full.
2. **`04_figures/` is read-only.** Its data files are the reference that
   verification compares against. Scripts that re-run write to a scratch
   directory.

## Layout

```
reproducibility_package/
├── README_en.md / README_zh.md
├── PROVENANCE.csv              274-row chain: figure -> data file -> cell -> script
├── MANIFEST.csv                every file, with source path and SHA256
├── VERIFICATION_REPORT.md      what was re-run and what reproduced
├── OPEN_QUESTIONS.md           15 items needing an author decision
├── 00_environment/             three environments, pinned versions, self-check
├── 01_model_dtb/               digital-twin-brain engine (code only)
├── 02_model_benchmark/         SAR, rWW, Hopf reference models (code)
├── 03_analysis/                the statistical layer (recovered, see below)
│   ├── 00_upstream_matlab_pipeline/   CPM profile definition, model inputs
│   └── fig1_2/ fig3/ fig4/ fig5/      228 organised scripts
├── 04_figures/                 figure scripts, figure data, final renders
│   ├── fig.1 … fig.5, supp_*/         mirrors the author's figure tree
│   ├── Model_Benchmark/               benchmark FITTING RESULTS (data, not code)
│   ├── _recovered_session_b194cd74/   5 final scripts recovered from a session
│   └── _final_deliverables/           submitted files, reference of record
├── 05_tables/                  supplementary-table builders
├── 06_upstream_inputs/         out-of-tree inputs the figure scripts read
├── recovered/                  verbatim cell archive (audit copy)
├── docs/                       recovery protocol, per-track provenance
└── tools/retarget_paths.py     rewrites the compiled-in absolute paths
```

## Running it

### Step 1 — check the environment

```bash
python 00_environment/check_environment.py
```

Python 3.11 with numpy, scipy, pandas, matplotlib, statsmodels, scikit-learn,
Pillow, python-pptx and openpyxl. Pinned versions in
`00_environment/requirements_figures.txt`.

### Step 2 — retarget the absolute paths

Every figure script was written with the author's absolute paths compiled in:

```python
FIGDIR = "<author figure tree>"
```

The scripts here are byte-identical copies of the ones that produced the
submitted figures, so those constants still point at the author's machine.

```bash
python tools/retarget_paths.py            # dry run, reports what would change
python tools/retarget_paths.py --apply    # rewrite (347 scripts), idempotent
python tools/retarget_paths.py --restore   # undo, from the .orig backups
```

The tool rewrites **only path literals** — never a statistic, a parameter or a
plotting instruction — and backs up each file once as `.orig` before its first
rewrite, so the byte-identical state is always recoverable.

**This step is not optional.** Without it the scripts write to the paths
compiled into them, which is how the one copy-only breach happened.

### Step 3 — reproduce a figure

```bash
cd 04_figures/fig.4
python fig4_main_A4.py                 # -> png, pdf, and an editable pptx
python fig4_main_A4.py --no-caption
```

Each script also writes `*_caption_values.csv`, the machine-readable form of
every statistic quoted in its legend. Check legend numbers against that file
rather than by eye.

Extended Data deliverables take one further step, a downscale of the A4 render
to 1270 px width:

```python
from PIL import Image
im = Image.open('figS_wbdrug_A4_nocaption.png')
im.resize((1270, int(1270 * im.size[1] / im.size[0])), Image.LANCZOS).save(
    'ExtendedData/Extended_Data_Fig_5.png')
```

## The figure layer

`docs/FIG_SCRIPT_MAP_final.csv` maps each of the 28 submitted figures to its
script. The mapping was established by hashing and pixel comparison against the
submitted files, not by filename inference; the evidence is in the
`identification_evidence` column.

Three things a reader needs to know:

**Five final scripts are not in the author's figure tree.** They were recovered
from the working directory of the last analysis session and are in
`04_figures/_recovered_session_b194cd74/`:

| script | produced |
|---|---|
| `fig5_main_A4_np12_adj.py` | Fig. 5 |
| `figS15_models_all_v4.py` | Extended Data Fig. 6 |
| `ed5_wbdrug.py` | Extended Data Fig. 5 |
| `ed7_finger.py` | Extended Data Fig. 7 |
| `figS1_stratify_k2.py` | Supplementary Fig. S1 |

A package built from the figure tree alone cannot reproduce those five figures.

**Fig. 1 and Fig. 2 are assembled in PowerPoint** from script-generated panels
(`fig.1/fig1_v4.py`, `fig.2/fig2.py` → `panels/`). The panels are reproducible;
the whole-page composite has no single command.

**Supplementary Fig. S4 is a schematic** with no data and no statistics.

## The statistical layer

This is the part that did not exist before.

Of the 162 data files under the figure tree, the figure scripts only ever
**read** them; no script in the repository writes them. The analyses that
produced them — group comparisons, paired tests, permutation nulls,
nested-model increments, cross-validation — were run interactively and were
never written out as files. The manuscript's numbers had a figure script but no
visible derivation.

Those cells are preserved verbatim in the platform execution log. 247 of 274
data files and workbook sheets were traced to the cell that produced them and
rebuilt as standalone scripts. The method is fixed in
`docs/RECOVERY_PROTOCOL.md`, which is binding rather than advisory: how the log
is queried, how a producer is distinguished from a reader, how competing
candidates are decided on evidence rather than recency, and what each file must
deliver.

Each traced file yields three artefacts:

1. `03_analysis/<track>/<NN>_<stem>.py` — organised and runnable, with a header
   naming the computation, inputs, output, statistical tests, local runnability
   and the source cell id.
2. `recovered/<track>/<stem>__cell_<id>.py` — the cell exactly as it ran, so a
   reviewer can confirm that only presentation changed.
3. a row in `docs/provenance_<track>.csv`.

**Reorganising did not change any analysis.** Same test, same covariates, same
correction, same seed. Where the original run fixed no seed, none was added: the
header says so and the verification column states that re-running reproduces the
statistic only up to Monte Carlo error. Of the Fig. 5 scripts, 34 had a seed in
the original run (seed 0 for the Fig. 5h increment nulls at 5,000 permutations,
1 for the increment nulls, 101 for the nine covariate-adjusted specifications,
7 for the sign-flip nulls, 2 for the fingerprint nulls) and reproduce their
permutation statistics exactly.

### What reproduces

| verification | n |
|---|---|
| re-ran, output equals the packaged file | 176 |
| inputs absent from the package | 74 |
| partially reproduced | 14 |
| re-ran, output differs | 10 |

The 74 unreproducible rows sit on population-scale simulation output (3 M to
1 B neurons, GPU cluster) that is far too large to ship; each names the upstream
file it needs. That is the intended boundary of this package: **figures and
statistics reproduce on a laptop, simulations require comparable cluster
hardware.**

The 10 mismatches are findings about the submitted material rather than defects
of the recovery — four Fig. 3 tables were edited in place after generation, and
the Extended Data Fig. 2 Oldham tables are stale with respect to an input that
was later rewritten. All ten are itemised in `VERIFICATION_REPORT.md` section 4
and the consequential ones in `OPEN_QUESTIONS.md`.

### End-to-end result

Re-run inside the package from packaged data:

- **Fig. 3, Fig. 4, Fig. 5: SHA256 identical** to the figures embedded in the
  submitted manuscript.
- **All nine Extended Data A4 renders: SHA256 identical** to the author's
  renders. Three of the nine final 1270 px files match byte for byte; the other
  six differ only in the resampling step (RMS 3.5–4.2 of 255), with identical
  source renders and therefore identical plotted values.

## Before submitting

Read `OPEN_QUESTIONS.md`. Items 1–4 affect numbers in the submitted material:
a stale input behind two Extended Data Fig. 2 values, a supplementary table
whose numbers disagree with the analysis, a legend that understates a
sparse-cell count, and a table that cannot be rebuilt in one command.
