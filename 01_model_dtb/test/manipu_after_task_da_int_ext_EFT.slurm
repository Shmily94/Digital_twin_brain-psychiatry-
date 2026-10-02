#!/bin/bash
#SBATCH -J psj_manipu
#SBATCH -p kshdexclu04
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task 4
#SBATCH --gres=dcu:4
#SBATCH --mem 90G
#SBATCH --exclude=e04r3n19,e04r4n05,e04r4n04,e04r1n12

date
write_path="/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000083037309/dti_distribution_100m_d100_blocks8_int_ext/DA/mani_EFT"
now=$(date +"%y%m%d-%H%M")
ampa_i=0.0008
ampa_e=0.0044 
gaba=0.0040
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
  --ip=11.5.13.22:50051 \
  --block_dir="/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000083037309/dti_distribution_100m_d100_blocks8_int_ext" \
  --dtype="uint8" \
  --write_path=${write_path} \
  --name="after_task" \
  --hp_after_task_da_path='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000083037309/dti_distribution_100m_d100_blocks8_int_ext/DA/DTB_task_IMAGEN_voxel_task_EFT_full_0.1_0.45_0.25_0.5_30/assimilation/hp.npy' \
  --hp_index="10 11 12 13 18 19 20" \
  --gui="$ampa_e $ampa_i $gaba 0 2 2 $tau" \
  --ou="10 0.66262627 0.12121212" \
  --stimulus_region="1 2 3 4 10 11 19 34 35 36 37 82 83 84 85 86 87 88 89 90 91 92 93 94 121 122 123 124 126 127 128 134 135 136 137 140 145 146 147 154 168 169 170 215 216 219 220 221 222 223 224 225 226 228 229 230 231 232 258 259 260 261 262 263 264" \
  --step=2200 \
> ${log_path}
