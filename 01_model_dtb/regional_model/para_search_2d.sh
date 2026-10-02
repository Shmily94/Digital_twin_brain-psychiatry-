#!/bin/bash
# Array to store IP addresses of servers
declare -a job_id_array
declare -a ip_array
declare -a job_id_array_client
declare -a ampa_task_array
declare -a gaba_task_array

multiply_value=($(seq 0.0005 0.0005 0.0040))

num_elements=${#multiply_value[@]}
echo $num_elements
NUM_SERVERS=${num_elements}
NUM_TASKS=${num_elements}
# Submit server jobs and store IP addresses
for ((i=0; i<NUM_SERVERS; i++)); do
    echo $i
    server_file="server_test.slurm"
    job_id=$(sbatch $server_file 8 2>&1 | tr -cd "[0-9]")
    job_id_array[i]=$job_id
    echo $job_id
done
sleep 120

for ((i=0; i<NUM_SERVERS; i++)); do
    job_id=${job_id_array[i]}
    echo $job_id
    job_out_file="slurm-${job_id}.out"
    ip=$(grep -oP 'Server listening on \K[0-9.]+(?=:50051)' $job_out_file)
    ip_array[i]=$ip
    echo $ip
done

# Submit client jobs with modified parameters
for ((i=0; i<NUM_TASKS; i++)); do
    echo "value is ${multiply_value[i]}"
    client_file="simulation_para_search_int_ext.slurm"
    # sed -in "16c ampa=${multiply_value[i]} " $client_file
    sed -in "27c gaba=${multiply_value[i]} " $client_file
    # sed -in "18c Iext=${multiply_value[i]} " $client_file
    # sed -in "19c tau_gaba=${multiply_value[i]} " $client_file
    job_id_client=$(sbatch $client_file ${ip_array[i]} 8 2>&1 | tr -cd "[0-9]")
    job_id_array_client[i]=$job_id_client
    echo “submit to job $job_id_client”
    sleep 30
done


# nohup bash para_search_2d.sh > para_search_2d_3m.log 2>&1 &
# pgrep -f para_search_1d.sh
