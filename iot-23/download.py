"""
IoT-23 Dataset — CTU IoT Botnet Dataset
Official source: Stratosphere Research Laboratory (CTU, Czech Technical University)
  https://www.stratosphereips.org/datasets-iot23

Data format: Zeek conn.log (tab-separated) with appended label columns.
  - 20 tab-separated flow fields: ts, uid, id.orig_h, id.orig_p, id.resp_h, id.resp_p,
    proto, service, duration, orig_bytes, resp_bytes, conn_state, local_orig, local_resp,
    missed_bytes, history, orig_pkts, orig_ip_bytes, resp_pkts, resp_ip_bytes
  - Last field (space-separated within the tab): tunnel_parents  label  detailed-label

Labels:
  label: "Benign" | "Malicious"
  detailed-label: "-" (benign) | attack type string

20 attack scenarios (malware families: Mirai, Torii, Okiru, Muhstik, etc.)
"""
import os
import urllib.request
import pandas as pd

BASE_URL = "https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/"
INPUT_FILENAME = "IoT-23.csv"
OUTPUT_FILENAME = "Reformatted_IoT-23.csv"
MAX_ROWS_PER_SCENARIO = 200_000

# IoT-23 detailed-label → kill-chain step
KILL_CHAIN = {
    "benign": 0,
    "-": 0,
    # Reconnaissance
    "partofahorizontalportscan": 1,
    "portscan": 1,
    # C&C (all botnet C&C variants)
    "c&c": 6,
    "c&c-heartbeat": 6,
    "c&c-heartbeat-attack": 6,
    "c&c-heartbeat-localnetwork": 6,
    "c&c-mirai": 6,
    "c&c-torii": 6,
    "c&c-okiru": 6,
    "c&c-filedownload": 6,
    "c&c-heartbeat-filedownload": 6,
    "filedownload": 6,
    "okiru": 6,        # Okiru botnet (Mirai variant) C&C activity
    # Actions on Objectives
    "ddos": 7,
    "attack": 7,
    "dos": 7,
    "okiru-attack": 7, # Okiru attack phase (DDoS/DoS)
}

FLOW_FIELDS = [
    "ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p",
    "proto", "service", "duration", "orig_bytes", "resp_bytes", "conn_state",
    "local_orig", "local_resp", "missed_bytes", "history",
    "orig_pkts", "orig_ip_bytes", "resp_pkts", "resp_ip_bytes",
]


def _get_scenarios():
    """Return list of scenario names from the official index page."""
    import re
    req = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        content = r.read().decode("utf-8", errors="ignore")
    return re.findall(r'href="(CTU-IoT[^"]+/)"', content)


def _parse_label(last_field):
    """Parse the combined 'tunnel_parents  label  detailed-label' field."""
    parts = last_field.strip().split()
    if len(parts) < 3:
        return "benign", "-"
    # parts[0] = tunnel_parents, parts[1] = label, parts[2] = detailed-label
    label = parts[1]        # "Benign" or "Malicious"
    detailed = parts[2]     # "-" or attack type
    return label, detailed


def _stream_scenario(scenario_dir, max_rows):
    """Stream-download a scenario's conn.log.labeled, return rows as list of dicts."""
    url = f"{BASE_URL}{scenario_dir}bro/conn.log.labeled"
    rows = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            for raw_line in r:
                line = raw_line.decode("utf-8", errors="ignore").rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) < 21:
                    continue
                label_str, detailed = _parse_label(parts[-1])
                attack_name = detailed.lower() if label_str.lower() == "malicious" else "benign"
                row = dict(zip(FLOW_FIELDS, parts[:20]))
                row["attack_name"] = attack_name
                rows.append(row)
                if max_rows and len(rows) >= max_rows:
                    break
    except Exception as e:
        print(f"[WARN] Error streaming {scenario_dir}: {e}")
    return rows


def download():
    print(f"[INFO] Fetching scenario list from: {BASE_URL}")
    scenarios = _get_scenarios()
    print(f"[INFO] Found {len(scenarios)} scenario(s)")

    dst = os.path.join(os.getcwd(), INPUT_FILENAME)
    first_write = True
    total_rows = 0
    all_labels = set()

    for sc_dir in scenarios:
        sc_name = sc_dir.strip("/")
        print(f"[INFO] Downloading: {sc_name} (max {MAX_ROWS_PER_SCENARIO:,} rows)")
        rows = _stream_scenario(sc_dir, MAX_ROWS_PER_SCENARIO)
        if not rows:
            print(f"[WARN] No data for {sc_name}, skipping.")
            continue
        df = pd.DataFrame(rows)
        all_labels.update(df["attack_name"].unique())
        df.to_csv(dst, index=False, mode="w" if first_write else "a", header=first_write)
        first_write = False
        total_rows += len(df)
        n_attack = (df["attack_name"] != "benign").sum()
        print(f"  → {len(df):,} rows, attack={n_attack:,}, "
              f"labels={sorted(df['attack_name'].unique())}")

    print(f"[INFO] Saved as: {dst}  (total {total_rows:,} rows)")
    print(f"[INFO] All unique labels: {sorted(all_labels)}")


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
        print(f"[WARNING] Unmapped labels: {unmapped}")
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
