# Cybersecurity & IoT Datasets

A comprehensive collection of publicly available datasets widely used for machine learning and deep learning research in cybersecurity, Intrusion Detection Systems (IDS), and IoT environments.

## Core Concept: Standardized Labeling

The most important feature of this repository is data standardization.
Every dataset is processed so that the final CSV files end with the exact same three columns:

1. `attack_name` — attack type string (lowercase)
2. `attack_flag` — binary label (0 = benign, 1 = attack)
3. `attack_step` — Cyber Kill Chain phase (integer)

Running `python3 download.py` in any dataset directory will download the raw data and produce a `Reformatted_*.csv` file in this standard format.

### Kill-Chain Step Mapping

| Step | Phase | Examples |
|---|---|---|
| 0 | Benign / Normal | Normal, Benign |
| 1 | Reconnaissance | PortScan, OS Scan, Fuzzing, Probe |
| 2 | Weaponization | *(unused)* |
| 3 | Delivery | TFTP amplification vector |
| 4 | Exploitation | Exploits, Brute Force, SQL Injection, XSS, Shellcode |
| 5 | Installation | U2R, Backdoor, Rootkit |
| 6 | Command & Control | Botnet C&C, Mirai, Torii, CTU-13 botnet |
| 7 | Actions on Objectives | DoS, DDoS, Exfiltration, Theft |
| -1 | Unknown / Unmapped | *(should be 0 for all verified datasets)* |

---

## Available Datasets

### Phase 1 — Original Collection (Verified)

| Dataset | Tags | Output file | Notes |
|---|---|---|---|
| **[CICIDS2017](./cicids2017)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | `training-flow.csv`, `test-flow.csv` | CICFlowMeter features |
| **[CSE-CIC-IDS2018](./cicids2018)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | `training-flow.csv`, `test-flow.csv` | Kaggle `solarmainframe/ids-intrusion-csv` |
| **[CICIoT2023](./ciciot2023)** | iot, general-purpose | `Reformatted_CICIoT2023.csv` | 105 IoT attack types |
| **[NSL-KDD](./nsl-kdd)** | general-purpose, anomaly | `Reformatted_NSL-KDD.csv` | 148k rows, 0/1/4/5/6/7 |
| **[UNSW-NB15](./unsw-nb15)** | general-purpose, anomaly | `Reformatted_UNSW-NB15.csv` | 258k rows, 10 attack categories |
| **[ToN-IoT](./ton-iot)** | iiot-ics, general-purpose | `Reformatted_*.csv` | — |
| **[Mirai Botnet Dataset](./mirai)** | iot, botnet | `training-flow.csv`, `test-flow.csv` | Raw pcap + flow |
| **[EPIC Attack Datasets](./EPIC_Attack_Datasets)** | apt | `Reformatted_*.csv` | APT scenarios |
| **[Edge-IIoTset](./edge-iiot)** | iiot-ics, iot | `Reformatted_*.csv` | — |
| **[XIIoTID](./xiiotid)** | iiot-ics, iot | `Reformatted_*.csv` | — |
| **[NF-ToN-IoT-v3](./nf-ton-iot-v3)** | iiot-ics | `Reformatted_*.csv` | NetFlow v9 features |
| **[WUSTL-IIoT-2021](./wustl-iiot-2021)** | iiot-ics | `Reformatted_*.csv` | SCADA environment |
| **[LSPR23](./lspr23)** | general-purpose, anomaly | `LSPR23/ls23pr_flows/Reformatted_LSPR23.csv` | 9.8 GB CSV, chunked |

### Phase 2 — Expansion (Verified, unmapped=0)

