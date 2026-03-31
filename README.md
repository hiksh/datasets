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

- **[CICIDS2017](./cicids2017)** / **[CICIDS2018](./cicids2018)**
- **[CICIoT2023](./ciciot2023)**
- **[NSL-KDD](./nsl-kdd)**
- **[UNSW-NB15](./unsw-nb15)**
- **[ToN-IoT](./ton-iot)**
- **[Mirai Botnet Dataset](./mirai)**
- **[EPIC Attack Datasets](./EPIC_Attack_Datasets)**
- **[LSPR23](./lspr23)** *(manual download required — see Special Instructions)*

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

To download and process all standard datasets automatically, run this loop from the root directory:

```bash
for dir in */ ; do
    if [ -f "$dir/download.py" ]; then
        echo "Downloading and processing dataset in $dir..."
        (cd "$dir" && python3 download.py)
    fi
done
```

> **Note:** LSPR23 does not have a `download.py` and is not included in this loop. See Special Instructions below for manual setup.

---

## Special Instructions for Specific Datasets

### LSPR23

Due to its large file size, the LSPR23 dataset cannot be downloaded automatically via script. Additionally, unlike other datasets, LSPR23 only requires a **processing step** — not a download step. Please follow these manual steps:

1. Download the dataset manually from: [Zenodo - LSPR23](https://zenodo.org/records/8042347)
2. Extract the downloaded file directly into the lspr23/ directory of this repository, keeping the extracted folder name exactly as LSPR23.
4. Run the processing script:

```bash
cd lspr23
python3 process.py
```

**Result:** The script will process the raw data and generate a standardized CSV file (ending with `attack_name`, `attack_flag`, `attack_step`) next to the original `LSPR23/ls23pr_flows/ls23pr_v1.csv` file.

### IoT Dataset

The Python scripts inside the IoT Dataset folder are designed to process existing raw CSV files (which share the same names as the Python scripts) and append the standardized `attack_name`, `attack_flag`, and `attack_step` columns.

> **Note:** The raw CSV files are currently not uploaded to this repository due to GitHub's file size limits. They will be hosted on an external server in the near future.

---

## License & Citation

- The download and processing scripts are provided for convenience and standardization.
- Each dataset's license and citation requirements are governed by their original creators. Please ensure you properly cite the original papers and authors when using these datasets for your research.
