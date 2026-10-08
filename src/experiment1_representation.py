"""src/experiment1_representation.py — So sánh vector item-invoice vs item-customer."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from src.features import build_item_matrix, compute_cosine, recommend_topn
from src.evaluate import leave_one_out_pairs, hit_rate_at_k, coverage_at_k

SEED = 42
MIN_FREQ = 60

df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
train = df[df["split"] == "train"]
val = df[df["split"] == "val"]

rng = np.random.default_rng(SEED)
pairs = leave_one_out_pairs(val, rng)

print("So sánh item-invoice vs item-customer (min_freq=60)\n")
for group_col, label in [("Invoice", "item-invoice"), ("Customer ID", "item-customer")]:
    mat, vocab = build_item_matrix(train, group_col, min_freq=MIN_FREQ)
    sim = compute_cosine(mat)
    for k in [5, 10, 20]:
        hr, n_eval = hit_rate_at_k(pairs, vocab, sim, k)
        cov = coverage_at_k(pairs, vocab, sim, k)
        print(f"{label:>14} | K={k:>2}: Hit-rate={hr:.3f} "
              f"(trên {n_eval} cặp), coverage={cov:.3f}, |từ vựng|={len(vocab)}")