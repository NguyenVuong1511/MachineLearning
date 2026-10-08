"""src/experiment4_packaging.py — Ảnh hưởng của mã quà tặng/đóng gói lên kết quả gợi ý."""
import numpy as np
import pandas as pd

from features import build_item_matrix, compute_cosine
from evaluate import leave_one_out_pairs, hit_rate_at_k, coverage_at_k

SEED = 42
MIN_FREQ = 60
GIFT_PACKAGING_CODES = {
    "PADS", "gift_0001_10", "gift_0001_20", "gift_0001_30",
    "DCGSSGIRL", "DCGSSBOY",
}

df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
train_full = df[df["split"] == "train"]
val_full = df[df["split"] == "val"]

rng = np.random.default_rng(SEED)

print("So sánh GIỮ vs LOẠI mã quà tặng/đóng gói (min_freq=60)\n")
for keep, label in [(True, "Giữ mã quà tặng"), (False, "Loại mã quà tặng")]:
    if keep:
        train, val = train_full, val_full
    else:
        train = train_full[~train_full["StockCode"].isin(GIFT_PACKAGING_CODES)]
        val = val_full[~val_full["StockCode"].isin(GIFT_PACKAGING_CODES)]

    mat, vocab = build_item_matrix(train, "Invoice", min_freq=MIN_FREQ)
    sim = compute_cosine(mat)
    pairs = leave_one_out_pairs(val, rng)   # tạo lại pairs vì val đã đổi (loại mã quà tặng)

    for k in [5, 10, 20]:
        hr, n_eval = hit_rate_at_k(pairs, vocab, sim, k)
        cov = coverage_at_k(pairs, vocab, sim, k)
        print(f"{label:>18} | K={k:>2}: Hit-rate={hr:.3f} "
              f"(trên {n_eval} cặp), coverage={cov:.3f}")