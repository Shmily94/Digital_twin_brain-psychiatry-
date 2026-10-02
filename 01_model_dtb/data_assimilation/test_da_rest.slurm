#!/bin/bash
#SBATCH -J rest_da_psj
#SBATCH -p kshdexclu04
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task 4
#SBATCH --gres=dcu:4
#SBATCH --mem 110G
#SBATCH --exclude=e04r1n00,j15r4n12,e12r1n12,e09r4n18

date
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
  --task='rest' \
  --ip=11.5.4.74:50051 \
  --block_path='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Regional_data/IMAGEN/000000112288/dti_distribution_3m_d100_int_ext' \
  --dtype='uint8' \
  --path_out='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Regional_data/IMAGEN/000000112288/dti_distribution_3m_d100_int_ext/DA/' \
  --para_ind='10 11' \
  --gui_real='0.0008 0.0008 0.0015 0' \
  --gui_label='10 11 12 13' \
  --hp_range_rate='2 2.5' \
  --bold_range='0.0065 0.015'\
  --hp_sigma_2=0.5 \
  --solo_rate=0.8 \
  --ou="10 0.66262627 0.12121212" \
  --label='DTB_rest_IMAGEN_voxel' \
  --ensembles=32 \
  --step=2200 \
