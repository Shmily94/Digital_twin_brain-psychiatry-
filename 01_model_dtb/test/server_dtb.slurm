#!/bin/bash
#SBATCH -J server_psj
#SBATCH -p kshdexlu11

#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --mem=110G
#SBATCH --gres=dcu:4

#SBATCH -N 3

#SBATCH -o log/%j.o
#SBATCH -e log/%j.e

# clush -w $SLURM_JOB_NODELIST -f 1000 -b "find /dev/shm -user ssct004t -delete"
mkdir -p log
mkdir -p log/$SLURM_JOB_ID
mkdir -p log/$SLURM_JOB_ID/dmesg
mkdir -p log/$SLURM_JOB_ID/debug
mkdir -p log/$SLURM_JOB_ID/output
mkdir -p log/$SLURM_JOB_ID/hostfile

dmesg_log=log/$SLURM_JOB_ID/dmesg
debug_log=log/$SLURM_JOB_ID/debug
output_log=log/$SLURM_JOB_ID/output
hostfile_path=log/$SLURM_JOB_ID/hostfile/hostfile.out

date
ulimit -l unlimited
ulimit -s unlimited
export UCX_MEMTYPE_CACHE=no
export UCX_MEM_CUDA_HOOK_MODE=no

srun hostname | sort | uniq -c | awk '{if(NR==1){printf "%s slots=1\n",$2}else{printf "%s slots=4\n",$2}}' > ${hostfile_path}

# ============================================================
# Runtime modules
# ============================================================
module purge
module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.11.0/gcc-7.3.1
module load compiler/rocm/dtk-22.10.1
module list

# ============================================================
# Shared protobuf / gRPC runtime dependencies
# These libraries are readable across accounts and are required
# by cuda_release/tools/dist_simulator.
# ============================================================
DEPS_ROOT=/public/home/ssct004t/software/cuda_release_deps
PROTOBUF_ROOT="$DEPS_ROOT/protobuf"
GRPC_ROOT="$DEPS_ROOT/grpc"

export PATH="$PROTOBUF_ROOT/bin:$GRPC_ROOT/bin:$PATH"
export PKG_CONFIG_PATH="$PROTOBUF_ROOT/lib/pkgconfig:$GRPC_ROOT/lib/pkgconfig:${PKG_CONFIG_PATH:-}"
export LD_LIBRARY_PATH="$PROTOBUF_ROOT/lib:$GRPC_ROOT/lib:${LD_LIBRARY_PATH:-}"

DIST_SIMULATOR=/public/home/ssct004t/project/Digital_twin_brain/cuda_release/tools/dist_simulator
DIST_LAUNCHER=/public/home/ssct004t/project/Digital_twin_brain/cuda_release/tools/dist_simulator.sh

# ============================================================
# Runtime validation before launching MPI
# ============================================================
echo "===== runtime dependency check ====="
echo "USER=$(whoami)"
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"

if [[ ! -x "$DIST_SIMULATOR" ]]; then
    echo "ERROR: dist_simulator not found or not executable: $DIST_SIMULATOR" >&2
    exit 1
fi

if [[ ! -x "$DIST_LAUNCHER" ]]; then
    echo "ERROR: dist_simulator launcher not found or not executable: $DIST_LAUNCHER" >&2
    exit 1
fi

if [[ ! -e "$PROTOBUF_ROOT/lib/libprotobuf.so.19" ]]; then
    echo "ERROR: libprotobuf.so.19 not found under $PROTOBUF_ROOT/lib" >&2
    exit 1
fi

if [[ ! -e "$GRPC_ROOT/lib/libgrpc.so.8" ]]; then
    echo "ERROR: libgrpc.so.8 not found under $GRPC_ROOT/lib" >&2
    exit 1
fi

LDD_OUTPUT=$(ldd "$DIST_SIMULATOR" 2>&1)

echo "===== selected DTB libraries ====="
grep -E 'libprotobuf|libgrpc|libgpr|libmpi|libhiprand|librocrand|libgalaxyhip|libstdc\+\+' <<< "$LDD_OUTPUT" || true

if grep -F 'not found' <<< "$LDD_OUTPUT" >/dev/null; then
    echo "ERROR: unresolved dynamic libraries:" >&2
    grep -F 'not found' <<< "$LDD_OUTPUT" >&2
    exit 1
fi

echo "All required dynamic libraries were found."

output=./log/$SLURM_JOB_ID/output/out
mkdir -p "$output"
log_path=$output

# LD_LIBRARY_PATH is explicitly exported to all MPI ranks so that
# protobuf/gRPC can also be resolved on every compute node.
mpirun --bind-to none --hostfile ${hostfile_path} \
       -x UCX_TLS=self,sm,rc \
       -x LD_LIBRARY_PATH \
       -x DMESG_LOG=${dmesg_log} \
       -x DEBUG_LOG=${debug_log} \
       -x OUTPUT_PATH=${output_log} \
       "$DIST_LAUNCHER" "$log_path"