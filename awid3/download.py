"""
AWID3 — Aegean Wi-Fi Intrusion Dataset 3
Source: Kaggle chatzoglou/awid3
        (license acceptance required at https://www.kaggle.com/datasets/chatzoglou/awid3)

Environment: 802.11 Wi-Fi SOHO testbed
Attacks: 13 Wi-Fi attack categories including KRACK, Kr00k, deauth, probe attacks
"""
import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "chatzoglou/awid3"
INPUT_FILENAME = "AWID3.csv"
OUTPUT_FILENAME = "Reformatted_AWID3.csv"

# AWID3 class → kill-chain step
KILL_CHAIN = {
    "normal": 0,
    # Reconnaissance
    "probe_request_flood": 1,
    "probe_response_flood": 1,
    "beacon_flood": 1,
    # Exploitation
    "krack": 4,            # Key Reinstallation Attack → Exploitation
    "kr00k": 4,            # Kr00k vulnerability → Exploitation
    "icv_error": 4,        # Integrity Check Value error exploit → Exploitation
    "michael_mic_failure": 4,
    # Actions on Objectives
    "deauthentication": 7,
    "disassociation": 7,
    "power_saving_dos": 7,
    "rts_flood": 7,
    "cts_flood": 7,
}


def find_all_csvs(base_path):
    csvs = []
    for root, _, files in os.walk(base_path):
        for f in sorted(files):
            if f.endswith(".csv"):
                csvs.append(os.path.join(root, f))
    return csvs


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    print("[INFO] NOTE: This dataset requires accepting the license on Kaggle.")
    print("[INFO] Visit: https://www.kaggle.com/datasets/chatzoglou/awid3")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    csvs = find_all_csvs(path)
    if not csvs:
        raise RuntimeError(f"No CSV found in {path}. Files: {os.listdir(path)}")

    print(f"[INFO] Found {len(csvs)} CSV file(s)")
    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0

    for csv_path in csvs:
        try:
            df_part = pd.read_csv(csv_path, low_memory=False)
            df_part.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_part)
            print(f"[INFO] {os.path.basename(csv_path)}: {len(df_part):,} rows")
        except Exception as e:
            print(f"[WARN] Skipping {csv_path}: {e}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")
    df = pd.read_csv(dst, nrows=5)
    print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()[:10]}...")
    label_col = "Label" if "Label" in df.columns else df.columns[-1]
    print(f"[INFO] Unique labels: {sorted(df[label_col].dropna().unique().tolist())}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    label_col = None
    for candidate in ["Label", "label", "Class", "class", "attack_type"]:
        if candidate in df.columns:
            label_col = candidate
            break
    if label_col is None:
        label_col = df.columns[-1]

    df.rename(columns={label_col: "attack_name"}, inplace=True)
    df["attack_flag"] = (df["attack_name"].astype(str).str.strip().str.lower() != "normal").astype(int)

    name_series = df["attack_name"].astype(str).str.strip().str.lower()
    unmapped = name_series[~name_series.isin(KILL_CHAIN)].unique()
    if len(unmapped):
        print(f"[WARNING] Unmapped labels: {unmapped}")
    df["attack_step"] = name_series.map(KILL_CHAIN).fillna(-1).astype(int)

    target_columns = ["attack_name", "attack_flag", "attack_step"]
    feature_columns = [c for c in df.columns if c not in target_columns]
    df = df[feature_columns + target_columns]

    print(f"[INFO] Saving: {output_filepath}")
    df.to_csv(output_filepath, index=False)
    print(f"[INFO] Done. Rows: {len(df):,}")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILENAME):
        download()
    else:
        print(f"[INFO] {INPUT_FILENAME} already exists, skipping download.")

    if not os.path.exists(OUTPUT_FILENAME):
        process(INPUT_FILENAME, OUTPUT_FILENAME)
    else:
        print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
