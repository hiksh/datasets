"""
AWID2 — Aegean Wi-Fi Intrusion Dataset 2
Source: Kaggle kolias93/awid2-wifi-intrusion-dataset
        (license acceptance required at https://www.kaggle.com/datasets/kolias93/awid2-wifi-intrusion-dataset)

Environment: 802.11 Wi-Fi testbed (SOHO)
Attacks: IEEE 802.11 protocol attacks — deauthentication, injection, impersonation
"""
import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "kolias93/awid2-wifi-intrusion-dataset"
INPUT_FILENAME = "AWID2.csv"
OUTPUT_FILENAME = "Reformatted_AWID2.csv"

# AWID2 class → kill-chain step
# Wi-Fi layer-2 attacks map primarily to Reconnaissance or Exploitation
KILL_CHAIN = {
    "normal": 0,
    "injection": 4,         # Packet injection → Exploitation
    "impersonation": 4,     # Identity spoofing → Exploitation
    "flooding": 7,          # Flood-type DoS → Actions on Objectives
    "deauthentication": 7,  # Forced disconnection → Actions on Objectives
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
    print("[INFO] Visit: https://www.kaggle.com/datasets/kolias93/awid2-wifi-intrusion-dataset")
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


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # Identify label column (may vary by version)
    label_col = None
    for candidate in ["class", "Class", "label", "Label", "attack_type"]:
        if candidate in df.columns:
            label_col = candidate
            break
    if label_col is None:
        label_col = df.columns[-1]
        print(f"[WARN] Label column not found, using last column: {label_col}")

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
