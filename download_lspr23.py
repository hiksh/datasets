"""
LSPR23 Dataset Preprocessing, Data Cleansing, and Cyber Kill Chain Mapping Script

Description:
    This script processes the large-scale LSPR23 dataset (approx. 9.8GB, ls23pr_v1.csv).
    To prevent MemoryError, it reads the data in chunks (default: 100,000 rows).
    It cleanses the raw data anomalies, maps the existing 'Category' and 'Label' columns 
    to a standardized format ('attack_name', 'attack_flag', 'attack_step'), 
    and translates cryptic numeric categories into readable attack signatures.

Data Cleansing Strategy (Resolving Label Contradictions):
    Raw security datasets often contain label noise due to merging issues between 
    network flow tools and Intrusion Detection Systems (IDS). This script addresses two critical anomalies:
    1. The "Unknown Attack" Anomaly: Rows with an attack flag (1) but a 'normal' category name.
       -> Resolution: Rename the attack_name to 'unknown_attack' to prevent confusing the ML model.
    2. The "Silent Attack" Anomaly: Rows with an explicit attack category (e.g., 2.0, 3.0) but a 'normal' flag (0).
       -> Resolution: Force the attack_flag to 1 for all rows where the attack_step > 0 (Steps 1~7).

Mapping Rationale (Cyber Kill Chain):
    The LSPR23 dataset utilizes numeric codes (1.0 ~ 15.0) from its IDS alert categories:
    - Step 1 (Reconnaissance): 
        * 1.0 (Misc activity): Exploratory actions like pinging or probing.
        * 6.0 (Network Scan): Direct scanning to map the target network.
        * 11.0 (Device Retrieving External IP): Gathering infrastructure details.
    - Step 4 (Exploitation): 
        * 2.0 (Protocol Command Decode): Abnormal parameters triggering parser vulnerabilities.
        * 7.0 (Potentially Bad Traffic): Known malicious payloads or shellcodes.
        * 13.0, 14.0, 15.0: Direct attempts to gain privilege or attack web applications.
    - Step 5 (Installation): 
        * 10.0 (Unwanted Program/PUP): Installation of spyware/adware.
    - Step 6 (Command & Control): 
        * 5.0 (Network Trojan): Backdoors communicating with external C2 servers.
    - Step 7 (Actions on Objectives): 
        * 3.0 (Attempted DoS): Degrading or denying system availability.
        * 4.0 (Privacy Violation) & 8.0 (Information Leak): Exfiltration of sensitive data.
"""

