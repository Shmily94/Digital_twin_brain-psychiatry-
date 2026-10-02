#!/bin/bash
# Submit all requested subject-task simulations.
#
# Design:
#   1. Every subject-task pair gets a fresh, dedicated 4-DCU server job.
#   2. MID and SST never reuse the same server job.
#   3. Within one subject-task pair, four conditions run concurrently:
#        50051 -> baseline
#        50052 -> AMPA
#        50053 -> GABA
#        50054 -> AMPA + GABA
#   4. Twelve subjects are arranged as three balanced batches of four.
#   5. A new batch starts only after all clients in the current batch finish.
#
# Examples:
#   nohup env TASKS=MID,SST bash submit_all_subject_tasks.sh > submit_all.out 2>&1 &
#   nohup env TASKS=MID bash submit_all_subject_tasks.sh > submit_mid.out 2>&1 &
#   nohup env TASKS=SST bash submit_all_subject_tasks.sh > submit_sst.out 2>&1 &

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_SCRIPT="${SCRIPT_DIR}/server_test.slurm"
MID_SCRIPT="${SCRIPT_DIR}/MID_batch.slurm"
SST_SCRIPT="${SCRIPT_DIR}/SST_batch_10m.slurm"
DATA_ROOT=/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data

POLL_SECONDS="${POLL_SECONDS:-10}"
SERVER_IP_WAIT_SECONDS="${SERVER_IP_WAIT_SECONDS:-30}"
SERVER_READY_TIMEOUT_SECONDS="${SERVER_READY_TIMEOUT_SECONDS:-900}"
SERVER_WARMUP_SECONDS="${SERVER_WARMUP_SECONDS:-20}"
TASKS_CSV="${TASKS:-MID,SST}"

for numeric_setting in \
    POLL_SECONDS \
    SERVER_IP_WAIT_SECONDS \
    SERVER_READY_TIMEOUT_SECONDS \
    SERVER_WARMUP_SECONDS
do
    value="${!numeric_setting}"
    if ! [[ "${value}" =~ ^[0-9]+$ ]]; then
        echo "ERROR: ${numeric_setting} must be a non-negative integer; received ${value}." >&2
        exit 2
    fi
done

if (( POLL_SECONDS < 1 || SERVER_READY_TIMEOUT_SECONDS < 1 )); then
    echo "ERROR: POLL_SECONDS and SERVER_READY_TIMEOUT_SECONDS must be positive." >&2
    exit 2
fi

for script in "${SERVER_SCRIPT}" "${MID_SCRIPT}" "${SST_SCRIPT}"; do
    if [[ ! -f "${script}" ]]; then
        echo "ERROR: missing script: ${script}" >&2
        exit 2
    fi
done

IFS=',' read -r -a TASKS <<< "${TASKS_CSV}"

for task in "${TASKS[@]}"; do
    case "${task}" in
        MID|SST)
            ;;
        *)
            echo "ERROR: TASKS may contain only MID and/or SST; received: ${task}" >&2
            exit 2
            ;;
    esac
done

BATCH_1=(
    "Clinical_sample|sub-000111086310"
    "Clinical_sample|sub-000112517217"
    "Control_sample|sub-000000112288"
    "Control_sample|sub-000016275727"
)

BATCH_2=(
    "Clinical_sample|sub-000113174215"
    "Clinical_sample|sub-000168370463"
    "Control_sample|sub-000044576096"
    "Control_sample|sub-000063218063"
)

BATCH_3=(
    "Clinical_sample|sub-000182136619"
    "Clinical_sample|sub-000191996808"
    "Control_sample|sub-000067342911"
    "Control_sample|sub-000067844279"
)

is_special_subject() {
    case "$1/$2" in
        Clinical_sample/sub-000182136619|\
        Clinical_sample/sub-000113174215|\
        Control_sample/sub-000000112288)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

