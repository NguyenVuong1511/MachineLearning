"""src/evaluate.py — đo Hit-rate@K và coverage trên validation."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import numpy as np
import pandas as pd

from src.features import build_item_matrix, compute_cosine, recommend_topn
from src.baseline import get_baseline_topk

SEED = 42


def leave_one_out_pairs(eval_df: pd.DataFrame, rng: np.random.Generator):
    """Với mỗi hóa đơn >= 2 sản phẩm: giấu 1 sản phẩm, trả về (sản_phẩm_còn_lại, sản_phẩm_bị_giấu)."""
    pairs = []
    for invoice, group in eval_df.groupby("Invoice"):
        codes = group["StockCode"].unique().tolist()
        if len(codes) < 2:
            continue
        hidden = rng.choice(codes)
        input_codes = [c for c in codes if c != hidden]
        pairs.append((input_codes, hidden))
    return pairs


def hit_rate_at_k(pairs, item_vocab, sim_matrix, k: int):
    """Trả về (tỷ lệ đúng, số cặp thực sự được đánh giá)."""
    hits, evaluated = 0, 0
    for input_codes, hidden in pairs:
        if hidden not in item_vocab:
            continue  # sản phẩm bị giấu không nằm trong từ vựng -> không tính
        evaluated += 1
        topk = recommend_topn(input_codes, item_vocab, sim_matrix, n=k)
        if hidden in topk:
            hits += 1
    return (hits / evaluated if evaluated else 0.0), evaluated


def coverage_at_k(pairs, item_vocab, sim_matrix, k: int):
    recommended = set()
    for input_codes, _ in pairs:
        recommended.update(recommend_topn(input_codes, item_vocab, sim_matrix, n=k))
    return len(recommended) / len(item_vocab)


def hit_rate_baseline(pairs, train_df, k: int):
    topk = get_baseline_topk(train_df, k)
    return sum(1 for _, hidden in pairs if hidden in topk) / len(pairs)


if __name__ == "__main__":
    df = pd.read_csv("data/processed/split.csv", dtype={"Invoice": str, "StockCode": str})
    train = df[df["split"] == "train"]
    val = df[df["split"] == "val"]

    rng = np.random.default_rng(SEED)
    pairs = leave_one_out_pairs(val, rng)
    print(f"Số cặp leave-one-out trên validation: {len(pairs)}\n")

    # Dải min_freq chọn theo phân vị thật của bạn: 5 (~không lọc), 20 (~cắt 25%),
    # 60 (~cắt 50%), 150 (~cắt 75%) — xem lại describe() của item_freq Thứ Ba
    for min_freq in [5, 20, 60, 150]:
        mat_inv, vocab_inv = build_item_matrix(train, "Invoice", min_freq=min_freq)
        sim_inv = compute_cosine(mat_inv)
        for k in [5, 10, 20]:
            hr, n_eval = hit_rate_at_k(pairs, vocab_inv, sim_inv, k)
            cov = coverage_at_k(pairs, vocab_inv, sim_inv, k)
            hr_base = hit_rate_baseline(pairs, train, k)
            print(f"min_freq={min_freq:>3}, K={k:>2}: "
                  f"Hit-rate cosine={hr:.3f} (trên {n_eval} cặp), "
                  f"coverage={cov:.3f}, Hit-rate baseline={hr_base:.3f}")