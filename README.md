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
| **[NSL-KDD](./nsl-kdd)** | general-purpose, anomaly | Verified (download.py added) |
| **[UNSW-NB15](./unsw-nb15)** | general-purpose, anomaly | Verified (download.py added) |
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
| **[NSL-KDD](./nsl-kdd)** (new download.py) | general-purpose, anomaly | 148k | 0,1,4,5,6,7 | Kaggle: hassan06/nslkdd |
| **[UNSW-NB15](./unsw-nb15)** (new download.py) | general-purpose, anomaly | 258k | 0,1,4,5,6,7 | Kaggle: mrwellsdavid/unsw-nb15 |
| **[InSDN](./insdn)** | sdn | 344k | 0,1,4,6,7 | SDN environment, 8 attack types |
| **[Bot-IoT](./bot-iot)** | iot, botnet, dos-ddos | ~3.6M | 0,1,7 | Full coverage after re-download |
| **[CIC-DDoS2019](./cic-ddos2019)** | dos-ddos, general-purpose | 431k | 0,3,7 | 10+ DrDoS attack types |

### Phase 2 — Improved CIC-IDS (Liu et al., 2022)

Fixed CICFlowMeter feature extraction and corrected labeling.  
Source: https://intrusion-detection.distrinet-research.be/CNS2022/

| Dataset | Tags | Notes |
|---|---|---|
| **[CIC-IDS2017 Improved](./cicids2017-imp)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | 328 MB zip; wget from distrinet URL |
| **[CSE-CIC-IDS2018 Improved](./cicids2018-imp)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | 9.7 GB zip; wget from distrinet URL |

### Phase 2 — Verified (New in this release)

| Dataset | Tags | Rows | Kill-chain steps | Notes |
|---|---|---|---|---|
| **[Kitsune](./kitsune)** | iot, anomaly | 1.8M | 0,1,4,6,7 | 9 scenarios × 200k sample; Kaggle `ymirsky/network-attack-dataset-kitsune` |
| **[IoT-23](./iot-23)** | iot, botnet | 2.6M | 0,1,6,7 | 20 scenarios; official CTU source (no Kaggle required) |

### Phase 2 — Pending (License acceptance required on Kaggle)

Run `python3 download.py` after accepting the dataset license at the URL shown.

| Dataset | Tags | Kaggle URL | Status |
|---|---|---|---|
| **[AWID2](./awid2)** | wireless | kaggle.com/datasets/kolias93/awid2-wifi-intrusion-dataset | download.py ready |
| **[AWID3](./awid3)** | wireless | kaggle.com/datasets/chatzoglou/awid3 | download.py ready |

Full tag definitions and paths are in [`datasets.yaml`](./datasets.yaml).

---

## Dataset Details

### KDDCup 1999
- **Source:** `kddcup99` (scikit-learn built-in) / Kaggle `galaxyh/kdd-cup-1999-data`
- **Label column:** `label` → renamed to `attack_name`
- **Attack types:** smurf, neptune, normal, back, satan, ipsweep, portsweep, warezclient, teardrop, pod, nmap, guess_passwd, buffer_overflow, land, warezmaster, imap, rootkit, loadmodule, ftp_write, multihop, phf, perl, spy

### NSL-KDD
- **Source:** Kaggle `hassan06/nslkdd` (KDDTrain+.txt, KDDTest+.txt)
- **Format:** 41 KDD features + label + difficulty score (43 cols)
- **Attack types:** Probe (ipsweep, nmap, portsweep, satan, saint, mscan, ...), R2L (guess_passwd, ftp_write, ...), U2R (buffer_overflow, rootkit, ps, ...), DoS (neptune, smurf, back, apache2, mailbomb, ...)

### UNSW-NB15
- **Source:** Kaggle `mrwellsdavid/unsw-nb15`
- **Label column:** `attack_cat` → `attack_name`, `label` → `attack_flag`
- **Attack categories:** Normal (0), Reconnaissance (1), Analysis (1), Fuzzers (1), Exploits (4), Shellcode (4), Generic (4), Backdoor (5), Worms (6), DoS (7)

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
- **Source:** Kaggle `kk0105/allflowmeter-hikari2021`
- **Label columns:** `traffic_category` → `attack_name`, `Label` → `attack_flag`
- **Attack types:** Background/Benign (step=0), Probing (step=1), Bruteforce/Bruteforce-XML (step=4), XMRIGCC CryptoMiner (step=7)

### InSDN
- **Source:** Kaggle `badcodebuilder/insdn-dataset`
- **Environment:** Software-Defined Networking (SDN) with OpenFlow/OVS
- **Attack types:** Normal (0), Probe (1), BFA/Web-Attack/U2R (4), BOTNET (6), DoS/DDoS (7)
- **Files:** Normal_data.csv + metasploitable-2.csv + OVS.csv (concatenated)

### Bot-IoT
- **Source:** Kaggle `vigneshvenkateswaran/bot-iot`
- **Label columns:** `category` → `attack_name`, `attack` → `attack_flag`
- **Attack types:** Normal (0), Reconnaissance (1), DoS/DDoS/Theft (7)