resolve_hp_path() {
    local task="$1"
    local group="$2"
    local subject="$3"
    local hp_root="${DATA_ROOT}/${group}/${subject}/dti_distribution_100m_d100_blocks8_int_ext"

    if is_special_subject "${group}" "${subject}"; then
        printf '%s/DA/task_da/hp_%s.npy\n' "${hp_root}" "${task}"
    else
        printf '%s/DA/DTB_task_IMAGEN_voxel_task_%s_full_0.1_0.45_0.25_0.5_30/assimilation/hp.npy\n' \
            "${hp_root}" "${task}"
    fi
}

all_subject_entries() {
    printf '%s\n' "${BATCH_1[@]}" "${BATCH_2[@]}" "${BATCH_3[@]}"
}

preflight_paths() {
    local errors=0
    local entry group subject task block_path hp_path

    echo "===== Preflight data-path check ====="

    while IFS= read -r entry; do
        IFS='|' read -r group subject <<< "${entry}"
        block_path="${DATA_ROOT}/${group}/${subject}/dti_distribution_10m_d100_blocks1_int_ext"

        if [[ -d "${block_path}" ]]; then
            echo "[OK] block ${group}/${subject}"
        else
            echo "[MISSING] ${block_path}" >&2
            errors=1
        fi

        for task in "${TASKS[@]}"; do
            hp_path="$(resolve_hp_path "${task}" "${group}" "${subject}")"

            if [[ -f "${hp_path}" ]]; then
                echo "[OK] ${task} HP ${group}/${subject}"
            else
                echo "[MISSING] ${hp_path}" >&2
                errors=1
            fi
        done
    done < <(all_subject_entries)

    if (( errors != 0 )); then
        echo "ERROR: preflight failed; no jobs were submitted." >&2
        return 1
    fi
}

job_is_active() {
    local job_id="$1"
    [[ -n "$(squeue -h -j "${job_id}" -o '%i' 2>/dev/null || true)" ]]
}

queue_state() {
    local job_id="$1"
    squeue -h -j "${job_id}" -o '%T' 2>/dev/null | awk 'NF {print $1; exit}'
}

job_state() {
    local job_id="$1"
    local state=""

    # Accounting can lag briefly after a job leaves squeue.
    for _ in {1..12}; do
        state=$(
            sacct -n -X -j "${job_id}" --format=State 2>/dev/null |
            awk 'NF {print $1; exit}'
        )

        if [[ -n "${state}" ]]; then
            printf '%s\n' "${state}"
            return 0
        fi

        sleep 5
    done

    printf '%s\n' UNKNOWN
}

wait_for_server_running() {
    local server_job_id="$1"
    local state=""
    local accounting_state=""

    while true; do
        state="$(queue_state "${server_job_id}")"

        case "${state}" in
            RUNNING)
                echo "Server job ${server_job_id} is RUNNING." >&2
                return 0
                ;;
            PENDING|CONFIGURING|RESIZING)
                echo "Waiting for server job ${server_job_id}; state=${state}." >&2
                ;;
            COMPLETING)
                echo "ERROR: server job ${server_job_id} entered COMPLETING before becoming usable." >&2
                return 1
                ;;
            "")
                accounting_state="$(job_state "${server_job_id}")"
                case "${accounting_state}" in
                    FAILED*|CANCELLED*|TIMEOUT*|NODE_FAIL*|OUT_OF_MEMORY*|PREEMPTED*|BOOT_FAIL*|DEADLINE*)
                        echo "ERROR: server job ${server_job_id} ended with state ${accounting_state}." >&2
                        return 1
                        ;;
                    *)
                        echo "Waiting for server job ${server_job_id}; squeue state unavailable, sacct=${accounting_state}." >&2
                        ;;
                esac
                ;;
            *)
                echo "Waiting for server job ${server_job_id}; state=${state}." >&2
                ;;
        esac

        sleep "${POLL_SECONDS}"
    done
}

