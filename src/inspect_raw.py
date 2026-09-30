from pathlib import Path
import pandas as pd

XLSX = Path("../data/raw/online_retail_II.xlsx")
CSV = Path("../data/raw/online_retail_II.csv")
REPORT = Path("../reports/data_inspection.txt")


def load_raw() -> pd.DataFrame:
    if CSV.exists():
        return pd.read_csv(CSV, dtype={"Invoice": str, "StockCode": str},
                           parse_dates=["InvoiceDate"])
    sheets = pd.read_excel(XLSX, sheet_name=None,
                           dtype={"Invoice": str, "StockCode": str})
    parts = []
    for name, part in sheets.items():
        part = part.copy()
        part["source_sheet"] = name
        parts.append(part)
    df = pd.concat(parts, ignore_index=True)
    df.to_csv(CSV, index=False)
    return df


def main():
    df = load_raw()
    lines = []

    def log(text=""):
        print(text)
        lines.append(str(text))

    inv = df["Invoice"].astype(str)
    sc = df["StockCode"].astype(str)

    log(f"Số dòng: {len(df):,} | Số cột: {df.shape[1]}")
    log(df.dtypes.to_string())

    log("\n-- Giá trị thiếu --")
    log(df.isna().sum().to_string())
    log(f"Tỷ lệ thiếu Customer ID: {df['Customer ID'].isna().mean():.1%}")

    log("\n-- Khoảng ngày theo từng sheet --")
    log(df.groupby("source_sheet")["InvoiceDate"].agg(["min", "max", "count"]).to_string())

    cols = [c for c in df.columns if c != "source_sheet"]
    log(f"\nSố dòng trùng lặp hoàn toàn: {df.duplicated(subset=cols).sum():,}")

    log("\n-- Các dòng sẽ bị loại khi làm sạch (chỉ đếm, chưa xóa) --")
    log(f"Hóa đơn hủy (Invoice bắt đầu bằng 'C'): {inv.str.startswith('C').sum():,}")
    log(f"Quantity <= 0: {(df['Quantity'] <= 0).sum():,}")
    log(f"Price <= 0: {(df['Price'] <= 0).sum():,}")
    log(f"Thiếu Description: {df['Description'].isna().sum():,}")

    log("\n-- Quy mô --")
    log(f"Số hóa đơn: {inv.nunique():,}")
    log(f"Số StockCode: {sc.nunique():,}")
    log(f"Số khách hàng: {df['Customer ID'].nunique():,}")
    log(f"Số quốc gia: {df['Country'].nunique()}")

    log("\n-- Invoice không toàn chữ số: ký tự đầu và số dòng --")
    log(inv[~inv.str.fullmatch(r"\d+")].str[0].value_counts().to_string())

    log("\n-- StockCode không bắt đầu bằng 5 chữ số (20 mã phổ biến nhất) --")
    log(sc[~sc.str.match(r"^\d{5}")].value_counts().head(20).to_string())

    # Chỉ để thống kê tạm; việc làm sạch thật sẽ làm ở src/data.py (Thứ Ba)
    valid = df[~inv.str.startswith("C") & (df["Quantity"] > 0) & (df["Price"] > 0)]

    log("\n-- Số sản phẩm khác nhau trong mỗi hóa đơn (kích thước giỏ hàng) --")
    log(valid.groupby("Invoice")["StockCode"].nunique().describe().to_string())

    log("\n-- 10 sản phẩm xuất hiện trong nhiều hóa đơn nhất --")
    top = valid.groupby("StockCode")["Invoice"].nunique().sort_values(ascending=False).head(10)
    for code, n in top.items():
        desc = valid.loc[valid["StockCode"] == code, "Description"].mode()
        log(f"{code:>10} | {n:>6} hóa đơn | {desc.iat[0] if len(desc) else ''}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()