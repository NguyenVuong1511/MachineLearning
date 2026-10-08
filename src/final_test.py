"""src/final_test.py — CHẠY ĐÚNG MỘT LẦN. Cấu hình theo project_brief.md mục 13."""
import numpy as np
import pandas as pd

from features import build_item_matrix, compute_cosine
from evaluate import leave_one_out_pairs, hit_rate_at_k, coverage_at_k, hit_rate_baseline

SEED = 42
MIN_FREQ = 60
K = 20
GROUP_COL = "Invoice"
GIFT_PACKAGING_CODES = {
    "PADS", "gift_0001_10", "gift_0001_20", "gift_0001_30",
    "DCGSSGIRL", "DCGSSBOY",
}

df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
df = df[~df["StockCode"].isin(GIFT_PACKAGING_CODES)]   # áp dụng quyết định Thí nghiệm 4

train = df[df["split"] == "train"]
test = df[df["split"] == "test"]   # LẦN ĐẦU TIÊN đụng vào test trong cả dự án

mat, vocab = build_item_matrix(train, GROUP_COL, min_freq=MIN_FREQ)
sim = compute_cosine(mat)

rng = np.random.default_rng(SEED)
pairs = leave_one_out_pairs(test, rng)

hr, n_eval = hit_rate_at_k(pairs, vocab, sim, K)
cov = coverage_at_k(pairs, vocab, sim, K)
hr_base = hit_rate_baseline(pairs, train, K)

print(f"KẾT QUẢ TEST CUỐI CÙNG (K={K}, min_freq={MIN_FREQ}, loại mã quà tặng)")
print(f"Hit-rate cosine   = {hr:.3f}  (trên {n_eval}/{len(pairs)} cặp)")
print(f"Hit-rate baseline = {hr_base:.3f}")
print(f"Coverage          = {cov:.3f}")

# Thêm vào cuối src/final_test.py
import joblib
joblib.dump({"sim_matrix": sim, "item_vocab": vocab}, "models/cosine_model.joblib")
print("Đã lưu model vào models/cosine_model.joblib")

# Thêm vào cuối src/final_test.py
import json
from pathlib import Path

top10 = (
    train.groupby("StockCode")["Invoice"].nunique()
    .sort_values(ascending=False).head(10)
)
top10_info = [{"stock_code": c, "invoice_count": int(n)} for c, n in top10.items()]

Path("reports").mkdir(exist_ok=True)
Path("reports/final_test_result.json").write_text(
    json.dumps({
        "hit_rate": round(hr, 3),
        "hit_rate_baseline": round(hr_base, 3),
        "coverage": round(cov, 3),
        "k": K,
        "min_freq": MIN_FREQ,
        "num_evaluated": n_eval,
        "num_total_pairs": len(pairs),
        "top_popular": top10_info,
    }, ensure_ascii=False, indent=2)
)
print("Đã lưu reports/final_test_result.json")