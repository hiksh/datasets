import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "vigneshvenkateswaran/bot-iot"
INPUT_FILENAME = "Bot-IoT.csv"
OUTPUT_FILENAME = "Reformatted_Bot-IoT.csv"

# Bot-IoT attack categories → kill-chain step
KILL_CHAIN = {
    "normal": 0,
    "reconnaissance": 1,    # OS fingerprint, service scan
    "ddos": 7,              # DDoS (UDP, TCP, HTTP)
    "dos": 7,               # DoS (UDP, TCP, HTTP)
    "theft": 7,             # Data exfiltration, keylogging
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

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    dfs = []
    for csv_path in csvs:
        try:
            df_part = pd.read_csv(csv_path, low_memory=False)
            print(f"[INFO] {os.path.basename(csv_path)}: {len(df_part):,} rows")
            dfs.append(df_part)
        except Exception as e:
            print(f"[WARN] Skipping {csv_path}: {e}")

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(dst, index=False)
    print(f"[INFO] Saved as: {dst}  (total {len(df):,} rows)")
    print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()}")
    cats = df["category"].unique().tolist() if "category" in df.columns else []
    print(f"[INFO] Unique categories: {sorted(cats)}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # category → attack_name, attack (0/1) → attack_flag
    if "category" in df.columns:
        df.rename(columns={"category": "attack_name"}, inplace=True)
    if "attack" in df.columns:
        df.rename(columns={"attack": "attack_flag"}, inplace=True)
    # drop subcategory (redundant with attack_name + attack_step)
    df.drop(columns=["subcategory "], errors="ignore", inplace=True)
    df.drop(columns=["subcategory"], errors="ignore", inplace=True)

    df["attack_flag"] = pd.to_numeric(df["attack_flag"], errors="coerce").fillna(0).astype(int)

    name_series = df["attack_name"].astype(str).str.strip().str.lower()
    unmapped = name_series[~name_series.isin(KILL_CHAIN)].unique()
    if len(unmapped) > 0:
        print(f"[WARNING] Unmapped categories: {unmapped}")
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
