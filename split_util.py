"""
split_util.py — shallow runner that splits Reformatted_*.csv into
training-flow.csv / test-flow.csv according to split.env.

All policy lives in split.env (one line per dataset). This file only reads that
config and applies it; do not hardcode ratios or dataset names here.

Usage:
  python split_util.py cidds-001              # cidds-001/Reformatted_*.csv -> two files
  python split_util.py unsw-nb15 cidds-001    # several at once
  python split_util.py cidds-001 --keep       # keep the intermediate Reformatted_*.csv
  python split_util.py cidds-001 --test-ratio 0.3 --seed 7   # override split.env

Can also be called from a download.py:
  from split_util import split_dataset
  split_dataset("cidds-001")
"""

import argparse
import glob
import os

import pandas as pd

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "split.env")

TRAIN_FILENAME = "training-flow.csv"
TEST_FILENAME = "test-flow.csv"


def _load_env(env_path=ENV_PATH):
    """Parse split.env into {key: value}. Keys are dataset dirs or mechanical settings."""
    settings = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            settings[key.strip()] = value.strip()
    return settings


def _find_reformatted(dataset_dir):
    """Find the single Reformatted_*.csv under dataset_dir (searched recursively)."""
    matches = sorted(glob.glob(os.path.join(dataset_dir, "**", "Reformatted_*.csv"), recursive=True))
    if not matches:
        raise FileNotFoundError(
            f"No Reformatted_*.csv under '{dataset_dir}'. Run that dataset's download.py first."
        )
    if len(matches) > 1:
        raise RuntimeError(
            f"Multiple Reformatted_*.csv under '{dataset_dir}': "
            f"{[os.path.basename(m) for m in matches]}. Keep only one."
        )
    return matches[0]


def _split_official(df, split_column):
    """Split by the train/test provenance column; drop that column from the output."""
    if split_column not in df.columns:
        raise RuntimeError(
            f"'official' dataset is missing the '{split_column}' column; "
            f"its download.py must tag rows as train/test before concatenating."
        )
    tag = df[split_column].astype(str).str.strip().str.lower()
    train_df = df[tag == "train"].drop(columns=[split_column])
    test_df = df[tag == "test"].drop(columns=[split_column])
    return train_df, test_df


def _split_stratified(df, test_ratio, seed, stratify_column, split_column):
    """Stratified split by stratify_column (whole frame in memory). Drop split column first."""
    df = df.drop(columns=[split_column], errors="ignore")
    if stratify_column in df.columns:
        test_df = df.groupby(stratify_column, group_keys=False).sample(
            frac=test_ratio, random_state=seed
        )
    else:
        print(f"[WARN] No '{stratify_column}' column; falling back to unstratified sample.")
        test_df = df.sample(frac=test_ratio, random_state=seed)
    train_df = df.drop(index=test_df.index)
    return train_df, test_df


def _split_stratified_lazy(reformatted_csv, train_path, test_path,
                           test_ratio, seed, stratify_column, split_column):
    """Memory-safe stratified split for very large files.

    Scans the CSV lazily with polars and processes one class at a time, so only
    a single class is ever held in memory. Rows in the output are grouped by
    class (shuffled within each class) — shuffle downstream if needed.
    Returns (n_train, n_test).
    """
    import polars as pl

    # infer_schema_length=0 reads every column as text: no type coercion, values
    # are written back exactly as-is; we only partition rows.
    lazy = pl.scan_csv(reformatted_csv, infer_schema_length=0)
    columns = lazy.collect_schema().names()
    if stratify_column not in columns:
        raise RuntimeError(f"No '{stratify_column}' column in {reformatted_csv}.")

    classes = (
        lazy.select(pl.col(stratify_column)).unique().collect()
        .to_series().drop_nulls().to_list()
    )

    n_train = n_test = 0
    first = True
    for cls in classes:
        df_cls = lazy.filter(pl.col(stratify_column) == cls).collect()
        if split_column in df_cls.columns:
            df_cls = df_cls.drop(split_column)
        df_cls = df_cls.sample(fraction=1.0, shuffle=True, seed=seed)
        k = int(round(df_cls.height * test_ratio))
        test_part = df_cls.head(k)
        train_part = df_cls.slice(k)

        with open(train_path, "wb" if first else "ab") as f:
            train_part.write_csv(f, include_header=first)
        with open(test_path, "wb" if first else "ab") as f:
            test_part.write_csv(f, include_header=first)
        first = False
        n_train += train_part.height
        n_test += test_part.height

    return n_train, n_test


