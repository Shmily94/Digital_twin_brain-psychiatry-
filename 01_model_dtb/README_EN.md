# Digital Twin Brain (DTB) Client Workflow

[简体中文](README.md) | English

> [!IMPORTANT]
> This workspace is a **snapshot of DTB client code, cluster job scripts, and preprocessed data for 12 participants**. It is not a complete DTB distribution. It contains neither the raw SC/GMV/fMRI inputs nor the DTB model Server, its binary, or its complete runtime. It also contains no generated network blocks, data-assimilation outputs, or simulation results.

This project organizes a four-stage workflow:

1. place data under `data/` and preprocess it;
2. generate networks from `test/` or `regional_model/`;
3. run data assimilation from `data_assimilation/`;
4. run simulation or parameter/region manipulation from `test/` or `regional_model/`.

Stages 3 and 4 require a separately deployed DTB Server. The Python code in this workspace is only the client interface used to call that Server.

## Project Boundary

### Included

- Python/MATLAB code for preprocessing, network generation, data assimilation, simulation, and analysis;
- Slurm, MPI, and batch scripts written for the original cluster;
- `pytorch-1.9_full_env.yml`, a snapshot of the original client-side Python environment;
- 12 preprocessed `*_voxel_data_cleaned.mat` files in MATLAB v7.3/HDF5 format;
- the Shen268 atlas, voxel-label NIfTI files, and region metadata.

### Not included

- raw structural connectivity (SC/DTI), gray-matter volume (GMV), or fMRI data;
- the private `cuda_release` Python client package and non-public `cuda_release_xia` release tree;
- the `dist_simulator` Server binary or its complete source;
- the Server-side HPC-X, ROCm/DTK, and gRPC/protobuf C++ runtime libraries;
- generated `block_*.npz` files or formal assimilation, simulation, analysis, or figure outputs;
- run logs, random-seed records, and result manifests sufficient to demonstrate an end-to-end successful run.

