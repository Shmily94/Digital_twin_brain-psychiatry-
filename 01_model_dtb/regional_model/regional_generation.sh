#!/bin/bash

# 目标目录
TARGET_DIR="/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data/Regional_data/HC"

# SLURM脚本路径
SLURM_SCRIPT="regional_generation.slurm"

start=0

# 遍历目标目录中的文件夹
for folder in "$TARGET_DIR"/*; do
    # 检查是否为文件夹
    if [ -d "$folder" ]; then
        folder_name=$(basename "$folder") # 获取文件夹名

        # if [ "$folder_name" = "000112517217" ]; then
        #     echo "Skipping folder: $folder_name"
        #     continue  # 跳过当前循环，继续下一个文件夹
        # fi

        # 修改 regional_generation.slurm 文件的第16行
        sed -i "18c \ \ --block_dir=$TARGET_DIR/$folder_name \\\\" "$SLURM_SCRIPT"

        # 检查剩余节点数是否足够
        while true; do
            # node_num=$(sinfo -p DCUq30 -h -o "%A" | awk -F'/' '{print $2}')
            # echo "当前剩余节点数: $node_num"
            if [ "$start" -eq 0 ]; then
                # 直接提交任务
                sbatch "$SLURM_SCRIPT"
                echo "First run: Submitted job for folder: $folder_name"
                start=1
                break # 跳出等待循环，继续处理下一个文件夹
            else
                node_num=$(squeue -h -n psj_generation -o "%D" | awk '{sum += $1} END {print (sum == "" ? 0 : sum)}')
                echo "psj_generation任务占用的总节点数: $node_num"
                if [ "$node_num" -lt 160 ]; then
                    # 提交任务
                    sbatch "$SLURM_SCRIPT"
                    echo "Submitted job for folder: $folder_name"
                    break # 跳出等待循环，继续处理下一个文件夹
                else
                    echo "Insufficient nodes for folder: $folder_name. Available nodes: $available_nodes"
                    echo "Waiting for 1 hour before retrying..."
                    sleep 180 # 等待
                fi
            fi
        done

        sleep 20
    fi
done

# nohup bash regional_generation.sh > regional_generation_HC.log 2>&1 &