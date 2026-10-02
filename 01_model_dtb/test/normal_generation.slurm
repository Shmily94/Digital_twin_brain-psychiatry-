#!/bin/bash
#SBATCH -J psj_generation
#SBATCH -p kshdexclu04
#SBATCH --no-requeue
#SBATCH --exclusive
#SBATCH -N 10
#SBATCH -n 20
#SBATCH --ntasks-per-node=2
#SBATCH --gres=dcu:4
#SBATCH --mem 90G
#SBATCH --exclude=e04r1n03,e04r1n00,j15r4n12,e12r1n12,e09r4n18,e04r3n19,e04r4n05,e09r4n09,e04r1n12,e09r4n16

set -e

date

module purge

source /public/home/ssct004t/software/anaconda3/etc/profile.d/conda.sh
conda deactivate 2>/dev/null || true

unset PYTHONHOME

module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.7.4/gcc-7.3.1
module load compiler/rocm/dtk-22.10

conda activate dtb

PROJECT_ROOT=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain
CUDA_PATH=/public/home/ssct004t/project/Digital_twin_brain

export CUDA_PATH
export PYTHONPATH=${PROJECT_ROOT}:${CUDA_PATH}:${CUDA_PATH}/cuda_release/python
export LD_LIBRARY_PATH=${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}

echo "===== Python info ====="
which python
python -V
python -c "import sys; print(sys.executable)"
python -c "import torch; print('torch:', torch.__version__); print('torch file:', torch.__file__); print('hip:', torch.version.hip)"
python -c "import h5py; print('h5py:', h5py.__version__); print('h5py file:', h5py.__file__)"
python -c "import tqdm; print('tqdm:', tqdm.__version__)"
python -c "import generation.make_block; print('generation.make_block OK')"

PYTHON=$(which python)

echo "===== Run program ====="
mpirun -np 20 -x PATH -x LD_LIBRARY_PATH -x PYTHONPATH ${PYTHON} normal_generation.py \
  --block_dir=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000044576096 \
  --scale=10000000 \
  --degree=100