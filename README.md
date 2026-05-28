# Cybersecurity & IoT Datasets

A comprehensive collection of publicly available datasets widely used for machine learning and deep learning research in cybersecurity, Intrusion Detection Systems (IDS), and IoT environments.

## Core Concept: Standardized Labeling

The most important feature of this repository is data standardization.  
Every dataset in this repository is processed so that the final CSV files end with the exact same three columns:

1. `attack_name`
2. `attack_flag`
3. `attack_step`

When you run the `download.py` scripts, they do not just download the raw CSV files; they automatically process and format the files to ensure they conclude with these three standard columns. This standardized format makes it significantly easier to perform cross-dataset evaluations and train universal machine learning models.

---

## Available Datasets

| Dataset | Tags |
|---|---|
| **[CICIDS2017](./cicids2017)** / **[CICIDS2018](./cicids2018)** | general-purpose, dos-ddos, web-attacks, brute-force, scan, infiltration, botnet |
| **[CICIoT2023](./ciciot2023)** | iot, general-purpose |
| **[NSL-KDD](./nsl-kdd)** | general-purpose, anomaly |
| **[UNSW-NB15](./unsw-nb15)** | general-purpose, anomaly |
| **[ToN-IoT](./ton-iot)** | iiot-ics, general-purpose |
| **[Mirai Botnet Dataset](./mirai)** | iot, botnet |
| **[EPIC Attack Datasets](./EPIC_Attack_Datasets)** | apt |
| **[Edge-IIoT](./edge-iiot)** | iiot-ics, iot |
| **[XIIoTID](./xiiotid)** | iiot-ics, iot |
| **[NF-ToN-IoT-v3](./nf-ton-iot-v3)** | iiot-ics |
| **[WUSTL-IIoT-2021](./wustl-iiot-2021)** | iiot-ics |
| **[LSPR23](./lspr23)** | general-purpose, anomaly |

Full tag definitions and paths are in [`datasets.yaml`](./datasets.yaml).

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
