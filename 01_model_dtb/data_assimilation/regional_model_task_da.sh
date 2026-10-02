#!/bin/bash
# Array to store IP addresses of servers
declare -a job_id_array
declare -a ip_array
declare -a job_id_array_client
declare -a ampa_task_array
declare -a gaba_task_array

# 函数：检查作业状态
check_job_status() {
    local job_id=$1
    local status=$(sacct -j $job_id --format=State -n | head -n 1 | tr -d ' ')
    echo $status
}

# 函数：取消作业
cancel_job() {
    local job_id=$1
    if [ ! -z "$job_id" ]; then
        scancel $job_id
        echo "Cancelled job $job_id"
    fi
}

# 函数：提交一对server-client任务
submit_job_pair() {
    local index=$1
    local client_file=$2
    local sub_name=$3
    local sub_set=$4
    local retry_count=0
    local max_retries=5
    local success=false

    {
        while [ $retry_count -lt $max_retries ] && [ "$success" = false ]; do
            echo "Attempting to submit job pair $index (attempt $((retry_count + 1)))"
            
            # 提交server任务
            local server_file="server_dtb_regional.slurm"
            local server_job_id=$(sbatch $server_file 2>&1 | tr -cd "[0-9]")
            echo "Submitted server job: $server_job_id"
            
            # 等待server启动并获取IP
            local ip=""
            local wait_count=0
            local max_wait=120  # 最多等待20*30=600秒
            
            while [ $wait_count -lt $max_wait ]; do
                sleep 30
                local server_status=$(check_job_status $server_job_id)
                if [[ $server_status == "FAILED" || $server_status == "TIMEOUT" || $server_status == "CANCELLED" || $server_status == "CANCELLED+" || $server_status == "NODE_FAIL" ]]; then
                    echo "Server job $server_job_id failed with status $server_status"
                    break
                fi
                cd ./log/
                local job_out_file="${server_job_id}.o"
                if [ -f "$job_out_file" ]; then
                    ip=$(grep -oP 'Server listening on \K[0-9.]+:[0-9]+' $job_out_file)
                    if [ ! -z "$ip" ]; then
                        echo "Got IP: $ip"
                        cd ..
                        break
                    fi
                fi
                cd ..
                ((wait_count++))
            done

            if [ -z "$ip" ]; then
                echo "Failed to get IP for server job $server_job_id"
                cancel_job $server_job_id
                ((retry_count++))
                continue
            fi

            # 提交client任务
            local client_job_id=$(sbatch $client_file $ip $sub_name $sub_set 2>&1 | tr -cd "[0-9]")
            echo "Submitted client job: $client_job_id for $sub_set/$sub_name"

            sleep 60

            # 等待并检查两个任务的完成状态
            while true; do
                local server_status=$(check_job_status $server_job_id)
                local client_status=$(check_job_status $client_job_id)
                
                echo "Server job $server_job_id status: $server_status"
                echo "Client job $client_job_id status: $client_status"

                if [[ $server_status == "FAILED" || $server_status == "TIMEOUT" || $server_status == "CANCELLED" || $server_status == "CANCELLED+" || $server_status == "NODE_FAIL" || \
                      $client_status == "FAILED" || $client_status == "TIMEOUT" || $client_status == "CANCELLED" || $client_status == "CANCELLED+" || $client_status == "NODE_FAIL" ]]; then
                    echo "One or both jobs failed, cancelling both and retrying"
                    cancel_job $server_job_id
                    cancel_job $client_job_id
                    break
                fi

                if [[ $server_status == "COMPLETED" && $client_status == "COMPLETED" ]]; then
                    echo "Both jobs completed successfully"
                    success=true
                    break
                fi

                if [[ $server_status == "RUNNING" || $server_status == "PENDING" || \
                      $client_status == "RUNNING" || $client_status == "PENDING" ]]; then
                    sleep 1000
                    continue
                fi
            done

            ((retry_count++))
        done

        if [ "$success" = false ]; then
            echo "Failed to submit job pair $index after $max_retries attempts"
        fi
    } &  # 在后台运行
}

# 主循环
# 目标目录
group="HC2"
TARGET_DIR="/home1/dtbrain/project/psj/Digital_twin_brain/data/Regional_data_selected/$group"
# NUM_TASKS=3

# 将所有文件夹存入数组
folders=()
while IFS= read -r -d '' folder; do
    if [ -d "$folder" ]; then
        folders+=("$folder")
    fi
done < <(find "$TARGET_DIR" -maxdepth 1 -mindepth 1 -type d -print0)

# 设置起始和结束的批次
# start_index=0  
# end_index=9

for ((k=1; k<=30; k++)); do

    folder="${folders[$k]}"
    folder_name=$(basename "$folder")

    while true; do
        # 获取剩余节点数
        node_num=$(sinfo -p DCUq30 -h -o "%A" | awk -F'/' '{print $2}')
        echo "当前剩余节点数: $node_num"
        # 检查节点数是否足够
        if [ "$node_num" -gt 7 ]; then
            client_file="test_da_task_MID_full_int_ext_batch.slurm"
            echo "Launching MID da for sub $k $folder_name"
            submit_job_pair $k "$client_file" "$folder_name" "$group"
            break
        else
            echo "节点数不足，等待 10 分钟后重新检查..."
            sleep 600  # 等待 10 分钟 (600 秒)
        fi
    done

    while true; do
        # 获取剩余节点数
        node_num=$(sinfo -p DCUq30 -h -o "%A" | awk -F'/' '{print $2}')
        echo "当前剩余节点数: $node_num"
        # 检查节点数是否足够
        if [ "$node_num" -gt 7 ]; then
            client_file="test_da_task_SST_full_int_ext_batch.slurm"
            echo "Launching SST da for sub $k $folder_name"
            submit_job_pair $k "$client_file" "$folder_name" "$group"
            break
        else
            echo "节点数不足，等待 10 分钟后重新检查..."
            sleep 600  # 等待 10 分钟 (600 秒)
        fi
    done

    sleep 100
done

echo "Task da of $group done!"

# for ((k=start_index; k<=end_index; k++)); do
#     echo "Starting batch $k"

#     for ((i=0; i<NUM_TASKS; i++)); do
#         actual_count=$((k * NUM_TASKS + i))
#         client_file_1="test_da_task_MID_full_int_ext_batch.slurm"
#         client_file_2="test_da_task_SST_full_int_ext_batch.slurm"

#         if [ $actual_count -ge ${#folders[@]} ]; then
#             echo "Warning: Requested index $actual_count exceeds number of available folders"
#             break
#         fi

#         folder="${folders[$actual_count]}"
#         folder_name=$(basename "$folder")
        
#         # 并行提交所有任务对
#         echo "Launching job pair $actual_count"
#         submit_job_pair $actual_count "$client_file_1" "$folder_name" "$group"
#         submit_job_pair $actual_count "$client_file_2" "$folder_name" "$group"
#         sleep 100
#     done

#     # 等待所有任务完成
#     wait
# done



# nohup bash regional_model_task_da.sh > regional_model_task_da_MDD_3m_nc.log 2>&1 &
# pgrep -f regional_model_task_da.sh
# pkill -f regional_model_task_da
# scancel -n server_da_psj_regional
# scancel -n task_da_psj_batch