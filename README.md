# Cybersecurity & IoT Datasets

A comprehensive collection of publicly available datasets widely used for machine learning and deep learning research in cybersecurity, Intrusion Detection Systems (IDS), and IoT environments.

## Core Concept: Standardized Labeling

The most important feature of this repository is data standardization.  
Every dataset in this repository is processed so that the final CSV files end with the exact same three columns:

1. `attack_name`
2. `attack_flag`
3. `attack_step`

When you run the `download.py` scripts, they do not just download the raw CSV files; they automatically process and format the files to ensure they conclude with these three standard columns. This standardized format makes it significantly easier to perform cross-dataset evaluations and train universal machine learning models.

### Kill-Chain Step Mapping

`attack_step` encodes each traffic record's position in the Cyber Kill Chain:

| Step | Phase |
|---|---|
| 0 | Benign / Normal |
| 1 | Reconnaissance |
| 2 | Weaponization |
| 3 | Delivery |
| 4 | Exploitation |
| 5 | Installation |
| 6 | Command & Control (C&C) |
| 7 | Actions on Objectives (DoS/DDoS/Exfil) |
| -1 | Unknown |

---

## Available Datasets

### Phase 1 — Original Collection

| Dataset | Tags | Status |
|---|---|---|
| **[CICIDS2017](./cicids2017)** / **[CICIDS2018](./cicids2018)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, infiltration, botnet | Verified |
| **[CICIoT2023](./ciciot2023)** | iot, general-purpose | Verified |
| **[NSL-KDD](./nsl-kdd)** | general-purpose, anomaly | Verified |
| **[UNSW-NB15](./unsw-nb15)** | general-purpose, anomaly | Verified |
| **[ToN-IoT](./ton-iot)** | iiot-ics, general-purpose | Verified |
| **[Mirai Botnet Dataset](./mirai)** | iot, botnet | Verified |
| **[EPIC Attack Datasets](./EPIC_Attack_Datasets)** | apt | Verified |
| **[Edge-IIoT](./edge-iiot)** | iiot-ics, iot | Verified |
| **[XIIoTID](./xiiotid)** | iiot-ics, iot | Verified |
| **[NF-ToN-IoT-v3](./nf-ton-iot-v3)** | iiot-ics | Verified |
| **[WUSTL-IIoT-2021](./wustl-iiot-2021)** | iiot-ics | Verified |
| **[LSPR23](./lspr23)** | general-purpose, anomaly | Verified |

### Phase 2 — Expansion (Verified)

| Dataset | Tags | Rows | Kill-chain steps | Notes |
|---|---|---|---|---|
| **[KDDCup 1999](./kddcup1999)** | general-purpose, anomaly | 494k | 0,1,4,5,7 | Full attack coverage |
| **[CTU-13](./ctu-13)** | botnet | 1.6M | 0,6 | Botnet vs Background/Normal |
| **[N-BaIoT](./n-baiot)** | iot, botnet | 2.4M+ | 0,1,7 | Mirai & Gafgyt families |
| **[CIDDS-001](./cidds-001)** | general-purpose, scan | 204k | 0,1,4 | BruteForce + PortScan |
| **[CIDDS-002](./cidds-002)** | general-purpose, scan | 2.6M | 0,1 | Scan attacks |
| **[IoTID20](./iotid20)** | iot | 626k | 0,1,4,6,7 | Mirai, DoS, Scan, MITM ARP |
| **[HIKARI-2021](./hikari-2021)** | general-purpose | 555k | 0,1,4,7 | Probing, Bruteforce, CryptoMiner |

### Phase 2 — Partial (Re-download needed for full coverage)

These datasets have correct `download.py` scripts and working kill-chain mapping, but the current raw file was created from only a subset of source files. Delete the raw file and re-run `download.py` for full attack coverage.

| Dataset | Tags | Current rows | Current labels | Raw file to delete |
|---|---|---|---|---|
| **[Bot-IoT](./bot-iot)** | iot, botnet, dos-ddos | 1M | Normal, Reconnaissance | `Bot-IoT.csv` |
| **[CIC-DDoS2019](./cic-ddos2019)** | dos-ddos, general-purpose | 6.7k | Benign, DrDoS_DNS | `CIC-DDoS2019.csv` |

