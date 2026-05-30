# Cybersecurity & IoT Datasets

A comprehensive collection of publicly available datasets widely used for machine learning and deep learning research in cybersecurity, Intrusion Detection Systems (IDS), and IoT environments.

## Core Concept: Standardized Labeling

The most important feature of this repository is data standardization.
Every dataset is processed so that the final CSV files end with the exact same three columns:

1. `attack_name` — attack type string (lowercase)
2. `attack_flag` — binary label (0 = benign, 1 = attack)
3. `attack_step` — Cyber Kill Chain phase (integer)

Running `python3 download.py` in any dataset directory will download the raw data and produce a standardized output CSV in this format.

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

These datasets use the original pipeline (pre-standardized format). Output files are `training-flow.csv` / `test-flow.csv` or dataset-specific names.

| Dataset | Tags | Output file(s) | Notes |
|---|---|---|---|
| **[CICIDS2017](./cicids2017)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | `training-flow.csv`, `test-flow.csv` | Kaggle `chethuhn/network-intrusion-dataset` |
| **[CSE-CIC-IDS2018](./cicids2018)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | `training-flow.csv`, `test-flow.csv` | Kaggle `solarmainframe/ids-intrusion-csv` |
| **[CICIoT2023](./ciciot2023)** | iot, general-purpose | `training-flow.csv`, `test-flow.csv` | 105 IoT attack types |
| **[ToN-IoT](./ton-iot)** | iiot-ics, general-purpose | `training-flow.csv`, `test-flow.csv` | — |
| **[Mirai Botnet Dataset](./mirai)** | iot, botnet | `training-flow.csv`, `test-flow.csv` | Pre-processed files included; no download.py |
| **[EPIC Attack Datasets](./EPIC_Attack_Datasets)** | apt | `Reformatted_EPICA.csv`, `Reformatted_EPICB.csv` | APT scenarios |
| **[Edge-IIoTset](./edge-iiot)** | iiot-ics, iot | `Reformatted_EdgeIIoT.csv` | Kaggle `mohamedamineferrag/edgeiiotset-...` |
| **[XIIoTID](./xiiotid)** | iiot-ics, iot | `Reformatted_XIIoTID.csv` | Kaggle `munaalhawawreh/xiiotid-...` |
| **[NF-ToN-IoT-v3](./nf-ton-iot-v3)** | iiot-ics | `Reformatted_NF-ToN-IoT-v3.csv` | NetFlow v9, Kaggle `seyhed/nf-ton-iot-v3` |
| **[WUSTL-IIoT-2021](./wustl-iiot-2021)** | iiot-ics | `Reformatted_WUSTL-IIoT-2021.csv` | SCADA, Kaggle `annaamalaiu/wustl-iiot-2021-dataset` |
| **[LSPR23](./lspr23)** | general-purpose, anomaly | `LSPR23/ls23pr_flows/Reformatted_LSPR23.csv` | Zenodo, 9.8 GB CSV, chunked processing |

### Phase 2 — Expansion (Verified, unmapped=0)

All datasets produce `Reformatted_*.csv` with the standardized 3-column format.

| Dataset | Tags | Rows | Steps | Kaggle / Source |
|---|---|---|---|---|
| **[KDDCup 1999](./kddcup1999)** | general-purpose, anomaly | 494k | 0,1,4,5,7 | `galaxyh/kdd-cup-1999-data` |
| **[NSL-KDD](./nsl-kdd)** | general-purpose, anomaly | 148k | 0,1,4,5,6,7 | `hassan06/nslkdd` |
| **[UNSW-NB15](./unsw-nb15)** | general-purpose, anomaly | 258k | 0,1,4,5,6,7 | `mrwellsdavid/unsw-nb15` |
| **[CTU-13](./ctu-13)** | botnet | 1.6M | 0,6 | `dhoogla/ctu13` |
| **[N-BaIoT](./n-baiot)** | iot, botnet | 2.4M+ | 0,1,7 | `mkashifn/nbaiot-dataset` |
| **[CIDDS-001](./cidds-001)** | general-purpose, scan | 204k | 0,1,4 | `dhoogla/cidds001` |
| **[CIDDS-002](./cidds-002)** | general-purpose, scan | 2.6M | 0,1 | `dhoogla/cidds002` |
| **[IoTID20](./iotid20)** | iot | 626k | 0,1,4,6,7 | `rohulaminlabid/iotid20-dataset` |
| **[HIKARI-2021](./hikari-2021)** | general-purpose | 555k | 0,1,4,7 | `kk0105/allflowmeter-hikari2021` |
| **[InSDN](./insdn)** | sdn | 344k | 0,1,4,6,7 | `badcodebuilder/insdn-dataset` |
| **[Bot-IoT](./bot-iot)** | iot, botnet, dos-ddos | 73.4M | 0,1,7 | `vigneshvenkateswaran/bot-iot` |
| **[CIC-DDoS2019](./cic-ddos2019)** | dos-ddos, general-purpose | 431k | 0,3,7 | `dhoogla/cicddos2019` |
| **[Kitsune](./kitsune)** | iot, anomaly | 1.8M | 0,1,4,6,7 | `ymirsky/network-attack-dataset-kitsune` |
| **[IoT-23](./iot-23)** | iot, botnet | 2.6M | 0,1,6,7 | Official CTU: mcfp.felk.cvut.cz |

