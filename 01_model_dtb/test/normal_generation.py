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
    parser.add_argument("--scale", type=int, default=int(2e7))
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

    extra_info: str
        supplementary information.

    dtype: str
        data type / precision information.

    Returns
    ----------
    second_path: str
        root path to save generated data.

    module_path: str
        module path to save connection table.
    """
    os.makedirs(root_path, exist_ok=True)
    os.makedirs(os.path.join(root_path, "raw_data"), exist_ok=True)

    second_path = os.path.join(
        root_path,
        f"dti_distribution_{int(scale // 1e6)}m_d{degree}_{extra_info}"
    )

    os.makedirs(second_path, exist_ok=True)
    os.makedirs(os.path.join(second_path, "module"), exist_ok=True)
    os.makedirs(os.path.join(second_path, "multi_module", dtype), exist_ok=True)
    os.makedirs(os.path.join(second_path, "supplementary_info"), exist_ok=True)
    os.makedirs(os.path.join(second_path, "DA"), exist_ok=True)

    return second_path, os.path.join(second_path, "module")


def safe_row_normalize(mat, name="matrix", raise_on_zero=True):
    """
    Safely normalize matrix by row.

    Parameters
    ----------
    mat : numpy.ndarray
        Input matrix.

    name : str
        Matrix name for error message.

    raise_on_zero : bool
        If True, raise error when zero row exists.
        If False, zero rows remain zero.

    Returns
    -------
    normalized_mat : numpy.ndarray
    """
    row_sum = mat.sum(axis=1, keepdims=True)

    bad = (~np.isfinite(row_sum[:, 0])) | (row_sum[:, 0] <= 0)

    if np.any(bad):
        bad_idx = np.where(bad)[0]

        msg = (
            f"{name} has invalid rows before normalization. "
            f"bad rows count={len(bad_idx)}, "
            f"bad local indices first 50={bad_idx[:50]}, "
            f"row_sum first 50={row_sum[bad_idx[:50], 0]}"
        )

        if raise_on_zero:
            raise ValueError(msg)
        else:
            print("Warning:", msg)

    out = np.divide(
        mat,
        row_sum,
        out=np.zeros_like(mat, dtype=np.float64),
        where=(row_sum > 0) & np.isfinite(row_sum)
    )

    return out


def get_valid_voxel_indices(dti, block_size, remove_diagonal=True, require_col=False):
    """
    Get valid voxel indices in original voxel coordinate.

    重要说明
    ----------
    返回的 nonzero_all 始终是原始 voxel 维度下的索引。
    也就是说，如果原始 dti 是 [N, N]，那么 nonzero_all 中的值始终在 0 到 N-1 之间。

    筛选逻辑
    ----------
    1. 先去除 grey_matter_size <= 0 或非有限值的体素；
    2. 再在剩余体素构成的 DTI 子矩阵中，迭代删除行和为 0 的孤立体素；
    3. 如果 require_col=True，则同时要求列和也大于 0；
    4. 每次迭代时，用子矩阵上的 valid mask 去筛 nonzero_all，
       保证 nonzero_all 始终是原始索引。

    Parameters
    ----------
    dti : numpy.ndarray, shape [N, N]
        Original DTI matrix.

    block_size : numpy.ndarray, shape [N]
        Original grey matter size.

    remove_diagonal : bool
        Whether to remove diagonal before checking isolated voxels.

    require_col : bool
        Whether to require column sum > 0 as well.

    Returns
    -------
    nonzero_all : numpy.ndarray
        Original voxel indices after filtering.
    """
    if dti.ndim != 2 or dti.shape[0] != dti.shape[1]:
        raise ValueError(f"dti must be a square matrix, got shape={dti.shape}")

    n_vox = dti.shape[0]

    if block_size.ndim != 1:
        block_size = np.asarray(block_size).reshape(-1)

    if block_size.shape[0] != n_vox:
        raise ValueError(
            f"block_size length does not match dti size. "
            f"block_size.shape={block_size.shape}, dti.shape={dti.shape}"
        )

    if np.any(~np.isfinite(dti)):
        nan_count = np.isnan(dti).sum()
        inf_count = np.isinf(dti).sum()
        raise ValueError(f"dti contains NaN or Inf. nan_count={nan_count}, inf_count={inf_count}")

    if np.any(dti < 0):
        neg_count = np.sum(dti < 0)
        raise ValueError(f"dti contains negative values. neg_count={neg_count}")

    if np.any(~np.isfinite(block_size)):
        nan_count = np.isnan(block_size).sum()
        inf_count = np.isinf(block_size).sum()
        raise ValueError(
            f"block_size contains NaN or Inf. nan_count={nan_count}, inf_count={inf_count}"
        )

    # nonzero_all 始终保存原始 voxel 索引
    nonzero_all = np.arange(n_vox, dtype=np.int64)

    # Step 1: 先删除灰质为 0 的体素
    valid_gm = block_size > 0
    nonzero_all = nonzero_all[valid_gm]

    print(f"After grey matter filtering: {len(nonzero_all)} / {n_vox}")

    if len(nonzero_all) == 0:
        raise ValueError("No valid voxels remain after grey matter filtering.")

    # Step 2: 在剩余 DTI 子网络中迭代删除孤立体素
    iteration = 0

    while True:
        iteration += 1

        sub_dti = dti[np.ix_(nonzero_all, nonzero_all)].copy()

        if remove_diagonal:
            np.fill_diagonal(sub_dti, 0)

        row_sum = sub_dti.sum(axis=1)

        valid = np.isfinite(row_sum) & (row_sum > 0)

        if require_col:
            col_sum = sub_dti.sum(axis=0)
            valid = valid & np.isfinite(col_sum) & (col_sum > 0)

        zero_row_count = np.sum(~valid)

        print(
            f"DTI filtering iteration {iteration}: "
            f"current voxels={len(nonzero_all)}, "
            f"invalid voxels={zero_row_count}, "
            f"min row_sum={np.nanmin(row_sum) if len(row_sum) > 0 else 'NA'}, "
            f"max row_sum={np.nanmax(row_sum) if len(row_sum) > 0 else 'NA'}"
        )

        if valid.all():
            break

        print("Removing isolated original voxel indices first 50:", nonzero_all[~valid][:50])

        # 关键：valid 是子矩阵维度的 mask，但筛的是原始索引数组 nonzero_all
        nonzero_all = nonzero_all[valid]

        if len(nonzero_all) == 0:
            raise ValueError("No valid voxels remain after DTI isolated voxel filtering.")

    print(f"Final valid voxel count: {len(nonzero_all)} / {n_vox}")
    print(f"Final valid voxel indices first 100: {nonzero_all[:100]}")

    return nonzero_all


def add_laminar_cortex_model(conn_prob, gm, canonical_voxel=False):
    """
    Process the connection probability matrix, grey matter and degree scale for DTB with pure voxel
    and micro-column structure.

    Each voxel is split into 2 populations E and I when canonical_voxel=True.
    Each micro-column is split into 10 populations when canonical_voxel=False.

    Parameters
    ----------
    conn_prob: numpy.ndarray, shape [N, N]
        connectivity probability matrix between N voxels/micro-columns.

    gm: numpy.ndarray, shape [N]
        normalized grey matter in each voxel/micro-column.

    canonical_voxel: bool
        True for voxel structure; False for micro-column structure.

    Returns
    -------
    out_conn_prob: sparse.COO
        connectivity probability matrix between populations.

    out_gm: numpy.ndarray
        grey matter for populations.

    out_degree_scale: numpy.ndarray
        scale of degree for populations.
    """
    if not canonical_voxel:
        lcm_connect_prob = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3554, 804, 881, 45, 431, 0, 136, 0, 1020],
                [0, 0, 1778, 532, 456, 29, 217, 0, 69, 0, 396],
                [0, 0, 417, 84, 1070, 690, 79, 93, 1686, 0, 1489],
                [0, 0, 168, 41, 628, 538, 36, 0, 1028, 0, 790],
                [0, 0, 2550, 176, 765, 99, 621, 596, 363, 7, 1591],
                [0, 0, 1357, 76, 380, 32, 375, 403, 129, 0, 214],
                [0, 0, 643, 46, 549, 196, 327, 126, 925, 597, 2609],
                [0, 0, 80, 8, 92, 3, 159, 11, 76, 499, 1794],
            ],
            dtype=np.float64
        )

        # ignore the L1 neurons
        lcm_gm = np.array(
            [
                0, 0,
                33.8 * 78, 33.8 * 22,
                34.9 * 80, 34.9 * 20,
                7.6 * 82, 7.6 * 18,
                22.1 * 83, 22.1 * 17
            ],
            dtype=np.float64
        )
    else:
        # canonical voxel: E/I = 4:1
        lcm_connect_prob = np.array(
            [
                [4 / 7, 1 / 7, 2 / 7],
                [4 / 7, 1 / 7, 2 / 7]
            ],
            dtype=np.float64
        )

        lcm_gm = np.array([0.8, 0.2], dtype=np.float64)

    if lcm_gm.sum() <= 0:
        raise ValueError("lcm_gm.sum() <= 0")

    lcm_gm = lcm_gm / lcm_gm.sum()

    syna_nums_in_lcm = lcm_connect_prob.sum(1) * lcm_gm

    denom = syna_nums_in_lcm.sum()
    if denom <= 0:
        raise ValueError("syna_nums_in_lcm.sum() <= 0")

    with np.errstate(divide="ignore", invalid="ignore"):
        lcm_degree_scale = syna_nums_in_lcm / denom / lcm_gm

    lcm_degree_scale = np.where(np.isfinite(lcm_degree_scale), lcm_degree_scale, 0)

    lcm_row_sum = lcm_connect_prob.sum(axis=1, keepdims=True)

    if np.any(lcm_row_sum <= 0):
        bad = np.where(lcm_row_sum[:, 0] <= 0)[0]
        raise ValueError(f"lcm_connect_prob has zero rows: {bad}")

    lcm_connect_prob = lcm_connect_prob / lcm_row_sum

    if conn_prob.shape[0] == 1:
        conn_prob[:, :] = 1
    else:
        conn_prob = conn_prob.copy()
        conn_prob[np.diag_indices(conn_prob.shape[0])] = 0

        row_sum = conn_prob.sum(axis=1, keepdims=True)

        if np.any((row_sum <= 0) | (~np.isfinite(row_sum))):
            bad = np.where((row_sum[:, 0] <= 0) | (~np.isfinite(row_sum[:, 0])))[0]
            raise ValueError(
                f"conn_prob has invalid rows inside add_laminar_cortex_model "
                f"after removing diagonal. bad count={len(bad)}, bad first 50={bad[:50]}"
            )

        conn_prob = conn_prob / row_sum

    if np.any(~np.isfinite(conn_prob)):
        nan_count = np.isnan(conn_prob).sum()
        inf_count = np.isinf(conn_prob).sum()
        raise ValueError(
            f"conn_prob contains NaN or Inf after normalization. "
            f"nan_count={nan_count}, inf_count={inf_count}"
        )

    if np.any(conn_prob < 0):
        neg_count = np.sum(conn_prob < 0)
        raise ValueError(f"conn_prob contains negative values after normalization. neg_count={neg_count}")

    out_gm = (gm[:, None] * lcm_gm[None, :]).reshape([-1])

    out_degree_scale = np.broadcast_to(
        lcm_degree_scale[None, :],
        [gm.shape[0], lcm_gm.shape[0]]
    ).reshape([-1])

    conn_prob = sparse.COO(conn_prob)

    # only e5 is allowed to output.
    corrds1 = np.empty(
        [4, conn_prob.coords.shape[1] * lcm_connect_prob.shape[0]],
        dtype=np.int64
    )

    if not canonical_voxel:
        corrds1[3, :] = 6
    else:
        corrds1[3, :] = 0

    corrds1[(0, 2), :] = np.broadcast_to(
        conn_prob.coords[:, :, None],
        [2, conn_prob.coords.shape[1], lcm_connect_prob.shape[0]]
    ).reshape([2, -1])

    corrds1[(1), :] = np.broadcast_to(
        np.arange(lcm_connect_prob.shape[0], dtype=np.int64)[None, :],
        [conn_prob.coords.shape[1], lcm_connect_prob.shape[0]]
    ).reshape([1, -1])

    data1 = (conn_prob.data[:, None] * lcm_connect_prob[:, -1]).reshape([-1])

    lcm_connect_prob_inner = sparse.COO(lcm_connect_prob[:, :-1])

    corrds2 = np.empty(
        [4, conn_prob.shape[0] * lcm_connect_prob_inner.data.shape[0]],
        dtype=np.int64
    )

    corrds2[0, :] = np.broadcast_to(
        np.arange(conn_prob.shape[0], dtype=np.int64)[:, None],
        [conn_prob.shape[0], lcm_connect_prob_inner.data.shape[0]]
    ).reshape([-1])

    corrds2[2, :] = corrds2[0, :]

    corrds2[(1, 3), :] = np.broadcast_to(
        lcm_connect_prob_inner.coords[:, None, :],
        [2, conn_prob.shape[0], lcm_connect_prob_inner.coords.shape[1]]
    ).reshape([2, -1])

    data2 = np.broadcast_to(
        lcm_connect_prob_inner.data[None, :],
        [conn_prob.shape[0], lcm_connect_prob_inner.coords.shape[1]]
    ).reshape([-1])

    out_conn_prob = sparse.COO(
        coords=np.concatenate([corrds1, corrds2], axis=1),
        data=np.concatenate([data1, data2], axis=0),
        shape=[
            conn_prob.shape[0],
            lcm_connect_prob.shape[0],
            conn_prob.shape[1],
            lcm_connect_prob.shape[1] - 1
        ]
    )

    out_conn_prob = out_conn_prob.reshape(
        (
            conn_prob.shape[0] * lcm_connect_prob.shape[0],
            conn_prob.shape[1] * (lcm_connect_prob.shape[1] - 1)
        )
    )

    if conn_prob.shape[0] == 1:
        out_conn_prob = out_conn_prob / out_conn_prob.sum(axis=1, keepdims=True)

    return out_conn_prob, out_gm, out_degree_scale


def find_mat_file(root_path):
    """
    Find one .mat file under root_path.
    """
    mat_files = []

    for fname in os.listdir(root_path):
        file_path = os.path.join(root_path, fname)

        if os.path.isfile(file_path) and fname.endswith(".mat"):
            mat_files.append(file_path)

    if len(mat_files) == 0:
        raise FileNotFoundError(f"No .mat file found in root_path={root_path}")

    if len(mat_files) > 1:
        print("Warning: multiple .mat files found. Use the first one:")
        for f in mat_files:
            print("  ", f)

    return mat_files[0]


def test_generate_normal_voxel_whole_brain_int_ext(
    root_path="../data/Clinical_sample/sub-000113174215",
    degree=100,
    minimum_neurons_for_block=(200, 50),
    scale=int(1e8),
    dtype="uint8"
):
    print(f"running test_generate_normal_regional_whole_brain for {root_path}")

    # make dirs
    blocks = scale // 12500000
    if scale % 12500000 != 0:
        blocks = blocks + 1

    first_path, second_path = make_directory_tree(
        root_path,
        scale,
        degree,
        "blocks{}_int_ext".format(blocks),
        dtype=dtype
    )

    print(f"Total {scale} neurons for DTB, merge to {blocks} blocks")

    # load data
    mat_files = find_mat_file(root_path)
    print(f"Loading mat file {mat_files}")

    file = h5py.File(mat_files, "r")

    block_size_raw = np.asarray(file["grey_matter_size"][0], dtype=np.float64)
    dti_raw = np.asarray(file["dti_net_full"], dtype=np.float32)

    if dti_raw.ndim != 2 or dti_raw.shape[0] != dti_raw.shape[1]:
        raise ValueError(f"dti_net_full should be square matrix, got shape={dti_raw.shape}")

    n_vox = dti_raw.shape[0]

    if block_size_raw.shape[0] != n_vox:
        raise ValueError(
            f"grey_matter_size length does not match dti size. "
            f"grey_matter_size.shape={block_size_raw.shape}, dti.shape={dti_raw.shape}"
        )

    # remove diagonal self-connection
    dti_raw = dti_raw.copy()
    dti_raw[np.diag_indices_from(dti_raw)] = 0

    print(f"Original voxel number: {n_vox}")
    print(f"dti shape: {dti_raw.shape}")
    print(f"block_size shape: {block_size_raw.shape}")
    print(f"dti nan count: {np.isnan(dti_raw).sum()}")
    print(f"dti inf count: {np.isinf(dti_raw).sum()}")
    print(f"dti negative count: {np.sum(dti_raw < 0)}")
    print(f"block_size positive count: {np.sum(block_size_raw > 0)}")

    # ----------------------------------------------------------------------
    # 关键修改：
    # 先去除灰质为 0 的体素；
    # 再在剩余 DTI 子矩阵中迭代删除孤立体素；
    # nonzero_all 始终是原始 voxel 索引。
    # ----------------------------------------------------------------------
    nonzero_all = get_valid_voxel_indices(
        dti=dti_raw,
        block_size=block_size_raw,
        remove_diagonal=True,
        require_col=False
    )

    print(f"valid voxel index length {len(nonzero_all)}")
    print(f"valid voxel index first 100 {nonzero_all[:100]}")

    # ----------------------------------------------------------------------
    # saving atlas_region data
    # 所有 voxel 级数据都用最终的 nonzero_all 进行筛选。
    # ----------------------------------------------------------------------
    atlas_region_raw = np.asarray(file["atlas_region"][0])
    uni_region = np.asarray(file["uni_region"][0])
    is_cortex = np.asarray(file["is_cortex"][0])
    voxel_label_raw = np.asarray(file["voxel_label"][0])

    if atlas_region_raw.shape[0] != n_vox:
        raise ValueError(
            f"atlas_region length does not match dti size. "
            f"atlas_region.shape={atlas_region_raw.shape}, n_vox={n_vox}"
        )

    if voxel_label_raw.shape[0] != n_vox:
        raise ValueError(
            f"voxel_label length does not match dti size. "
            f"voxel_label.shape={voxel_label_raw.shape}, n_vox={n_vox}"
        )

    atlas_region = atlas_region_raw[nonzero_all]
    voxel_label = voxel_label_raw[nonzero_all]

    region_in_data = np.empty(uni_region.shape, dtype=bool)

    for i in range(len(uni_region)):
        region_in_data[i] = uni_region[i] in atlas_region

    np.savez(
        os.path.join(first_path, "supplementary_info", "atlas_region.npz"),
        atlas_region=atlas_region,
        uni_region=uni_region,
        is_cortex=is_cortex,
        region_in_data=region_in_data,
        voxel_label=voxel_label
    )

    print("Saved atlas_region.npz")
    print(f"atlas_region filtered shape: {atlas_region.shape}")
    print(f"voxel_label filtered shape: {voxel_label.shape}")

    # ----------------------------------------------------------------------
    # saving BOLD signals
    # 注意：原代码是读取后转置，然后用 [:, nonzero_all] 筛选 voxel 维度。
    # ----------------------------------------------------------------------
    rest_bold = np.array(file["rest_state_bold"]).T

    if rest_bold.shape[1] != n_vox:
        raise ValueError(
            f"rest_state_bold voxel dimension does not match dti size after transpose. "
            f"rest_bold.shape={rest_bold.shape}, n_vox={n_vox}"
        )

    rest_bold = rest_bold[:, nonzero_all]

    np.save(
        os.path.join(first_path, "supplementary_info", "rest_state_bold.npy"),
        rest_bold
    )

    print(f"Saved rest_state_bold.npy, shape={rest_bold.shape}")

    # MID task
    task_bold = np.array(file["MID_task_bold"]).T

    if task_bold.shape[1] != n_vox:
        raise ValueError(
            f"MID_task_bold voxel dimension does not match dti size after transpose. "
            f"task_bold.shape={task_bold.shape}, n_vox={n_vox}"
        )

    task_bold = task_bold[:, nonzero_all]

    np.save(
        os.path.join(first_path, "supplementary_info", "MID_task_bold.npy"),
        task_bold
    )

    print(f"Saved MID_task_bold.npy, shape={task_bold.shape}")

    # SST task
    task_bold = np.array(file["SST_task_bold"]).T

    if task_bold.shape[1] != n_vox:
        raise ValueError(
            f"SST_task_bold voxel dimension does not match dti size after transpose. "
            f"task_bold.shape={task_bold.shape}, n_vox={n_vox}"
        )

    task_bold = task_bold[:, nonzero_all]

    np.save(
        os.path.join(first_path, "supplementary_info", "SST_task_bold.npy"),
        task_bold
    )

    print(f"Saved SST_task_bold.npy, shape={task_bold.shape}")

    # EFT task
    # if "EFT_task_bold" in file:
    #     task_bold = np.array(file["EFT_task_bold"]).T
    #
    #     if task_bold.shape[1] != n_vox:
    #         raise ValueError(
    #             f"EFT_task_bold voxel dimension does not match dti size after transpose. "
    #             f"task_bold.shape={task_bold.shape}, n_vox={n_vox}"
    #         )
    #
    #     task_bold = task_bold[:, nonzero_all]
    #
    #     np.save(
    #         os.path.join(first_path, "supplementary_info", "EFT_task_bold.npy"),
    #         task_bold
    #     )
    #
    #     print(f"Saved EFT_task_bold.npy, shape={task_bold.shape}")

    # ----------------------------------------------------------------------
    # generate conn_prob for populations from voxel to population
    # ----------------------------------------------------------------------
    block_size = block_size_raw[nonzero_all].astype(np.float64)

    if np.any(~np.isfinite(block_size)):
        raise ValueError("Filtered block_size contains NaN or Inf.")

    if np.any(block_size <= 0):
        bad = np.where(block_size <= 0)[0]
        raise ValueError(
            f"Filtered block_size still contains non-positive values. "
            f"bad count={len(bad)}, bad first 50={bad[:50]}"
        )

    block_size_sum = block_size.sum()

    if block_size_sum <= 0:
        raise ValueError("Filtered block_size.sum() <= 0.")

    block_size = block_size / block_size_sum

    conn_prob = dti_raw[np.ix_(nonzero_all, nonzero_all)].astype(np.float64)
    np.fill_diagonal(conn_prob, 0)

    row_sum = conn_prob.sum(axis=1)

    zero_rows = np.where((row_sum <= 0) | (~np.isfinite(row_sum)))[0]

    if len(zero_rows) > 0:
        raise ValueError(
            f"conn_prob has invalid rows before normalization. "
            f"bad count={len(zero_rows)}, "
            f"bad local indices first 50={zero_rows[:50]}, "
            f"bad original voxel indices first 50={nonzero_all[zero_rows[:50]]}, "
            f"row_sum first 50={row_sum[zero_rows[:50]]}"
        )

    conn_prob = conn_prob / row_sum[:, None]

    if np.any(~np.isfinite(conn_prob)):
        raise ValueError("conn_prob contains NaN or Inf after normalization.")

    if np.any(conn_prob < 0):
        raise ValueError("conn_prob contains negative values after normalization.")

    print(f"conn_prob shape before laminar model: {conn_prob.shape}")
    print(f"block_size shape before laminar model: {block_size.shape}")
    print(f"conn_prob row_sum min after normalize: {conn_prob.sum(axis=1).min()}")
    print(f"conn_prob row_sum max after normalize: {conn_prob.sum(axis=1).max()}")

    conn_prob, block_size, degree_scale = add_laminar_cortex_model(
        conn_prob,
        block_size,
        canonical_voxel=True
    )

    print(f"conn_prob shape after laminar model: {conn_prob.shape}")
    print(f"block_size shape after laminar model: {block_size.shape}")
    print(f"degree_scale shape after laminar model: {degree_scale.shape}")

    # default parameters
    # gui = np.array([0.0008, 0.00027282, 0.00565657, 0.00066528]) # ou, from wjx
    gui = np.array([0.0008, 0.0008, 0.0015, 0])

    degree_ = np.maximum((degree * degree_scale).astype(np.uint16), 1)

    kwords = [
        {
            "V_th": -50,
            "V_reset": -65,
            "g_Li": 0.03,
            "g_ui": gui,
            "tao_ui": (2, 2, 10, 50),
            "noise_rate": 0,
            "size": int(max(b * scale, minimum_neurons_for_block[i % 2]))
        }
        for i, b in enumerate(block_size)
    ]

    population_base = np.array(
        [kword["size"] for kword in kwords],
        dtype=np.int64
    )

    population_base = np.add.accumulate(population_base)
    population_base = np.insert(population_base, 0, 0)

    np.save(
        os.path.join(first_path, "supplementary_info", "population_base.npy"),
        population_base
    )

    print(f"Saved population_base.npy, shape={population_base.shape}")
    print(f"Total generated population neurons: {population_base[-1]}")

    # make block
    conn = connect_for_multi_sparse_block(
        conn_prob,
        kwords,
        degree=degree_,
        dtype=dtype
    )

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(f"MPI rank {rank}/{size} starts merging blocks.")

    for i in range(rank, blocks, size):
        print(f"MPI rank {rank} processing block {i} / {blocks}")

        merge_dti_distributation_block(
            conn,
            second_path,
            MPI_rank=i,
            number=blocks,
            avg_degree=degree,
            dtype=dtype,
            debug_block_dir=None,
            # debug_block_dir="/public/home/ssct004t/project/zenglb/Digital_twin_brain/data/small_blocks/d1000_ou/uint8",
            # only_load=(i != 0)
            only_load=False
        )

    print(f"MPI rank {rank} finished.")


if __name__ == "__main__":
    args = get_args()

    test_generate_normal_voxel_whole_brain_int_ext(
        root_path=args.block_dir,
        scale=args.scale,
        degree=args.degree
    )