wait_for_server_ready() {
    local server_job_id="$1"
    local server_log="$2"
    local start_time elapsed endpoints endpoint_count port_count ip_count
    local actual_ip required_port all_ports_ready

    start_time=$(date +%s)

    while true; do
        endpoints=""

        if [[ -f "${server_log}" ]]; then
            if grep -Eq \
                'ERROR: server process|unresolved dynamic libraries|unresolved runtime symbols|could not access|could not execute|unable to launch|incorrect libstdc\+\+' \
                "${server_log}"
            then
                echo "ERROR: server ${server_job_id} reported a startup failure." >&2
                tail -n 180 "${server_log}" >&2 || true
                return 1
            fi

            # Use the addresses actually reported by dist_simulator. Do not use
            # BACKEND_IP, which may belong to the management network (10.5.*).
            endpoints=$(
                grep -oE \
                    'Server listening on ([0-9]{1,3}\.){3}[0-9]{1,3}:5005[1-4]' \
                    "${server_log}" |
                sed 's/^Server listening on //' |
                sort -u || true
            )

            endpoint_count=$(printf '%s\n' "${endpoints}" | awk 'NF' | wc -l)
            port_count=$(printf '%s\n' "${endpoints}" | awk -F: 'NF {print $NF}' | sort -u | wc -l)
            ip_count=$(printf '%s\n' "${endpoints}" | sed -E '/^$/d; s/:[0-9]+$//' | sort -u | wc -l)

            all_ports_ready=1
            for required_port in 50051 50052 50053 50054; do
                if ! grep -qE ":${required_port}$" <<< "${endpoints}"; then
                    all_ports_ready=0
                    break
                fi
            done

            if (( endpoint_count >= 4 &&
                  port_count == 4 &&
                  ip_count == 1 &&
                  all_ports_ready == 1 )); then

                actual_ip=$(printf '%s\n' "${endpoints}" | awk 'NF {print; exit}' | sed -E 's/:[0-9]+$//')

                echo "Server ${server_job_id} reported all four actual endpoints:" >&2
                while IFS= read -r endpoint; do
                    [[ -n "${endpoint}" ]] && echo "  ${endpoint}" >&2
                done <<< "${endpoints}"

                if (( SERVER_WARMUP_SECONDS > 0 )); then
                    echo "Additional server warm-up: ${SERVER_WARMUP_SECONDS}s" >&2
                    sleep "${SERVER_WARMUP_SECONDS}"
                fi

                if ! job_is_active "${server_job_id}"; then
                    echo "ERROR: server ${server_job_id} exited during warm-up." >&2
                    tail -n 180 "${server_log}" >&2 || true
                    return 1
                fi

                printf '%s\n' "${actual_ip}"
                return 0
            fi
        fi

        if ! job_is_active "${server_job_id}"; then
            echo "ERROR: server ${server_job_id} exited before all four endpoints became ready." >&2
            [[ -f "${server_log}" ]] && tail -n 180 "${server_log}" >&2 || true
            return 1
        fi

        elapsed=$(( $(date +%s) - start_time ))

        if (( elapsed >= SERVER_READY_TIMEOUT_SECONDS )); then
            echo "ERROR: timed out waiting for server ${server_job_id}." >&2
            echo "Required ports: 50051, 50052, 50053, 50054" >&2
            echo "Detected endpoints:" >&2
            if [[ -n "${endpoints}" ]]; then
                printf '  %s\n' ${endpoints} >&2
            else
                echo "  none" >&2
            fi
            [[ -f "${server_log}" ]] && tail -n 180 "${server_log}" >&2 || true
            return 1
        fi

        sleep "${POLL_SECONDS}"
    done
}

RUN_ID="$(date +'%Y%m%d-%H%M%S')"
LOG_DIR="${SCRIPT_DIR}/submission_logs/${RUN_ID}"
mkdir -p "${LOG_DIR}"

MANIFEST="${LOG_DIR}/job_manifest.tsv"
COMPLETION_LOG="${LOG_DIR}/completion_summary.tsv"

printf 'task\tbatch\tgroup\tsubject\tserver_job_id\tserver_ip\tclient_job_id\tserver_log\tclient_log\n' > "${MANIFEST}"
printf 'task\tbatch\tgroup\tsubject\tserver_job_id\tclient_job_id\tclient_state\tclient_log\n' > "${COMPLETION_LOG}"

