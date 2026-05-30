"""
IoT-23 Dataset — CTU IoT Botnet Dataset
Source: Stratosphere Research Laboratory (CTU, Czech Technical University)
Official: https://www.stratosphereips.org/datasets-iot23

Kaggle mirrors (require license acceptance):
  - pchaberger/iot-23-network-traffic-dataset
  - aarontfrancis/iot-23-dataset

NOTE: The Kaggle source surajsooraj26/iot-23 only contains '-' labels (benign flows).
      Use a different source with proper detailed_label column values.

Environment: 20 malware captures + 3 benign captures on IoT devices
Attacks: Mirai, Torii, Okiru botnets + DDoS, PortScan, C&C
"""
import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "pchaberger/iot-23-network-traffic-dataset"
INPUT_FILENAME = "IoT-23.csv"
OUTPUT_FILENAME = "Reformatted_IoT-23.csv"

# IoT-23 detailed_label → kill-chain step
# Labels follow format like "Benign", "Attack", "PartOfAHorizontalPortScan", etc.
KILL_CHAIN = {
    "benign": 0,
    "-": 0,                      # unlabeled flows → treat as benign
    # Reconnaissance
    "partofahorizontalportscan": 1,
    "portscan": 1,
    # C&C
    "c&c": 6,
    "c&c-heartbeat": 6,
    "c&c-heartbeat-attack": 6,
    "c&c-mirai": 6,
    "c&c-torii": 6,
    "c&c-okiru": 6,
    "c&c-filedownload": 6,
    # Actions on Objectives
    "ddos": 7,
    "attack": 7,
    "dos": 7,
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
    print("[INFO] Visit: https://www.kaggle.com/datasets/pchaberger/iot-23-network-traffic-dataset")
    print("[INFO] Alternative: https://www.stratosphereips.org/datasets-iot23")
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
            # Check if detailed_label has actual labels (not just '-')
            if "detailed_label" in df_part.columns:
                unique_labels = df_part["detailed_label"].dropna().unique()
                non_dash = [l for l in unique_labels if str(l).strip() not in ("-", "")]
                if not non_dash:
                    print(f"[WARN] {os.path.basename(csv_path)}: only '-' labels found, skipping")
                    continue
            df_part.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_part)
            print(f"[INFO] {os.path.basename(csv_path)}: {len(df_part):,} rows")
        except Exception as e:
            print(f"[WARN] Skipping {csv_path}: {e}")

    if total_rows == 0:
        raise RuntimeError(
            "No labeled data found. The current Kaggle source may only contain '-' labels.\n"
            "Try a different Kaggle source or download from the official CTU website:\n"
            "  https://www.stratosphereips.org/datasets-iot23"
        )
    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # Use detailed_label as the primary label
    label_col = "detailed_label" if "detailed_label" in df.columns else "label"
    if label_col not in df.columns:
        label_col = df.columns[-1]

    df.rename(columns={label_col: "attack_name"}, inplace=True)

    # Normalize labels
    df["attack_name"] = df["attack_name"].astype(str).str.strip().str.lower()
    df["attack_flag"] = (df["attack_name"].isin(["benign", "-"])).astype(int)
    df["attack_flag"] = 1 - df["attack_flag"]  # flip: 1=attack, 0=benign

    unmapped = df["attack_name"][~df["attack_name"].isin(KILL_CHAIN)].unique()
    if len(unmapped):
        print(f"[WARNING] Unmapped labels: {unmapped}")
    df["attack_step"] = df["attack_name"].map(KILL_CHAIN).fillna(-1).astype(int)

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
