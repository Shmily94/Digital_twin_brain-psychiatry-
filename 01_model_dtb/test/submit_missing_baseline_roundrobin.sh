#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Refill missing 100m / 1000m baseline simulations to 5 BOLDs.
#
# Scheduling policy:
#   - At most ONE active client per subject (avoids subject-level I/O conflicts).
#   - No global cap on the number of simultaneously active subject tasks.
#   - Round-robin over subjects.
#   - A subject is revisited only after its previous client ends.
#   - Each simulation gets a fresh server.
#   - Before submitting a server, dynamically check IDLE nodes in the
#     server script's Slurm partition. If nodes are insufficient, wait.
#   - The server is cancelled after its client finishes.
#
# Default is DRY_RUN=1.  Set DRY_RUN=0 to submit real jobs.
# ============================================================

WORK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${WORK_DIR}"

DATA_ROOT="${DATA_ROOT:-/public/home/ssct004t/project/pengsongjun/Digital_twin_brain/data}"

TARGET_FILE="${TARGET_FILE:-${WORK_DIR}/missing_baseline_targets.tsv}"
SERVER_100M="${SERVER_100M:-${WORK_DIR}/server_dtb_100m.slurm}"
SERVER_1000M="${SERVER_1000M:-${WORK_DIR}/server_dtb_1000m.slurm}"
CLIENT_MID="${CLIENT_MID:-${WORK_DIR}/baseline_client_MID.slurm}"
CLIENT_SST="${CLIENT_SST:-${WORK_DIR}/baseline_client_SST.slurm}"

DRY_RUN="${DRY_RUN:-1}"
TARGET_COUNT="${TARGET_COUNT:-5}"
SERVER_READY_TIMEOUT="${SERVER_READY_TIMEOUT:-7200}"
POLL_SECONDS="${POLL_SECONDS:-5}"
NODE_WAIT_POLL_SECONDS="${NODE_WAIT_POLL_SECONDS:-10}"
NODE_WAIT_LOG_SECONDS="${NODE_WAIT_LOG_SECONDS:-60}"
MAX_RETRIES_PER_COMBO="${MAX_RETRIES_PER_COMBO:-2}"

BASELINE_PARAM="ampa-0.0008-0.0008-gaba-0.0015"

MODEL_100M="dti_distribution_100m_d100_blocks8_int_ext"
MODEL_1000M="dti_distribution_1000m_d100_blocks80_int_ext"

mkdir -p "${WORK_DIR}/log"
mkdir -p "${WORK_DIR}/queue_logs"

STAMP="$(date +%Y%m%d_%H%M%S)"
QUEUE_LOG="${WORK_DIR}/queue_logs/baseline_refill_${STAMP}.tsv"

printf "time\taction\tsubject\tscale\ttask\tcount\tneed\tserver_job\tclient_job\tserver_ip\tmessage\n" > "${QUEUE_LOG}"

log_event() {
    local action="$1" subject="$2" scale="$3" task="$4" count="$5" need="$6"
    local server_job="${7:-}" client_job="${8:-}" server_ip="${9:-}" message="${10:-}"
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
        "$(date '+%F %T')" "${action}" "${subject}" "${scale}" "${task}" \
        "${count}" "${need}" "${server_job}" "${client_job}" "${server_ip}" "${message}" \
        | tee -a "${QUEUE_LOG}" >&2
}

model_dir_for() {
    local group="$1" subject="$2" scale="$3"
    local model_name
    case "${scale}" in
        100m)  model_name="${MODEL_100M}" ;;
        1000m) model_name="${MODEL_1000M}" ;;
        *) echo "ERROR: unsupported scale: ${scale}" >&2; return 2 ;;
    esac
    printf "%s/%s/%s/%s\n" "${DATA_ROOT}" "${group}" "${subject}" "${model_name}"
}

count_baseline() {
    local group="$1" subject="$2" scale="$3" task="$4"
    local model_dir base
    model_dir="$(model_dir_for "${group}" "${subject}" "${scale}")"
    base="${model_dir}/DA/mani_task_${task}"

    if [[ ! -d "${base}" ]]; then
        echo 0
        return 0
    fi

    find "${base}" \
        -type f \
        -name 'bold_after_assim.npy' \
        -path "*${BASELINE_PARAM}*/bold_after_assim.npy" \
        -print \
        | wc -l
}

