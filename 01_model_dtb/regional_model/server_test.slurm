#!/bin/bash
#SBATCH -J server_psj
#SBATCH -p kshdnormal
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --mem=0
#SBATCH -N 1
#SBATCH -n 2
#SBATCH --gres=dcu:4
#SBATCH --exclude=e07r3n18

set -uo pipefail


# ============================================================
# 1. Fixed paths
# ============================================================

CUDA_RELEASE_XIA=/public/home/ssct004t/project/Digital_twin_brain/cuda_release_xia
DIST_SIMULATOR="$CUDA_RELEASE_XIA/tools/dist_simulator"
DIST_LAUNCHER="$CUDA_RELEASE_XIA/tools/dist_simulator_xia.sh"

DEPS_ROOT=/public/home/ssct004t/software/cuda_release_deps
PROTOBUF_ROOT="$DEPS_ROOT/protobuf"
GRPC_ROOT="$DEPS_ROOT/grpc"

# GCC 8.2 runtime has been verified to contain:
# GLIBCXX_3.4.21
# GLIBCXX_3.4.22
# CXXABI_1.3.9
# CXXABI_1.3.11
GCC_RUNTIME_DIR=/public/software/compiler/gcc-8.2.0/lib64

# Keep runtime logs under the directory from which sbatch was submitted.
WORK_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$WORK_DIR" || {
    echo "ERROR: unable to enter working directory: $WORK_DIR" >&2
    exit 1
}


# ============================================================
# 2. Runtime environment
# ============================================================

module purge

# HPC-X 2.11.0 requires devtoolset/7.3.1 as a prerequisite.
module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.11.0/gcc-7.3.1
module load compiler/dtk/24.04.1

hash -r

export PATH="$PROTOBUF_ROOT/bin:$GRPC_ROOT/bin:$PATH"

export PKG_CONFIG_PATH="$PROTOBUF_ROOT/lib/pkgconfig:$GRPC_ROOT/lib/pkgconfig:${PKG_CONFIG_PATH:-}"

# GCC 8.2 runtime must come before system /lib64.
export LD_LIBRARY_PATH="$GCC_RUNTIME_DIR:$PROTOBUF_ROOT/lib:$GRPC_ROOT/lib:${LD_LIBRARY_PATH:-}"

export UCX_WARN_UNUSED_ENV_VARS=n
export UCX_TLS=self,sm
export OMP_NUM_THREADS=4


# ============================================================
# 3. Basic validation
# ============================================================

if [[ "$CUDA_RELEASE_XIA" != \
      "/public/home/ssct004t/project/Digital_twin_brain/cuda_release_xia" ]]; then
    echo "ERROR: unexpected CUDA_RELEASE_XIA path." >&2
    exit 1
fi

if [[ ! -x "$DIST_SIMULATOR" ]]; then
    echo "ERROR: executable not found or not executable:" >&2
    echo "$DIST_SIMULATOR" >&2
    exit 1
fi

if [[ ! -x "$DIST_LAUNCHER" ]]; then
    echo "ERROR: launcher not found or not executable:" >&2
    echo "$DIST_LAUNCHER" >&2
    exit 1
fi

if [[ ! -e "$GCC_RUNTIME_DIR/libstdc++.so.6" ]]; then
    echo "ERROR: GCC 8.2 libstdc++.so.6 not found:" >&2
    echo "$GCC_RUNTIME_DIR/libstdc++.so.6" >&2
    exit 1
fi

if [[ ! -e "$PROTOBUF_ROOT/lib/libprotobuf.so.19" ]]; then
    echo "ERROR: libprotobuf.so.19 not found." >&2
    exit 1
fi

if [[ ! -e "$GRPC_ROOT/lib/libgrpc.so.8" ]]; then
    echo "ERROR: libgrpc.so.8 not found." >&2
    exit 1
fi


# ============================================================
# 4. Dynamic-library validation
# ============================================================

echo "===== runtime environment ====="
date
hostname

echo "===== loaded modules ====="
module list 2>&1

