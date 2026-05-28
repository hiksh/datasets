import kagglehub
import os
import shutil
import pandas as pd

KAGGLE_DATASET = "munaalhawawreh/xiiotid-iiot-intrusion-dataset"
REQUIRED_COLUMNS = ["class", "class2", "class3"]
INPUT_FILENAME = "XIIoTID.csv"
OUTPUT_FILENAME = "Reformatted_XIIoTID.csv"


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
    if "class2" in df.columns:
        rename_mapping["class2"] = "attack_name"
    if "class3" in df.columns:
        rename_mapping["class3"] = "attack_flag"
    if "class" in df.columns:
        rename_mapping["class"] = "attack_step"
    df.rename(columns=rename_mapping, inplace=True)

    if "attack_flag" in df.columns:
        df["attack_flag"] = (
            df["attack_flag"].astype(str).str.strip().str.lower()
            .apply(lambda x: 0 if x == "normal" else 1)
        )

    if "attack_step" in df.columns:
        kill_chain_mapping = {
            "normal": 0,
            "reconnaissance": 1, "os_scan": 1, "vul_scan": 1, "coap_scan": 1,
            "modbus_reading": 1, "fuzzing": 1, "mqtt_subscription": 1,
            "weapon": 2, "weaponization": 2, "insider_malcious": 2,
            "delivery": 3, "fake_notification": 3,
            "exploitation": 4, "bruteforce": 4, "dictionary": 4,
            "data_injection": 4, "mitm": 4,
            "installation": 5, "shell": 5,
            "c&c": 6, "command & control": 6, "tcp_relay": 6,
            "exfiltration": 7, "actions on objectives": 7, "rdos": 7, "crypto_ransom": 7,
        }
        step_series = df["attack_step"].astype(str).str.strip().str.lower()
        unmapped = step_series[~step_series.isin(kill_chain_mapping)].unique()
        if len(unmapped) > 0:
            print(f"[WARNING] Unmapped values: {unmapped}")
        df["attack_step"] = step_series.map(kill_chain_mapping).fillna(-1).astype(int)

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
