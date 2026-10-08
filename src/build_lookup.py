"""src/build_lookup.py — Tạo bảng tra cứu StockCode -> Description. Chạy 1 lần."""
import pandas as pd
import joblib

df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
train = df[df["split"] == "train"]

# Một mã có thể có vài cách viết Description khác nhau -> lấy tên xuất hiện nhiều nhất
lookup = (
    train.groupby("StockCode")["Description"]
    .agg(lambda x: x.mode().iat[0])
    .to_dict()
)

joblib.dump(lookup, "models/product_lookup.joblib")
print(f"Đã lưu {len(lookup)} mã sản phẩm vào models/product_lookup.joblib")