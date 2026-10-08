"""src/baseline.py — baseline: top sản phẩm bán chạy nhất trong train."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import pandas as pd

SPLIT_CSV = Path("data/processed/split.csv")


def get_baseline_topk(train_df: pd.DataFrame, k: int) -> list[str]:
    """Trả về k mã sản phẩm xuất hiện trong nhiều hóa đơn train nhất."""
    freq = train_df.groupby("StockCode")["Invoice"].nunique()
    return freq.sort_values(ascending=False).head(k).index.tolist()


if __name__ == "__main__":
    df = pd.read_csv(SPLIT_CSV, dtype={"Invoice": str, "StockCode": str})
    train = df[df["split"] == "train"]
    top10 = get_baseline_topk(train, 10)
    print("Top 10 baseline:", top10)