# -*- coding: utf-8 -*- 
# @Time : 2022/8/10 14:31 
# @Author : lepold
# @File : test_generation.py
import os.path
import numpy as np
import argparse

import os
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(current_dir)
import sys
sys.path.append('../')

import h5py
import sparse
from mpi4py import MPI
from scipy.io import loadmat

from generation.make_block import *


def get_args():
    parser = argparse.ArgumentParser(description="Model simulation")
    parser.add_argument("--block_dir", type=str, default=None) 
    parser.add_argument("--scale", type=int, default=2e7)
    parser.add_argument("--degree", type=int, default=100)
    args = parser.parse_args()
    return args

def make_directory_tree(root_path, scale, degree, extra_info, dtype="single"):
    """
    make directory tree for each subject.

    Parameters
    ----------
    root_path: str
        each subject has a root path.

    scale: int
        number of neurons of whole brain.
    degree:
        in-degree of each neuron.

    init_min: float
        the lower bound of uniform distribution where w is sampled from.

    init_max: float
        the upper bound of uniform distribution where w is sampled from.

    extra_info: str
        supplementary information.

    Returns
    ----------
    second_path: str
        second path to save connection table

    """
    os.makedirs(root_path, exist_ok=True)
    os.makedirs(os.path.join(root_path, "raw_data"), exist_ok=True)
    second_path = os.path.join(root_path,
                                f"dti_distribution_{int(scale // 1e6)}m_d{degree}_{extra_info}")
    os.makedirs(second_path, exist_ok=True)
    os.makedirs(os.path.join(second_path, "module"), exist_ok=True)
    os.makedirs(os.path.join(second_path, "multi_module", dtype), exist_ok=True)  # 'single' means the precision.
    os.makedirs(os.path.join(second_path, "supplementary_info"), exist_ok=True)
    os.makedirs(os.path.join(second_path, "DA"), exist_ok=True)

    return second_path, os.path.join(second_path, "module")


