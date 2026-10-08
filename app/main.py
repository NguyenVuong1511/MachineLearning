"""app/main.py — API gợi ý sản phẩm mua kèm."""
import json
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Gợi ý sản phẩm mua kèm — Online Retail II",
    description="API item-item recommendation dựa trên cosine similarity. "
                 "Dữ liệu: Online Retail II (UCI). Không dùng Customer ID.",
    version="1.0.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Nạp model MỘT LẦN lúc khởi động — không tính lại cosine mỗi request
model = joblib.load("models/cosine_model.joblib")
SIM_MATRIX = model["sim_matrix"]
ITEM_VOCAB = model["item_vocab"]
CODE_TO_IDX = {code: i for i, code in enumerate(ITEM_VOCAB)}
CODE_TO_NAME: dict = joblib.load("models/product_lookup.joblib")

RESULT_PATH = Path("reports/final_test_result.json")


def recommend(input_codes: list[str], n: int) -> list[dict]:
    input_idx = [CODE_TO_IDX[c] for c in input_codes if c in CODE_TO_IDX]
    if not input_idx:
        return []
    scores = SIM_MATRIX[input_idx].sum(axis=0)
    scores[input_idx] = -1
    top_idx = scores.argsort()[::-1][:n]
    return [
        {
            "stock_code": ITEM_VOCAB[i],
            "description": CODE_TO_NAME.get(ITEM_VOCAB[i], ""),
            "score": round(float(scores[i]), 4),
        }
        for i in top_idx
    ]


@app.get("/api/search-products", tags=["tìm kiếm"], summary="Tìm sản phẩm theo tên hoặc mã")
def search_products(
    q: str = Query(..., min_length=2, description="Từ khóa tìm theo tên hoặc mã sản phẩm"),
    limit: int = Query(10, ge=1, le=30),
):
    q_lower = q.lower()
    matches = [
        {"stock_code": code, "description": CODE_TO_NAME.get(code, "")}
        for code in ITEM_VOCAB
        if q_lower in CODE_TO_NAME.get(code, "").lower() or q_lower in code.lower()
    ]
    return {"query": q, "results": matches[:limit]}


@app.get("/api/similar-items", tags=["gợi ý"], summary="Gợi ý sản phẩm mua kèm")
def similar_items(
    stock_code: str = Query(..., description="Mã sản phẩm, ví dụ 85123A"),
    k: int = Query(10, ge=1, le=50, description="Số lượng gợi ý, 1-50"),
):
    if stock_code not in CODE_TO_IDX:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy mã sản phẩm '{stock_code}' trong hệ thống")
    return {
        "stock_code": stock_code,
        "description": CODE_TO_NAME.get(stock_code, ""),
        "k": k,
        "recommendations": recommend([stock_code], n=k),
    }


@app.get("/api/model-stats", tags=["dashboard"], summary="Số liệu đánh giá mô hình")
def model_stats():
    if not RESULT_PATH.exists():
        raise HTTPException(status_code=503, detail="Chưa có kết quả đánh giá, chạy src/final_test.py trước")
    data = json.loads(RESULT_PATH.read_text())
    for item in data["top_popular"]:
        item["description"] = CODE_TO_NAME.get(item["stock_code"], "")
    return data


@app.get("/api/health", tags=["hệ thống"], summary="Kiểm tra API còn sống")
def health():
    return {"status": "ok", "num_products": len(ITEM_VOCAB)}


# Phục vụ giao diện HTML tĩnh — đặt SAU CÙNG, vì route "/" phải nhường cho các route /api/* ở trên
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")