### Phase 2 — Improved CIC-IDS (Liu et al., 2022)

Fixed CICFlowMeter tool and corrected labeling errors in the original CIC datasets.
Source: https://intrusion-detection.distrinet-research.be/CNS2022/

| Dataset | Tags | Rows | Steps | Archive size |
|---|---|---|---|---|
| **[CIC-IDS2017 Improved](./cicids2017-imp)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | 2.1M | 0,1,4,6,7 | 328 MB |
| **[CSE-CIC-IDS2018 Improved](./cicids2018-imp)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, botnet | 63.2M | 0,4,6,7 | 9.7 GB |

### Phase 2 — Pending (Kaggle license acceptance required)

| Dataset | Tags | Download |
|---|---|---|
| **[AWID2](./awid2)** | wireless | Kaggle `kolias93/awid2-wifi-intrusion-dataset` **or** `python3 download.py register NAME LAST EMAIL AFFIL` |
| **[AWID3](./awid3)** | wireless | Kaggle `chatzoglou/awid3` **or** `python3 download.py register NAME LAST EMAIL AFFIL` |

---

## Dataset Details

### KDDCup 1999
- **Source:** Kaggle `galaxyh/kdd-cup-1999-data`
- **Output:** `Reformatted_KDDCup1999.csv`
- **Kill-chain:** normal→0, probe attacks→1, R2L→4, U2R→5, DoS→7

### NSL-KDD
- **Source:** Kaggle `hassan06/nslkdd` (KDDTrain+.txt + KDDTest+.txt, no header, 43 cols)
- **Output:** `Reformatted_NSL-KDD.csv`
- **Kill-chain:** same as KDDCup 1999; extended with saint/mscan/apache2/mailbomb/udpstorm etc.

### UNSW-NB15
- **Source:** Kaggle `mrwellsdavid/unsw-nb15`
- **Output:** `Reformatted_UNSW-NB15.csv`
- **Label:** `attack_cat` → `attack_name`, `label` → `attack_flag`
- **Kill-chain:** Normal→0, Reconnaissance/Analysis/Fuzzers→1, Exploits/Shellcode/Generic→4, Backdoor→5, Worms→6, DoS→7

### CTU-13
- **Source:** Kaggle `dhoogla/ctu13` (13 parquet files)
- **Output:** `Reformatted_CTU-13.csv`
- **Label:** `label` with `flow=` prefix stripped; botnet→6, normal/background→0

### N-BaIoT
- **Source:** Kaggle `mkashifn/nbaiot-dataset`
- **Output:** `Reformatted_N-BaIoT.csv`
- **Label:** Derived from filename — `{device}.benign.csv`→0, `*.mirai.scan`/`*.gafgyt.scan`→1, others→7

### CIDDS-001 / CIDDS-002
- **Source:** Kaggle `dhoogla/cidds001`, `dhoogla/cidds002` (parquet)
- **Output:** `Reformatted_CIDDS-001.csv`, `Reformatted_CIDDS-002.csv`
- **Label:** `attack_type` → `attack_name`

### IoTID20
- **Source:** Kaggle `rohulaminlabid/iotid20-dataset`
- **Output:** `Reformatted_IoTID20.csv`
- **Label:** `Cat` → `attack_name`, `Label` → `attack_flag`