def add_laminar_cortex_model(conn_prob, gm, canonical_voxel=False):
    """
    Process the connection probability matrix, grey matter and degree scale for DTB with pure voxel and micro-column
    structure.  Each voxel is split into 2 populations (E and I). Each micro-column is spilt into 10 populations
    (L1E, L1I, L2/3E, L2/3I, L4E, L4I, L5E, L5I, L6E, L6I).

    Parameters
    ----------
    conn_prob: numpy.ndarray, shape [N, N]
        the connectivity probability matrix between N voxels/micro-columns.

    gm: numpy.ndarray, shape [N]
        the normalized grey matter in each voxel/micro-column.

    canonical_voxel: bool
        Ture for voxel structure; False for micro-column structure.

    Returns
    -------
    out_conn_prob: numpy.ndarray
        connectivity probability matrix between populations (shape [2*N, 2*N] for voxel; shape[10*N, 10*N] for micro
        -column) in the sparse matrix form.

    out_gm: numpy.ndarray
        grey matter for populations in DTB (shape [2*N] for voxel; shape[10*N] for micro-column).

    out_degree_scale: numpy.ndarray
        scale of degree for populations in DTB (shape [2*N] for voxel; shape[10*N] for micro-column).

    """
    if not canonical_voxel:
        lcm_connect_prob = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 3554, 804, 881, 45, 431, 0, 136, 0, 1020],
                                        [0, 0, 1778, 532, 456, 29, 217, 0, 69, 0, 396],
                                        [0, 0, 417, 84, 1070, 690, 79, 93, 1686, 0, 1489],
                                        [0, 0, 168, 41, 628, 538, 36, 0, 1028, 0, 790],
                                        [0, 0, 2550, 176, 765, 99, 621, 596, 363, 7, 1591],
                                        [0, 0, 1357, 76, 380, 32, 375, 403, 129, 0, 214],
                                        [0, 0, 643, 46, 549, 196, 327, 126, 925, 597, 2609],
                                        [0, 0, 80, 8, 92, 3, 159, 11, 76, 499, 1794]], dtype=np.float64
                                    )

        lcm_gm = np.array([0, 0,
                            33.8 * 78, 33.8 * 22,
                            34.9 * 80, 34.9 * 20,
                            7.6 * 82, 7.6 * 18,
                            22.1 * 83, 22.1 * 17], dtype=np.float64)  # ignore the L1 neurons
    else:
        # 4:1 setting, setting from wenyong
        # lcm_connect_prob = np.array([[0.3, 0.2, 0.5],
        #                              [0.3, 0.2, 0.5]], dtype=np.float64)
        # 4:1 setting, setting inferred from micro-column

        # critical nn, E:I=4:1 and most mass center in inner part.
        # lcm_connect_prob = np.array([[0.6, 0.2, 0.2],
        #                              [0.6, 0.2, 0.2]], dtype=np.float64)

        lcm_connect_prob = np.array([[4 / 7, 1 / 7, 2 / 7],
                                        [4 / 7, 1 / 7, 2 / 7]], dtype=np.float64)
        lcm_gm = np.array([0.8, 0.2], dtype=np.float64)

    lcm_gm /= lcm_gm.sum()

    syna_nums_in_lcm = lcm_connect_prob.sum(1) * lcm_gm
    lcm_degree_scale = syna_nums_in_lcm / syna_nums_in_lcm.sum() / lcm_gm
    lcm_degree_scale = np.where(np.isnan(lcm_degree_scale), 0, lcm_degree_scale)
    lcm_connect_prob /= lcm_connect_prob.sum(axis=1, keepdims=True)

    if conn_prob.shape[0] == 1:
        conn_prob[:, :] = 1
    else:
        conn_prob[np.diag_indices(conn_prob.shape[0])] = 0
        conn_prob = conn_prob / conn_prob.sum(axis=1, keepdims=True)

    conn_prob[np.isnan(conn_prob)] = 0
    out_gm = (gm[:, None] * lcm_gm[None, :]).reshape([-1])
    out_degree_scale = np.broadcast_to(lcm_degree_scale[None, :], [gm.shape[0], lcm_gm.shape[0]]).reshape([-1])
    conn_prob = sparse.COO(conn_prob)
    # only e5 is allowed to output.
    corrds1 = np.empty([4, conn_prob.coords.shape[1] * lcm_connect_prob.shape[0]], dtype=np.int64)
    if not canonical_voxel:
        corrds1[3, :] = 6
    else:
        corrds1[3, :] = 0
    corrds1[(0, 2), :] = np.broadcast_to(conn_prob.coords[:, :, None],
                                            [2, conn_prob.coords.shape[1], lcm_connect_prob.shape[0]]).reshape([2, -1])
    corrds1[(1), :] = np.broadcast_to(np.arange(lcm_connect_prob.shape[0], dtype=np.int64)[None, :],
                                        [conn_prob.coords.shape[1], lcm_connect_prob.shape[0]]).reshape([1, -1])

    data1 = (conn_prob.data[:, None] * lcm_connect_prob[:, -1]).reshape([-1])

    lcm_connect_prob_inner = sparse.COO(lcm_connect_prob[:, :-1])
    corrds2 = np.empty([4, conn_prob.shape[0] * lcm_connect_prob_inner.data.shape[0]], dtype=np.int64)
    corrds2[0, :] = np.broadcast_to(np.arange(conn_prob.shape[0], dtype=np.int64)[:, None],
                                    [conn_prob.shape[0], lcm_connect_prob_inner.data.shape[0]]).reshape([-1])
    corrds2[2, :] = corrds2[0, :]
    corrds2[(1, 3), :] = np.broadcast_to(lcm_connect_prob_inner.coords[:, None, :],
                                            [2, conn_prob.shape[0], lcm_connect_prob_inner.coords.shape[1]]).reshape(
        [2, -1])
    data2 = np.broadcast_to(lcm_connect_prob_inner.data[None, :],
                            [conn_prob.shape[0], lcm_connect_prob_inner.coords.shape[1]]).reshape([-1])

    out_conn_prob = sparse.COO(coords=np.concatenate([corrds1, corrds2], axis=1),
                                data=np.concatenate([data1, data2], axis=0),
                                shape=[conn_prob.shape[0], lcm_connect_prob.shape[0], conn_prob.shape[1],
                                        lcm_connect_prob.shape[1] - 1])

    out_conn_prob = out_conn_prob.reshape((conn_prob.shape[0] * lcm_connect_prob.shape[0],
                                            conn_prob.shape[1] * (lcm_connect_prob.shape[1] - 1)))
    if conn_prob.shape[0] == 1:
        out_conn_prob = out_conn_prob / out_conn_prob.sum(axis=1, keepdims=True)
    return out_conn_prob, out_gm, out_degree_scale

    
