# Environments

Three separate environments are involved, and only the first is needed to
reproduce the figures and the statistics.

## 1. Analysis and figures — laptop, CPU only

This is the environment that produced every figure and every statistic in the
package. Versions below are the ones the verification runs used.

| package      | version  |
|--------------|----------|
| python       | 3.11.15  |
| numpy        | 2.4.6    |
| scipy        | 1.17.1   |
| pandas       | 2.3.3    |
| matplotlib   | 3.11.1   |
| statsmodels  | 0.14.6   |
| scikit-learn | 1.9.0    |
| Pillow       | 12.3.0   |
| python-pptx  | 1.0.2    |
| openpyxl     | 3.1.5    |
| h5py         | 3.16.0   |

    conda create -n dtb_figures python=3.11
    conda activate dtb_figures
    pip install -r requirements_figures.txt

`python-pptx` is needed because every figure script emits an editable `.pptx`
text layer alongside the `.png` and `.pdf`. `h5py` is needed only by the
scripts that read simulation output.

Check the environment before running anything:

    python 00_environment/check_environment.py

## 2. Digital twin brain simulation — GPU cluster

The DTB itself does not run on a laptop. The population-scale simulations
(3 M to 1 B neurons) were run on a multi-GPU cluster with MPI; a single
build-and-assimilate job for one participant occupies several GPUs for hours,
and the 288-twin population runs were submitted as SLURM arrays. The
environment is specified by

    01_model_dtb/pytorch-1.9_full_env.yml

whose load-bearing components are PyTorch 1.9 with CUDA, `mpi4py`, `cupy` and
`numba`. `01_model_dtb/README_EN.md` is the model's own documentation and
`01_model_dtb/doc/` its Sphinx source.

**Nothing in this package re-runs those simulations.** The simulation output
they produced enters the package only as the summary data files under
`04_figures/`, and the analysis scripts that sit directly on that output are
marked `local_runnable=no` in the provenance tables, each naming the upstream
file it would need. This is the intended boundary: the figures and statistics
are reproducible on a laptop, the simulations are reproducible only on
comparable cluster hardware.

## 3. Benchmark whole-brain models

`02_model_benchmark/` holds the three reference models the DTB is scored
against: SAR, rWW and Hopf. The rWW implementation uses `cubnm`, which needs
its own install and a GPU for the parameter sweeps:

    pip install cubnm

SAR and Hopf run on CPU with numpy and scipy only.

## 4. The originally submitted MATLAB pipeline

`03_analysis/00_upstream_matlab_pipeline/` is MATLAB, not Python: the
connectome-based predictive modelling that defines the negative-psychopathology
profile, the extraction of individual structural and functional inputs for the
model, and the first-level processing of the simulated BOLD. It needs MATLAB
R2019b or later with SPM12 and the Image Processing Toolbox. It is upstream of
everything in this package and is included so the profile definition is
auditable, not because the figure pipeline calls it.
