#!/bin/bash
#SBATCH -J baseline_MID
#SBATCH -p kshdexlu11
#SBATCH --no-requeue
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --exclusive
#SBATCH --cpus-per-task=8
#SBATCH --gres=dcu:4
#SBATCH --exclude=e04r1n00,j15r4n12,e12r1n12,e09r4n18,e04r4n04,e04r4n05,e04r3n19,e04r1n12

# Conda activation hooks may read optional variables (for example HOST), so
# do not enable nounset until conda activate has completed.
set -eo pipefail

date

: "${MODEL_DIR:?MODEL_DIR must be exported by the submission script}"
: "${HP_PATH:?HP_PATH must be exported by the submission script}"
: "${SERVER_IP:?SERVER_IP must be exported by the submission script}"
: "${SUBJECT:?SUBJECT must be exported by the submission script}"

TASK="MID"
PROJECT_ROOT="/public/home/ssct004t/project/pengsongjun/Digital_twin_brain"
CUDA_PATH="/public/home/ssct004t/project/Digital_twin_brain"

# Baseline parameters
ampa_i=0.0008
ampa_e=0.0008
gaba=0.0015
tau=10

write_base="${MODEL_DIR}/DA/mani_task_${TASK}"
hp_path="${HP_PATH}"

if [[ ! -d "${MODEL_DIR}" ]]; then
    echo "ERROR: MODEL_DIR does not exist: ${MODEL_DIR}" >&2
    exit 2
fi

if [[ ! -f "${hp_path}" ]]; then
    echo "ERROR: hp.npy does not exist: ${hp_path}" >&2
    exit 3
fi

# Include seconds and Slurm job ID to avoid same-minute directory collisions.
now=$(date +"%y%m%d-%H%M%S")
run_name="${now}-job-${SLURM_JOB_ID}-ampa-${ampa_i}-${ampa_e}-gaba-${gaba}"
write_path="${write_base}/${run_name}"
mkdir -p "${write_path}"
log_path="${write_path}/${now}.out"

echo "SUBJECT=${SUBJECT}"
echo "TASK=${TASK}"
echo "MODEL_DIR=${MODEL_DIR}"
echo "HP_PATH=${hp_path}"
echo "SERVER_IP=${SERVER_IP}"
echo "WRITE_PATH=${write_path}"

# ============================================================
# Runtime environment: matched to the known-working 10M client
# supplied by the user.
# ============================================================
module purge

source /public/home/ssct004t/software/anaconda3/etc/profile.d/conda.sh
conda deactivate 2>/dev/null || true
unset PYTHONHOME

module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.7.4/gcc-7.3.1
module load compiler/rocm/dtk-22.10

conda activate pytorch-1.9

# Conda activation is complete; undefined-variable checking is now safe.
set -u

export PROJECT_ROOT
export CUDA_PATH
export PYTHONPATH="${PROJECT_ROOT}:${CUDA_PATH}:${CUDA_PATH}/cuda_release/python"
export LD_LIBRARY_PATH="${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH:-}"

module list 2>&1

echo "===== Python info ====="
which python
python -V
python -c "import sys; print(sys.executable)"
python -c "import torch; print('torch:', torch.__version__); print('torch file:', torch.__file__); print('hip:', torch.version.hip)"
python -c "import h5py; print('h5py:', h5py.__version__); print('h5py file:', h5py.__file__)"
python -c "import tqdm; print('tqdm:', tqdm.__version__)"
python -c "import generation.make_block; print('generation.make_block OK')"

PYTHON="$(which python)"

cd "${PROJECT_ROOT}"

mpirun "${PYTHON}" "${PROJECT_ROOT}/test/test_simulation.py" \
  --ip="${SERVER_IP}" \
  --block_dir="${MODEL_DIR}" \
  --dtype="uint8" \
  --write_path="${write_path}" \
  --name="after_task" \
  --hp_after_task_da_path="${hp_path}" \
  --hp_index="10 11 12 13 20" \
  --gui="${ampa_e} ${ampa_i} ${gaba} 0 ${tau}" \
  --ou="10 0.66262627 0.12121212" \
  --stimulus_region="1 2 3 4 5 6 14 23 36 82 83 84 93 94 120 121 122 123 124 125 126 127 128 134 135 136 137 138 140 141 158 169 215 216 217 219 220 221 228 229 230 231 232 257 258 259 260 261 262 263 264" \
  --step=2200 \
  > "${log_path}" 2>&1
