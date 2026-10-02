#!/bin/bash
# Array to store IP addresses of servers
declare -a job_id_array
declare -a ip_array
declare -a job_id_array_client
declare -a ampa_task_array
declare -a gaba_task_array

multiply_value=($(seq 5 10 45))

num_elements=${#multiply_value[@]}
echo $num_elements
NUM_SERVERS=${num_elements}
NUM_TASKS=${num_elements}
# Submit server jobs and store IP addresses
for ((i=0; i<NUM_SERVERS; i++)); do
    echo $i
    server_file="server_dtb.slurm"
    job_id=$(sbatch $server_file 2>&1 | tr -cd "[0-9]")
    job_id_array[i]=$job_id
    echo $job_id
done
sleep 120

cd log

for ((i=0; i<NUM_SERVERS; i++)); do
    job_id=${job_id_array[i]}
    echo $job_id
    job_out_file="${job_id}.o"
    str_row_ip=$(cat $job_out_file | grep 'listening' | sed -n 1p)
    ip=$(echo $str_row_ip | tr -cd "[0-9][.][:]")
    ip_array[i]=$ip
    echo $ip
done

cd ../
# Submit client jobs with modified parameters
for ((i=0; i<NUM_TASKS; i++)); do
    echo "value is ${multiply_value[i]}"
    client_file="simulation_para_search_int_ext.slurm"
    # sed -in "16c ampa=${multiply_value[i]} " $client_file
    # sed -in "17c gaba=${multiply_value[i]} " $client_file
    # sed -in "18c Iext=${multiply_value[i]} " $client_file
    sed -in "19c tau_gaba=${multiply_value[i]} " $client_file
    sed -in "36c \ \ --ip=${ip_array[i]} \\\\" $client_file
    job_id_client=$(sbatch $client_file 2>&1 | tr -cd "[0-9]")
    job_id_array_client[i]=$job_id_client
    echo “submit to job $job_id_client”
    sleep 10
done


# nohup bash para_search_1d.sh > para_search_Iext.log 2>&1 &
# pgrep -f para_search_1d.sh
