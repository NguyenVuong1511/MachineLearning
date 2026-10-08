"""src/split.py — chia train/val/test theo hóa đơn (70/15/15, seed=42)."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import pandas as pd
import numpy as np

CLEAN_CSV = Path("data/processed/clean.csv")
SEED = 42


def main():
    df = pd.read_csv(CLEAN_CSV, dtype={"Invoice": str, "StockCode": str})

    invoices = df["Invoice"].unique()
    rng = np.random.default_rng(SEED)
    rng.shuffle(invoices)

    n = len(invoices)
    n_train = int(n * 0.70)
    n_val = int(n * 0.15)

    train_inv = set(invoices[:n_train])
    val_inv = set(invoices[n_train:n_train + n_val])
    test_inv = set(invoices[n_train + n_val:])

    df["split"] = df["Invoice"].map(
        lambda x: "train" if x in train_inv else "val" if x in val_inv else "test"
    )

    # Kiểm tra không có hóa đơn nào lọt sang 2 tập (bắt lỗi sớm nếu code sai)
    check = df.groupby("Invoice")["split"].nunique()
    assert (check == 1).all(), "Có hóa đơn bị chia vào 2 tập! Kiểm tra lại code."

    print(df["split"].value_counts())
    print(f"Số hóa đơn: train={len(train_inv)}, val={len(val_inv)}, test={len(test_inv)}")

    df.to_csv("data/processed/split.csv", index=False)


if __name__ == "__main__":
    main()