#!/bin/bash
#SBATCH -J psj_manipu
#SBATCH -p kshdexlu11
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task 4
#SBATCH --gres=dcu:4
#SBATCH --mem 90G
#SBATCH --exclude=e04r3n19,e04r4n05,e04r4n04,e04r1n12

date
write_path="/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Clinical_sample/sub-000063218063/dti_distribution_100m_d100_blocks8_int_ext/DA/mani_task_SST_modu_ampa"
now=$(date +"%y%m%d-%H%M")
ampa_i=0.0008
ampa_e=0.0044 
gaba=0.0015
tau=10

write_path="$write_path/$now-ampa-$ampa_i-$ampa_e-gaba-$gaba"
mkdir -p ${write_path}
log_path="$write_path/$now.out"

export CUDA_PATH=/public/home/ssct004t/project/Digital_twin_brain
export PYTHONPATH=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain:$CUDA_PATH:$CUDA_PATH/cuda_release/python
echo $PYTHONPATH

module purge
module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.11.0/gcc-7.3.1 
module add compiler/rocm/4.0.1
module list
which python3

mpirun python test_simulation.py \
  --ip=11.5.8.76:50051 \
  --block_dir="/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Clinical_sample/sub-000063218063/dti_distribution_100m_d100_blocks8_int_ext" \
  --dtype="uint8" \
  --write_path=${write_path} \
  --name="after_task" \
  --hp_after_task_da_path='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Clinical_sample/sub-000063218063/dti_distribution_100m_d100_blocks8_int_ext/DA/DTB_task_IMAGEN_voxel_task_SST_full_0.1_0.45_0.25_0.5_30/assimilation/hp.npy' \
  --hp_index="10 11 12 13 20" \
  --gui="$ampa_e $ampa_i $gaba 0 $tau" \
  --ou="10 0.66262627 0.12121212" \
  --stimulus_region="1 4 7 8 9 19 21 22 23 30 31 34 35 37 82 83 120 121 122 123 124 126 127 128 139 140 142 143 147 154 157 158 164 168 170 215 216 217 219 257 258 259 260 261 262 263 264" \
  --step=2200 \
> ${log_path}