A related public implementation is available at [DTB-consortium/Digital_twin_brain-open](https://github.com/DTB-consortium/Digital_twin_brain-open). It is not directly interchangeable with the non-public `cuda_release_xia` implementation historically used by this project. The public Server must not be treated as a drop-in backend for the clients in this workspace without a compatibility port and validation.

> [!NOTE]
> Names such as `cuda_release` and `CUDA_PATH` are historical project names. The environment snapshot and cluster scripts actually refer to AMD ROCm/HIP, DCU devices, and `torch.version.hip`. A directory name alone is not evidence of an NVIDIA CUDA runtime.

## Model Design and Scientific Positioning

DTB integrates individual anatomy, neuronal dynamics, and functional imaging into a multi-population spiking neural network for individualized BOLD/functional-connectivity simulation and post-fitting virtual synaptic-gain perturbation.

### Individualized network construction

The full framework maps individual anatomy and functional imaging to a multi-population spiking neural network.

| Layer | Design |
|---|---|
| Individual anatomy | Individual diffusion MRI is processed with iFOD2 probabilistic tractography and ACT. Tracking is performed in native diffusion space before fibers are mapped to a common space. |
| Nodes and scale | Gray-matter volume determines neuron allocation across voxels/regions; row-normalized structural connectivity determines inter-node coupling. |
| Neuronal populations | Each voxel/region contains excitatory and inhibitory populations with a fixed `4:1` neuron-count ratio and leaky integrate-and-fire (LIF) dynamics. |
| Synaptic architecture | The simplified ratio of internal excitatory, internal inhibitory, and external excitatory synapses is `4:1:2`; long-range structural connections are excitatory. |
| Neurovascular coupling | Population activity is converted into BOLD through a Balloon–Windkessel hemodynamic model. |

The neuronal model contains AMPA, NMDA, GABA-A, and GABA-B synaptic channels and uses Ornstein–Uhlenbeck background input. Virtual perturbations focus on AMPA and GABA-A gain. The fixed E:I ratio, homogeneous local architecture, and uniform GMV-to-neuron allocation rule are computational approximations rather than complete representations of regional, laminar, cellular, or glial heterogeneity.

### HMDA and task-state forward simulation

Individual fitting uses Hierarchical Mesoscale Data Assimilation (HMDA). A diffusion ensemble Kalman filter (EnKF) iteratively updates parameters from the mismatch between simulated and empirical BOLD. The method uses 30 parallel realizations; the runtime ensemble count is configurable and must match the Server worker topology.

The scientific sequence is:

```text
individual anatomy and BOLD
            │
            ▼
network construction → rest/task HMDA → frozen fitted model
                                              │
                                              ▼
                                forward simulation or virtual
                                synaptic-gain perturbation
                                (no re-assimilation or refitting)
```

Empirical BOLD in task-engaged regions serves as the assimilation anchor and is used to estimate task-specific digital external input currents. Non-assimilated regions are forward-propagated through the individual structural connectome. In the NP-network example, 5 of 19 involved regions are directly assimilated and the remaining 14 are used for forward-propagation evaluation.

### Multi-scale implementations and their roles

Different resolutions serve different analytical goals and are not numerically or biologically equivalent models.

| Model family | Primary use | Interpretation boundary |
|---|---|---|
| 1B voxel-wise DTB | Individual high-resolution simulation and high-fidelity reference. | Its computational cost is high, and results from a small individual set cannot alone support group inference. |
| 100M voxel-wise DTB | Individual AMPA/GABA-A parameter sweeps. | It reduces computational cost, but individual effect sizes require separate comparison with the 1B model. |
| 10M voxel-wise DTB | Lower-cost cross-scale simulation. | Individual dynamics and perturbation responses require separate validation. |
| 10M, 1,000-region coarse model | Comparison of spatial granularity and neuron scale. | It must not be assumed equivalent to a voxel-wise model with the same neuron count. |
| 3M, Shen268 regional DTB | Computationally feasible cohort-level statistics. | Group-level effect direction may be more stable than effect size, individual perturbation pattern, or responder rank; these cannot be transferred directly from the high-resolution model. |

Voxel-wise and regional paths are different model families. Record their neuron count, spatial granularity, parameter settings, and validation results separately.

### Virtual AMPA/GABA-A perturbations

After fitting, whole-brain AMPA/GABA-A synaptic-gain control variables can be swept to examine how microscopic gain changes relate to macroscopic BOLD and functional-connectivity responses. Candidate operating points are screened using firing rate, synchrony/coherence, and the dynamic range of simulated BOLD. Regimes with excessive firing, excessive synchronization, silence, or nonphysiological BOLD plateaus should be excluded.

These operations are **virtual whole-brain synaptic-gain perturbations**. They are biologically informed phenomenological controls, not direct proxies for receptor concentration, local dynamic E/I balance, drug dose, or the molecular action of ketamine or midazolam. A code path named `manipulation` is not evidence of a clinical intervention or causal identification.

The stacked protocol does not sweep the two gains independently from the same baseline. The GABA-A sweep is added at a selected AMPA-adjusted working point and should therefore be labeled `AMPA+GABA-A`. Incremental AMPA and GABA-A effects must be compared against their correct operating points.

## Research Applications and Evidence Boundaries

### Application workflow

Research applications include:

1. derive a continuous, transdiagnostic neuropsychopathology (NP) factor in IMAGEN (`n=1,050`) and validate it in an independent clinical cohort;
2. perform individualized virtual perturbation analysis around an NP example circuit composed of 12 cortico-subcortical edges;
3. build high-resolution voxel-wise DTBs for a small representative set and coarse regional DTBs for a larger cohort;
4. compare model perturbation responses with observations from a healthy-male crossover pharmacological-fMRI sample (`n=27`) and a clinical pharmacological sample (full sample `n=41`; principal paired analysis MDD `n=22`, HC `n=14`);
5. explore a prospective observational association between a model-derived restoration index and later symptom trajectories in a longitudinal subset (`n=85`).

### Supported and unsupported interpretations

This project positions the DTB as a **perturbation-capable computational research platform** for individualized BOLD/FC forward simulation, virtual perturbation analysis of predefined circuits, and model-derived response-correspondence studies.

This positioning does not include claims that:

- causal mechanisms linking AMPA/GABA-A changes to clinical phenotypes have been identified;
- AMPA/GABA-A controls map directly to a drug, dose, or individual receptor state;
- independent individual treatment-response prediction, treatment selection, or personalized neuromodulation targeting has been achieved;
- the NP factor is a disease-specific diagnostic tool or validated treatment target;
- population PET receptor maps validate individual synaptic mechanisms;
- the 3M regional DTB is equivalent to the 1B voxel-wise DTB in effect size or individual ranking;
- the system is ready for clinical deployment or clinical decision support.

Pharmacological comparisons should be described as associations or out-of-sample correspondence between modeled and observed responses. The longitudinal restoration index is a preliminary observational association. A baseline-to-change mapping that is a deterministic function of baseline does not demonstrate independent predictive information beyond baseline. GABAergic correspondence in a healthy sample cannot be generalized as pharmacological validation in AUD.

## Workflow Overview

```text
raw SC / GMV / fMRI (not provided)
              │
              ▼
1. data/: MATLAB preprocessing and voxel cleaning
              │
              ▼
   *_voxel_data_cleaned.mat (provided)
              │
              ▼
2. test/ or regional_model/: generation
              │
              ├── module/<dtype>/block_*.npz
              └── supplementary_info/*
                              │
                 external DTB Server loads blocks
                              │
              ┌───────────────┴────────────────┐
              ▼                                ▼
3. data_assimilation/                  4. simulation/manipulation
   estimate rest/task parameters          forward reproduction, validation,
                                          or virtual perturbation
              │                                │
              └───────────────┬────────────────┘
                              ▼
                   BOLD / firing rate / parameters
```

## Repository Layout

| Path | Purpose |
|---|---|
| `data/` | Cleaned participant data, Shen268 atlas, and MATLAB preprocessing scripts |
| `generation/` | Low-level connectivity generation, partitioning, reading, and checking |
| `test/` | Whole-brain/multi-block generation, simulation, validation, and manipulation entry points |
| `regional_model/` | Regional models, batch MID/SST simulations, and a private-Server launch template |
| `data_assimilation/` | Rest/task assimilation code and Slurm examples |
| `simulation/` | Base client wrapper around the external DTB Server |
| `models/` | Reference Python neuronal and BOLD models |
| `analysis/`, `drawing/` | Power-spectrum, spike-statistics, and plotting utilities |
| `doc/` | Early Sphinx documentation |
| `pytorch-1.9_full_env.yml` | Historical Linux/ROCm client environment snapshot |

## Data

### Data currently provided

`data/` contains cleaned data for 12 participants. These are preprocessed products, not raw data.

| Participant ID | Final voxel count | MID / rest / SST time points |
|---|---:|---:|
| `000000112288` | 12,358 | 191 / 187 / 349 |
| `000016275727` | 11,766 | 191 / 187 / 349 |
| `000044576096` | 10,370 | 191 / 164 / 350 |
| `000063218063` | 10,362 | 191 / 164 / 349 |
| `000067342911` | 12,398 | 191 / 164 / 350 |
| `000067844279` | 11,484 | 191 / 164 / 349 |
| `000111086310` | 10,639 | 191 / 164 / 349 |
| `000112517217` | 10,612 | 191 / 164 / 349 |
| `000113174215` | 13,040 | 191 / 164 / 349 |
| `000168370463` | 10,809 | 191 / 164 / 349 |
| `000182136619` | 12,873 | 191 / 164 / 350 |
| `000191996808` | 12,980 | 191 / 164 / 349 |

Across all files, 139,691 of 176,232 pre-cleaning voxels were retained (approximately 79.27%). Two participants have 187 rest-BOLD time points and the others have 164, so cross-participant code must not assume identical temporal dimensions.

Principal fields in each cleaned MAT file are:

| Field | Meaning |
|---|---|
| `dti_net_full` | Voxel-to-voxel structural-connectivity matrix with shape `N × N` |
| `grey_matter_size` | Gray-matter weight for each voxel |
| `rest_state_bold` | Resting-state BOLD |
| `MID_task_bold`, `SST_task_bold` | Task-state BOLD |
| `atlas_region` | Shen268 region assigned to each voxel |
| `uni_region`, `is_cortex` | Region identifiers and cortical flags |
| `voxel_label` | Voxel label in the original mask |
| `valid_*`, `removed_*`, `filter_info` | Index lineage and cleaning records |

The workspace audit confirmed that index/atlas lineage can be reconstructed. Numerical checks of the large DTI/BOLD arrays were sampled, not exhaustive validation of every matrix element.

### Layout required for generation

`test/normal_generation.py` requires `--block_dir` to identify a **single-participant directory** containing exactly one top-level `.mat` file. The current `data/` directory is flat and contains 12 MAT files, so it must not be passed directly. If multiple MAT files are present, the script warns and uses the first filesystem result, which is not a deterministic participant selection rule.

A suitable generation layout is:

```text
data/
└── <cohort>/
    └── sub-<subject_id>/
        └── sub-<subject_id>_voxel_data_cleaned.mat
```

Files may be copied or linked, but preserve source hashes and ensure that each participant directory has exactly one candidate MAT file.

This differs from the raw-preprocessing scan rule. `data/ordinary_generetion.m` scans only top-level `sub-*` entries under its `project_dir`, normally `data/sub-<subject_id>/`; it does not recursively discover `data/<cohort>/sub-*`. If a cohort layer is used, explicitly change `project_dir` or the scan logic. Preprocessing and generation must not be assumed to discover the same directory layout automatically.

## Environment

### Client-side Python environment

`pytorch-1.9_full_env.yml` records an old Linux/ROCm cluster environment.

| Software | Version |
|---|---|
| Python | 3.7.7 |
| PyTorch | `1.9.0+rocm4.0.1` |
| NumPy / SciPy | 1.19.2 / 1.7.3 |
| h5py / sparse | 3.3.0 / 0.12.0 |
| mpi4py | 3.0.3 |
| grpcio / grpcio-tools | 1.25.0 |
| protobuf | 3.8.0 |
| numba / pandas | 0.56.4 / 1.3.0 |

On a compatible Linux/ROCm cluster, first create a local copy with the historical `prefix:` removed, then try:

```bash
sed '/^prefix:/d' pytorch-1.9_full_env.yml > pytorch-1.9_full_env.portable.yml
conda env create -n pytorch-1.9 -f pytorch-1.9_full_env.portable.yml
conda activate pytorch-1.9
```

This is not guaranteed to succeed on a modern system. The original YAML contains an account-specific absolute prefix, Linux builds, an old ROCm wheel, a custom torchvision build, and historical channels that may no longer serve identical packages. It also contains some `nvidia-cu11` packages; those do not change the fact that the recorded PyTorch build is a ROCm build.

Prefer a cluster environment already validated by its administrator. If rebuilding, use archived wheels or the original cluster cache that match the target ROCm/DTK version.

### MPI, ROCm, and Server runtime

The Conda environment covers only the Python client. A complete run also needs:

- MPI/HPC-X ABI-compatible with `mpi4py`;
- ROCm/DTK compatible with the devices and PyTorch build;
- the private `cuda_release.python.dist_blockwrapper_pytorch` package;
- the Server-side `dist_simulator` and matching launcher;
- matching gRPC/protobuf C++ shared libraries on the Server;
- a model-block directory accessible to client and Server nodes;
- a client-reachable `IP:PORT`, commonly beginning at `50051`.

The scripts span several historical module combinations, including ROCm 4.0.1, DTK 22.10, and DTK 24.04.1. They cannot be mixed arbitrarily. Migration must be based on the target Server binary's `ldd` output, MPI ABI, GPU/DCU architecture, and cluster modules.

A typical client path setup is:

```bash
export PROJECT_ROOT=/path/to/Digital_Twin_Brain
export DTB_RUNTIME_ROOT=/path/to/external/Digital_twin_brain
export PYTHONPATH="${PROJECT_ROOT}:${DTB_RUNTIME_ROOT}:${DTB_RUNTIME_ROOT}/cuda_release/python:${PYTHONPATH:-}"
```

The non-public file tree uses the directory basename `cuda_release_xia`, while this workspace imports `cuda_release.python...`. A directory basename is not necessarily the importable package name. If the cluster does not separately expose a standard `cuda_release` client package, inspect `PYTHONPATH` and the wrapper/protobuf contract and implement an adapter. Renaming the directory alone is not a compatibility solution.

### Preflight checks

```bash
python -V
python -c "import torch; print(torch.__version__, torch.version.hip, torch.cuda.is_available())"
python -c "import h5py, sparse, mpi4py, grpc, google.protobuf, prettytable"
python -c "import generation.make_block; print('generation.make_block OK')"
python -c "from cuda_release.python.dist_blockwrapper_pytorch import BlockWrapper; print('private wrapper OK')"
mpirun -np 2 python -c "from mpi4py import MPI; print(MPI.COMM_WORLD.rank, MPI.COMM_WORLD.size)"
```

Do not submit a large run if the private wrapper, MPI, or gRPC checks fail.

## Compute-resource Planning

For `degree=100`, this project uses the following empirical capacity rule:

```text
approximately one Server device with at least 16 GB free VRAM per 12,500,000 neurons
planning:    n_blocks_requested = ceil(requested_scale / 12,500,000)
post-build:  n_workers_required = ceil(actual_neurons / 12,500,000)
```

`test/normal_generation.py` likewise partitions at 12.5 million neurons per block.

| Requested scale | Planned blocks | Nominal device capacity at 16 GB per block |
|---:|---:|---:|
| 10 million | 1 | approximately 16 GB |
| 100 million | 8 | approximately 128 GB |
| 1 billion | 80 | approximately 1,280 GB |
| 3 billion | 240 | approximately 3,840 GB |

These are planning values for `degree=100`, not measured memory use or exact upper bounds. After generation, read the final value of `supplementary_info/population_base.npy` as `actual_neurons` and recalculate capacity. Minimum E/I-population constraints may make the actual count exceed the request. If the required worker count exceeds the generated block count, adjust the generation block partition/count and regenerate; if the current CLI cannot set that count independently, implement and validate that capability first. Change `scale` only when the scientific design permits it, because doing so changes the model. Reserve runtime headroom on every device.

The estimate excludes client GPU memory, host memory, communication routes, sampled outputs, and safety margins. Assimilation expands `B` source blocks into `B × E` Server ensemble blocks, where `E` is the actual `--ensembles`. Eight blocks with 30 ensembles require 240 ensemble blocks; the 32-ensemble rest example in this README requires 256. The HMDA reference configuration uses 30, the Python default is 100, and historical rest/task templates contain 32/30. These values are not interchangeable, and Server workers must match the client run. Benchmark memory at small scale after changing `degree`, dtype, or Server implementation.

Simulation output can also be large. The current implementation writes firing rates in 50-observation chunks. With `step=2200`, approximately 10,000–13,000 voxels, and two populations per voxel, one frequency chunk is approximately 8.8–11.4 GB. Enabling `vmean`, spike, sample, or `imean` increases client memory and storage requirements. Plan Server memory, client accelerator/host memory, shared storage, and log space together.

## Stage 1: Data Placement and Preprocessing

### 1.1 Build voxel data from raw inputs

The expected entry point is `data/ordinary_generetion.m` (`generetion` is the historical filename spelling). It reads, for each participant:

- an SC/DTI MAT whose name contains `connectome`;
- `<subject>_gmv_new.mat`;
- fMRI MAT files whose names contain `bold`, `func`, or `fmri`;
- `shen_268.csv`;
- `MNI152_T1_3mm_gmwmi_shen268_label.nii`;
- `shen_3mm_268_parcellation.nii`.

The script writes `<subject>_voxel_data.mat` and performs atlas alignment, DTI symmetrization, BOLD z-scoring, and 0.01–0.1 Hz band-pass filtering.

```bash
matlab -batch "cd('data'); ordinary_generetion"
```

The raw participant data are absent, and `target_subjects` currently lists only five participants. Before using new data, inspect the participant list and the condition/time-point discovery logic.

### 1.2 Remove empty and isolated voxels

`data/clean_voxel_data.m`:

1. removes voxels with `grey_matter_size <= 0`;
2. zeros the DTI diagonal;
3. iteratively removes isolated voxels from the remaining network;
4. applies the same selection to BOLD, atlas, and voxel labels;
5. writes 0-based/1-based valid and removed indices plus `filter_info`.

```bash
matlab -batch "cd('data'); clean_voxel_data"
```

> [!WARNING]
> The script currently reads `data/data/` and writes `data/data_cleaned/`, which does not directly match either the current flat layout or the participant directories written by `ordinary_generetion.m`. Set `dataDir`, `outputDir`, and file organization to the real paths before running it. The 12 provided `*_cleaned.mat` files have already passed this stage and normally should not be cleaned again.

`aggregate_data_cleaned_to_subject_shen10to1.m` is an optional subject-specific 10:1 coarsening branch. It depends on a missing mapping file and `make_subject_cleaned_shen10to1_nodes.py`, so this snapshot cannot execute that branch independently.

## Stage 2: Generation

### 2.1 Recommended whole-brain, multi-block entry point

`test/normal_generation.py` is the most complete generation entry point in this snapshot:

```bash
cd test
MPI_RANKS=1
SUBJECT_DIR=/path/to/one-subject-directory
mpirun -np "${MPI_RANKS}" python normal_generation.py \
  --block_dir="${SUBJECT_DIR}" \
  --scale=10000000 \
  --degree=100
```

| Argument | Meaning |
|---|---|
| `--block_dir` | Single-participant input directory and parent of generated output; not the `block_*.npz` directory |
| `--scale` | Requested total neuron count |
| `--degree` | Mean in-degree per neuron |

Ten million neurons produce one output block, so the example uses one MPI rank. In general use `1 <= MPI_RANKS <= n_blocks`; extra ranks may still reload the large DTI matrix and waste host memory. Run `mpirun` only inside resources allocated by Slurm, never directly on a login node.

The CLI has no dtype flag; the current function defaults to `uint8` weights. A typical output is:

```text
sub-<subject_id>/
└── dti_distribution_10m_d100_blocks1_int_ext/
    ├── module/
    │   └── uint8/
    │       └── block_0.npz
    ├── multi_module/
    │   └── uint8/
    ├── supplementary_info/
    │   ├── atlas_region.npz
    │   ├── population_base.npy
    │   ├── rest_state_bold.npy
    │   ├── MID_task_bold.npy
    │   └── SST_task_bold.npy
    └── DA/
```

Core fields in each `block_*.npz` are:

```text
property
output_neuron_idx
input_block_idx
input_neuron_idx
input_channel_offset
weight
```

Because every E/I population has a minimum neuron-count constraint, `--scale` is only the requested count. Use the final value of `supplementary_info/population_base.npy` for the actual total.

Connectivity generation reseeds from system entropy, and the current workflow does not bind the seed, input hashes, source version, and full parameters to the output. Repeated generation is therefore not guaranteed to produce the same network. Formal runs should preserve a manifest and file hashes. The low-level generator generally skips an existing `block_*.npz` based only on file existence; a skipped file is not proof of completeness or parameter identity. Verify every file before resuming, and use a new output directory for a formal generation run.

### 2.2 Regional-model entry point

The historical regional model can be generated with:

```bash
cd regional_model
MPI_RANKS=1
SUBJECT_DIR=/path/to/one-subject-directory
mpirun -np "${MPI_RANKS}" python regional_generation.py \
  --block_dir="${SUBJECT_DIR}" \
  --scale=3000000 \
  --degree=100
```

This entry point always creates one block, so one MPI rank is used. Its supplementary output is smaller than that of `normal_generation.py`. It serves the historical regional scripts and is not an unconditional substitute for the whole-brain/multi-block path.

`test/normal_generation.slurm` and `regional_model/regional_generation.slurm` are templates from the original cluster. Before submission, change the partition, modules, environment name, absolute paths, node count, and participant directory.

## External Server: Prerequisite for Stages 3 and 4

Generation itself does not call the model Server through gRPC. Data assimilation, simulation, and manipulation require a Server that is compatible with the client.

The external DTB Server runtime must provide `snn.proto`, `dist_blockwrapper_pytorch.py`, `dist_simulator`, `dist_simulator_xia.sh`, and matching gRPC/MPI Server modules.

`regional_model/server_test.slurm` is a deployment template for that private Server. It:

- checks the external `cuda_release_xia` path, gRPC/protobuf, and GCC runtime;
- checks dynamic libraries for `dist_simulator`;
- starts 1–4 Server instances;
- assigns one device and two MPI ranks to each instance;
- listens on ports `50051` through `50054`.

Illustrative submissions are:

```bash
cd regional_model
sbatch server_test.slurm 1   # one non-DA single-block instance, usually port 50051
sbatch server_test.slurm 4   # four independent single-worker instances, usually 50051..50054
```

Each gRPC instance started by `server_test.slurm` has one accelerator worker and is intended mainly for independent single-block simulations/manipulations. It cannot host the `B × E` blocks required by data assimilation. Use `data_assimilation/server_dtb*.slurm` or an equivalent topology that gives one gRPC Server enough controller/worker ranks. Do not confuse the number of gRPC Server instances with the number of model-block workers inside one instance.

> [!WARNING]
> `data_assimilation/server_dtb_regional.slurm` currently runs the hard-coded command `find /dev/shm -user ssct004t -delete` on every allocated node. Never submit it unchanged, and do not merely replace the username with the current account: it may remove shared memory belonging to other jobs under the same account. Remove the command or restrict cleanup to an exact, resolved, ownership-checked subpath bound to the current job and confirmed to remain inside its intended `/dev/shm` namespace.

These commands can run only after the original private paths, shared libraries, cluster partition, and devices have been configured. On a new cluster, first compare the wrapper/protobuf contract and complete a small `Init → Run → Shutdown` test.

## Stage 3: Data Assimilation

The entry point is `data_assimilation/DataAssimilation_demo.py`:

- `--task=rest` estimates rest parameters using `rest_state_bold.npy`;
- `--task=task` estimates task-state external inputs using `<task_name>_task_bold.npy` and, optionally, a rest result.

### 3.1 Rest example

```bash
cd data_assimilation
SERVER_IP=10.0.0.1
MODEL_ROOT=/path/to/dti_distribution_10m_d100_blocks1_int_ext
mpirun -np 1 python DataAssimilation_demo.py \
  --task=rest \
  --ip="${SERVER_IP}:50051" \
  --block_path="${MODEL_ROOT}" \
  --dtype=uint8 \
  --path_out="${MODEL_ROOT}/DA/" \
  --label=DTB_rest_voxel \
  --para_ind="10 11" \
  --gui_real="0.0008 0.0008 0.0015 0" \
  --gui_label="10 11 12 13" \
  --hp_range_rate="2 2.5" \
  --bold_range="0.0065 0.015" \
  --hp_sigma_2=0.5 \
  --solo_rate=0.8 \
  --ou="10 0.66262627 0.12121212" \
  --ensembles=32 \
  --step=2200
```

`--path_out`, `--label`, and `--gui_label` are effectively required by the current rest path even though their parser defaults are `None`. Without `gui_label`, a later use of the local `gui_real` variable is undefined. `--gui_real` has a historical default, but a formal run should supply it explicitly and ensure that its length and order match `gui_label`. `path_out` should end in a path separator because the implementation concatenates strings.

This example has `B=1` and `E=32`. The DA backend therefore needs one gRPC service capable of hosting 32 ensemble blocks; a typical logical topology is one controller rank plus 32 worker ranks/devices. `server_test.slurm 1` has only one worker and cannot host this example. For multiple source blocks, scale to `B × E`; the exact rank/device mapping is defined by the matching private launcher.

At runtime the client creates a task-specific temporary directory below `multi_module/<dtype>/` and symlinks the source blocks once per ensemble. The filesystem must support symlinks. These directories are not automatically removed after a successful run; clean them only by exact path after the Server has stopped and outputs have been preserved.

Use the task-isolated logic in `DataAssimilation_demo.py`. Do not use the old `data_assimilation/ln.py` as a concurrent-task entry point: it deletes and reconstructs the shared `multi_module/<dtype>` directory, so concurrent runs can destroy each other's state.

Principal rest outputs include:

- `w.npy`, `w_fix.npy`;
- `bold_assimilation.npy`;
- `hp_log.npy`, `hp_sm.npy`, `hp_ms.npy`;
- BOLD and parameter figures under `figure/`.

### 3.2 Task example

Task assimilation needs `MID_task_bold.npy` or `SST_task_bold.npy` and atlas metadata. The current implementation requires one of two paths: provide a rest `--hp_after_da_path`, or provide both a matching `--gui` and `--para_ind`. If neither path is supplied, `da_para_ind` remains undefined and the run fails. `--path_out`, `--label`, and `--task_name` are also effectively non-null for this path. A formal task must verify that the baseline parameters match the study design; parser defaults of `None` do not make these inputs scientifically optional.

Templates are:

- `data_assimilation/test_da_task_MID_full_int_ext.slurm`;
- `data_assimilation/test_da_task_SST_full_int_ext.slurm`.

Principal outputs are `W.npy`, `hp.npy`, and images under `show/`. The 12 current MAT files contain no `EFT_task_bold`, so the EFT Slurm file is only a historical template and cannot be run directly on these data.

## Stage 4: Simulation and Manipulation

General entry points are:

- `test/test_simulation.py`;
- `regional_model/test_simulation.py`.

`--block_dir` must refer to the model root. The code appends `module/<dtype>` and reads `atlas_region.npz` and `population_base.npy` from `supplementary_info/`.

### 4.1 Baseline simulation

Run from the project root so that package imports resolve:

```bash
SERVER_IP=10.0.0.1
MODEL_ROOT=/path/to/dti_distribution_10m_d100_blocks1_int_ext
OUTPUT_DIR=/path/to/output/baseline
cd "${PROJECT_ROOT}"
python -m test.test_simulation \
  --ip="${SERVER_IP}:50051" \
  --block_dir="${MODEL_ROOT}" \
  --dtype=uint8 \
  --write_path="${OUTPUT_DIR}" \
  --name=baseline \
  --ou="10 0.66262627 0.12121212" \
  --step=800 \
  --observation=100
```

Explicitly supply `--write_path`. Common outputs are:

- `freqs_<state>_assim_<chunk>.npy`;
- `bold_<state>_assim.npy` and `.mat`.

`test/test_simulation.py` calls `clear_mode()` before running, so its common path mainly writes firing rate and BOLD. `regional_model/test_simulation.py` does not clear those modes and may additionally write `spike`, `vi`, or `vmean` when constructed accordingly. `imean` and statistics files are not produced by the current defaults.

### 4.2 Replay with assimilated parameters

For the whole-brain `test/` entry point, a rest replay can use:

```text
--hp_after_da_path=/path/to/assimilation/hp_sm.npy
--hp_a_index="10 11"
```

`--hp_a_index` must exactly match the `--para_ind` used to generate the file, including column order. The assimilation example above estimates `10 11`, so the replay uses `10 11`. `hp_sm.npy` and `hp_ms.npy` represent different ensemble-mean transformation orders. Choose and record one; do not mix them across experiments.

The regional entry point uses a different flag: `regional_model/test_simulation.py` uses `--hp_index`, whereas `test/test_simulation.py` uses `--hp_a_index` for assimilated columns. From the project root, invoke the regional entry point with `python -m regional_model.test_simulation ...`. Do not substitute one CLI flag for the other.

A task replay can use:

```text
--hp_after_task_da_path=/path/to/task_hp.npy
--stimulus_region="43 44"
```

The `stimulus_region` value is a formatting example only. A real run must use exactly the same region set and order as the task-assimilation command that generated the `hp.npy`. Equal-length but differently mapped regions may not fail immediately and can still invalidate the scientific interpretation.

### 4.3 Parameter or region manipulation

Whole-brain parameter modification uses `--gui` and `--hp_index`. Region-specific modification uses:

```text
--manipulate_region="43 44"
--hp_index_manipulate="12"
--gui_manipulate="0.00565657"
```

These values are formatting examples, not a paper NP circuit or recommended biological parameter set.

Historical templates include:

- `test/baseline_client_MID.slurm`, `baseline_client_SST.slurm`;
- `test/validation_after_task_da_int_ext_*.slurm`;
- `test/manipu_after_task_da_int_ext_*.slurm`;
- `regional_model/MID_batch.slurm`, `SST_batch_10m.slurm`.

Some old scripts containing `manipu` in their filenames actually change whole-brain parameters through `--gui` and do not pass `--manipulate_region`. Interpret an experiment from the executed command and saved metadata, not from its filename alone.

A four-condition regional batch connects to `50051..50054` simultaneously. Start four independent Server instances first, and bind every client to the correct HIP device.

## Rules for Slurm Scripts

Treat every `.slurm` and `.sh` file as an original-cluster template. Before execution, verify at least:

1. partition, node count, MPI ranks, GPU/DCU resources, and excluded nodes;
2. `PROJECT_ROOT`, data paths, private runtime, and output paths;
3. Conda environment name—some scripts still use `dtb`, whereas the YAML uses `pytorch-1.9`;
4. HPC-X, ROCm/DTK, GCC, and shared-library ABI;
5. Server IP/port and client reachability;
6. agreement between block count and Server worker count;
7. agreement between dtype and the real `module/<dtype>` directory;
8. task-isolated output directories and preservation of parameters, logs, and run metadata.

In particular, every cleanup command involving `/dev/shm` must be restricted to an exact path for the current job. Never delete broadly by account across allocated nodes.

Do not launch a batch before a small-scale validation run succeeds.

## Known Limitations and Validation Status

- the 40 Python source files in the current inventory passed AST syntax parsing, but that does not demonstrate successful dependencies, interfaces, or numerical execution;
- modern Python emits `invalid escape sequence '\i'` SyntaxWarnings for the LaTeX `\includegraphics` strings in `drawing/draw.py`;
- no private wrapper or Server is available for end-to-end validation;
- no `block_*.npz` or downstream formal result is present;
- MATLAB, MPI, Slurm, ROCm/GPU, Server, generation, assimilation, and simulation have not been reproduced end to end from this snapshot;
- `pytorch-1.9_full_env.yml` uses an old NumPy; modern NumPy will reject historical aliases such as `np.int`, `np.float`, and `np.bool`;
- generation uses non-fixed random seeding and lacks a manifest binding input hashes, code version, seed, and full parameters;
- scripts contain private absolute paths, IPs, partitions, and experimental parameters that are not portable defaults;
- `data/ordinary_generetion.m` handles only five hard-coded `target_subjects` and scans only top-level `sub-*` entries;
- the rest path in `DataAssimilation_demo.py` has implicit dependencies among nominally optional flags, and ensemble counts differ across entry points/templates;
- the `test/` and `regional_model/` simulation CLIs use different flags for assimilated parameter columns;
- five participants follow a visibly different cleaning branch, and semantics such as ROI 29/Nacc classification still need domain review;
- this workspace has no Git metadata or LICENSE, so its version history and redistribution rights cannot be established from the snapshot alone;

A formal experiment should preserve at least the source version or source hash, environment inventory, input hashes, generation parameters, random seeds, block manifest, Server binary and proto/wrapper hashes, Slurm job ID, complete logs, and result-file hashes.

## References

- [Digital_twin_brain-open public repository](https://github.com/DTB-consortium/Digital_twin_brain-open)
- `doc/source/install.rst`: early client environment notes
- `doc/source/user_guide.rst`: early user-guide entry point
- `pytorch-1.9_full_env.yml`: historical client environment snapshot
