"""src/error_analysis.py — Xem hệ thống đoán sai ở đâu, để viết phần phân tích lỗi."""
import numpy as np
import pandas as pd

from features import build_item_matrix, compute_cosine, recommend_topn
from evaluate import leave_one_out_pairs

SEED = 42
MIN_FREQ = 60
K = 20
GIFT_PACKAGING_CODES = {
    "PADS", "gift_0001_10", "gift_0001_20", "gift_0001_30",
    "DCGSSGIRL", "DCGSSBOY",
}

df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
df = df[~df["StockCode"].isin(GIFT_PACKAGING_CODES)]
train = df[df["split"] == "train"]
test = df[df["split"] == "test"]

mat, vocab = build_item_matrix(train, "Invoice", min_freq=MIN_FREQ)
sim = compute_cosine(mat)

rng = np.random.default_rng(SEED)
pairs = leave_one_out_pairs(test, rng)

# Tần suất từng sản phẩm trong train, để biết sản phẩm "hiếm" hay "phổ biến"
item_freq = train.groupby("StockCode")["Invoice"].nunique()

rows = []
for input_codes, hidden in pairs:
    if hidden not in vocab:
        continue
    topk = recommend_topn(input_codes, vocab, sim, n=K)
    hit = hidden in topk
    rows.append({
        "hidden": hidden,
        "hit": hit,
        "hidden_freq": item_freq.get(hidden, 0),
        "basket_size": len(input_codes) + 1,
    })

result = pd.DataFrame(rows)

print(f"Tổng số lượt kiểm tra: {len(result)}")
print(f"Hit-rate chung: {result['hit'].mean():.3f}\n")

print("-- Hit-rate theo độ hiếm của sản phẩm bị giấu --")
result["freq_bucket"] = pd.cut(
    result["hidden_freq"], bins=[0, 60, 150, 500, 5000],
    labels=["60-150 (hiếm)", "150-500 (vừa)", "500-5000 (phổ biến)", ">5000"]
)
print(result.groupby("freq_bucket", observed=True)["hit"].agg(["mean", "count"]))

print("\n-- Hit-rate theo kích thước giỏ hàng --")
result["basket_bucket"] = pd.cut(
    result["basket_size"], bins=[0, 3, 10, 30, 1000],
    labels=["2-3", "4-10", "11-30", ">30"]
)
print(result.groupby("basket_bucket", observed=True)["hit"].agg(["mean", "count"]))

print("\n-- 10 sản phẩm bị đoán SAI nhiều nhất --")
miss = result[~result["hit"]]
print(miss["hidden"].value_counts().head(10))

result.to_csv("reports/error_analysis.csv", index=False)