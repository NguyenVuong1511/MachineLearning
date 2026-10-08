"""src/train.py — Train model cuối cùng với cấu hình đã đóng băng, lưu lại để serving và evaluate dùng."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import joblib
from src.features import build_item_matrix, compute_cosine

MIN_FREQ = 60
GROUP_COL = "Invoice"
GIFT_PACKAGING_CODES = {
    "PADS", "gift_0001_10", "gift_0001_20", "gift_0001_30",
    "DCGSSGIRL", "DCGSSBOY",
}

def main():
    df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
    df = df[~df["StockCode"].isin(GIFT_PACKAGING_CODES)]
    train = df[df["split"] == "train"]

    mat, vocab = build_item_matrix(train, GROUP_COL, min_freq=MIN_FREQ)
    sim = compute_cosine(mat)

    joblib.dump({"sim_matrix": sim, "item_vocab": vocab}, "models/cosine_model.joblib")
    print(f"Đã train và lưu model: {len(vocab)} sản phẩm trong từ vựng")

if __name__ == "__main__":
    main()