"""
LSPR23 데이터셋 전처리, 데이터 클렌징 및 사이버 킬 체인 매핑 스크립트

설명 (Description):
    본 스크립트는 약 9.8GB 규모의 대용량 LSPR23 데이터셋(ls23pr_v1.csv)을 전처리합니다.
    메모리 초과(MemoryError)를 방지하기 위해 데이터를 청크 단위(기본값: 100,000행)로 분할하여 읽어옵니다.
    원시 데이터의 이상치(Anomalies)를 정제하고, 기존의 'Category' 및 'Label' 컬럼을 머신러닝 파이프라인에 
    적합한 표준화된 규격('attack_name', 'attack_flag', 'attack_step')으로 매핑하며, 난해한 숫자형 카테고리 코드를 
    직관적인 공격 명칭(텍스트)으로 변환합니다.

데이터 클렌징 전략 - 라벨 모순 해결 (Data Cleansing Strategy):
    원시(Raw) 보안 데이터셋은 네트워크 플로우 수집 도구와 침입 탐지 시스템(IDS) 간의 병합 과정에서 
    발생하는 시간차 등으로 인해 종종 라벨 노이즈(Label Noise)를 포함합니다. 본 스크립트는 두 가지 치명적인 이상 데이터를 교정합니다:

    1. "미분류 공격(Unknown Attack)" 이상치: 
       공격 플래그(attack_flag)는 1(공격)이지만, 공격명(Category, attack_name)이 'normal'로 기록된 모순된 행.
       -> 해결 방안: 머신러닝 모델의 학습 혼란을 방지하기 위해 해당 공격명을 'unknown_attack'으로 강제 변경합니다.

    2. "조용한 공격(Silent Attack)" 이상치: 
       공격명(Category)에는 명확한 악성 카테고리(예: 2.0, 3.0)가 명시되어 있으나, 플래그(Label)는 0(정상)으로 기록된 모순된 행.
       -> 해결 방안: 매핑된 사이버 킬 체인 단계(attack_step)가 0보다 큰(즉, 1~7단계) 모든 데이터의 공격 플래그를 1로 강제 교정합니다.

사이버 킬 체인 매핑 근거 (Mapping Rationale):
    LSPR23 데이터셋은 IDS 알람 카테고리에서 파생된 숫자 코드(1.0 ~ 15.0)를 사용하며, 
    이는 보안적 관점에 따라 다음의 사이버 킬 체인 단계로 분류됩니다:

    - 1단계 (정찰 / Reconnaissance): 
        * 1.0 (Misc activity): 핑(Ping) 전송 또는 프로빙(Probing)과 같은 탐색 목적의 활동.
        * 6.0 (Network Scan): 타겟 네트워크 구조를 파악하기 위한 직접적인 스캔 시도.
        * 11.0 (Device Retrieving External IP): 외부 IP를 조회하여 인프라 정보를 수집하는 행위.

    - 4단계 (취약점 공격 / Exploitation): 
        * 2.0 (Protocol Command Decode): 파서(Parser) 취약점을 유발하는 비정상적인 파라미터 전송.
        * 7.0 (Potentially Bad Traffic): 알려진 악성 페이로드 또는 쉘코드(Shellcode) 통신.
        * 13.0, 14.0, 15.0: 사용자/관리자 권한 탈취 시도 및 웹 어플리케이션에 대한 직접적인 공격.

    - 5단계 (설치 / Installation): 
        * 10.0 (Unwanted Program/PUP): 타겟 시스템 내부에 스파이웨어 또는 애드웨어 등 원치 않는 프로그램 설치.

    - 6단계 (명령 및 제어 / Command & Control): 
        * 5.0 (Network Trojan): 외부 C2(Command and Control) 서버와 지속적으로 통신하는 트로이 목마(백도어) 활동.

    - 7단계 (목표 달성 / Actions on Objectives): 
        * 3.0 (Attempted DoS): 타겟 시스템의 가용성을 저하시키거나 거부하는 DoS 공격 시도.
        * 4.0 (Privacy Violation) & 8.0 (Information Leak): 기업의 민감한 사생활 및 중요 데이터 탈취/유출.
"""

import pandas as pd
import os
import json
from datetime import datetime


# ============================================================
# Checkpoint Utilities
# ============================================================

def _get_checkpoint_path(output_filepath):
    """Returns the checkpoint file path based on the output file path."""
    dirpath  = os.path.dirname(output_filepath) or "."
    basename = os.path.basename(output_filepath)
    return os.path.join(dirpath, f".ckpt_{basename}.json")


def _load_checkpoint(checkpoint_filepath):
    """
    Load the checkpoint file

    Returns:
        dict  : Saved checkpoint status (if file exists)
        None  : If checkpoint files are missing or corrupted (start fresh)
    """
    if not os.path.exists(checkpoint_filepath):
        return None
    try:
        with open(checkpoint_filepath, "r", encoding="utf-8") as f:
            ckpt = json.load(f)
        print(f"[RESUME] Checkpoint detected: '{checkpoint_filepath}'")
        print(f"[RESUME] Last completed chunk : {ckpt['last_completed_chunk']:,}")
        print(f"[RESUME] Rows already processed: {ckpt['rows_processed']:,}")
        print(f"[RESUME] Saved at             : {ckpt['saved_at']}")
        print(f"[RESUME] Skipping to chunk {ckpt['last_completed_chunk'] + 1} ...")
        return ckpt
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[WARNING] Checkpoint file is corrupted ({e}). Starting fresh.")
        os.remove(checkpoint_filepath)
        return None


