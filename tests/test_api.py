"""tests/test_api.py"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_valid_stock_code():
    # Thay "85123A" bằng 1 mã thật có trong models/cosine_model.joblib nếu mã này không tồn tại
    r = client.get("/api/similar-items", params={"stock_code": "85123A", "k": 5})
    assert r.status_code == 200
    assert len(r.json()["recommendations"]) <= 5


def test_invalid_stock_code():
    r = client.get("/api/similar-items", params={"stock_code": "KHONG-TON-TAI", "k": 5})
    assert r.status_code == 404


def test_k_out_of_range():
    r = client.get("/api/similar-items", params={"stock_code": "85123A", "k": 999})
    assert r.status_code == 422


def test_search_short_query():
    r = client.get("/api/search-products", params={"q": "a"})  # ngắn hơn min_length=2
    assert r.status_code == 422


def test_search_no_results():
    r = client.get("/api/search-products", params={"q": "zzzzznotfound"})
    assert r.status_code == 200
    assert r.json()["results"] == []


def test_model_stats():
    r = client.get("/api/model-stats")
    assert r.status_code == 200
    assert "hit_rate" in r.json()