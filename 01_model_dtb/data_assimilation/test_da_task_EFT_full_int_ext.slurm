#!/bin/bash
#SBATCH -J task_da_psj
#SBATCH -p kshdexclu04
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task 4
#SBATCH --gres=dcu:4
#SBATCH --mem 110G
#SBATCH --exclude=e04r1n00,j15r4n12,e12r1n12,e09r4n18

date
hostname
export CUDA_PATH=/public/home/ssct004t/project/Digital_twin_brain
export PYTHONPATH=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain:$CUDA_PATH:$CUDA_PATH/cuda_release/python
echo $PYTHONPATH

module purge
module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.11.0/gcc-7.3.1 
module add compiler/rocm/4.0.1
module list
which python3

mpirun python3 DataAssimilation_demo.py \
  --task='task' \
  --ip=11.5.4.18:50051 \
  --block_path='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000083037309/dti_distribution_100m_d100_blocks8_int_ext' \
  --dtype='uint8' \
  --path_out='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000083037309/dti_distribution_100m_d100_blocks8_int_ext/DA/' \
  --stimulus_hp_range='0.1 0.45' \
  --stimulus_region='1 2 3 4 10 11 19 34 35 36 37 82 83 84 85 86 87 88 89 90 91 92 93 94 121 122 123 124 126 127 128 134 135 136 137 140 145 146 147 154 168 169 170 215 216 219 220 221 222 223 224 225 226 228 229 230 231 232 258 259 260 261 262 263 264' \
  --bold_range='0.04 0.06'\
  --hp_sigma_2=0.25 \
  --para_ind='10 11 12 13 18 19 20' \
  --gui='0.0008 0.0008 0.0015 0 2 2 10' \
  --solo_rate=0.5 \
  --ou="10 0.66262627 0.12121212" \
  --label='DTB_task_IMAGEN_voxel' \
  --task_name='EFT' \
  --ensembles=30 \
  --step=2200 \

