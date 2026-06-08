import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "galaxyh/kdd-cup-1999-data"
INPUT_FILENAME = "KDDCup1999.csv"
OUTPUT_FILENAME = "Reformatted_KDDCup1999.csv"

# Column names from kddcup.names (42 features + label)
COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label",
]

KILL_CHAIN = {
    "normal": 0,
    # Reconnaissance / Probe
    "ipsweep": 1, "nmap": 1, "portsweep": 1, "satan": 1,
    # Delivery / R2L (remote-to-local exploitation)
    "ftp_write": 4, "guess_passwd": 4, "imap": 4, "multihop": 4,
    "phf": 4, "spy": 4, "warezclient": 4, "warezmaster": 4,
    # Installation / U2R (user-to-root privilege escalation)
    "buffer_overflow": 5, "loadmodule": 5, "perl": 5, "rootkit": 5,
    # Actions on Objectives — DoS
    "back": 7, "land": 7, "neptune": 7, "pod": 7, "smurf": 7, "teardrop": 7,
}


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    print(f"[INFO] Files: {os.listdir(path)}")

    src = os.path.join(path, "kddcup.data_10_percent_corrected")
    if not os.path.exists(src):
        src = os.path.join(path, "kddcup.data.corrected")
    if not os.path.exists(src):
        raise RuntimeError(f"Expected labeled data file not found in {path}")

    print(f"[INFO] Reading: {src}")
    df = pd.read_csv(src, header=None, names=COLUMNS)
    df["label"] = df["label"].str.rstrip(".")

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    df.to_csv(dst, index=False)
    print(f"[INFO] Saved as: {dst}")
    print(f"[INFO] Columns ({len(df.columns)}): {df.columns.tolist()}")
    print(f"[INFO] Unique labels: {df['label'].unique().tolist()}")
    print(f"[INFO] Sample:\n{df.head(2).to_string()}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    df.rename(columns={"label": "attack_name"}, inplace=True)
    df["attack_flag"] = (df["attack_name"] != "normal").astype(int)

    name_series = df["attack_name"].astype(str).str.strip().str.lower()
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
