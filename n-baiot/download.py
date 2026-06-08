import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "mkashifn/nbaiot-dataset"
INPUT_FILENAME = "N-BaIoT.csv"
OUTPUT_FILENAME = "Reformatted_N-BaIoT.csv"

# N-BaIoT has no label column — attack type is encoded in the filename.
# Filename patterns:
#   {device}.benign.csv                      → normal
#   {device}.mirai.{attack}.csv              → mirai botnet
#   {device}.gafgyt.{attack}.csv             → gafgyt botnet
# mirai attack subtypes: ack, scan, syn, udp, udpplain
# gafgyt attack subtypes: combo, junk, scan, tcp, udp

KILL_CHAIN = {
    "benign": 0,
    "mirai.scan": 1,      # Reconnaissance
    "gafgyt.scan": 1,
    "mirai.syn": 7,        # Actions on Objectives — DoS/DDoS
    "mirai.ack": 7,
    "mirai.udp": 7,
    "mirai.udpplain": 7,
    "gafgyt.combo": 7,
    "gafgyt.junk": 7,
    "gafgyt.tcp": 7,
    "gafgyt.udp": 7,
}


def _parse_attack_from_filename(filename):
    """Return (attack_name, attack_flag) derived from the CSV filename."""
    stem = os.path.splitext(os.path.basename(filename))[0]
    parts = stem.split(".")
    # parts[0] = device id, rest = malware[.subtype]
    if len(parts) < 2:
        return "unknown", -1
    malware_parts = parts[1:]
    name = ".".join(malware_parts).lower()
    flag = 0 if name == "benign" else 1
    return name, flag


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

    print(f"[INFO] Found {len(csvs)} CSV file(s)")

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0

    for csv_path in csvs:
        try:
            attack_name, attack_flag = _parse_attack_from_filename(csv_path)
            df_feat = pd.read_csv(csv_path, low_memory=False)
            step = KILL_CHAIN.get(attack_name, -1 if attack_flag == 1 else 0)
            n = len(df_feat)
            extra = pd.DataFrame({
                "attack_name": [attack_name] * n,
                "attack_flag": [attack_flag] * n,
                "attack_step": [step] * n,
            })
            df_part = pd.concat([df_feat, extra], axis=1)
            df_part.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_part)
            print(f"[INFO] {os.path.basename(csv_path)}: {len(df_part):,} rows  [{attack_name}]")
        except Exception as e:
            print(f"[WARN] Skipping {csv_path}: {e}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")


def process(input_filepath, output_filepath):
    """Labels were embedded during download. Reorder columns to standard layout."""
    print(f"[INFO] Reading header: {input_filepath}")
    header_df = pd.read_csv(input_filepath, nrows=0)
    target_columns = ["attack_name", "attack_flag", "attack_step"]
    target_columns = [c for c in target_columns if c in header_df.columns]
    feature_columns = [c for c in header_df.columns if c not in target_columns]
    col_order = feature_columns + target_columns

    print(f"[INFO] Writing: {output_filepath}")
    first_write = True
    total_rows = 0
    for chunk in pd.read_csv(input_filepath, chunksize=100_000, low_memory=False):
        chunk = chunk[col_order].dropna(subset=["attack_name"])
        chunk.to_csv(output_filepath, index=False, mode="w" if first_write else "a", header=first_write)
        first_write = False
        total_rows += len(chunk)
    print(f"[INFO] Done. Rows: {total_rows:,}")


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