is_special_subject() {
    local group="$1" subject="$2"
    case "${group}/${subject}" in
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

hp_path_for() {
    local group="$1" subject="$2" task="$3"
    # IMPORTANT: HP always lives under the subject's 100m model,
    # even when the simulation itself is 1000m.
    local hp_root="${DATA_ROOT}/${group}/${subject}/${MODEL_100M}"

    if is_special_subject "${group}" "${subject}"; then
        printf '%s/DA/task_da/hp_%s.npy\n' "${hp_root}" "${task}"
    else
        printf '%s/DA/DTB_task_IMAGEN_voxel_task_%s_full_0.1_0.45_0.25_0.5_30/assimilation/hp.npy\n' \
            "${hp_root}" "${task}"
    fi
}

job_active() {
    local jobid="$1"
    [[ -n "${jobid}" ]] || return 1
    squeue -h -j "${jobid}" 2>/dev/null | grep -q .
}

# ------------------------------------------------------------
# Slurm node-capacity helpers.
#
# The node requirement and partition are read directly from each
# server script's #SBATCH directives, so the submission driver does
# not maintain a second hard-coded copy of "3 nodes" / "21 nodes".
# ------------------------------------------------------------
server_nodes_for_script() {
    local script="$1"
    awk '
        $1 == "#SBATCH" {
            for (i = 2; i <= NF; i++) {
                if ($i == "-N" || $i == "--nodes") {
                    print $(i + 1)
                    exit
                }
                if ($i ~ /^--nodes=/) {
                    sub(/^--nodes=/, "", $i)
                    print $i
                    exit
                }
                if ($i ~ /^-N[0-9]+$/) {
                    sub(/^-N/, "", $i)
                    print $i
                    exit
                }
            }
        }
    ' "${script}"
}

server_partition_for_script() {
    local script="$1"
    awk '
        $1 == "#SBATCH" {
            for (i = 2; i <= NF; i++) {
                if ($i == "-p" || $i == "--partition") {
                    print $(i + 1)
                    exit
                }
                if ($i ~ /^--partition=/) {
                    sub(/^--partition=/, "", $i)
                    print $i
                    exit
                }
            }
        }
    ' "${script}"
}

idle_nodes_for_partition() {
    local partition="$1"
    local out

    # -t idle excludes allocated/mixed/draining/down nodes.  The
    # server jobs are exclusive, so only fully IDLE nodes are safe
    # to count as immediately available capacity.
    if ! out="$(sinfo -h -p "${partition}" -t idle -o '%D' 2>/dev/null)"; then
        return 1
    fi

    awk 'NF && $1 ~ /^[0-9]+$/ {sum += $1} END {print sum + 0}' <<< "${out}"
}

partition_state_summary() {
    local partition="$1"
    sinfo -h -p "${partition}" -o '%T:%D' 2>/dev/null \
        | awk 'NF {a[++n]=$0} END {for(i=1;i<=n;i++) printf "%s%s", a[i], (i<n ? "," : "")}'
}

wait_for_available_nodes() {
    local server_script="$1" subject="$2" scale="$3" task="$4"
    local required partition idle summary
    local last_log=0 now

    required="$(server_nodes_for_script "${server_script}")"
    partition="$(server_partition_for_script "${server_script}")"

    if ! [[ "${required}" =~ ^[0-9]+$ ]] || (( required < 1 )); then
        echo "ERROR: could not determine a positive #SBATCH -N/--nodes from ${server_script}" >&2
        return 40
    fi
    if [[ -z "${partition}" ]]; then
        echo "ERROR: could not determine #SBATCH -p/--partition from ${server_script}" >&2
        return 41
    fi

    while true; do
        # Important while waiting: retire completed clients and cancel
        # their dedicated servers so those nodes can become IDLE again.
        cleanup_finished_clients

        if ! idle="$(idle_nodes_for_partition "${partition}")"; then
            echo "ERROR: sinfo failed while checking partition ${partition}" >&2
            return 42
        fi

        if (( idle >= required )); then
            log_event "NODE_READY" "${subject}" "${scale}" "${task}" "" "" "" "" "" \
                "partition=${partition}; idle_nodes=${idle}; required_nodes=${required}"
            return 0
        fi

        now="$(date +%s)"
        if (( last_log == 0 || now - last_log >= NODE_WAIT_LOG_SECONDS )); then
            summary="$(partition_state_summary "${partition}" || true)"
            log_event "WAIT_NODES" "${subject}" "${scale}" "${task}" "" "" "" "" "" \
                "partition=${partition}; idle_nodes=${idle}; required_nodes=${required}; states=${summary:-unknown}"
            last_log="${now}"
        fi

        sleep "${NODE_WAIT_POLL_SECONDS}"
    done
}

declare -a KEYS=()
declare -a SUBJECTS_ORDER=()
declare -A GROUP=()
declare -A SUBJECT_OF=()
declare -A SCALE_OF=()
declare -A TASK_OF=()
declare -A NEED=()
declare -A INITIAL_NEED=()
declare -A ATTEMPTS=()
declare -A MAX_ATTEMPTS=()
declare -A SEEN_SUBJECT=()

# Runtime state: only one active client per subject.
declare -A LAST_CLIENT=()
declare -A LAST_SERVER=()
declare -A LAST_KEY=()
declare -A LAST_COUNT_BEFORE=()
declare -A LAST_SERVER_IP=()

# ------------------------------------------------------------
# Read the user-derived missing target list, but recompute the
# CURRENT count from the original source tree before submission.
# This makes reruns safer if some baseline jobs have since finished.
# ------------------------------------------------------------
while IFS=$'\t' read -r group subject scale task reported_count reported_need; do
    [[ "${group}" == "source_group" ]] && continue
    [[ -n "${group}" ]] || continue

    key="${subject}|${scale}|${task}"
    KEYS+=("${key}")
    GROUP["${key}"]="${group}"
    SUBJECT_OF["${key}"]="${subject}"
    SCALE_OF["${key}"]="${scale}"
    TASK_OF["${key}"]="${task}"
    ATTEMPTS["${key}"]=0

    current="$(count_baseline "${group}" "${subject}" "${scale}" "${task}")"
    need=$(( TARGET_COUNT - current ))
    (( need < 0 )) && need=0

    NEED["${key}"]="${need}"
    INITIAL_NEED["${key}"]="${need}"
    MAX_ATTEMPTS["${key}"]=$(( need + MAX_RETRIES_PER_COMBO ))

    if [[ -z "${SEEN_SUBJECT[${subject}]+x}" ]]; then
        SUBJECTS_ORDER+=("${subject}")
        SEEN_SUBJECT["${subject}"]=1
    fi

    log_event "INIT" "${subject}" "${scale}" "${task}" "${current}" "${need}" "" "" "" \
        "reported_count=${reported_count}; reported_need=${reported_need}"
done < "${TARGET_FILE}"

# ------------------------------------------------------------
# Preflight before any real submission.
# ------------------------------------------------------------
for f in "${TARGET_FILE}" "${SERVER_100M}" "${SERVER_1000M}" "${CLIENT_MID}" "${CLIENT_SST}"; do
    if [[ ! -f "${f}" ]]; then
        echo "ERROR: required file not found: ${f}" >&2
        exit 10
    fi
done

for cmd in sinfo sbatch squeue scancel; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
        if [[ "${DRY_RUN}" == "1" ]]; then
            echo "WARNING: ${cmd} not found; node-capacity query will only run on the Slurm login node during real submission." >&2
        else
            echo "ERROR: required Slurm command not found: ${cmd}" >&2
            exit 12
        fi
    fi
done

for server_script in "${SERVER_100M}" "${SERVER_1000M}"; do
    req_nodes="$(server_nodes_for_script "${server_script}")"
    req_part="$(server_partition_for_script "${server_script}")"
    if ! [[ "${req_nodes}" =~ ^[0-9]+$ ]] || (( req_nodes < 1 )) || [[ -z "${req_part}" ]]; then
        echo "ERROR: cannot parse node/partition request from ${server_script}" >&2
        exit 13
    fi
    echo "PREFLIGHT SERVER RESOURCES: $(basename "${server_script}") -> partition=${req_part}, nodes=${req_nodes}" >&2
done

preflight_failed=0
for key in "${KEYS[@]}"; do
    (( NEED["${key}"] > 0 )) || continue
    group="${GROUP[${key}]}"
    subject="${SUBJECT_OF[${key}]}"
    scale="${SCALE_OF[${key}]}"
    task="${TASK_OF[${key}]}"
    model_dir="$(model_dir_for "${group}" "${subject}" "${scale}")"
    hp_path="$(hp_path_for "${group}" "${subject}" "${task}")"

    if [[ ! -d "${model_dir}" ]]; then
        echo "ERROR: missing model directory: ${model_dir}" >&2
        preflight_failed=1
    fi
    if [[ ! -f "${hp_path}" ]]; then
        echo "ERROR: missing hp.npy: ${hp_path}" >&2
        preflight_failed=1
    else
        echo "PREFLIGHT HP OK: ${subject} ${scale} ${task} -> ${hp_path}" >&2
    fi
done

if (( preflight_failed != 0 )); then
    echo "Preflight failed. No jobs were submitted." >&2
    exit 11
fi

next_pending_key_for_subject() {
    local subject="$1" key
    for key in "${KEYS[@]}"; do
        [[ "${SUBJECT_OF[${key}]}" == "${subject}" ]] || continue
        if (( NEED["${key}"] > 0 )); then
            printf "%s\n" "${key}"
            return 0
        fi
    done
    return 1
}

# ------------------------------------------------------------
# Dry-run: print exact round-robin order without submitting.
# ------------------------------------------------------------
print_plan() {
    declare -A tmp=()
    local key subject round=0 any
    for key in "${KEYS[@]}"; do
        tmp["${key}"]="${NEED[${key}]}"
    done

    echo
    echo "================ ROUND-ROBIN PLAN ================"
    while true; do
        any=0
        declare -a round_lines=()

        for subject in "${SUBJECTS_ORDER[@]}"; do
            for key in "${KEYS[@]}"; do
                [[ "${SUBJECT_OF[${key}]}" == "${subject}" ]] || continue
                if (( tmp["${key}"] > 0 )); then
                    round_lines+=("${subject}  ${SCALE_OF[${key}]}  ${TASK_OF[${key}]}  (remaining before submit=${tmp[${key}]})")
                    tmp["${key}"]=$(( tmp["${key}"] - 1 ))
                    any=1
                    break
                fi
            done
        done

        (( any == 1 )) || break
        round=$((round + 1))
        echo "--- round ${round} ---"
        printf "%s\n" "${round_lines[@]}"
    done
    echo "=================================================="
}

if [[ "${DRY_RUN}" == "1" ]]; then
    echo
    echo "================ NODE POLICY ====================="
    for server_script in "${SERVER_100M}" "${SERVER_1000M}"; do
        req_nodes="$(server_nodes_for_script "${server_script}")"
        req_part="$(server_partition_for_script "${server_script}")"
        if command -v sinfo >/dev/null 2>&1; then
            idle_now="$(idle_nodes_for_partition "${req_part}" 2>/dev/null || echo unknown)"
        else
            idle_now="unknown"
        fi
        echo "$(basename "${server_script}"): partition=${req_part}, required_nodes=${req_nodes}, idle_now=${idle_now}"
    done
    echo "Global task limit: NONE (subject-level one-client-at-a-time protection remains)."
    echo "If idle nodes < required nodes for the next server, real mode waits and rechecks every ${NODE_WAIT_POLL_SECONDS}s."
    echo "=================================================="

    print_plan
    echo
    echo "DRY_RUN=1: no sbatch command was executed."
    echo "Queue log: ${QUEUE_LOG}"
    echo
    echo "Run for real with:"
    echo "  DRY_RUN=0 ./$(basename "$0")"
    exit 0
fi

# ------------------------------------------------------------
# When a client disappears from squeue, verify that the baseline
# count actually increased, then cancel its dedicated server.
# If not, restore the remaining need so it can be retried.
# ------------------------------------------------------------
cleanup_finished_clients() {
    local subject client server key group scale task before current need ip
    for subject in "${SUBJECTS_ORDER[@]}"; do
        client="${LAST_CLIENT[${subject}]:-}"
        [[ -n "${client}" ]] || continue

        if job_active "${client}"; then
            continue
        fi

        server="${LAST_SERVER[${subject}]:-}"
        key="${LAST_KEY[${subject}]}"
        group="${GROUP[${key}]}"
        scale="${SCALE_OF[${key}]}"
        task="${TASK_OF[${key}]}"
        before="${LAST_COUNT_BEFORE[${subject}]}"
        ip="${LAST_SERVER_IP[${subject}]:-}"

        # Give the filesystem a moment to settle after Slurm removes the job.
        sleep 2
        current="$(count_baseline "${group}" "${subject}" "${scale}" "${task}")"
        need=$(( TARGET_COUNT - current ))
        (( need < 0 )) && need=0
        NEED["${key}"]="${need}"

        if (( current > before )); then
            log_event "CLIENT_DONE" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
                "${server}" "${client}" "${ip}" "baseline count increased"
        else
            log_event "CLIENT_NO_OUTPUT" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
                "${server}" "${client}" "${ip}" "count did not increase; task will be retried if attempts remain"
        fi

        if [[ -n "${server}" ]] && job_active "${server}"; then
            scancel "${server}" || true
            log_event "SERVER_CANCEL" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
                "${server}" "${client}" "${ip}" "client finished"
        fi

        LAST_CLIENT["${subject}"]=""
        LAST_SERVER["${subject}"]=""
        LAST_KEY["${subject}"]=""
        LAST_COUNT_BEFORE["${subject}"]=""
        LAST_SERVER_IP["${subject}"]=""
    done
}

# ------------------------------------------------------------
# Wait until the server prints:
#   Server listening on X.X.X.X:50051
#
# While waiting, also clean up servers belonging to clients that
# have completed, preventing large server jobs from lingering.
# ------------------------------------------------------------
wait_for_server_ready() {
    local server_job="$1"
    local start="${SECONDS}" match ip
    local top_o="${WORK_DIR}/log/${server_job}.o"
    local top_e="${WORK_DIR}/log/${server_job}.e"
    local job_dir="${WORK_DIR}/log/${server_job}"

    while true; do
        cleanup_finished_clients

        match="$(
            {
                grep -hsE 'Server listening on ([0-9]{1,3}\.){3}[0-9]{1,3}:50051' \
                    "${top_o}" "${top_e}" 2>/dev/null || true
                if [[ -d "${job_dir}" ]]; then
                    grep -RhsE 'Server listening on ([0-9]{1,3}\.){3}[0-9]{1,3}:50051' \
                        "${job_dir}" 2>/dev/null || true
                fi
            } | tail -n 1
        )"

        if [[ -n "${match}" ]]; then
            ip="$(grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}:50051' <<< "${match}" | tail -n 1)"
            if [[ -n "${ip}" ]]; then
                printf "%s\n" "${ip}"
                return 0
            fi
        fi

        if ! job_active "${server_job}"; then
            echo "ERROR: server job ${server_job} left squeue before becoming ready." >&2
            return 20
        fi

        if (( SECONDS - start >= SERVER_READY_TIMEOUT )); then
            echo "ERROR: timed out waiting for server job ${server_job}." >&2
            return 21
        fi

        sleep "${POLL_SECONDS}"
    done
}