def _save_checkpoint(checkpoint_filepath, chunk_count, total_rows,
                     total_unmapped, cumulative_steps, output_filepath):
    """
    Saves the current processing status to a checkpoint JSON file.

    저장 항목:
        - last_completed_chunk : Last completed chunk number
        - rows_processed       : Total number of rows processed so far (used for calculating skiprows upon restart)
        - total_unmapped       : Cumulative number of unmapped rows
        - cumulative_steps     : Cumulative distribution by kill chain stage
        - output_filepath      : Output file path (for verifying consistency upon restart)
        - saved_at             : Save time
    """
    ckpt = {
        "last_completed_chunk": int(chunk_count),
        "rows_processed"      : int(total_rows),
        "total_unmapped"      : int(total_unmapped),
        "cumulative_steps"    : {str(k): int(v) for k, v in cumulative_steps.items()},
        "output_filepath"     : output_filepath,
        "saved_at"            : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(checkpoint_filepath, "w", encoding="utf-8") as f:
        json.dump(ckpt, f, indent=2, ensure_ascii=False)


# ============================================================
# Main Processing Function
# ============================================================

def process_lspr23_dataset(input_filepath, output_filepath, chunk_size=100000):
    print(f"[INFO] Starting data processing for: {input_filepath}")
    print(f"[INFO] Chunk size set to: {chunk_size:,} rows to optimize memory usage.")

    # ----------------------------------------------------
    # Dictionary 1: Numeric Category Code to Readable Text
    # ----------------------------------------------------
    category_name_mapping = {
        '1.0': 'misc activity', '1': 'misc activity',
        '2.0': 'generic protocol command decode', '2': 'generic protocol command decode',
        '3.0': 'attempted denial of service', '3': 'attempted denial of service',
        '4.0': 'potential corporate privacy violation', '4': 'potential corporate privacy violation',
        '5.0': 'network trojan detected', '5': 'network trojan detected',
        '6.0': 'network scan', '6': 'network scan',
        '7.0': 'potentially bad traffic', '7': 'potentially bad traffic',
        '8.0': 'attempted information leak', '8': 'attempted information leak',
        '9.0': 'empty category', '9': 'empty category',
        '10.0': 'unwanted program detected', '10': 'unwanted program detected',
        '11.0': 'device retrieving external ip', '11': 'device retrieving external ip',
        '12.0': 'not suspicious traffic', '12': 'not suspicious traffic',
        '13.0': 'web application attack', '13': 'web application attack',
        '14.0': 'attempted user privilege gain', '14': 'attempted user privilege gain',
        '15.0': 'attempted administrator privilege gain', '15': 'attempted administrator privilege gain'
    }

    # ----------------------------------------------------
    # Dictionary 2: Cyber Kill Chain Mapping
    # ----------------------------------------------------
    kill_chain_mapping = {
        # 0. Normal
        'normal': 0, 'none': 0,
        'empty category': 0,           # 9.0
        'not suspicious traffic': 0,   # 12.0

        # Original Text-based Signatures
        'reconn': 1, 'comminj': 4, 'backdoor': 5,
        # unknown_attack → -1 (mapped via kill_chain_mapping, not via resolution logic)
        'unknown_attack': -1,

        # 1. Reconnaissance
        'misc activity': 1,
        'network scan': 1,
        'device retrieving external ip': 1,

        # 4. Exploitation
        'generic protocol command decode': 4,
        'potentially bad traffic': 4,
        'web application attack': 4,
        'attempted user privilege gain': 4,
        'attempted administrator privilege gain': 4,

        # 5. Installation
        'unwanted program detected': 5,

        # 6. Command & Control
        'network trojan detected': 6,

        # 7. Actions on Objectives
        'attempted denial of service': 7,
        'potential corporate privacy violation': 7,
        'attempted information leak': 7
    }

    # ====================================================
    # Checkpoint Initialization
    # ====================================================
    checkpoint_filepath = _get_checkpoint_path(output_filepath)
    ckpt = _load_checkpoint(checkpoint_filepath)

    if ckpt:
        # --- Resume mode: restore state from checkpoint ---
        # Verify the output file still exists; if missing, restart from scratch.
        if not os.path.exists(output_filepath):
            print("[WARNING] Checkpoint found but output file is missing. Starting fresh.")
            ckpt = None

    if ckpt:
        chunk_count      = ckpt["last_completed_chunk"] + 1
        total_rows       = ckpt["rows_processed"]
        total_unmapped   = ckpt["total_unmapped"]
        cumulative_steps = pd.Series(
            {int(k): v for k, v in ckpt["cumulative_steps"].items()}, dtype=int
        )
        rows_to_skip = total_rows   # For skiprows calculation (number of data rows excluding headers)
    else:
        # --- Fresh start: remove stale output file if present ---
        if os.path.exists(output_filepath):
            os.remove(output_filepath)
            print(f"[INFO] Existing output file '{output_filepath}' removed for a fresh start.")

        chunk_count      = 1
        total_rows       = 0
        total_unmapped   = 0
        cumulative_steps = pd.Series(dtype=int)
        rows_to_skip     = 0

    unmapped_values_set = set()

    # ====================================================
    # CSV Reader  (callable skiprows → O(1) memory)
    # ====================================================
    # skiprows as a callable avoids building a large in-memory set.
    # The lambda keeps the header (index 0) and skips data rows
    # 1 … rows_to_skip that were already written in a previous run.
    skip_func = (lambda x: 0 < x <= rows_to_skip) if rows_to_skip > 0 else None
    reader    = pd.read_csv(
        input_filepath,
        chunksize=chunk_size,
        skiprows=skip_func,
        low_memory=False
    )

    for chunk in reader:

        # ====================================================
        # 1. Feature Renaming & Handling Missing Values
        # ====================================================
        if 'Category' in chunk.columns:
            # Fill NaNs with 'normal'
            chunk['Category'] = chunk['Category'].fillna('normal')
            # Replace numeric 0 representations with 'normal'
            chunk['Category'] = chunk['Category'].replace({0: 'normal', 0.0: 'normal', '0': 'normal', '0.0': 'normal'})
            chunk.rename(columns={'Category': 'attack_name'}, inplace=True)

        # Note: Label_src/Label_dst are network segment identifiers and not attack labels.
        # WARNING: Do NOT use Label_src or Label_dst as attack_flag.
        #          Only 'Label' carries the binary attack ground-truth (0 = normal, 1 = attack).
        if 'Label' in chunk.columns:
            chunk.rename(columns={'Label': 'attack_flag'}, inplace=True)

        if 'attack_flag' in chunk.columns:
            chunk['attack_flag'] = pd.to_numeric(chunk['attack_flag'], errors='coerce').fillna(0).astype(int)

        # ====================================================
        # 2. Data Cleansing & Text Translation
        # ====================================================
        if 'attack_name' in chunk.columns and 'attack_flag' in chunk.columns:
            chunk['attack_name'] = chunk['attack_name'].astype(str).str.strip().str.lower()

            conflict_mask = (chunk['attack_flag'] == 1) & (chunk['attack_name'] == 'normal')
            chunk.loc[conflict_mask, 'attack_name'] = 'unknown_attack'

            chunk['attack_name'] = chunk['attack_name'].replace(category_name_mapping)

        # ====================================================
        # 3. Cyber Kill Chain Mapping (attack_step)
        # ====================================================
        if 'attack_name' in chunk.columns:
            name_series = chunk['attack_name']

            # Identify unmapped items
            unmapped = name_series[~name_series.isin(kill_chain_mapping.keys())].unique()
            unmapped_values_set.update(unmapped)

            chunk['attack_step'] = name_series.map(kill_chain_mapping).fillna(-1).astype(int)

        # ====================================================
        # 4. Final Attack Flag Correction
        # ====================================================
        # Anomaly 2 Resolution: Overwrite unreliable flags based on the mapped attack_step
        if 'attack_step' in chunk.columns:
            chunk['attack_flag'] = (chunk['attack_step'] != 0).astype(int)

        # ====================================================
        # 5. Column Reordering (Targets at the end)
        # ====================================================
        target_columns = ['attack_name', 'attack_flag', 'attack_step']
        target_columns = [col for col in target_columns if col in chunk.columns]
        feature_columns = [col for col in chunk.columns if col not in target_columns]
        chunk = chunk[feature_columns + target_columns]

        # ====================================================
        # 6. Calculate Cumulative Statistics
        # ====================================================
        total_rows += len(chunk)
        chunk_unmapped_count = (chunk['attack_step'] == -1).sum()
        total_unmapped += chunk_unmapped_count
        mapped_count = total_rows - total_unmapped

        chunk_step_counts = chunk['attack_step'].value_counts()
        cumulative_steps = cumulative_steps.add(chunk_step_counts, fill_value=0)

        # ====================================================
        # 7. Real-time Chunk Report
        # ====================================================
        print("-" * 50)
        print(f"[CHUNK {chunk_count:04d} PROCESSED]")
        print("[Summary of Cyber Kill Chain Mapping Results]")
        print(f"  - Total number of data : {total_rows:,}")
        print(f"  - Mapping well (0~7)   : {mapped_count:,}")
        print(f"  - Unconfirmed (-1)     : {total_unmapped:,}")
        print("-" * 50)
        print("[Detailed distribution by stage (Step 0 ~ 7)]")
        for step, count in cumulative_steps.sort_index().items():
            print(f"  Step {int(step):2d} : {int(count):,}")
        print("-" * 50 + "")

        # ====================================================
        # 8. Save (Append mode)
        # ====================================================
        # chunk_count == 1 AND rows_to_skip == 0  → fresh start, write header
        # otherwise                               → append without header
        write_header = (chunk_count == 1) and (rows_to_skip == 0)
        chunk.to_csv(
            output_filepath,
            index=False,
            mode='w' if write_header else 'a',
            header=write_header
        )

        # ====================================================
        # 9. Save Checkpoint  (after successful CSV write)
        # ====================================================
        _save_checkpoint(
            checkpoint_filepath,
            chunk_count, total_rows, total_unmapped,
            cumulative_steps, output_filepath
        )

        chunk_count += 1

    # ==========================================
    # FINAL REPORT
    # ==========================================
    final_mapped_count = total_rows - total_unmapped

    print("=" * 60)
    print("[FINAL REPORT] LSPR23 Dataset Processing Completed")
    print("=" * 60)
    print(f"  - Total Rows Processed : {total_rows:,}")
    print(f"  - Successfully Mapped  : {final_mapped_count:,}")
    print(f"  - Unmapped Rows (-1)   : {total_unmapped:,}")
    print("-" * 60)
    print("[Final Distribution by Stage]")
    for step, count in cumulative_steps.sort_index().items():
        print(f"  Step {int(step):2d} : {int(count):,}")
    print("=" * 60)

    print(f"[INFO] Output saved successfully to: {output_filepath}")

    if len(unmapped_values_set) > 0:
        print(f"[WARNING] Unmapped categories found: {list(unmapped_values_set)}")
        print("[WARNING] Please update the 'kill_chain_mapping' dictionary and re-run if necessary.")
    else:
        print("[INFO] All categories were successfully mapped to stages 0-7.")

    # ====================================================
    # 10. Remove Checkpoint  (processing fully completed)
    # ====================================================
    if os.path.exists(checkpoint_filepath):
        os.remove(checkpoint_filepath)
        print(f"[INFO] Checkpoint file removed: {checkpoint_filepath}")

    print("============================================================")


if __name__ == "__main__":
    # Define file paths
    input_file  = "./LSPR23/ls23pr_flows/ls23pr_v1.csv"
    output_file = "./LSPR23/ls23pr_flows/Reformatted_ls23pr_v1.csv"

    process_lspr23_dataset(input_file, output_file)