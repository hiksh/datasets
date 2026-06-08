"""
Kitsune Network Attack Dataset
Source: Kaggle ymirsky/network-attack-dataset-kitsune (no license required)

Structure per scenario (directory):
  {Scenario_Name}_dataset.csv  — 115 AfterImage network-stat features (no header row)
  {scenario_name}_labels.csv   — per-sample labels
    * Most scenarios: CSV with header '"","x"' then (row_index, 0|1)
    * Mirai Botnet: headerless, single column of 0|1 values
  {Scenario_Name}_pcap.pcap[ng] — raw packet capture (not used)

Label encoding: 0 = benign, 1 = attack
"""
import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "ymirsky/network-attack-dataset-kitsune"
INPUT_FILENAME = "Kitsune.csv"
OUTPUT_FILENAME = "Reformatted_Kitsune.csv"
MAX_ROWS_PER_SCENARIO = 200_000

FEATURE_COLUMNS = [f"feature_{i}" for i in range(115)]

# Scenario directory name (lowercase) → kill-chain step
KILL_CHAIN = {
    "benign": 0,
    "arp mitm": 4,           # ARP Man-in-the-Middle → Exploitation
    "active wiretap": 4,     # Network wiretapping → Exploitation
    "fuzzing": 1,            # Protocol fuzzing → Reconnaissance
    "ssdp flood": 7,         # SSDP amplification DDoS → Actions on Objectives
    "ssl renegotiation": 7,  # SSL DoS → Actions on Objectives
    "syn dos": 7,            # SYN flood → Actions on Objectives
    "mirai botnet": 6,       # Mirai C&C → Command & Control
    "os scan": 1,            # OS fingerprinting → Reconnaissance
    "video injection": 4,    # Media injection → Exploitation
}


def _read_labels(labels_path):
    """Return a Series of 0/1 labels from a Kitsune labels CSV.

    Two formats exist:
      - With header: '"","x"' then (row_idx, label) → read column 'x'
      - No header (Mirai): each line is a single 0 or 1
    """
    with open(labels_path, "r") as f:
        first_line = f.readline()

    if '"x"' in first_line or first_line.strip() in ('","x"', '"","x"'):
        df = pd.read_csv(labels_path, index_col=0)
        return df.iloc[:, 0].reset_index(drop=True)
    else:
        df = pd.read_csv(labels_path, header=None)
        return df.iloc[:, 0].reset_index(drop=True)


def find_scenario_pairs(base_path):
    """Return list of (dataset_path, labels_path, scenario_name) tuples."""
    pairs = []
    for direntry in sorted(os.scandir(base_path), key=lambda e: e.name):
        if not direntry.is_dir():
            continue
        dir_path = direntry.path
        scenario_name = direntry.name  # e.g. "ARP MitM"

        # Find dataset and labels files (case-insensitive match on stem)
        files = {f.lower(): f for f in os.listdir(dir_path)}
        dataset_file = next(
            (files[f] for f in files if f.endswith("_dataset.csv")), None
        )
        labels_file = next(
            (files[f] for f in files if f.endswith("_labels.csv")), None
        )

        if dataset_file and labels_file:
            pairs.append((
                os.path.join(dir_path, dataset_file),
                os.path.join(dir_path, labels_file),
                scenario_name,
            ))
    return pairs


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    pairs = find_scenario_pairs(path)
    if not pairs:
        raise RuntimeError(f"No scenario pairs found in {path}.")

    print(f"[INFO] Found {len(pairs)} scenario(s):")
    for _, _, name in pairs:
        print(f"  {name}")

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0

    for feat_path, label_path, scenario_name in pairs:
        try:
            df_feat = pd.read_csv(feat_path, header=None, names=FEATURE_COLUMNS,
                                  low_memory=False)
            labels = _read_labels(label_path)

            if len(df_feat) != len(labels):
                min_len = min(len(df_feat), len(labels))
                print(f"[WARN] {scenario_name}: row mismatch "
                      f"({len(df_feat)} vs {len(labels)}), truncating to {min_len}")
                df_feat = df_feat.iloc[:min_len].reset_index(drop=True)
                labels = labels.iloc[:min_len].reset_index(drop=True)

            if MAX_ROWS_PER_SCENARIO and len(df_feat) > MAX_ROWS_PER_SCENARIO:
                idx = df_feat.sample(n=MAX_ROWS_PER_SCENARIO, random_state=42).index
                df_feat = df_feat.loc[idx].reset_index(drop=True)
                labels = labels.loc[idx].reset_index(drop=True)

            attack_name = scenario_name.lower()
            df_feat["attack_name"] = labels.apply(
                lambda x: "benign" if int(x) == 0 else attack_name
            )

            n_attack = int((labels != 0).sum())
            n_benign = int((labels == 0).sum())
            sampled = min(len(df_feat), MAX_ROWS_PER_SCENARIO) if MAX_ROWS_PER_SCENARIO else len(df_feat)
            print(f"[INFO] {scenario_name}: {sampled:,} rows "
                  f"(benign={n_benign:,}, attack={n_attack:,} before sampling)")

            df_feat.to_csv(dst, index=False,
                           mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_feat)

        except Exception as e:
            print(f"[WARN] Skipping {scenario_name}: {e}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading header: {input_filepath}")
    header_df = pd.read_csv(input_filepath, nrows=0)
    target_columns = ["attack_name", "attack_flag", "attack_step"]
    feature_columns = [c for c in header_df.columns if c not in target_columns]

    print(f"[INFO] Writing: {output_filepath}")
    first_write = True
    total_rows = 0
    unmapped = set()

    for chunk in pd.read_csv(input_filepath, chunksize=100_000, low_memory=False):
        name_series = chunk["attack_name"].astype(str).str.strip().str.lower()
        chunk["attack_flag"] = (name_series != "benign").astype(int)
        u = name_series[~name_series.isin(KILL_CHAIN)].unique()
        unmapped.update(u)
        chunk["attack_step"] = name_series.map(KILL_CHAIN).fillna(-1).astype(int)

        col_order = [c for c in feature_columns if c in chunk.columns] + target_columns
        chunk = chunk[col_order]
        chunk.to_csv(output_filepath, index=False,
                     mode="w" if first_write else "a", header=first_write)
        first_write = False
        total_rows += len(chunk)

    if unmapped:
        print(f"[WARNING] Unmapped attack names: {unmapped}")
    print(f"[INFO] Done. Rows: {total_rows:,}")
    df_check = pd.read_csv(output_filepath, usecols=["attack_step"], low_memory=False)
    vc = df_check["attack_step"].value_counts().sort_index()
    for step, cnt in vc.items():
        print(f"  Step {step:2d}: {cnt:,}")


if __name__ == "__main__":
    if not os.path.exists(INPUT_FILENAME):
        download()
    else:
        print(f"[INFO] {INPUT_FILENAME} already exists, skipping download.")

    if not os.path.exists(OUTPUT_FILENAME):
        process(INPUT_FILENAME, OUTPUT_FILENAME)
    else:
        print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
