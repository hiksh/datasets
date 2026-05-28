#!/bin/bash
# Download and process all (or selected) datasets.
#
# Usage:
#   bash download_all.sh                  # download everything
#   bash download_all.sh cicids2017 lspr23  # download specific datasets only
#
# Each dataset runs its download.py in its own subdirectory.
# A failed dataset is logged but does not stop the rest.

set -euo pipefail

DATASETS=(
    cicids2017
    cicids2018
    ciciot2023
    nsl-kdd
    unsw-nb15
    ton-iot
    mirai
    EPIC_Attack_Datasets
    edge-iiot
    xiiotid
    nf-ton-iot-v3
    wustl-iiot-2021
    lspr23
)

if [ $# -gt 0 ]; then
    DATASETS=("$@")
fi

FAILED=()
SKIPPED=()
SUCCEEDED=()

for dataset in "${DATASETS[@]}"; do
    if [ ! -f "$dataset/download.py" ]; then
        echo "[SKIP] $dataset: no download.py found"
        SKIPPED+=("$dataset")
        continue
    fi

    echo ""
    echo "=============================="
    echo " $dataset"
    echo "=============================="
    if (cd "$dataset" && python3 download.py); then
        SUCCEEDED+=("$dataset")
    else
        echo "[ERROR] $dataset failed — continuing with next dataset"
        FAILED+=("$dataset")
    fi
done

echo ""
echo "=============================="
echo " Summary"
echo "=============================="
echo "  Succeeded : ${#SUCCEEDED[@]}  — ${SUCCEEDED[*]:-none}"
echo "  Failed    : ${#FAILED[@]}  — ${FAILED[*]:-none}"
echo "  Skipped   : ${#SKIPPED[@]}  — ${SKIPPED[*]:-none}"

if [ ${#FAILED[@]} -gt 0 ]; then
    exit 1
fi
