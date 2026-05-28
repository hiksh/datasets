import kagglehub
import os
import shutil
import pandas as pd

KAGGLE_DATASET = "mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot"
REQUIRED_COLUMNS = ["Attack_type", "Attack_label"]
INPUT_FILENAME = "EdgeIIoT.csv"
OUTPUT_FILENAME = "Reformatted_EdgeIIoT.csv"


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
    path = kagglehub.dataset_download(KAGGLE_DATASET)
    src = find_csv_with_columns(path, REQUIRED_COLUMNS)
    if not src:
        raise RuntimeError(
            f"[ERROR] Could not find a CSV with columns {REQUIRED_COLUMNS} in {path}.\n"
            "Column names may differ from the expected format."
        )
    print(f"[INFO] Found dataset file: {src}")
    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    shutil.copy(src, dst)
    print(f"[INFO] Saved as: {dst}")
    return dst


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    rename_mapping = {}
    if "Attack_type" in df.columns:
        rename_mapping["Attack_type"] = "attack_name"
    if "Attack_label" in df.columns:
        rename_mapping["Attack_label"] = "attack_flag"
    df.rename(columns=rename_mapping, inplace=True)

    if "attack_step" not in df.columns:
        df["attack_step"] = 0

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