active_clients=()
active_servers=()
active_tasks=()
active_batches=()
active_groups=()
active_subjects=()
active_client_logs=()

cleanup_active_jobs() {
    local id

    for id in "${active_clients[@]}"; do
        scancel "${id}" 2>/dev/null || true
    done

    for id in "${active_servers[@]}"; do
        scancel "${id}" 2>/dev/null || true
    done
}

on_exit() {
    local rc=$?
    trap - EXIT INT TERM HUP

    if (( ${#active_clients[@]} > 0 || ${#active_servers[@]} > 0 )); then
        echo "Submission driver is exiting; cancelling remaining active jobs." >&2
        cleanup_active_jobs
    fi

    exit "${rc}"
}

on_signal() {
    trap - EXIT INT TERM HUP
    echo "Submission driver interrupted; cancelling active jobs." >&2
    cleanup_active_jobs
    exit 130
}

trap on_exit EXIT
trap on_signal INT TERM HUP

submit_pair() {
    local task="$1"
    local batch_number="$2"
    local group="$3"
    local subject="$4"
    local short_subject="${subject#sub-}"
    local label="${task}:batch${batch_number}:${group}/${subject}"
    local server_log_template="${LOG_DIR}/server_${task}_batch${batch_number}_${short_subject}_%j.out"
    local client_log_template="${LOG_DIR}/client_${task}_batch${batch_number}_${short_subject}_%j.out"
    local server_raw server_job_id server_log server_ip
    local client_script client_raw client_job_id client_log

    echo "Submitting dedicated server for ${label}"

    server_raw=$(
        sbatch \
            --parsable \
            --chdir="${SCRIPT_DIR}" \
            --job-name="srv_${task}_${short_subject}" \
            --output="${server_log_template}" \
            --error="${server_log_template}" \
            "${SERVER_SCRIPT}" \
            4
    )

    server_job_id="${server_raw%%;*}"
    server_log="${server_log_template//%j/${server_job_id}}"

    echo "Server job ID: ${server_job_id}"
    echo "Server log:    ${server_log}"

    if ! wait_for_server_running "${server_job_id}"; then
        scancel "${server_job_id}" 2>/dev/null || true
        return 1
    fi

    if (( SERVER_IP_WAIT_SECONDS > 0 )); then
        echo "Server ${server_job_id} is RUNNING; waiting ${SERVER_IP_WAIT_SECONDS}s before checking actual listening endpoints."
        sleep "${SERVER_IP_WAIT_SECONDS}"
    fi

    if ! job_is_active "${server_job_id}"; then
        echo "ERROR: server ${server_job_id} exited during the initial wait." >&2
        [[ -f "${server_log}" ]] && tail -n 180 "${server_log}" >&2 || true
        return 1
    fi

    if ! server_ip=$(wait_for_server_ready "${server_job_id}" "${server_log}"); then
        scancel "${server_job_id}" 2>/dev/null || true
        return 1
    fi

    case "${task}" in
        MID) client_script="${MID_SCRIPT}" ;;
        SST) client_script="${SST_SCRIPT}" ;;
    esac

    echo "Submitting client for ${label}; server=${server_job_id}; actual IP=${server_ip}"

    if ! client_raw=$(
        sbatch \
            --parsable \
            --chdir="${SCRIPT_DIR}" \
            --job-name="${task}_${short_subject}" \
            --output="${client_log_template}" \
            --error="${client_log_template}" \
            "${client_script}" \
            "${server_ip}" \
            "${group}" \
            "${subject}" \
            "${server_job_id}"
    ); then
        echo "ERROR: failed to submit client for ${label}; cancelling server ${server_job_id}." >&2
        scancel "${server_job_id}" 2>/dev/null || true
        return 1
    fi

    client_job_id="${client_raw%%;*}"
    client_log="${client_log_template//%j/${client_job_id}}"

    active_clients+=("${client_job_id}")
    active_servers+=("${server_job_id}")
    active_tasks+=("${task}")
    active_batches+=("${batch_number}")
    active_groups+=("${group}")
    active_subjects+=("${subject}")
    active_client_logs+=("${client_log}")

    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "${task}" "${batch_number}" "${group}" "${subject}" \
        "${server_job_id}" "${server_ip}" "${client_job_id}" \
        "${server_log}" "${client_log}" >> "${MANIFEST}"

    echo "Submitted ${label}: server=${server_job_id}, client=${client_job_id}, IP=${server_ip}"
    echo "Client log: ${client_log}"
}

wait_for_current_batch() {
    local remaining i client_id server_id state client_log

    while true; do
        remaining=0

        for ((i=0; i<${#active_clients[@]}; i++)); do
            client_id="${active_clients[$i]}"
            if job_is_active "${client_id}"; then
                remaining=$((remaining + 1))
            fi
        done

        if (( remaining == 0 )); then
            break
        fi

        echo "Current batch: ${remaining}/${#active_clients[@]} client jobs are still active."
        sleep "${POLL_SECONDS}"
    done

    for ((i=0; i<${#active_clients[@]}; i++)); do
        client_id="${active_clients[$i]}"
        server_id="${active_servers[$i]}"
        client_log="${active_client_logs[$i]}"
        state="$(job_state "${client_id}")"

        scancel "${server_id}" 2>/dev/null || true

        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
            "${active_tasks[$i]}" "${active_batches[$i]}" \
            "${active_groups[$i]}" "${active_subjects[$i]}" \
            "${server_id}" "${client_id}" "${state}" "${client_log}" \
            >> "${COMPLETION_LOG}"

        echo "Completed ${active_tasks[$i]} batch ${active_batches[$i]} ${active_groups[$i]}/${active_subjects[$i]}: client=${client_id}, state=${state}"
        echo "Client log: ${client_log}"

        case "${state}" in
            COMPLETED*)
                ;;
            *)
                echo "===== Failed/non-completed client log tail: ${client_log} =====" >&2
                [[ -f "${client_log}" ]] && tail -n 200 "${client_log}" >&2 || true
                ;;
        esac
    done

    active_clients=()
    active_servers=()
    active_tasks=()
    active_batches=()
    active_groups=()
    active_subjects=()
    active_client_logs=()
}

submit_batch() {
    local task="$1"
    local batch_number="$2"
    shift 2
    local entries=("$@")
    local entry group subject

    echo "============================================================"
    echo "Submitting ${task} batch ${batch_number} (${#entries[@]} subjects)"
    echo "============================================================"

    for entry in "${entries[@]}"; do
        IFS='|' read -r group subject <<< "${entry}"
        submit_pair "${task}" "${batch_number}" "${group}" "${subject}"
    done

    wait_for_current_batch
    echo "${task} batch ${batch_number} completed."
}

preflight_paths

echo "===== Submission settings ====="
echo "Tasks:                       ${TASKS[*]}"
echo "Subjects:                    12"
echo "Batches per task:            3"
echo "Subjects per batch:          4"
echo "Poll interval:               ${POLL_SECONDS}s"
echo "Initial server wait:         ${SERVER_IP_WAIT_SECONDS}s"
echo "Server-ready timeout:        ${SERVER_READY_TIMEOUT_SECONDS}s"
echo "Additional server warm-up:   ${SERVER_WARMUP_SECONDS}s"
echo "Manifest:                    ${MANIFEST}"
echo "Completion summary:          ${COMPLETION_LOG}"

for task in "${TASKS[@]}"; do
    submit_batch "${task}" 1 "${BATCH_1[@]}"
    submit_batch "${task}" 2 "${BATCH_2[@]}"
    submit_batch "${task}" 3 "${BATCH_3[@]}"
done

echo "All requested subject-task simulations have completed or left the queue."
echo "Job manifest:       ${MANIFEST}"
echo "Completion summary: ${COMPLETION_LOG}"
