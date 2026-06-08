import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "badcodebuilder/insdn-dataset"
INPUT_FILENAME = "InSDN.csv"
OUTPUT_FILENAME = "Reformatted_InSDN.csv"

# InSDN label → kill-chain step
# Source: SDN environment with normal traffic + Metasploitable-2 and OVS attack traffic
KILL_CHAIN = {
    "normal": 0,
    "probe": 1,          # Reconnaissance / network probing
    "bfa": 4,            # Brute Force Attack → Exploitation (credential attack)
    "u2r": 4,            # User-to-Root → Privilege Escalation
    "dos": 7,            # Denial of Service
    "ddos": 7,           # Distributed DoS
    "web-attack": 4,     # Web application attack → Exploitation
    "botnet": 6,         # Botnet C&C activity
}

# Label source files
SOURCE_FILES = ["Normal_data.csv", "metasploitable-2.csv", "OVS.csv"]


def find_csvs(base_path):
    subdir = os.path.join(base_path, "InSDN_DatasetCSV")
    if os.path.isdir(subdir):
        return [os.path.join(subdir, f) for f in sorted(os.listdir(subdir)) if f.endswith(".csv")]
    return [os.path.join(base_path, f) for f in sorted(os.listdir(base_path)) if f.endswith(".csv")]


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    csvs = find_csvs(path)
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
            n = len(df_part)
            labels = sorted(df_part["Label"].dropna().str.strip().unique().tolist()) if "Label" in df_part.columns else []
            print(f"[INFO] {os.path.basename(csv_path)}: {n:,} rows  labels={labels}")
            dfs.append(df_part)
        except Exception as e:
            print(f"[WARN] Skipping {csv_path}: {e}")

    if not dfs:
        raise RuntimeError("No data loaded.")

    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(dst, index=False)
    print(f"[INFO] Saved as: {dst}  (total {len(df):,} rows)")
    print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()[:10]}...")
    all_labels = sorted(df["Label"].dropna().str.strip().unique().tolist()) if "Label" in df.columns else []
    print(f"[INFO] All labels: {all_labels}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # Drop non-feature columns
    df.drop(columns=["Flow ID", "Src IP", "Dst IP", "Timestamp"], errors="ignore", inplace=True)

    df.rename(columns={"Label": "attack_name"}, inplace=True)

    # Strip trailing spaces from labels (OVS.csv has "DDoS ")
    df["attack_name"] = df["attack_name"].astype(str).str.strip()
    df["attack_flag"] = (df["attack_name"].str.lower() != "normal").astype(int)

    name_series = df["attack_name"].str.lower()
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
    vc = df["attack_step"].value_counts().sort_index()
    for step, cnt in vc.items():
        print(f"  Step {step:2d}: {cnt:,}")


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
