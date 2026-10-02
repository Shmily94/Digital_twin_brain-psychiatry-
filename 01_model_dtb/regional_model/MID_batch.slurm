#!/bin/bash
#SBATCH -J psj_MID_10m
#SBATCH -p kshdexlu11
#SBATCH --no-requeue
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --exclusive
#SBATCH --cpus-per-task=8
#SBATCH --gres=dcu:4
#SBATCH --exclude=e04r1n00,j15r4n12,e12r1n12,e09r4n18,e04r4n04,e04r4n05,e04r3n19,e04r1n12

# Do not enable nounset until Conda activation has completed. Some Conda
# activation hooks read optional variables such as HOST.
set -eo pipefail

if (( $# < 3 || $# > 4 )); then
    echo "Usage: sbatch MID_batch.slurm <server_ip> <Clinical_sample|Control_sample> <subject_id> [server_job_id]" >&2
    exit 2
fi

SERVER_IP="$1"
SUB_SET="$2"
SUBJECT="$3"
SERVER_JOB_ID="${4:-}"

case "${SUB_SET}" in
    Clinical_sample|Control_sample)
        ;;
    *)
        echo "ERROR: invalid sample directory: ${SUB_SET}" >&2
        exit 2
        ;;
esac

PROJECT_ROOT=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain
CUDA_PATH=/public/home/ssct004t/project/Digital_twin_brain
DATA_ROOT="${PROJECT_ROOT}/data"

CLIENT_LOG_ROOT="${PROJECT_ROOT}/job_logs/client_jobs"
mkdir -p "${CLIENT_LOG_ROOT}"
CLIENT_DIAG_LOG="${CLIENT_LOG_ROOT}/MID_${SUBJECT}_${SLURM_JOB_ID}.log"
CLIENT_STATUS_FILE="${CLIENT_LOG_ROOT}/MID_${SUBJECT}_${SLURM_JOB_ID}.status"

# Keep a persistent client log in addition to the Slurm output file.
exec > >(tee -a "${CLIENT_DIAG_LOG}") 2>&1

echo "CLIENT_DIAG_LOG=${CLIENT_DIAG_LOG}"
echo "CLIENT_STATUS_FILE=${CLIENT_STATUS_FILE}"
echo "SERVER_JOB_ID=${SERVER_JOB_ID:-not supplied}"
echo "SERVER_IP=${SERVER_IP}"
echo "SUBJECT=${SUB_SET}/${SUBJECT}"

date
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
export DATA_ROOT
export PYTHONPATH="${PROJECT_ROOT}:${CUDA_PATH}:${CUDA_PATH}/cuda_release/python"
export LD_LIBRARY_PATH="${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH:-}"

echo "===== Python info ====="
which python
python -V
python -c "import sys; print(sys.executable)"
python -c "import torch; print('torch:', torch.__version__); print('torch file:', torch.__file__); print('hip:', torch.version.hip)"
python -c "import h5py; print('h5py:', h5py.__version__); print('h5py file:', h5py.__file__)"
python -c "import tqdm; print('tqdm:', tqdm.__version__)"
python -c "import generation.make_block; print('generation.make_block OK')"
module list 2>&1

PYTHON=$(which python)
pids=()

cleanup_resources() {
    local pid

    for pid in "${pids[@]}"; do
        if kill -0 "${pid}" 2>/dev/null; then
            kill "${pid}" 2>/dev/null || true
        fi
    done
    wait 2>/dev/null || true

    if [[ -n "${SERVER_JOB_ID}" ]]; then
        echo "Stopping dedicated MID server job ${SERVER_JOB_ID}."
        scancel "${SERVER_JOB_ID}" 2>/dev/null || true
    fi
}

on_exit() {
    local rc=$?
    trap - EXIT INT TERM HUP

    {
        echo "END_TIME=$(date '+%Y-%m-%d %H:%M:%S')"
        echo "EXIT_CODE=${rc}"
        echo "CLIENT_DIAG_LOG=${CLIENT_DIAG_LOG}"
    } > "${CLIENT_STATUS_FILE}"

    cleanup_resources
    exit "${rc}"
}

on_signal() {
    trap - EXIT INT TERM HUP
    cleanup_resources

    {
        echo "END_TIME=$(date '+%Y-%m-%d %H:%M:%S')"
        echo "EXIT_CODE=130"
        echo "CLIENT_DIAG_LOG=${CLIENT_DIAG_LOG}"
    } > "${CLIENT_STATUS_FILE}"

    exit 130
}

trap on_exit EXIT
trap on_signal INT TERM HUP

TEST_SIMULATION="${TEST_SIMULATION:-}"

if [[ -z "${TEST_SIMULATION}" ]]; then
    for candidate in \
        "${PROJECT_ROOT}/test_simulation.py" \
        "${SLURM_SUBMIT_DIR:-$PWD}/test_simulation.py"
    do
        if [[ -f "${candidate}" ]]; then
            TEST_SIMULATION="${candidate}"
            break
        fi
    done
fi

if [[ -z "${TEST_SIMULATION}" || ! -f "${TEST_SIMULATION}" ]]; then
    echo "ERROR: test_simulation.py was not found." >&2
    echo "Checked:" >&2
    echo "  ${PROJECT_ROOT}/test_simulation.py" >&2
    echo "  ${SLURM_SUBMIT_DIR:-$PWD}/test_simulation.py" >&2
    exit 3
fi

echo "TEST_SIMULATION=${TEST_SIMULATION}"

