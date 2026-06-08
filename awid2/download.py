"""
AWID2 — Aegean Wi-Fi Intrusion Dataset 2
두 가지 다운로드 방법:

  방법 1 (즉시): Kaggle 라이선스 수락 후 kagglehub 사용
    → https://www.kaggle.com/datasets/kolias93/awid2-wifi-intrusion-dataset

  방법 2 (1-3일 소요): 공식 사이트 이메일 요청
    → https://icsdweb.aegean.gr/awid/download-dataset
    → 폼 제출 시 이메일로 다운로드 링크 수신
    → 이 스크립트의 register() 함수로 자동 제출 가능

Environment: 802.11 Wi-Fi testbed (SOHO)
Attacks: injection, impersonation, flooding, deauthentication
"""
import kagglehub
import json
import os
import urllib.request
import pandas as pd

KAGGLE_DATASET = "kolias93/awid2-wifi-intrusion-dataset"
INPUT_FILENAME = "AWID2.csv"
OUTPUT_FILENAME = "Reformatted_AWID2.csv"

OFFICIAL_REGISTER_URL = "https://icsdweb.aegean.gr/awid/src/api/register.php"

# AWID2 class → kill-chain step
KILL_CHAIN = {
    "normal": 0,
    "injection": 4,         # 802.11 packet injection → Exploitation
    "impersonation": 4,     # AP/client impersonation → Exploitation
    "flooding": 7,          # Deauth/probe flooding DoS → Actions on Objectives
    "deauthentication": 7,  # Forced disconnection → Actions on Objectives
}


def register(name, lastname, email, affiliation, notes="Research purpose",
             website="", events="research", request_awid3_csv=False):
    """Submit AWID dataset request to official site.
    A download link will be sent to the provided email within 1-3 days.
    """
    data = {
        "name": name,
        "lastname": lastname,
        "email": email,
        "affiliation": affiliation,
        "events": events,
        "notes": notes,
        "website": website,
        "awid2": True,
        "awid3Pcap": False,
        "awid3Csv": request_awid3_csv,
        "H23Q": False,
        "value": "script-submitted",
    }
    print(f"[INFO] Submitting AWID2 request for: {email}")
    req = urllib.request.Request(
        OFFICIAL_REGISTER_URL,
        data=json.dumps(data).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://icsdweb.aegean.gr/awid/download-dataset",
            "Origin": "https://icsdweb.aegean.gr",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = r.read().decode("utf-8", errors="ignore")
    print(f"[INFO] Response: {resp[:200]}")
    print(f"[INFO] Check your email '{email}' for the download link (1-3 days).")
    return resp


def download_from_link(download_url):
    """Download AWID2 from the link received by email."""
    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    print(f"[INFO] Downloading from: {download_url}")
    req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r, open(dst, "wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)
    print(f"[INFO] Saved as: {dst}")


def download():
    print(f"[INFO] Attempting Kaggle download: {KAGGLE_DATASET}")
    print(f"[INFO] If 403, accept license at: https://www.kaggle.com/datasets/{KAGGLE_DATASET}")
    print(f"[INFO] Alternative: call register() then download_from_link(email_url)")
    path = kagglehub.dataset_download(KAGGLE_DATASET)

    csvs = []
    for root, _, files in os.walk(path):
        for f in sorted(files):
            if f.endswith(".csv"):
                csvs.append(os.path.join(root, f))

    if not csvs:
        raise RuntimeError(f"No CSV found in {path}. Files: {os.listdir(path)}")

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0
    for csv_path in csvs:
        try:
            df_part = pd.read_csv(csv_path, low_memory=False)
            df_part.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
            first_write = False
            total_rows += len(df_part)
            print(f"[INFO] {os.path.basename(csv_path)}: {len(df_part):,} rows")
        except Exception as e:
            print(f"[WARN] Skipping {csv_path}: {e}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")
    df = pd.read_csv(dst, nrows=5)
    label_col = next((c for c in ["class", "Class", "label", "Label"] if c in df.columns),
                     df.columns[-1])
    print(f"[INFO] Label column: {label_col}, sample values: {df[label_col].unique().tolist()}")


def process(input_filepath, output_filepath):
    print(f"[INFO] Reading: {input_filepath}")
    df = pd.read_csv(input_filepath, low_memory=False)

    label_col = next((c for c in ["class", "Class", "label", "Label", "attack_type"]
                      if c in df.columns), df.columns[-1])
    df.rename(columns={label_col: "attack_name"}, inplace=True)
    df["attack_flag"] = (df["attack_name"].astype(str).str.strip().str.lower() != "normal").astype(int)

    name_series = df["attack_name"].astype(str).str.strip().str.lower()
    unmapped = name_series[~name_series.isin(KILL_CHAIN)].unique()
    if len(unmapped):
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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "register":
        # Usage: python3 download.py register NAME LASTNAME EMAIL AFFILIATION
        name = sys.argv[2] if len(sys.argv) > 2 else input("Name: ")
        lastname = sys.argv[3] if len(sys.argv) > 3 else input("Lastname: ")
        email = sys.argv[4] if len(sys.argv) > 4 else input("Email: ")
        affiliation = sys.argv[5] if len(sys.argv) > 5 else input("Affiliation: ")
        register(name, lastname, email, affiliation)
    elif len(sys.argv) > 1 and sys.argv[1] == "download-link":
        # Usage: python3 download.py download-link https://...
        download_from_link(sys.argv[2])
        process(INPUT_FILENAME, OUTPUT_FILENAME)
    else:
        if not os.path.exists(INPUT_FILENAME):
            download()
        else:
            print(f"[INFO] {INPUT_FILENAME} already exists, skipping download.")
        if not os.path.exists(OUTPUT_FILENAME):
            process(INPUT_FILENAME, OUTPUT_FILENAME)
        else:
            print(f"[INFO] {OUTPUT_FILENAME} already exists, skipping processing.")
