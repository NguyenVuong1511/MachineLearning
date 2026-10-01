"""src/features.py — xây ma trận item-invoice/item-customer và hàm gợi ý Top-N."""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

SPLIT_CSV = Path("data/processed/split.csv")


def build_item_matrix(train_df: pd.DataFrame, group_col: str, min_freq: int = 60):
    """
    Xây ma trận nhị phân sản phẩm x group_col.
    group_col = "Invoice" (vector item-invoice) hoặc "Customer ID" (vector item-customer).
    min_freq: chỉ giữ sản phẩm xuất hiện >= min_freq lần trong group_col, CHỈ TÍNH TRÊN train_df.
    """
    df = train_df.dropna(subset=[group_col]).copy()

    item_counts = df.groupby("StockCode")[group_col].nunique()
    vocab = item_counts[item_counts >= min_freq].index
    df = df[df["StockCode"].isin(vocab)]

    items = df["StockCode"].astype("category")
    groups = df[group_col].astype("category")

    mat = csr_matrix(
        (np.ones(len(df)), (items.cat.codes, groups.cat.codes)),
        shape=(len(items.cat.categories), len(groups.cat.categories)),
    )
    mat.data[:] = 1  # nhị phân hóa

    item_vocab = items.cat.categories.tolist()
    return mat, item_vocab


def compute_cosine(mat: csr_matrix) -> np.ndarray:
    return cosine_similarity(mat)


def recommend_topn(input_codes: list[str], item_vocab: list[str],
                    sim_matrix: np.ndarray, n: int) -> list[str]:
    """Gợi ý Top-N sản phẩm cho các sản phẩm đã có trong giỏ (input_codes)."""
    code_to_idx = {code: i for i, code in enumerate(item_vocab)}
    input_idx = [code_to_idx[c] for c in input_codes if c in code_to_idx]
    if not input_idx:
        return []

    scores = sim_matrix[input_idx].sum(axis=0)
    scores[input_idx] = -1  # không tự gợi ý lại sản phẩm đã có trong giỏ

    top_idx = np.argsort(-scores)[:n]
    return [item_vocab[i] for i in top_idx]


if __name__ == "__main__":
    df = pd.read_csv(SPLIT_CSV, dtype={"Invoice": str, "StockCode": str})
    train = df[df["split"] == "train"]

    mat_inv, vocab_inv = build_item_matrix(train, "Invoice", min_freq=20)
    sim_inv = compute_cosine(mat_inv)
    print(f"Item-invoice: {len(vocab_inv)} sản phẩm trong từ vựng (min_freq=20)")

    test_code = vocab_inv[0]
    print(f"Gợi ý cho {test_code}:", recommend_topn([test_code], vocab_inv, sim_inv, n=5))