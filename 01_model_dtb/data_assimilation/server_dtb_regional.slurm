#!/bin/bash
#SBATCH -J server_psj
#SBATCH -p kshdexclu04
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH --mem=110G
#SBATCH --gres=dcu:4
#SBATCH -N 9
#SBATCH --exclude=e04r1n00,j15r4n12,e12r1n12,e09r4n18,e04r4n04,e04r4n05,e04r3n19,e04r1n12

# 手工直接 sbatch 本脚本时，stdout/stderr 也合并到一个日志文件。
# 通过主提交脚本运行时，这两个路径会被 sbatch 命令覆盖到本次 RUN_ROOT/logs 中。
#SBATCH --output=server_%j.log
#SBATCH --error=server_%j.log
#SBATCH --open-mode=append

set -Eeuo pipefail

log_error() {
  local rc=$?
  local line=${BASH_LINENO[0]:-unknown}
  local command=${BASH_COMMAND:-unknown}
  printf '[%s] ERROR: exit_code=%s line=%s command=%q\n' \
    "$(date '+%F %T')" "${rc}" "${line}" "${command}"
}

log_exit() {
  local rc=$?
  if ((rc == 0)); then
    echo "[$(date '+%F %T')] SERVER JOB COMPLETED SUCCESSFULLY"
  else
    echo "[$(date '+%F %T')] SERVER JOB FAILED: exit_code=${rc}"
  fi
}

trap log_error ERR
trap log_exit EXIT

# 不使用 BASH_SOURCE 切换目录。Slurm 可能从临时副本执行脚本；
# 主提交脚本已通过 --chdir 指定正确工作目录。
echo "============================================================"
echo "SERVER JOB START"
echo "START_TIME=$(date '+%F %T')"
echo "SLURM_JOB_ID=${SLURM_JOB_ID:-unknown}"
echo "SLURM_JOB_NAME=${SLURM_JOB_NAME:-unknown}"
echo "SLURM_JOB_NODELIST=${SLURM_JOB_NODELIST:-unknown}"
echo "SUBMIT_DIR=${SLURM_SUBMIT_DIR:-unknown}"
echo "WORK_DIR=$(pwd)"
echo "============================================================"

clush -w "${SLURM_JOB_NODELIST}" -f 1000 -b \
  "find /dev/shm -user ssct004t -delete"

# 以下目录是 simulator 原有运行输出目录，不是额外的 Slurm stdout/stderr 日志。
mkdir -p "log/${SLURM_JOB_ID}/dmesg"
mkdir -p "log/${SLURM_JOB_ID}/debug"
mkdir -p "log/${SLURM_JOB_ID}/output"
mkdir -p "log/${SLURM_JOB_ID}/hostfile"

dmesg_log="log/${SLURM_JOB_ID}/dmesg"
debug_log="log/${SLURM_JOB_ID}/debug"
output_log="log/${SLURM_JOB_ID}/output"
hostfile_path="log/${SLURM_JOB_ID}/hostfile/hostfile.out"

ulimit -l unlimited
ulimit -s unlimited
export UCX_MEMTYPE_CACHE=no
export UCX_MEM_CUDA_HOOK_MODE=no

srun hostname \
  | sort \
  | uniq -c \
  | awk '{if(NR==1){printf "%s slots=1\n",$2}else{printf "%s slots=4\n",$2}}' \
  > "${hostfile_path}"

echo "===== HOSTFILE ====="
cat "${hostfile_path}"

module purge
module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.11.0/gcc-7.3.1
module load compiler/rocm/dtk-22.10.1
module list

output="./log/${SLURM_JOB_ID}/output/out"
mkdir -p "${output}"
log_path=${output}

echo "===== START DIST SIMULATOR ====="
echo "DIST_SIMULATOR=/public/home/ssct004t/project/Digital_twin_brain/cuda_release/tools/dist_simulator.sh"
echo "LOG_PATH=${log_path}"

mpirun --bind-to none --hostfile "${hostfile_path}" -x UCX_TLS=self,sm,rc \
  -x DMESG_LOG="${dmesg_log}" \
  -x DEBUG_LOG="${debug_log}" \
  -x OUTPUT_PATH="${output_log}" \
  /public/home/ssct004t/project/Digital_twin_brain/cuda_release/tools/dist_simulator.sh \
  "${log_path}"
