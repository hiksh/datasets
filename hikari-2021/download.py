import kagglehub
import os
import shutil
import pandas as pd

KAGGLE_DATASET = "kk0105/allflowmeter-hikari2021"
INPUT_FILENAME = "HIKARI-2021.csv"
OUTPUT_FILENAME = "Reformatted_HIKARI-2021.csv"

# HIKARI-2021 traffic_category → kill-chain step
KILL_CHAIN = {
    "background": 0,
    "benign": 0,
    "probing": 1,                  # Reconnaissance
    "bruteforce": 4,               # Exploitation — credential attack
    "bruteforce-xml": 4,           # Exploitation — XML brute-force
    "xmrigcc cryptominer": 7,      # Actions on Objectives — cryptomining
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
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    csvs = find_all_csvs(path)
    if not csvs:
        raise RuntimeError(f"No CSV found in {path}. Files: {os.listdir(path)}")

    print(f"[INFO] Found {len(csvs)} CSV file(s):")
    for c in csvs:
        print(f"  {c}")

    src = csvs[0]
    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    shutil.copy(src, dst)
    print(f"[INFO] Saved as: {dst}")

    df = pd.read_csv(dst, nrows=5)
    print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()}")
    print(f"[INFO] Sample:\n{df.head(2).to_string()}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # traffic_category is the semantic label; Label is 0/1 binary
    df.rename(columns={"traffic_category": "attack_name"}, inplace=True)
    df.rename(columns={"Label": "attack_flag"}, inplace=True)
    # Drop index columns added by AllFlowMeter
    df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], errors="ignore", inplace=True)

    df["attack_flag"] = pd.to_numeric(df["attack_flag"], errors="coerce").fillna(0).astype(int)

    name_series = df["attack_name"].astype(str).str.strip().str.lower()
    unmapped = name_series[~name_series.isin(KILL_CHAIN)].unique()
    if len(unmapped) > 0:
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
        df = pd.read_csv(INPUT_FILENAME, nrows=0)
        print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()}")

    if not os.path.exists(OUTPUT_FILENAME):
        process(INPUT_FILENAME, OUTPUT_FILENAME)
    else:
        print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