def test_generate_normal_voxel_whole_brain_int_ext(root_path="../data/Clinical_sample/sub-000159066706", degree=100,
                                                minimum_neurons_for_block=(200, 50),
                                                scale=int(2e7), dtype="uint8"):
    print("running test_generate_normal_regional_whole_brain")
    # make dirs
    blocks = 1
    first_path, second_path = make_directory_tree(root_path, scale, degree, "int_ext", dtype=dtype)
    print(f"Total {scale} neurons for DTB, merge to {blocks} blocks")
    
    for root, dirs, files in os.walk(root_path):  # 遍历目录及其子目录
        for file in files:
            if file.endswith('.mat'):  # 检查文件扩展名
                mat_files = os.path.join(root, file)  # 保存完整路径
    
    # load data
    file = h5py.File(mat_files, 'r')
    block_size = file['grey_matter_size'][0]
    dti = np.float32(file['dti_net_full'])
    dti[np.diag_indices_from(dti)] = 0

    # remove unconnected voxels
    nonzero_gm = (block_size > 0).nonzero()[0]
    nonzero_dti = (dti.sum(axis=1) > 0).nonzero()[0]
    nonzero_all = np.intersect1d(nonzero_gm, nonzero_dti)
    print(f"valid voxel index length {len(nonzero_all)}")
    print(f"valid voxel index {nonzero_all}")

    # saving atlas_region data
    atlas_region = file['atlas_region'][0]
    uni_region = file['uni_region'][0]
    is_cortex = file['is_cortex'][0]

    atlas_region = atlas_region[nonzero_all]
    region_in_data = np.empty(uni_region.shape)
    for i in range(len(uni_region)):
        region_in_data[i] = atlas_region.__contains__(uni_region[i])
    region_in_data = region_in_data.astype('bool')

    np.savez(os.path.join(first_path, "supplementary_info", "atlas_region.npz"), atlas_region = atlas_region, 
            uni_region = uni_region, is_cortex = is_cortex, region_in_data = region_in_data)

    # MID task
    task_bold = np.array(file['MID_task_bold'])
    task_bold = task_bold.T
    task_bold = task_bold[:, nonzero_all]
    np.save(os.path.join(first_path, "supplementary_info", "MID_task_bold.npy"), task_bold)

    # SST task
    task_bold = np.array(file['SST_task_bold'])
    task_bold = task_bold.T
    task_bold = task_bold[:, nonzero_all]
    np.save(os.path.join(first_path, "supplementary_info", "SST_task_bold.npy"), task_bold)

    # generate conn_prob for pupolations (from voxel to population)
    block_size = block_size[nonzero_all]
    block_size /= block_size.sum()
    conn_prob = dti[np.ix_(nonzero_all, nonzero_all)]
    conn_prob /= conn_prob.sum(axis=1, keepdims=True)
    conn_prob, block_size, degree_scale = add_laminar_cortex_model(conn_prob, block_size,
                                                                        canonical_voxel=True)

    # default parameters
    # gui = np.array([0.0008, 0.00027282, 0.00565657, 0.00066528]) # ou, from wjx
    gui = np.array([0.0008, 0.0008, 0.0015, 0]) 
    degree_ = np.maximum((degree * degree_scale).astype(np.uint16), 1)

    kwords = [{"V_th": -50,
                "V_reset": -65,
                'g_Li': 0.03,
                'g_ui': gui,
                'tao_ui': (2, 2, 10, 50),
                'noise_rate': 0,
                "size": int(max(b * scale, minimum_neurons_for_block[i % 2]))}
                for i, b in enumerate(block_size)]

    population_base = np.array([kword['size'] for kword in kwords], dtype=np.int64)
    population_base = np.add.accumulate(population_base)
    population_base = np.insert(population_base, 0, 0)
    np.save(os.path.join(first_path, "supplementary_info", "population_base.npy"), population_base)

    # make block
    conn = connect_for_multi_sparse_block(conn_prob, kwords,
                                            degree=degree_, dtype=dtype,
                                        )
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    for i in range(rank, blocks, size):
        merge_dti_distributation_block(conn, second_path,
                                    MPI_rank=i,
                                    number=blocks,
                                    avg_degree=degree,
                                    dtype=dtype,
                                    debug_block_dir=None,
                                    #    debug_block_dir="/public/home/ssct004t/project/zenglb/Digital_twin_brain/data/small_blocks/d1000_ou/uint8",  # None
                                    #    only_load=(i != 0))
                                    only_load=False)
        
        
if __name__ == "__main__":
    args = get_args()
    test_generate_normal_voxel_whole_brain_int_ext(root_path=args.block_dir, scale=args.scale, degree=args.degree)