| Dataset | Tags | Rows | Steps | Source |
|---|---|---|---|---|
| **[KDDCup 1999](./kddcup1999)** | general-purpose, anomaly | 494k | 0,1,4,5,7 | Kaggle `galaxyh/kdd-cup-1999-data` |
| **[CTU-13](./ctu-13)** | botnet | 1.6M | 0,6 | Kaggle `dhoogla/ctu13` |
| **[N-BaIoT](./n-baiot)** | iot, botnet | 2.4M+ | 0,1,7 | Kaggle `mkashifn/nbaiot-dataset` |
| **[CIDDS-001](./cidds-001)** | general-purpose, scan | 204k | 0,1,4 | Kaggle `dhoogla/cidds001` |
| **[CIDDS-002](./cidds-002)** | general-purpose, scan | 2.6M | 0,1 | Kaggle `dhoogla/cidds002` |
| **[IoTID20](./iotid20)** | iot | 626k | 0,1,4,6,7 | Kaggle `rohulaminlabid/iotid20-dataset` |
| **[HIKARI-2021](./hikari-2021)** | general-purpose | 555k | 0,1,4,7 | Kaggle `kk0105/allflowmeter-hikari2021` |
| **[NSL-KDD](./nsl-kdd)** | general-purpose, anomaly | 148k | 0,1,4,5,6,7 | Kaggle `hassan06/nslkdd` |
| **[UNSW-NB15](./unsw-nb15)** | general-purpose, anomaly | 258k | 0,1,4,5,6,7 | Kaggle `mrwellsdavid/unsw-nb15` |
| **[InSDN](./insdn)** | sdn | 344k | 0,1,4,6,7 | Kaggle `badcodebuilder/insdn-dataset` |
| **[Bot-IoT](./bot-iot)** | iot, botnet, dos-ddos | 73.4M | 0,1,7 | Kaggle `vigneshvenkateswaran/bot-iot` |
| **[CIC-DDoS2019](./cic-ddos2019)** | dos-ddos, general-purpose | 431k | 0,3,7 | Kaggle `dhoogla/cicddos2019` |
| **[Kitsune](./kitsune)** | iot, anomaly | 1.8M | 0,1,4,6,7 | Kaggle `ymirsky/network-attack-dataset-kitsune` |
| **[IoT-23](./iot-23)** | iot, botnet | 2.6M | 0,1,6,7 | Official CTU: mcfp.felk.cvut.cz |

### Phase 2 — Improved CIC-IDS (Liu et al., 2022)

Fixed CICFlowMeter tool and corrected labeling errors in original CIC datasets.
Source: https://intrusion-detection.distrinet-research.be/CNS2022/

| Dataset | Tags | Rows | Steps | Notes |
|---|---|---|---|---|
| **[CIC-IDS2017 Improved](./cicids2017-imp)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | 2.1M | 0,1,4,6,7 | `CICIDS2017_improved.zip` (328 MB) |
| **[CSE-CIC-IDS2018 Improved](./cicids2018-imp)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | 63.2M | 0,4,6,7 | `CSECICIDS2018_improved.zip` (9.7 GB) |

### Phase 2 — Pending (Kaggle license acceptance required)

| Dataset | Tags | How to download |
|---|---|---|
| **[AWID2](./awid2)** | wireless | 1) Kaggle: accept at `kaggle.com/datasets/kolias93/awid2-wifi-intrusion-dataset`, then `python3 download.py` 2) Official: `python3 download.py register NAME LAST EMAIL AFFIL` |
| **[AWID3](./awid3)** | wireless | 1) Kaggle: accept at `kaggle.com/datasets/chatzoglou/awid3`, then `python3 download.py` 2) Official: `python3 download.py register NAME LAST EMAIL AFFIL` |

---

## Dataset Details

### KDDCup 1999
- **Source:** Kaggle `galaxyh/kdd-cup-1999-data`
- **Label:** `label` → `attack_name` (23 attack types)
- **Kill-chain:** normal→0, probe attacks→1, R2L→4, U2R→5, DoS→7