submit_one() {
    local key="$1"
    local group subject scale task current need model_dir hp_path server_script client_script
    local server_raw server_job server_ip client_raw client_job

    group="${GROUP[${key}]}"
    subject="${SUBJECT_OF[${key}]}"
    scale="${SCALE_OF[${key}]}"
    task="${TASK_OF[${key}]}"

    current="$(count_baseline "${group}" "${subject}" "${scale}" "${task}")"
    need=$(( TARGET_COUNT - current ))
    (( need < 0 )) && need=0
    NEED["${key}"]="${need}"

    if (( need == 0 )); then
        log_event "SKIP_COMPLETE" "${subject}" "${scale}" "${task}" "${current}" "0" "" "" "" "already at target"
        return 0
    fi

    if (( ATTEMPTS["${key}"] >= MAX_ATTEMPTS["${key}"] )); then
        echo "ERROR: retry limit reached for ${subject} ${scale} ${task}; current=${current}" >&2
        log_event "RETRY_LIMIT" "${subject}" "${scale}" "${task}" "${current}" "${need}" "" "" "" "aborting"
        return 30
    fi

    model_dir="$(model_dir_for "${group}" "${subject}" "${scale}")"
    hp_path="$(hp_path_for "${group}" "${subject}" "${task}")"

    case "${scale}" in
        100m)  server_script="${SERVER_100M}" ;;
        1000m) server_script="${SERVER_1000M}" ;;
        *) echo "ERROR: unsupported scale ${scale}" >&2; return 31 ;;
    esac

    case "${task}" in
        MID) client_script="${CLIENT_MID}" ;;
        SST) client_script="${CLIENT_SST}" ;;
        *) echo "ERROR: unsupported task ${task}" >&2; return 32 ;;
    esac

    echo
    echo "================================================================"
    echo "Submitting: ${subject}  ${scale}  ${task}"
    echo "Current baseline count: ${current}; target: ${TARGET_COUNT}"
    echo "MODEL_DIR: ${model_dir}"
    echo "HP_PATH:   ${hp_path}"
    echo "================================================================"

    # No global concurrency cap.  Keep filling the cluster while enough
    # fully IDLE nodes exist for the next server; otherwise wait here
    # until capacity is released.
    if ! wait_for_available_nodes "${server_script}" "${subject}" "${scale}" "${task}"; then
        echo "ERROR: node-capacity check failed for ${subject} ${scale} ${task}" >&2
        return 36
    fi

    if ! server_raw="$(sbatch --parsable "${server_script}")"; then
        echo "ERROR: failed to submit server for ${subject} ${scale} ${task}" >&2
        return 33
    fi
    server_job="${server_raw%%;*}"

    log_event "SERVER_SUBMIT" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
        "${server_job}" "" "" "${server_script}"

    # Give Slurm a moment to register the job before the first squeue check.
    sleep 2

    if ! server_ip="$(wait_for_server_ready "${server_job}")"; then
        scancel "${server_job}" 2>/dev/null || true
        log_event "SERVER_FAILED" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
            "${server_job}" "" "" "server never became ready"
        return 34
    fi

    log_event "SERVER_READY" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
        "${server_job}" "" "${server_ip}" "Server listening"

    if ! client_raw="$(
        sbatch --parsable \
            "--export=ALL,MODEL_DIR=${model_dir},HP_PATH=${hp_path},SERVER_IP=${server_ip},SUBJECT=${subject}" \
            "${client_script}"
    )"; then
        scancel "${server_job}" 2>/dev/null || true
        log_event "CLIENT_SUBMIT_FAILED" "${subject}" "${scale}" "${task}" "${current}" "${need}" \
            "${server_job}" "" "${server_ip}" "server cancelled"
        return 35
    fi

    client_job="${client_raw%%;*}"

    ATTEMPTS["${key}"]=$(( ATTEMPTS["${key}"] + 1 ))
    # Reserve this one in-flight attempt. After the client finishes,
    # cleanup_finished_clients recomputes NEED from actual files.
    NEED["${key}"]=$(( need - 1 ))

    LAST_CLIENT["${subject}"]="${client_job}"
    LAST_SERVER["${subject}"]="${server_job}"
    LAST_KEY["${subject}"]="${key}"
    LAST_COUNT_BEFORE["${subject}"]="${current}"
    LAST_SERVER_IP["${subject}"]="${server_ip}"

    log_event "CLIENT_SUBMIT" "${subject}" "${scale}" "${task}" "${current}" "${NEED[${key}]}" \
        "${server_job}" "${client_job}" "${server_ip}" "${client_script}"

    sleep 2
}

