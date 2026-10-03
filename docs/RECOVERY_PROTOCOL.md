# Recovery protocol for the statistical-analysis layer

This note fixes the method used to rebuild the statistics layer of the
reproducibility package, so that every track produced comparable output. It
records what was known before the work started and what each track was
required to do; it is part of the audit trail, not a set of suggestions.

## The situation this protocol addresses

The figure layer of this paper was complete and reproducible: every final
figure has a script, and every script reads its numbers from a data file that
sits next to it in `04_figures/<figure>/…_data/` or `…/data/`.

The layer *below* that was missing. Of the 162 data files under the figure
tree, the figure scripts only ever **read** them; no script in the repository
writes them. The analyses that produced them — the group comparisons, the
paired tests, the permutation nulls, the nested-model increments, the
cross-validation loops — were run interactively in earlier sessions of this
project and never written out as files. The numbers in the manuscript
therefore had a figure script but no visible derivation.

Those interactive cells are preserved verbatim in the platform's execution
log, which is queryable. That log is the source of record for this recovery.
Of the 162 data files, 156 were confirmed to have at least one candidate
producing cell before the tracks were dispatched.

## Where the code comes from

Query the execution log from the `repl` tool:

```python
host.query(
    "SELECT id, frame_id, created_at, conda_env, source "
    "FROM execution_log WHERE source LIKE ? ORDER BY created_at DESC",
    ["%fig4_subject_level_n288.csv%"], scope="global", limit=20)
```

`scope="global"` is required — the relevant sessions span more than one
project scope. `limit` is capped at 1000 per call; paginate with
`LIMIT ? OFFSET ?` when a filename is widely referenced.

A cell **reads** a data file far more often than it **writes** one. Only a
writing cell is a producer, so narrow on the write idiom as well:

```sql
AND (source LIKE '%to_csv%' OR source LIKE '%to_excel%'
     OR source LIKE '%savemat%' OR source LIKE '%np.save%')
```

When several cells wrote the same filename over the session history, the file
on disk is the output of one of them — usually, but not always, the last.
Decide by evidence, not by recency: read the data file that is actually in the
package, and keep the cell whose code produces that file's exact columns, row
count and grouping. If two candidates are indistinguishable on those grounds,
keep the later one and say so in the `notes` column.

## What each track delivers

Three artefacts per data file, plus one table per track.

**1. An organised script** — `03_analysis/<track>/<NN>_<stem>.py`

Runnable, one per data file, carrying a header that states in this order:
what the script computes; its input files; its output file; the statistical
tests it performs, named as the manuscript names them; whether it can be run
on a laptop; and the execution-log cell id it was rebuilt from.

Reorganising means: add that header, make the imports and paths explicit,
drop interactive debris (exploratory prints, abandoned branches, repeated
re-reads). It does **not** mean improving the analysis. Every computation
stays numerically identical — the same test, the same covariates, the same
correction, the same seed. If a recovered cell computed something in a way
you would not have chosen, it stays as it is: this package documents what
produced the submitted numbers, not what an alternative analysis would give.
If one cell produced several data files, split it by output file and let the
shared computation repeat across the scripts rather than refactoring it into
a shared module — each script must stand alone.

Where the original cell did not fix a random seed — permutation nulls,
cross-validation splits, bootstrap resamples — do not add one. Record
`seed: not fixed in the original run` in the header and note in the
verification column that re-running reproduces the statistic only up to Monte
Carlo error.

**2. A verbatim archive** — `recovered/<track>/<stem>__cell_<id8>.py`

The cell source exactly as it ran, with nothing removed and nothing
reformatted. Prepend a comment block giving the cell id, frame id, timestamp,
conda environment and the data file it produced. This is the audit copy: a
reviewer comparing it against the organised script must be able to see that
only presentation changed.

**3. A provenance table** — `docs/provenance_<track>.csv`

One row per data file, with these columns exactly:

```
data_file, producing_cell_id, frame_id, created_at, analysis_script,
recovered_archive, inputs, tests, local_runnable, verification, notes
```

`local_runnable` is `yes`, `no` or `partial`. `verification` is `match`,
`mismatch`, `partial` or `not_run`, and means what it says: `match` is only
for a script you actually re-ran and compared against the file in the
package.

## Verification

Re-run every script whose inputs are present, and compare its output against
the data file already in `04_figures/`: same columns, same row count, and
values equal within `1e-6` relative tolerance for deterministic quantities.
Record the result honestly. A mismatch is a finding, not a failure to hide —
report the column and the magnitude of the discrepancy in `notes`.

Many analyses sit on top of simulation output that is not in this package:
the population-scale digital-twin runs (3 M, 10 M, 100 M and 1 B neurons)
produced intermediate files far too large to ship, and they were generated on
a GPU cluster. A script that needs them is `local_runnable=no`, and the
`notes` column must name the upstream file it needs and the directory it came
from. That is a complete and acceptable answer for those scripts; inventing a
smaller substitute is not.

## Boundaries

- **Copy only.** Nothing outside `reproducibility_package/` is ever modified,
  moved or deleted. The author's working tree is the reference.
- **The figure tree is read-only.** Never write into `04_figures/`. Its data
  files are the reference the verification compares against; a script that
  overwrites one destroys the evidence. Write outputs to a scratch directory
  and compare.
- **Create only** under `03_analysis/`, `recovered/`, `05_tables/` and
  `docs/`.
- **Never invent code.** If no producing cell can be found for a data file,
  write `NOT_FOUND` in `producing_cell_id`, list in `notes` the search terms
  tried, and move on. A missing derivation recorded as missing is useful; a
  plausible reconstruction presented as the original is not.
- **Never fabricate a statistic, a p value or a verification result.**