### CIC-DDoS2019
- **Source:** Kaggle `dhoogla/cicddos2019` (parquet, 17 files)
- **Attack types:** Benign (0), TFTP (3), all DrDoS/DDoS/UDP flooding variants (7)

### CIC-IDS2017 Improved *(Liu et al., 2022)*
- **Source:** `https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip`
- **Files:** monday.csv, tuesday.csv, wednesday.csv, thursday.csv, friday.csv
- **Note:** Uses "Attempted" sub-label for flows intended as attacks with no malicious behavior

### CSE-CIC-IDS2018 Improved *(Liu et al., 2022)*
- **Source:** `https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CSECICIDS2018_improved.zip` (9.7 GB)
- **Note:** Same fix approach as CIC-IDS2017 improved; requires significant disk space

### Kitsune *(license required)*
- **Source:** Kaggle `ymirsky/kitsune-network-attack-dataset`
- **Structure:** 9 attack scenarios × `{scenario}_dataset.csv` (115 features) + `{scenario}_labels.csv`
- **Attack scenarios:** ARP MitM (4), Active Wiretap (4), Fuzzing (1), SSDP Flood (7), SSL Renegotiation (7), SYN DoS (7), Mirai (6), OS Scan (1), Video Injection (4)

### AWID2 / AWID3 *(license required)*
- **Source:** Kaggle `kolias93/awid2-wifi-intrusion-dataset` / `chatzoglou/awid3`
- **Environment:** 802.11 Wi-Fi SOHO testbed
- **AWID2:** Deauthentication, injection, impersonation attacks
- **AWID3:** 13 attack categories including KRACK, Kr00k, deauth/disassoc flood

### Kitsune
- **Source:** Kaggle `ymirsky/network-attack-dataset-kitsune` (no license required)
- **Structure:** 9 attack scenarios, each directory has `{Name}_dataset.csv` (115 features, no header) + `{name}_labels.csv`
- **Attack scenarios:** ARP MitM (4), Active Wiretap (4), Fuzzing (1), Mirai Botnet (6), OS Scan (1), SSDP Flood (7), SSL Renegotiation (7), SYN DoS (7), Video Injection (4)
- **Sampling:** 200k rows per scenario (total ~1.8M rows)

### IoT-23
- **Source:** Official CTU/Stratosphere: `https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/`
- **Format:** Zeek conn.log (tab-separated), last field contains `tunnel_parents  label  detailed-label` (space-separated)
- **Attack types:** Benign (0), PortScan (1), C&C variants (6), DDoS/Attack (7)
- **20 scenarios:** Mirai, Torii, Okiru, Muhstik and other IoT malware families
- **Sampling:** 200k rows per scenario (total ~2.6M rows)

---

## Prerequisites

| Requirement | Purpose | Install |
|---|---|---|
| Python 3.8+ | All datasets | — |
| Python packages | All datasets | `pip install -r requirements.txt` |
| Kaggle API key | All Kaggle-based datasets | `~/.kaggle/kaggle.json` ([guide](https://www.kaggle.com/docs/api)) |
| `wget` | LSPR23, CIC-IDS improved | Linux/Mac: built-in · Windows: `winget install GnuWin32.Wget` or WSL |

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

### CIC-IDS2017 / CSE-CIC-IDS2018 Improved (Liu et al., 2022)

These improved versions fix labeling errors and feature extraction bugs in the originals.

```bash
# CIC-IDS2017 improved (328MB zip)
cd cicids2017-imp
python3 download.py

# CSE-CIC-IDS2018 improved (9.7GB zip — requires significant time and disk space)
cd cicids2018-imp
python3 download.py
```

### Kitsune

Kitsune consists of 9 attack scenarios, each with a separate `{scenario}_dataset.csv` (115 network-stat features, no header) and a matching `{scenario}_labels.csv`. The `download.py` script locates these pairs automatically, reads the feature files with correct column names (`feature_0` … `feature_114`), and merges them with the per-scenario kill-chain labels.

> **License acceptance required.** Visit https://www.kaggle.com/datasets/ymirsky/kitsune-network-attack-dataset and accept the terms before running.

```bash
cd kitsune
python3 download.py
```

### AWID2 / AWID3 / IoT-23

These datasets require accepting specific licenses on Kaggle before the download will work.

```bash
# Accept license at Kaggle first, then:
cd awid2 && python3 download.py
cd awid3 && python3 download.py
cd iot-23 && python3 download.py
```

> **IoT-23 note:** The source `surajsooraj26/iot-23` only contains `-` labels (benign flows). Use `pchaberger/iot-23-network-traffic-dataset` instead.

### IIoT Datasets (Edge-IIoT, XIIoTID, NF-ToN-IoT-v3, WUSTL-IIoT-2021)

These datasets are downloaded from Kaggle via `kagglehub`. A Kaggle account and API key (`~/.kaggle/kaggle.json`) are required.

Each `download.py`:
1. Downloads from Kaggle (skips if the raw CSV already exists locally).
2. Validates that the expected columns are present.
3. Applies the standardized `attack_name`, `attack_flag`, `attack_step` mapping.

---

## License & Citation

- The download and processing scripts are provided for convenience and standardization.
- Each dataset's license and citation requirements are governed by their original creators. Please ensure you properly cite the original papers and authors when using these datasets for your research.
