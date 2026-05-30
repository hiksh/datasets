"""
Kitsune Network Attack Dataset
Source: Kaggle ymirsky/kitsune-network-attack-dataset
        (license acceptance required at https://www.kaggle.com/datasets/ymirsky/kitsune-network-attack-dataset)

Structure: 9 attack scenarios, each with:
  {scenario}_dataset.csv  — 115 network-stat features (no header)
  {scenario}_labels.csv   — ground truth labels (0=benign, 1=attack)
"""
import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "ymirsky/kitsune-network-attack-dataset"
INPUT_FILENAME = "Kitsune.csv"
OUTPUT_FILENAME = "Reformatted_Kitsune.csv"
MAX_ROWS_PER_SCENARIO = 200_000

FEATURE_COLUMNS = [f"feature_{i}" for i in range(115)]

# Kitsune scenario → kill-chain step
KILL_CHAIN = {
    "benign": 0,
    "arp mitm": 4,           # Man-in-the-Middle via ARP spoofing → Exploitation
    "active wiretap": 4,     # Network wiretapping → Exploitation
    "fuzzing": 1,            # Protocol fuzzing → Reconnaissance
    "ssdp flood": 7,         # SSDP amplification DDoS → Actions on Objectives
    "ssl renegotiation": 7,  # SSL DoS → Actions on Objectives
    "syn dos": 7,            # SYN flood DoS → Actions on Objectives
    "mirai": 6,              # Mirai botnet C&C → Command & Control
    "os scan": 1,            # OS fingerprinting → Reconnaissance
    "video injection": 4,    # Media injection attack → Exploitation
}

SCENARIO_NAMES = {
    "ARP_MitM": "arp mitm",
    "Active_Wiretap": "active wiretap",
    "Fuzzing": "fuzzing",
    "SSDP_Flood": "ssdp flood",
    "SSL_Renegotiation": "ssl renegotiation",
    "SYN_DoS": "syn dos",
    "Mirai": "mirai",
    "OS_Scan": "os scan",
    "Video_Injection": "video injection",
}


def find_scenario_pairs(base_path):
    pairs = []
    for root, _, files in os.walk(base_path):
        dataset_files = {f.replace("_dataset.csv", "") for f in files if f.endswith("_dataset.csv")}
        label_files = {f.replace("_labels.csv", "") for f in files if f.endswith("_labels.csv")}
        for scenario in sorted(dataset_files & label_files):
            pairs.append((
                os.path.join(root, f"{scenario}_dataset.csv"),
                os.path.join(root, f"{scenario}_labels.csv"),
                scenario,
            ))
    return pairs


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    print("[INFO] NOTE: This dataset requires accepting the license on Kaggle.")
    print("[INFO] Visit: https://www.kaggle.com/datasets/ymirsky/kitsune-network-attack-dataset")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    pairs = find_scenario_pairs(path)
    if not pairs:
        raise RuntimeError(f"No scenario pairs found in {path}.")

    print(f"[INFO] Found {len(pairs)} scenarios")
    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0

    for feat_path, label_path, scenario_key in pairs:
        scenario_name = SCENARIO_NAMES.get(scenario_key, scenario_key.lower().replace("_", " "))
        try:
            df_feat = pd.read_csv(feat_path, header=None, names=FEATURE_COLUMNS, low_memory=False)
            df_label = pd.read_csv(label_path, header=None, names=["label"], low_memory=False)

            if len(df_feat) != len(df_label):
                print(f"[WARN] {scenario_key}: row count mismatch ({len(df_feat)} vs {len(df_label)}), truncating")
                min_len = min(len(df_feat), len(df_label))
                df_feat = df_feat.iloc[:min_len]
                df_label = df_label.iloc[:min_len]

            df_feat["_label"] = df_label["label"].values
            if MAX_ROWS_PER_SCENARIO and len(df_feat) > MAX_ROWS_PER_SCENARIO:
                df_feat = df_feat.sample(n=MAX_ROWS_PER_SCENARIO, random_state=42)
                print(f"[INFO] {scenario_key}: sampled {MAX_ROWS_PER_SCENARIO:,} rows")

            attack_name = scenario_name
            df_feat["attack_name"] = df_feat["_label"].apply(
                lambda x: "benign" if int(x) == 0 else attack_name
            )
            df_feat.drop(columns=["_label"], inplace=True)

            df_feat.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_feat)
            print(f"[INFO] {scenario_key}: {len(df_feat):,} rows")
        except Exception as e:
            print(f"[WARN] Skipping {scenario_key}: {e}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df_header = pd.read_csv(input_filepath, nrows=0)
    target_columns = ["attack_name", "attack_flag", "attack_step"]
    feature_columns = [c for c in df_header.columns if c not in target_columns]

    print(f"[INFO] Writing: {output_filepath}")
    first_write = True
    total_rows = 0

    for chunk in pd.read_csv(input_filepath, chunksize=100_000, low_memory=False):
        name_series = chunk["attack_name"].astype(str).str.strip().str.lower()
        chunk["attack_flag"] = (name_series != "benign").astype(int)
        unmapped = name_series[~name_series.isin(KILL_CHAIN)].unique()
        if len(unmapped):
            print(f"[WARNING] Unmapped: {unmapped}")
        chunk["attack_step"] = name_series.map(KILL_CHAIN).fillna(-1).astype(int)

        col_order = [c for c in feature_columns if c in chunk.columns] + target_columns
        chunk = chunk[col_order]
        chunk.to_csv(output_filepath, index=False, mode="w" if first_write else "a", header=first_write)
        first_write = False
        total_rows += len(chunk)

    print(f"[INFO] Done. Rows: {total_rows:,}")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILENAME):
        download()
    else:
        print(f"[INFO] {INPUT_FILENAME} already exists, skipping download.")

    if not os.path.exists(OUTPUT_FILENAME):
        process(INPUT_FILENAME, OUTPUT_FILENAME)
    else:
        print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