### Phase 2 — Pending (Not yet verified)

The following directories are excluded from version control (`.gitignore`) until a full re-download and kill-chain verification is complete.

| Dataset | Tags | Reason |
|---|---|---|
| **Kitsune** | iot, anomaly | Full dataset ~54 GB; needs complete Kaggle re-download |
| **IoT-23** | iot, botnet | Source CSV only contained benign flows (`-` labels) |
| **InSDN** | sdn | Source CSV only contained Normal traffic |
| **AWID2** | wireless | 745 source CSVs; sampled batch was all Normal |
| **AWID3** | wireless | Same issue as AWID2 |

Full tag definitions and paths are in [`datasets.yaml`](./datasets.yaml).

---

## Dataset Details

### KDDCup 1999
- **Source:** `kddcup99` (scikit-learn built-in)
- **Label column:** `label` → renamed to `attack_name`
- **Attack types:** smurf, neptune, normal, back, satan, ipsweep, portsweep, warezclient, teardrop, pod, nmap, guess_passwd, buffer_overflow, land, warezmaster, imap, rootkit, loadmodule, ftp_write, multihop, phf, perl, spy

### CTU-13
- **Source:** Kaggle `dhoogla/ctu13` (13 parquet files)
- **Label column:** `label` (e.g., `flow=From-Botnet-V42-TCP-...`) → strips `flow=` prefix
- **Attack classification:** Labels containing "botnet" → step=6, "normal"/"background" → step=0

### N-BaIoT
- **Source:** Kaggle `mkashifn/nbaiot-dataset`
- **Label source:** Filename-based (no label column in raw data)
  - `{device}.benign.csv` → benign (step=0)
  - `{device}.mirai.scan.csv` → mirai.scan (step=1)
  - `{device}.mirai.{syn,ack,udp,udpplain}.csv` → step=7
  - `{device}.gafgyt.{combo,junk,tcp,udp}.csv` → step=7
  - `{device}.gafgyt.scan.csv` → step=1
- **Devices:** Danmini, Ecobee, Ennio, Philips B120N, Provision PT737E, Provision PT1, Samsung SNH, SimpleHome XCS7 1002, SimpleHome XCS7 1003

### CIDDS-001
- **Source:** Kaggle `dhoogla/cidds001` (parquet)
- **Label column:** `attack_type` → renamed to `attack_name`
- **Attack types:** benign (step=0), PortScan (step=1), BruteForce (step=4)

### CIDDS-002
- **Source:** Kaggle `dhoogla/cidds002` (parquet)
- **Label column:** `attack_type` → renamed to `attack_name`
- **Attack types:** benign (step=0), scan (step=1)

### IoTID20
- **Source:** Kaggle `azalhowayleh/iotid20`
- **Label columns:** `Cat` → `attack_name`, `Label` → `attack_flag`
- **Attack types:** Normal (step=0), Scan (step=1), MITM ARP Spoofing (step=4), Mirai (step=6), DoS (step=7)

### HIKARI-2021
- **Source:** Kaggle `nilaychauhan/hikari-2021`
- **Label columns:** `traffic_category` → `attack_name`, `Label` → `attack_flag`
- **Attack types:** Background/Benign (step=0), Probing (step=1), Bruteforce/Bruteforce-XML (step=4), XMRIGCC CryptoMiner (step=7)

### Bot-IoT *(partial)*
- **Source:** Kaggle `anushonkar/bot-iot-dataset`
- **Label columns:** `category` → `attack_name`, `attack` → `attack_flag`
- **Current data:** Normal + Reconnaissance only. Re-download for DoS/DDoS/Theft coverage.

### CIC-DDoS2019 *(partial)*
- **Source:** Kaggle `dhoogla/cicddos2019` (parquet)
- **Current data:** Benign + DrDoS_DNS only. Re-download for full 10-attack-type coverage.

---

## Prerequisites