pending_total() {
    local key total=0
    for key in "${KEYS[@]}"; do
        total=$(( total + NEED["${key}"] ))
    done
    echo "${total}"
}

active_subject_count() {
    local subject n=0
    for subject in "${SUBJECTS_ORDER[@]}"; do
        [[ -n "${LAST_CLIENT[${subject}]:-}" ]] && n=$((n + 1))
    done
    echo "${n}"
}

# ============================================================
# Real round-robin queue
# ============================================================
round=0

while true; do
    cleanup_finished_clients

    pending="$(pending_total)"
    active="$(active_subject_count)"

    if (( pending == 0 && active == 0 )); then
        break
    fi

    if (( pending == 0 )); then
        sleep "${POLL_SECONDS}"
        continue
    fi

    round=$((round + 1))
    echo
    echo "################ ROUND ${round} ################"
    echo "Pending attempts: ${pending}; active subjects: ${active}"

    submitted_this_round=0

    for subject in "${SUBJECTS_ORDER[@]}"; do
        cleanup_finished_clients

        # Never overlap two clients for the same subject.
        if [[ -n "${LAST_CLIENT[${subject}]:-}" ]]; then
            continue
        fi

        if key="$(next_pending_key_for_subject "${subject}")"; then
            submit_one "${key}"
            submitted_this_round=$((submitted_this_round + 1))
        fi
    done

    if (( submitted_this_round == 0 )); then
        sleep "${POLL_SECONDS}"
    fi
done

echo
echo "============================================================"
echo "All target 100m/1000m baseline combinations reached ${TARGET_COUNT},"
echo "or no further jobs remain active."
echo "Queue log: ${QUEUE_LOG}"
echo "============================================================"