SUBJECT_ROOT="${DATA_ROOT}/${SUB_SET}/${SUBJECT}"
BLOCK_PATH="${SUBJECT_ROOT}/dti_distribution_10m_d100_blocks1_int_ext"
HP_ROOT="${SUBJECT_ROOT}/dti_distribution_100m_d100_blocks8_int_ext"
SUBJECT_KEY="${SUB_SET}/${SUBJECT}"

case "${SUBJECT_KEY}" in
    Clinical_sample/sub-000182136619|\
    Clinical_sample/sub-000113174215|\
    Control_sample/sub-000000112288)
        HP_PATH="${HP_ROOT}/DA/task_da/hp_MID.npy"
        ;;
    *)
        HP_PATH="${HP_ROOT}/DA/DTB_task_IMAGEN_voxel_task_MID_full_0.1_0.45_0.25_0.5_30/assimilation/hp.npy"
        ;;
esac

if [[ ! -d "${BLOCK_PATH}" ]]; then
    echo "ERROR: missing block directory: ${BLOCK_PATH}" >&2
    exit 4
fi

if [[ ! -f "${HP_PATH}" ]]; then
    echo "ERROR: missing MID HP file: ${HP_PATH}" >&2
    exit 5
fi

CONDITION_NAMES=(baseline ampa gaba ampa_gaba)
AMPA_E_VALUES=(0.0008 0.0044 0.0008 0.0044)
AMPA_I_VALUES=(0.0008 0.0008 0.0008 0.0008)
GABA_VALUES=(0.0015 0.0015 0.0040 0.0040)

TAU_GABA=10
BASE_PORT=50051
STEP=2200
RUN_TAG="$(date +'%y%m%d-%H%M%S')-job-${SLURM_JOB_ID}"
OUTPUT_ROOT="${BLOCK_PATH}/DA/manipu_after_task_MID_10m"
STIMULUS_REGION="1 2 3 4 5 6 14 23 36 82 83 84 93 94 120 121 122 123 124 125 126 127 128 134 135 136 137 138 140 141 158 169 215 216 217 219 220 221 228 229 230 231 232 257 258 259 260 261 262 263 264"

mkdir -p "${OUTPUT_ROOT}"

cat <<INFO
===== MID simulation =====
Subject:       ${SUBJECT_KEY}
Server IP:     ${SERVER_IP}
Server job:    ${SERVER_JOB_ID:-not supplied}
Block path:    ${BLOCK_PATH}
HP path:       ${HP_PATH}
Output root:   ${OUTPUT_ROOT}
Run tag:       ${RUN_TAG}
Conditions:    baseline, ampa, gaba, ampa_gaba
INFO

condition_logs=()

for ((i=0; i<4; i++)); do
    condition="${CONDITION_NAMES[$i]}"
    ampa_e="${AMPA_E_VALUES[$i]}"
    ampa_i="${AMPA_I_VALUES[$i]}"
    gaba="${GABA_VALUES[$i]}"
    server_port=$((BASE_PORT + i))

    write_path="${OUTPUT_ROOT}/${condition}/${RUN_TAG}-ampa_e-${ampa_e}-ampa_i-${ampa_i}-gaba-${gaba}-tauGaba-${TAU_GABA}"
    mkdir -p "${write_path}"

    log_path="${write_path}/simulation.out"
    condition_logs[$i]="${log_path}"

    cat > "${write_path}/run_metadata.txt" <<META
subject=${SUBJECT_KEY}
task=MID
condition=${condition}
server_job_id=${SERVER_JOB_ID}
server_endpoint=${SERVER_IP}:${server_port}
block_path=${BLOCK_PATH}
hp_path=${HP_PATH}
ampa_e=${ampa_e}
ampa_i=${ampa_i}
gaba=${gaba}
tau_gaba=${TAU_GABA}
step=${STEP}
META

    echo "Launching MID condition=${condition}, endpoint=${SERVER_IP}:${server_port}, output=${write_path}"

    # Keep only HIP_VISIBLE_DEVICES. Setting both HIP_VISIBLE_DEVICES and
    # ROCR_VISIBLE_DEVICES can remap the device twice on this platform.
    HIP_VISIBLE_DEVICES="${i}" \
    mpirun \
        -np 1 \
        --bind-to none \
        -x HIP_VISIBLE_DEVICES \
        "${PYTHON}" "${TEST_SIMULATION}" \
        --ip="${SERVER_IP}:${server_port}" \
        --block_dir="${BLOCK_PATH}" \
        --dtype="uint8" \
        --write_path="${write_path}" \
        --name="after_task" \
        --hp_after_task_da_path="${HP_PATH}" \
        --hp_index="10 11 12 13 18 19 20" \
        --gui="${ampa_e} ${ampa_i} ${gaba} 0 2 2 ${TAU_GABA}" \
        --ou="10 0.66262627 0.12121212" \
        --stimulus_region="${STIMULUS_REGION}" \
        --step="${STEP}" \
        >"${log_path}" 2>&1 &

    pids[$i]=$!
done

failed=0

for ((i=0; i<4; i++)); do
    if wait "${pids[$i]}"; then
        echo "MID condition ${CONDITION_NAMES[$i]} completed: ${condition_logs[$i]}"
    else
        rc=$?
        echo "ERROR: MID condition ${CONDITION_NAMES[$i]} failed with exit code ${rc}: ${condition_logs[$i]}" >&2
        tail -n 100 "${condition_logs[$i]}" >&2 || true
        failed=1
    fi
done

# All child processes have been reaped.
pids=()

date

if (( failed != 0 )); then
    exit 10
fi

echo "All four MID conditions completed for ${SUBJECT_KEY}."