| Requirement | Purpose | Install |
|---|---|---|
| Python 3.8+ | All datasets | — |
| Python packages | All datasets | `pip install -r requirements.txt` |
| Kaggle API key | All Kaggle-based datasets | `~/.kaggle/kaggle.json` ([guide](https://www.kaggle.com/docs/api)) |
| `wget` | LSPR23 only | Linux/Mac: built-in · Windows: `winget install GnuWin32.Wget` or WSL |

> **Windows note:** `download_all.sh` requires WSL or Git Bash. Individual `download.py` scripts run natively with Python.

---

## Quick Start

### 1. Basic Setup

```bash
# Clone the repository
git clone https://github.com/comsyssec/datasets.git
cd datasets

# Install required libraries
python3 -m pip install -r requirements.txt
```

### 2. Download Specific Dataset

Go to the dataset directory you want and run the script:

```bash
# Example: cicids2017
cd cicids2017
python3 download.py
```

### 3. Download ALL Datasets at Once

```bash
bash download_all.sh
```

To download only specific datasets:

```bash
bash download_all.sh cicids2017 lspr23
```

> **Note:** LSPR23 downloads automatically (~compressed archive from Zenodo). `wget` must be installed.

---

## Special Instructions for Specific Datasets

### LSPR23

LSPR23 is automatically downloaded from [Zenodo](https://zenodo.org/records/8042347) via the API. `wget` must be installed (`wget -c` is used to support resume on interruption).

```bash
cd lspr23
python3 download.py
```

**Result:** Downloads the archive, extracts it to `lspr23/LSPR23/`, then processes the 9.8 GB CSV in chunks. Output: `LSPR23/ls23pr_flows/Reformatted_LSPR23.csv`.

### Kitsune

Kitsune consists of 9 attack scenarios, each with a separate `{scenario}_dataset.csv` (115 network-stat features, no header) and a matching `{scenario}_labels.csv`. The `download.py` script locates these pairs automatically, reads the feature files with correct column names (`feature_0` … `feature_114`), and merges them with the per-scenario kill-chain labels.

> **Full dataset is ~54 GB.** The script samples up to 200,000 rows per scenario. If `Kitsune.csv` is absent, running `download.py` will trigger the full Kaggle download.

```bash
cd kitsune
python3 download.py
```

**Result:** `Kitsune.csv` (merged, labeled) → `Reformatted_Kitsune.csv`.

### Partial datasets (re-download for full coverage)

For Bot-IoT and CIC-DDoS2019, the current Reformatted files have limited attack coverage because the original raw file was built from only a subset of the Kaggle source. Delete the raw input file and re-run:

```bash
# Bot-IoT: adds DoS, DDoS, Theft attack types
rm bot-iot/Bot-IoT.csv
cd bot-iot && python3 download.py

# CIC-DDoS2019: adds all 10 DrDoS attack types
rm cic-ddos2019/CIC-DDoS2019.csv
cd cic-ddos2019 && python3 download.py
```

### IIoT Datasets (Edge-IIoT, XIIoTID, NF-ToN-IoT-v3, WUSTL-IIoT-2021)

These datasets are downloaded from Kaggle via `kagglehub`. A Kaggle account and API key (`~/.kaggle/kaggle.json`) are required.

Each `download.py`:
1. Downloads from Kaggle (skips if the raw CSV already exists locally).
2. Validates that the expected columns are present.
3. Applies the standardized `attack_name`, `attack_flag`, `attack_step` mapping.

> **Note on NF-ToN-IoT-v3:** The Kaggle source (`seyhed/nf-ton-iot-v3`) may provide the full dataset; the previously stored file was a reduced subset. Column structure is identical.

> **Note on WUSTL-IIoT-2021:** Uses a Kaggle re-upload. If column validation fails, download manually from the [WUSTL Edge Lab](https://www.cse.wustl.edu/~jain/iiot/index.html).

---

## License & Citation

- The download and processing scripts are provided for convenience and standardization.
- Each dataset's license and citation requirements are governed by their original creators. Please ensure you properly cite the original papers and authors when using these datasets for your research.
