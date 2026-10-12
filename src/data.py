"""src/data.py — làm sạch dữ liệu Online Retail II theo đúng docs/project_brief.md mục 5."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import pandas as pd

RAW_CSV = Path("data/raw/online_retail_II.csv")   # đã cache ở Thứ Hai
OUT_CSV = Path("data/processed/clean.csv")
REPORT = Path("reports/cleaning_report.txt")

# Mã dịch vụ / không phải sản phẩm thật -> loại vĩnh viễn (mục 5, bước 7)
NON_PRODUCT_CODES = {
    "POST", "DOT", "M", "C2", "D", "S",
    "BANK CHARGES", "ADJUST", "AMAZONFEE", "CRUK", "TEST001",
}


def load_raw() -> pd.DataFrame:
    return pd.read_csv(RAW_CSV, dtype={"Invoice": str, "StockCode": str},
                        parse_dates=["InvoiceDate"])


def clean(df: pd.DataFrame) -> pd.DataFrame:
    lines = []
    n0 = len(df)
    lines.append(f"Số dòng ban đầu: {n0:,}")

    # Bước 1: bỏ dòng trùng lặp hoàn toàn (bỏ cột source_sheet khi so trùng)
    cols_for_dup = [c for c in df.columns if c != "source_sheet"]
    before = len(df)
    df = df.drop_duplicates(subset=cols_for_dup)
    lines.append(f"Bước 1 - bỏ trùng lặp hoàn toàn: -{before - len(df):,} dòng")

    inv = df["Invoice"].astype(str)

    # Bước 2: bỏ hóa đơn hủy (bắt đầu bằng 'C')
    before = len(df)
    df = df[~inv.str.startswith("C")]
    lines.append(f"Bước 2 - bỏ hóa đơn hủy (C...): -{before - len(df):,} dòng")

    # Bước 3: bỏ hóa đơn điều chỉnh (bắt đầu bằng 'A')
    inv = df["Invoice"].astype(str)
    before = len(df)
    df = df[~inv.str.startswith("A")]
    lines.append(f"Bước 3 - bỏ hóa đơn điều chỉnh (A...): -{before - len(df):,} dòng")

    # Bước 4: Quantity <= 0
    before = len(df)
    df = df[df["Quantity"] > 0]
    lines.append(f"Bước 4 - bỏ Quantity <= 0: -{before - len(df):,} dòng")

    # Bước 5: Price <= 0
    before = len(df)
    df = df[df["Price"] > 0]
    lines.append(f"Bước 5 - bỏ Price <= 0: -{before - len(df):,} dòng")

    # Bước 6: thiếu Description
    before = len(df)
    df = df[df["Description"].notna()]
    lines.append(f"Bước 6 - bỏ thiếu Description: -{before - len(df):,} dòng")

    # Bước 7: mã không phải sản phẩm thật
    before = len(df)
    df = df[~df["StockCode"].isin(NON_PRODUCT_CODES)]
    lines.append(f"Bước 7 - bỏ mã dịch vụ (POST/TEST001/...): -{before - len(df):,} dòng")

    lines.append(f"\nSố dòng còn lại: {len(df):,} ({len(df)/n0:.1%} so với ban đầu)")
    lines.append(f"Số hóa đơn còn lại: {df['Invoice'].nunique():,}")
    lines.append(f"Số StockCode còn lại: {df['StockCode'].nunique():,}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return df


def main():
    df = load_raw()
    df = clean(df)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)


if __name__ == "__main__":
    main()