### NSL-KDD
- **Source:** Kaggle `hassan06/nslkdd` (KDDTrain+.txt + KDDTest+.txt, no header, 43 cols)
- **Kill-chain:** same as KDDCup 1999; extended with saint/mscan/apache2/mailbomb/udpstorm etc.

### UNSW-NB15
- **Source:** Kaggle `mrwellsdavid/unsw-nb15`
- **Label:** `attack_cat` → `attack_name`, `label` → `attack_flag`
- **Kill-chain:** Normal→0, Reconnaissance/Analysis/Fuzzers→1, Exploits/Shellcode/Generic→4, Backdoor→5, Worms→6, DoS→7

### CTU-13
- **Source:** Kaggle `dhoogla/ctu13` (13 parquet files)
- **Label:** `label` with `flow=` prefix stripped; botnet→6, normal/background→0

### N-BaIoT
- **Source:** Kaggle `mkashifn/nbaiot-dataset`
- **Label:** Derived from filename — `{device}.benign.csv`→0, `*.mirai.scan`/`*.gafgyt.scan`→1, others→7

### CIDDS-001 / CIDDS-002
- **Source:** Kaggle `dhoogla/cidds001`, `dhoogla/cidds002` (parquet)
- **Label:** `attack_type` → `attack_name`

### IoTID20
- **Source:** Kaggle `rohulaminlabid/iotid20-dataset`
- **Label:** `Cat` → `attack_name`, `Label` → `attack_flag`

### HIKARI-2021
- **Source:** Kaggle `kk0105/allflowmeter-hikari2021`
- **Label:** `traffic_category` → `attack_name`, `Label` → `attack_flag`

### InSDN
- **Source:** Kaggle `badcodebuilder/insdn-dataset`
- **Files:** Normal_data.csv + metasploitable-2.csv + OVS.csv (concatenated, 344k rows)
- **Label:** `Label` column; strip trailing spaces (`DDoS ` → `ddos`)
- **Kill-chain:** Normal→0, Probe→1, BFA/U2R/Web-Attack→4, BOTNET→6, DoS/DDoS→7

### Bot-IoT
- **Source:** Kaggle `vigneshvenkateswaran/bot-iot` (75 CSV files, 73.4M rows)
- **Label:** `category` → `attack_name`, `attack` → `attack_flag`
- **Kill-chain:** Normal→0, Reconnaissance→1, DoS/DDoS/Theft→7
- **Note:** `subcategory ` column has trailing space → use `errors="ignore"` when dropping

### CIC-DDoS2019
- **Source:** Kaggle `dhoogla/cicddos2019` (17 parquet files)
- **Label:** `Label` column (Benign, DrDoS_*, Syn, UDP, LDAP, MSSQL, NetBIOS, etc.)
- **Kill-chain:** Benign→0, TFTP→3, all DDoS/DoS variants→7

### Kitsune
- **Source:** Kaggle `ymirsky/network-attack-dataset-kitsune` (no license required)
- **Structure:** 9 attack scenario directories; each has `{Name}_dataset.csv` (115 features, no header) + `{name}_labels.csv`
- **Label format:** Most scenarios: CSV with `"","x"` header, col `x` = 0/1. Mirai: headerless, single 0/1 column.
- **Kill-chain:** ARP MitM/Active Wiretap/Video Injection→4, Fuzzing/OS Scan→1, Mirai Botnet→6, SSDP Flood/SSL Renegotiation/SYN DoS→7
- **Sampling:** 200k rows per scenario (total 1.8M)

### IoT-23
- **Source:** Official CTU/Stratosphere (`mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/`)
- **Format:** Zeek conn.log (tab-separated); last tab-field contains `tunnel_parents  label  detailed-label` (space-separated within field)
- **Label:** `detailed-label` (Benign→0, PartOfAHorizontalPortScan→1, C&C variants→6, DDoS/Attack→7)
- **Scenarios:** 20 malware captures (Mirai, Torii, Okiru, Muhstik, etc.)
- **Sampling:** 200k rows per scenario (total 2.6M)

