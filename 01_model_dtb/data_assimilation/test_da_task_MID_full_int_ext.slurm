#!/bin/bash
#SBATCH -J task_da_psj
#SBATCH -p kshdexclu04
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --cpus-per-task 4
#SBATCH --gres=dcu:4
#SBATCH --mem 110G
#SBATCH --exclude=e04r1n00,j15r4n12,e12r1n12,e09r4n18

set -e

date

module purge

source /public/home/ssct004t/software/anaconda3/etc/profile.d/conda.sh
conda deactivate 2>/dev/null || true

unset PYTHONHOME

module load compiler/devtoolset/7.3.1
module load mpi/hpcx/2.7.4/gcc-7.3.1
module load compiler/rocm/dtk-22.10

conda activate pytorch-1.9

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

mpirun python3 DataAssimilation_demo.py \
  --task='task' \
  --ip=11.5.4.2:50051 \
  --block_path='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000000112288/dti_distribution_100m_d100_blocks8_int_ext' \
  --dtype='uint8' \
  --path_out='/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Control_sample/sub-000000112288/dti_distribution_100m_d100_blocks8_int_ext/DA/' \
  --stimulus_hp_range='0.1 0.45' \
  --stimulus_region='1 2 3 4 5 6 14 23 36 82 83 84 93 94 120 121 122 123 124 125 126 127 128 134 135 136 137 138 140 141 158 169 215 216 217 219 220 221 228 229 230 231 232 257 258 259 260 261 262 263 264' \
  --bold_range='0.04 0.06'\
  --hp_sigma_2=0.25 \
  --para_ind='10 11 12 13 20' \
  --gui='0.0008 0.0008 0.0015 0 10' \
  --solo_rate=0.5 \
  --ou="10 0.66262627 0.12121212" \
  --label='DTB_task_IMAGEN_voxel' \
  --task_name='MID' \
  --ensembles=30 \
  --step=2200 \