echo "===== executables ====="
for command_name in g++ hipcc mpirun mpicxx numactl; do
    printf '%-20s ' "$command_name"
    command -v "$command_name" || true
done

echo "===== MPI version ====="
mpirun --version | head -10

echo "===== DCU architecture ====="
rocminfo 2>/dev/null |
    grep -oE 'gfx[0-9a-z]+' |
    sort -u || true

LDD_OUTPUT=$(ldd "$DIST_SIMULATOR" 2>&1)

echo "===== selected core libraries ====="
grep -E \
    'libstdc\+\+|libgcc_s|libmpi|libhiprand|librocrand|libgalaxyhip|libprotobuf|libgrpc|libgpr' \
    <<< "$LDD_OUTPUT" || true

if grep -F 'not found' <<< "$LDD_OUTPUT" >/dev/null; then
    echo "ERROR: unresolved dynamic libraries:" >&2
    grep -F 'not found' <<< "$LDD_OUTPUT" >&2
    exit 1
fi

SELECTED_STDCPP=$(
    awk '/libstdc\+\+\.so\.6/ {
        print $3
        exit
    }' <<< "$LDD_OUTPUT"
)

echo "SELECTED_STDCPP=${SELECTED_STDCPP}"

case "$SELECTED_STDCPP" in
    "$GCC_RUNTIME_DIR"/*)
        echo "Correct GCC 8.2 libstdc++ selected."
        ;;
    *)
        echo "ERROR: incorrect libstdc++ selected:" >&2
        echo "$SELECTED_STDCPP" >&2
        exit 1
        ;;
esac

RELOCATION_OUTPUT=$(ldd -r "$DIST_SIMULATOR" 2>&1 || true)

RUNTIME_ERRORS=$(
    grep -Ei \
        'undefined symbol|version .* not found|not found' \
        <<< "$RELOCATION_OUTPUT" || true
)

if [[ -n "$RUNTIME_ERRORS" ]]; then
    echo "ERROR: unresolved runtime symbols:" >&2
    echo "$RUNTIME_ERRORS" >&2
    exit 1
fi

echo "All runtime libraries and symbols resolved."


# ============================================================
# 5. Input validation
# ============================================================

port=50051
procs="${1:-}"

if [[ -z "$procs" ]]; then
    echo "ERROR: missing server process count." >&2
    echo "Usage: sbatch $(basename "$0") 4" >&2
    exit 2
fi

if ! [[ "$procs" =~ ^[0-9]+$ ]] ||
   (( procs < 1 || procs > 4 )); then
    echo "ERROR: server process count must be an integer from 1 to 4." >&2
    echo "Usage: sbatch $(basename "$0") 4" >&2
    exit 2
fi


# ============================================================
# 6. Log directories
# ============================================================

LOG_ROOT="$WORK_DIR/log/$SLURM_JOB_ID"
CUDA_LOG_ROOT="$WORK_DIR/cuda_log/$(hostname)"

DMESG_ROOT="$LOG_ROOT/dmesg"
DEBUG_ROOT="$LOG_ROOT/debug"
OUTPUT_ROOT="$LOG_ROOT/output"

mkdir -p \
    "$LOG_ROOT" \
    "$CUDA_LOG_ROOT" \
    "$DMESG_ROOT" \
    "$DEBUG_ROOT" \
    "$OUTPUT_ROOT"

hostfile_path="$LOG_ROOT/hostfile"

# Each dist_simulator instance launches exactly two MPI ranks.
printf '%s slots=2\n' "$(hostname)" > "$hostfile_path"

echo "===== hostfile ====="
cat "$hostfile_path"

echo "===== Python locations ====="
which -a python || true


# ============================================================
# 7. Backend address markers
# ============================================================

backend_hostname=$(hostname -f 2>/dev/null || hostname)

backend_ip=$(
    hostname -I 2>/dev/null |
    tr ' ' '\n' |
    awk '
        /^[0-9]+\./ && $0 !~ /^127\./ {
            print
            exit
        }
    '
)

if [[ -z "$backend_ip" ]]; then
    backend_ip=$(
        ip -4 route get 1.1.1.1 2>/dev/null |
        awk '
            {
                for (i = 1; i <= NF; i++) {
                    if ($i == "src") {
                        print $(i + 1)
                        exit
                    }
                }
            }
        '
    )
fi

if [[ -z "$backend_ip" ]]; then
    echo "ERROR: unable to determine backend IPv4 address." >&2
    exit 3
fi

# Stable markers read by submit_all_subject_tasks.sh.
echo "SERVER_JOB_ID=${SLURM_JOB_ID}"
echo "BACKEND_HOSTNAME=${backend_hostname}"
echo "BACKEND_IP=${backend_ip}"
echo "SERVER_PROCESS_COUNT=${procs}"

for ((i = 0; i < procs; i++)); do
    echo "BACKEND_ENDPOINT_${i}=${backend_ip}:$((port + i))"
done


# ============================================================
# 8. Child-process management
# ============================================================

pids=()
active=()

cleanup_children()
{
    local pid

    echo "Stopping remaining server processes..." >&2

    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done

    sleep 2

    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -KILL "$pid" 2>/dev/null || true
        fi
    done

    wait 2>/dev/null || true
}

handle_signal()
{
    echo "Received termination signal." >&2
    cleanup_children
    exit 143
}

trap handle_signal INT TERM HUP


# ============================================================
# 9. Launch server instances
# ============================================================

for ((i = 0; i < procs; i++)); do
    listen_port=$((port + i))
    gpu_id=$i

    cuda_log="$CUDA_LOG_ROOT/$gpu_id"
    dmesg_log="$DMESG_ROOT/$gpu_id"
    debug_log="$DEBUG_ROOT/$gpu_id"
    output_log="$OUTPUT_ROOT/$gpu_id"

    mkdir -p \
        "$cuda_log" \
        "$dmesg_log" \
        "$debug_log" \
        "$output_log"

    echo "Starting server process $i:"
    echo "  GPU ID:       $gpu_id"
    echo "  Listen port:  $listen_port"
    echo "  CUDA log:     $cuda_log"
    echo "  DMESG log:    $dmesg_log"
    echo "  DEBUG log:    $debug_log"
    echo "  OUTPUT path:  $output_log"

    mpirun \
        -np 2 \
        --bind-to none \
        --hostfile "$hostfile_path" \
        -x PATH \
        -x LD_LIBRARY_PATH \
        -x UCX_WARN_UNUSED_ENV_VARS \
        -x UCX_TLS \
        -x OMP_NUM_THREADS \
        -x DMESG_LOG="$dmesg_log" \
        -x DEBUG_LOG="$debug_log" \
        -x OUTPUT_PATH="$output_log" \
        "$DIST_LAUNCHER" \
        "$gpu_id" \
        "$listen_port" \
        "$cuda_log" &

    pids[$i]=$!
    active[$i]=1

    echo "SERVER_PROCESS_${i}_PID=${pids[$i]}"
done


# ============================================================
# 10. Monitor server instances
# ============================================================

remaining=$procs
status=0

while (( remaining > 0 )); do
    for ((i = 0; i < procs; i++)); do
        if [[ "${active[$i]:-0}" -ne 1 ]]; then
            continue
        fi

        pid="${pids[$i]}"

        if kill -0 "$pid" 2>/dev/null; then
            continue
        fi

        if wait "$pid"; then
            rc=0
        else
            rc=$?
        fi

        active[$i]=0
        remaining=$((remaining - 1))

        if [[ "$rc" -eq 0 ]]; then
            echo "Server process $i exited normally."
        else
            echo "ERROR: server process $i exited with status $rc." >&2
            status=1

            # A server instance should normally remain active.
            # Stop all other instances when any one fails.
            cleanup_children
            exit "$status"
        fi
    done

    if (( remaining > 0 )); then
        sleep 5
    fi
done

exit "$status"