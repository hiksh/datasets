"""
CIC-IDS2017 Improved Dataset (Liu et al., 2022)
Source: https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip

Reference:
  Liu, L., Engelen, G., Lynar, T., Essam, D., Joosen, W. (2022).
  Error Prevalence in NIDS Datasets: A Case Study on CIC-IDS-2017 and CSE-CIC-IDS-2018.
  IEEE CNS 2022. DOI: 10.1109/CNS56114.2022.9947235

This is an improved version of the original CIC-IDS2017 dataset with:
  - Fixed CICFlowMeter feature extraction
  - Corrected labeling (uses "Attempted" sub-label for flows with no malicious behaviour)
  - Removed duplicate flows and fixed timestamp issues
"""
import os
import subprocess
import zipfile
import pandas as pd

DOWNLOAD_URL = "https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip"
ARCHIVE_NAME = "CICIDS2017_improved.zip"
OUTPUT_FILENAME = "Reformatted_CIC-IDS2017-Imp.csv"

# CIC-IDS2017 improved labels → kill-chain step
# Labels may include "Attempted" suffix (e.g., "DoS GoldenEye - Attempted") → treat same step
KILL_CHAIN = {
    "benign": 0,
    # Reconnaissance
    "portscan": 1,
    # Exploitation
    "brute force": 4,      # SSH/FTP brute force
    "ftp-patator": 4,
    "ssh-patator": 4,
    "heartbleed": 4,
    "xss": 4,
    "sql injection": 4,
    "web attacks": 4,
    # C&C
    "bot": 6,
    # Infiltration / Actions
    "infiltration": 7,
    # DoS/DDoS
    "ddos": 7,
    "dos": 7,
    "dos hulk": 7,
    "dos goldeneye": 7,
    "dos slowloris": 7,
    "dos slowhttptest": 7,
}


def _map_label(label: str) -> int:
    """Map a label string (possibly with '- Attempted' suffix) to kill-chain step."""
    normalized = label.strip().lower()
    # Strip "- attempted" suffix for mapping purposes
    base = normalized.replace(" - attempted", "").strip()
    for key, step in KILL_CHAIN.items():
        if key in base or base.startswith(key):
            return step
    return -1


def download():
    if os.path.exists(ARCHIVE_NAME):
        print(f"[INFO] Archive already exists: {ARCHIVE_NAME}")
    else:
        print(f"[INFO] Downloading: {DOWNLOAD_URL}")
        try:
            subprocess.run(["wget", "-c", "-O", ARCHIVE_NAME, DOWNLOAD_URL], check=True)
        except FileNotFoundError:
            raise RuntimeError(
                "[ERROR] wget not found. Install it or download manually:\n"
                f"  URL: {DOWNLOAD_URL}\n"
                f"  Save as: {ARCHIVE_NAME}"
            )

    print(f"[INFO] Extracting: {ARCHIVE_NAME}")
    with zipfile.ZipFile(ARCHIVE_NAME, "r") as z:
        z.extractall(".")
    print("[INFO] Extraction complete.")


def process(output_filepath):
    # Find all extracted CSV files (monday.csv, tuesday.csv, etc.)
    day_files = sorted([f for f in os.listdir(".") if f.endswith(".csv") and f not in
                        [OUTPUT_FILENAME] and not f.startswith("Reformatted")])

    if not day_files:
        raise RuntimeError("No day CSV files found. Run download() first.")

    print(f"[INFO] Processing {len(day_files)} day file(s): {day_files}")
    first_write = True
    total_rows = 0

    for fname in day_files:
        print(f"[INFO] Reading: {fname}")
        for chunk in pd.read_csv(fname, chunksize=200_000, low_memory=False):
            # Find label column
            label_col = None
            for candidate in ["Label", "label", "Class", "class"]:
                if candidate in chunk.columns:
                    label_col = candidate
                    break
            if label_col is None:
                label_col = chunk.columns[-1]

            chunk.rename(columns={label_col: "attack_name"}, inplace=True)
            chunk["attack_name"] = chunk["attack_name"].astype(str).str.strip()

            # attack_flag: "Benign" and "Attempted" variants of benign → 0; everything else → 1
            chunk["attack_flag"] = chunk["attack_name"].apply(
                lambda x: 0 if x.lower() == "benign" else 1
            )

            chunk["attack_step"] = chunk["attack_name"].apply(_map_label)

            target_columns = ["attack_name", "attack_flag", "attack_step"]
            feature_columns = [c for c in chunk.columns if c not in target_columns]
            chunk = chunk[feature_columns + target_columns]

            chunk.to_csv(output_filepath, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(chunk)

        print(f"[INFO] Done: {fname}")

    print(f"[INFO] Total rows: {total_rows:,}")
    print(f"[INFO] Output: {output_filepath}")


if __name__ == "__main__":
    extracted_csvs = [f for f in os.listdir(".") if f.endswith(".csv")
                      and f not in [OUTPUT_FILENAME] and not f.startswith("Reformatted")]

    if not extracted_csvs and not os.path.exists(ARCHIVE_NAME):
        download()
    elif not extracted_csvs and os.path.exists(ARCHIVE_NAME):
        print(f"[INFO] Archive exists. Extracting...")
        with zipfile.ZipFile(ARCHIVE_NAME, "r") as z:
            z.extractall(".")
    else:
        print(f"[INFO] Source files found: {extracted_csvs}")

    if not os.path.exists(OUTPUT_FILENAME):
        process(OUTPUT_FILENAME)
    else:
        print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
