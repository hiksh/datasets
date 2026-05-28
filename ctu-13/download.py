import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "dhoogla/ctu13"
INPUT_FILENAME = "CTU-13.csv"
OUTPUT_FILENAME = "Reformatted_CTU-13.csv"

# CTU-13 label patterns: flow=from-botnet-*, flow=from-normal-*, flow=Background*
KILL_CHAIN = {
    "normal": 0,
    "background": 0,
    "botnet": 6,   # C&C — active botnet communication
    "to-botnet": 6,
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
    dfs = []
    for p in parquets:
        df_part = pd.read_parquet(p)
        print(f"[INFO] {os.path.basename(p)}: {len(df_part):,} rows")
        dfs.append(df_part)

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(dst, index=False)
    print(f"[INFO] Saved as: {dst}  (total {len(df):,} rows)")
    print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()}")
    print(f"[INFO] Unique labels: {df['label'].unique().tolist()[:20]}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # Parse CTU-13 binetflow label format: "flow=from-botnet-neris"
    raw = df["label"].astype(str).str.strip()
    # Strip "flow=" prefix
    raw = raw.str.replace(r"^flow=", "", regex=True)

    df["attack_name"] = raw

    # attack_flag: botnet traffic = 1, normal/background = 0
    is_botnet = raw.str.lower().str.contains("botnet", na=False)
    df["attack_flag"] = is_botnet.astype(int)

    # attack_step: classify by label category
    def label_to_step(label_lower):
        if "botnet" in label_lower or "to-botnet" in label_lower:
            return 6
        if "normal" in label_lower or "background" in label_lower:
            return 0
        return -1

    df["attack_step"] = raw.str.lower().map(label_to_step)

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