### HIKARI-2021
- **Source:** Kaggle `kk0105/allflowmeter-hikari2021`
- **Output:** `Reformatted_HIKARI-2021.csv`
- **Label:** `traffic_category` → `attack_name`, `Label` → `attack_flag`

### InSDN
- **Source:** Kaggle `badcodebuilder/insdn-dataset`
- **Output:** `Reformatted_InSDN.csv`
- **Files:** Normal_data.csv + metasploitable-2.csv + OVS.csv (concatenated, 344k rows)
- **Kill-chain:** Normal→0, Probe→1, BFA/U2R/Web-Attack→4, BOTNET→6, DoS/DDoS→7

### Bot-IoT
- **Source:** Kaggle `vigneshvenkateswaran/bot-iot` (75 CSV files, 73.4M rows)
- **Output:** `Reformatted_Bot-IoT.csv`
- **Label:** `category` → `attack_name`, `attack` → `attack_flag`
- **Kill-chain:** Normal→0, Reconnaissance→1, DoS/DDoS/Theft→7
- **Note:** `subcategory ` column has trailing space → use `errors="ignore"` when dropping

### CIC-DDoS2019
- **Source:** Kaggle `dhoogla/cicddos2019` (17 parquet files)
- **Output:** `Reformatted_CIC-DDoS2019.csv`
- **Kill-chain:** Benign→0, TFTP→3, all DDoS/DoS variants→7

### Kitsune
- **Source:** Kaggle `ymirsky/network-attack-dataset-kitsune` (no license required)
- **Output:** `Reformatted_Kitsune.csv`
- **Structure:** 9 scenario directories; `{Name}_dataset.csv` (115 features, no header) + `{name}_labels.csv`
- **Kill-chain:** ARP MitM/Active Wiretap/Video Injection→4, Fuzzing/OS Scan→1, Mirai Botnet→6, SSDP Flood/SSL Renegotiation/SYN DoS→7
- **Sampling:** 200k rows per scenario (total 1.8M)

### IoT-23
- **Source:** Official CTU/Stratosphere (`mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/`)
- **Output:** `Reformatted_IoT-23.csv`
- **Format:** Zeek conn.log; last tab-field = `tunnel_parents  label  detailed-label` (space-separated)
- **Kill-chain:** Benign→0, PortScan→1, C&C variants→6, DDoS/Attack→7
- **Sampling:** 200k rows per scenario (total 2.6M)

### CIC-IDS2017 Improved *(Liu et al., 2022)*
- **Source:** `https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CICIDS2017_improved.zip` (328 MB)
- **Output:** `Reformatted_CIC-IDS2017-Imp.csv`
- **Files:** monday.csv ~ friday.csv (5 day files)
- **Note:** "Attempted" flows treated as benign (attack_step=0)

### CSE-CIC-IDS2018 Improved *(Liu et al., 2022)*
- **Source:** `https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/CSECICIDS2018_improved.zip` (9.7 GB)
- **Output:** `Reformatted_CSE-CIC-IDS2018-Imp.csv`
- **Files:** 10 day CSV files (~30 GB uncompressed, 63.2M rows)

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
# CIC-IDS2017 improved (328 MB)
cd cicids2017-imp && python3 download.py

# CSE-CIC-IDS2018 improved (~9.7 GB compressed, ~60 min)
cd cicids2018-imp && python3 download.py
```

---

## Special Notes

### Mirai Botnet Dataset
Pre-processed `training-flow.csv` and `test-flow.csv` are included directly in the repository. No `download.py` exists — the source is proprietary PCAP captures.

### LSPR23
Downloads from Zenodo automatically. Requires `wget`. Processes 9.8 GB CSV in chunks.

### Kitsune
Two Kaggle uploads exist — use the correct one:
- `ymirsky/network-attack-dataset-kitsune` ← **use this** (no license required)
- `ymirsky/kitsune-network-attack-dataset` ← requires license acceptance

### IoT-23
Downloads directly from the official CTU server (no Kaggle account needed). 20 scenarios × 200k rows = 2.6M total.

### Bot-IoT / CSE-CIC-IDS2018 Improved
Very large outputs (14 GB / 34 GB). `process()` uses chunked writes to avoid OOM.

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