### CIC-IDS2017 Improved *(Liu et al., 2022)*
- **Source:** `https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip` (328 MB)
- **Files:** monday.csv ~ friday.csv (5 day files)
- **Note:** "Attempted" flows (e.g., `DoS GoldenEye - Attempted`) are treated as benign (no malicious behavior observed)

### CSE-CIC-IDS2018 Improved *(Liu et al., 2022)*
- **Source:** `https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CSECICIDS2018_improved.zip` (9.7 GB)
- **Note:** Same fix methodology as CIC-IDS2017 improved; significantly larger dataset

### AWID2 *(Kolias et al., 2016)*
- **Source option 1:** Kaggle `kolias93/awid2-wifi-intrusion-dataset` (license acceptance required)
- **Source option 2:** `python3 download.py register NAME LASTNAME EMAIL AFFIL` → email link in 1-3 days
- **Kill-chain:** Normal→0, Injection/Impersonation→4, Flooding/Deauthentication→7

### AWID3 *(Chatzoglou et al., 2021)*
- **Source option 1:** Kaggle `chatzoglou/awid3` (license acceptance required)
- **Source option 2:** `python3 download.py register NAME LASTNAME EMAIL AFFIL` → email link in 1-3 days
- **Kill-chain:** Normal→0, KRACK/Kr00k/ICV/MIC failures→4, Deauth/Disassoc/RTS/CTS flood→7

---

## Prerequisites

| Requirement | Purpose | Install |
|---|---|---|
| Python 3.8+ | All datasets | — |
| Python packages | All datasets | `pip install -r requirements.txt` |
| Kaggle API key | All Kaggle-based datasets | `~/.kaggle/kaggle.json` ([guide](https://www.kaggle.com/docs/api)) |
| `wget` | LSPR23, CIC-IDS improved | Linux/Mac: built-in |

---

## Quick Start

```bash
git clone https://github.com/comsyssec/datasets.git
cd datasets
pip install -r requirements.txt

# Download a specific dataset
cd unsw-nb15
python3 download.py

# Download all at once
bash download_all.sh
```

### AWID2/3 — official site registration

```bash
# Submit request (sends download link to email within 1-3 days)
cd awid2
python3 download.py register "Gildong" "Hong" "hong@university.ac.kr" "Seoul Nat'l Univ"

# After receiving email link:
python3 download.py download-link "https://icsdweb.aegean.gr/..."
```

### CIC-IDS2017/2018 Improved

```bash
# CIC-IDS2017 improved (328MB)
cd cicids2017-imp && python3 download.py

# CSE-CIC-IDS2018 improved (9.7GB, ~30-60 min)
cd cicids2018-imp && python3 download.py
```

---

## Special Notes

### LSPR23
Downloads from Zenodo automatically. Requires `wget`. Processes 9.8 GB CSV in chunks.

### Kitsune
Two Kaggle uploads exist:
- `ymirsky/network-attack-dataset-kitsune` ← **use this** (no license required)
- `ymirsky/kitsune-network-attack-dataset` ← requires license acceptance

### IoT-23
Downloads directly from official CTU server (no Kaggle account needed). 20 scenarios × 200k rows = 2.6M total.

### Bot-IoT
Large dataset (73.4M rows, 14 GB raw). `process()` uses 500k-row chunks to avoid OOM.

### Cache issues (n-baiot, nf-ton-iot-v3)
If you see "Bad magic number" error, the local Kaggle cache is corrupted:
```bash
rm -rf ~/.cache/kagglehub/datasets/mkashifn/nbaiot-dataset/
rm -rf ~/.cache/kagglehub/datasets/seyhed/nf-ton-iot-v3/
python3 download.py
```

---

## License & Citation

The download and processing scripts are provided for convenience and standardization.
Each dataset's license and citation requirements are governed by their original creators.
Please cite the original papers when using these datasets in your research.
