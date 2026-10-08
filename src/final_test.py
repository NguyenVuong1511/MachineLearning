"""src/final_test.py — Đánh giá model đã train trên tập test. CHẠY ĐÚNG MỘT LẦN."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from evaluate import leave_one_out_pairs, hit_rate_at_k, coverage_at_k, hit_rate_baseline

SEED = 42
K = 20
GIFT_PACKAGING_CODES = {
    "PADS", "gift_0001_10", "gift_0001_20", "gift_0001_30",
    "DCGSSGIRL", "DCGSSBOY",
}

model = joblib.load("models/cosine_model.joblib")
sim, vocab = model["sim_matrix"], model["item_vocab"]

df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
df = df[~df["StockCode"].isin(GIFT_PACKAGING_CODES)]
train = df[df["split"] == "train"]
test = df[df["split"] == "test"]

rng = np.random.default_rng(SEED)
pairs = leave_one_out_pairs(test, rng)

hr, n_eval = hit_rate_at_k(pairs, vocab, sim, K)
cov = coverage_at_k(pairs, vocab, sim, K)
hr_base = hit_rate_baseline(pairs, train, K)

print(f"Hit-rate cosine={hr:.3f} ({n_eval}/{len(pairs)}), baseline={hr_base:.3f}, coverage={cov:.3f}")

top10 = train.groupby("StockCode")["Invoice"].nunique().sort_values(ascending=False).head(10)
Path("reports").mkdir(exist_ok=True)
Path("reports/final_test_result.json").write_text(json.dumps({
    "hit_rate": round(hr, 3), "hit_rate_baseline": round(hr_base, 3),
    "coverage": round(cov, 3), "k": K, "min_freq": 60,
    "num_evaluated": n_eval, "num_total_pairs": len(pairs),
    "top_popular": [{"stock_code": c, "invoice_count": int(n)} for c, n in top10.items()],
}, ensure_ascii=False, indent=2))