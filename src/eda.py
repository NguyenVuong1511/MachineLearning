"""src/eda.py — khám phá dữ liệu trên tập train (chỉ dùng train, không đụng val/test)."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

SPLIT_CSV = Path("data/processed/split.csv")
FIG_DIR = Path("reports/figures")


def main():
    df = pd.read_csv(SPLIT_CSV, dtype={"Invoice": str, "StockCode": str})
    train = df[df["split"] == "train"]
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Kích thước giỏ hàng
    basket_size = train.groupby("Invoice")["StockCode"].nunique()
    plt.figure()
    basket_size.hist(bins=50)
    plt.xlabel("Số sản phẩm khác nhau / hóa đơn")
    plt.title("Phân bố kích thước giỏ hàng (train)")
    plt.savefig(FIG_DIR / "basket_size_hist.png")
    print(basket_size.describe())

    # Tần suất sản phẩm
    item_freq = train.groupby("StockCode")["Invoice"].nunique().sort_values(ascending=False)
    plt.figure()
    item_freq.head(20).plot(kind="bar")
    plt.title("Top 20 sản phẩm theo số hóa đơn (train)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "top20_products.png")
    print(item_freq.describe())
    item_freq.to_csv("data/processed/item_freq_train.csv")


if __name__ == "__main__":
    main()