def split_dataset(dataset, root=None, test_ratio=None, seed=None, clean=None, env=None):
    """Split one dataset directory per split.env policy.

    dataset    : directory name (also the split.env key), e.g. "cidds-001".
    root       : parent dir of the datasets (defaults to this file's dir).
    test_ratio / seed / clean : override split.env when not None.
    """
    env = env or _load_env()
    if root is None:
        root = os.path.dirname(os.path.abspath(ENV_PATH))
    dataset_dir = os.path.join(root, dataset)

    policy = env.get(dataset)
    if policy is None:
        raise KeyError(f"'{dataset}' has no entry in split.env.")
    if policy == "pipeline":
        print(f"[INFO] '{dataset}' is pipeline-managed (own download.py splits it); skipping.")
        return None

    stratify_column = env.get("STRATIFY_COLUMN", "attack_flag")
    split_column = env.get("SPLIT_COLUMN", "split")
    if clean is None:
        clean = env.get("CLEAN", "true").strip().lower() == "true"

    reformatted_csv = _find_reformatted(dataset_dir)
    out_dir = os.path.dirname(reformatted_csv)
    train_path = os.path.join(out_dir, TRAIN_FILENAME)
    test_path = os.path.join(out_dir, TEST_FILENAME)

    if policy == "official":
        print(f"[INFO] Reading: {reformatted_csv}")
        df = pd.read_csv(reformatted_csv, low_memory=False)
        print(f"[INFO] '{dataset}' -> preserving original split (by '{split_column}')")
        train_df, test_df = _split_official(df, split_column)
        train_df.to_csv(train_path, index=False)
        test_df.to_csv(test_path, index=False)
        n_train, n_test = len(train_df), len(test_df)
    else:
        fields = policy.split(",")
        ratio = test_ratio if test_ratio is not None else float(fields[0])
        rs = seed if seed is not None else int(fields[1])
        lazy = len(fields) > 2 and fields[2].strip().lower() == "lazy"
        mode = "lazy polars" if lazy else "pandas"
        print(f"[INFO] '{dataset}' -> stratified split ({mode}, test_ratio={ratio}, seed={rs}, by='{stratify_column}')")
        if lazy:
            n_train, n_test = _split_stratified_lazy(
                reformatted_csv, train_path, test_path, ratio, rs, stratify_column, split_column
            )
        else:
            print(f"[INFO] Reading: {reformatted_csv}")
            df = pd.read_csv(reformatted_csv, low_memory=False)
            train_df, test_df = _split_stratified(df, ratio, rs, stratify_column, split_column)
            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)
            n_train, n_test = len(train_df), len(test_df)

    print(f"[INFO] Saved: {train_path}  ({n_train:,} rows)")
    print(f"[INFO] Saved: {test_path}  ({n_test:,} rows)")

    if clean:
        os.remove(reformatted_csv)
        print(f"[INFO] Removed intermediate: {reformatted_csv}")

    return train_path, test_path


def main():
    parser = argparse.ArgumentParser(
        description="Split Reformatted_*.csv into training-flow.csv / test-flow.csv per split.env."
    )
    parser.add_argument("datasets", nargs="+", help="dataset directory names (e.g. cidds-001 unsw-nb15)")
    parser.add_argument("--test-ratio", type=float, default=None, help="override split.env test ratio")
    parser.add_argument("--seed", type=int, default=None, help="override split.env random_state")
    parser.add_argument("--keep", action="store_true", help="keep the intermediate Reformatted_*.csv")
    args = parser.parse_args()

    env = _load_env()
    for dataset in args.datasets:
        split_dataset(
            dataset.rstrip("/\\"),
            test_ratio=args.test_ratio,
            seed=args.seed,
            clean=False if args.keep else None,
            env=env,
        )


if __name__ == "__main__":
    main()
