import kagglehub
import os
import pandas as pd

KAGGLE_DATASET = "hassan06/nslkdd"
INPUT_FILENAME = "NSL-KDD.csv"
OUTPUT_FILENAME = "Reformatted_NSL-KDD.csv"

# 41 KDD features + label + difficulty_score (43 cols total)
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
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty",
]

KILL_CHAIN = {
    "normal": 0,
    # Reconnaissance / Probe
    "ipsweep": 1, "nmap": 1, "portsweep": 1, "satan": 1,
    "saint": 1,     # security scanner
    "mscan": 1,     # multi-scan probe
    "snmpguess": 1, # SNMP community string guessing
    "xsnoop": 1,    # X11 network snooping
    # Exploitation — R2L (remote-to-local)
    "ftp_write": 4, "guess_passwd": 4, "imap": 4, "multihop": 4,
    "phf": 4, "spy": 4, "warezclient": 4, "warezmaster": 4,
    "snmpgetattack": 4, # SNMP exploitation
    "httptunnel": 4,    # covert HTTP tunnel
    "named": 4,         # BIND/DNS buffer overflow
    "sendmail": 4,      # Sendmail exploit
    "xlock": 4,         # X11 lock exploit
    "sqlattack": 4,     # SQL injection
    # Installation — U2R (user-to-root privilege escalation)
    "buffer_overflow": 5, "loadmodule": 5, "perl": 5, "rootkit": 5,
    "ps": 5,    # privilege escalation via ps
    "xterm": 5, # X11 privilege escalation
    # C&C
    "worm": 6,
    # Actions on Objectives — DoS
    "back": 7, "land": 7, "neptune": 7, "pod": 7, "smurf": 7, "teardrop": 7,
    "apache2": 7,      # Apache DoS
    "processtable": 7, # process table exhaustion
    "mailbomb": 7,     # mail bombing
    "udpstorm": 7,     # UDP flooding
}


def download():
    print(f"[INFO] Downloading from Kaggle: {KAGGLE_DATASET}")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    train_src = os.path.join(path, "KDDTrain+.txt")
    test_src = os.path.join(path, "KDDTest+.txt")

    if not os.path.exists(train_src):
        raise RuntimeError(f"KDDTrain+.txt not found in {path}. Files: {os.listdir(path)}")

    print(f"[INFO] Reading train: {train_src}")
    df_train = pd.read_csv(train_src, header=None, names=COLUMNS)
    print(f"[INFO] Reading test: {test_src}")
    df_test = pd.read_csv(test_src, header=None, names=COLUMNS)

    df = pd.concat([df_train, df_test], ignore_index=True)

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    df.to_csv(dst, index=False)
    print(f"[INFO] Saved as: {dst}  ({len(df):,} rows)")
    print(f"[INFO] Unique labels: {sorted(df['label'].unique().tolist())}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    # Drop difficulty score (NSL-KDD-specific metadata, not a network feature)
    df.drop(columns=["difficulty"], errors="ignore", inplace=True)

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
