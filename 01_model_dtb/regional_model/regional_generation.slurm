#!/bin/bash
#SBATCH -J psj_generation
#SBATCH -p kshdexclu04
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH -N 10
#SBATCH -n 20
#SBATCH --gres=dcu:4
#SBATCH --mem 90G
#SBATCH --exclude=e04r1n03
##SBATCH --ntasks-per-node=1

date
module load mpi/hpcx/2.11.0-gcc-7.3.1
module load dtk/22.10.1

mpirun -np 20 python regional_generation.py \
  --block_dir=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Regional_data/HC/000064309040 \
  --scale=3000000 \
  --degree=100 \