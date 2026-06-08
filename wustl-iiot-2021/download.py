import kagglehub
import os
import shutil
import pandas as pd

KAGGLE_DATASET = "annaamalaiu/wustl-iiot-2021-dataset"
REQUIRED_COLUMNS = ["Traffic", "Target"]
INPUT_FILENAME = "WUSTL-IIoT-2021.csv"
OUTPUT_FILENAME = "Reformatted_WUSTL-IIoT-2021.csv"


def find_csv_with_columns(base_path, required_columns):
    for root, _, files in os.walk(base_path):
        for f in sorted(files):
            if not f.endswith(".csv"):
                continue
            fpath = os.path.join(root, f)
            try:
                cols = pd.read_csv(fpath, nrows=0).columns.tolist()
                if all(c in cols for c in required_columns):
                    return fpath
            except Exception:
                continue
    return None


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    print("[NOTE] This is a Kaggle re-upload of the official WUSTL-IIoT-2021 dataset.")
    print("       Verifying expected columns: Traffic, Target ...")
    path = kagglehub.dataset_download(KAGGLE_DATASET)
    src = find_csv_with_columns(path, REQUIRED_COLUMNS)
    if not src:
        raise RuntimeError(
            f"[ERROR] Could not find a CSV with columns {REQUIRED_COLUMNS} in {path}.\n"
            "The Kaggle re-upload may use different column names than the official source.\n"
            "Please download manually from: https://www.cse.wustl.edu/~jain/iiot/index.html"
        )
    print(f"[INFO] Column verification passed. Found: {src}")
    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    shutil.copy(src, dst)
    print(f"[INFO] Saved as: {dst}")
    return dst


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    df.columns = df.columns.str.strip().str.replace('"', "", regex=False)

    rename_mapping = {}
    if "Traffic" in df.columns:
        rename_mapping["Traffic"] = "attack_name"
    if "Target" in df.columns:
        rename_mapping["Target"] = "attack_flag"
    df.rename(columns=rename_mapping, inplace=True)

    if "attack_name" in df.columns:
        kill_chain_mapping = {
            "normal": 0,
            "reconn": 1,
            "weapon": 2, "weaponization": 2, "insider_malcious": 2,
            "comminj": 4,
            "backdoor": 5,
            "dos": 7, "ddos": 7,
        }
        name_series = df["attack_name"].astype(str).str.strip().str.lower()
        unmapped = name_series[~name_series.isin(kill_chain_mapping)].unique()
        if len(unmapped) > 0:
            print(f"[WARNING] Unmapped values: {unmapped}")
        df["attack_step"] = name_series.map(kill_chain_mapping).fillna(-1).astype(int)

    if "attack_flag" in df.columns:
        df["attack_flag"] = pd.to_numeric(df["attack_flag"], errors="coerce").fillna(0).astype(int)

    target_columns = ["attack_name", "attack_flag", "attack_step"]
    target_columns = [c for c in target_columns if c in df.columns]
    feature_columns = [c for c in df.columns if c not in target_columns]
    df = df[feature_columns + target_columns]

    print(f"[INFO] Saving: {output_filepath}")
    df.to_csv(output_filepath, index=False)
    print("[INFO] Done.")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILENAME):
        download()
    else:
        print(f"[INFO] {INPUT_FILENAME} already exists, skipping download.")

    if not os.path.exists(OUTPUT_FILENAME):
        process(INPUT_FILENAME, OUTPUT_FILENAME)
    else:
        print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
