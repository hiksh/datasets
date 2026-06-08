import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "dhoogla/cidds002"
INPUT_FILENAME = "CIDDS-002.csv"
OUTPUT_FILENAME = "Reformatted_CIDDS-002.csv"

# CIDDS-002 attack_type → kill-chain step
KILL_CHAIN = {
    "benign": 0,
    "scan": 1,     # Reconnaissance
}


def find_all_parquets(base_path):
    parquets = []
    for root, _, files in os.walk(base_path):
        for f in sorted(files):
            if f.endswith(".parquet"):
                parquets.append(os.path.join(root, f))
    return parquets


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    parquets = find_all_parquets(path)
    if not parquets:
        raise RuntimeError(f"No parquet found in {path}. Files: {os.listdir(path)}")

    print(f"[INFO] Found {len(parquets)} parquet file(s):")
    for p in parquets:
        print(f"  {p}")

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0
    last_df = None

    for p in parquets:
        try:
            df_part = pd.read_parquet(p)
            df_part.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_part)
            last_df = df_part
            labels = sorted(df_part["attack_type"].dropna().unique().tolist()) if "attack_type" in df_part.columns else []
            print(f"[INFO] {os.path.basename(p)}: {len(df_part):,} rows  attack_types={labels}")
        except Exception as e:
            print(f"[WARN] Skipping {p}: {e}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")
    if last_df is not None:
        print(f"[INFO] Columns ({len(last_df.columns)}): {last_df.columns.tolist()}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    df.rename(columns={"attack_type": "attack_name"}, inplace=True)
    df["attack_flag"] = (df["attack_name"].astype(str).str.strip().str.lower() != "benign").astype(int)
    df.drop(columns=["label", "attack_id"], errors="ignore", inplace=True)

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
