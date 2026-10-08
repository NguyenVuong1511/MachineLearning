const API = {
  async get(path) {
    const r = await fetch(path);
    const body = await r.json().catch(() => ({}));
    if (!r.ok) {
      const err = new Error(body.detail || `Lỗi HTTP ${r.status}`);
      err.status = r.status;
      throw err;
    }
    return body;
  },
  searchProducts(q, limit = 10) {
    return this.get(`/api/search-products?q=${encodeURIComponent(q)}&limit=${limit}`);
  },
  similarItems(stockCode, k = 10) {
    return this.get(`/api/similar-items?stock_code=${encodeURIComponent(stockCode)}&k=${k}`);
  },
  modelStats() {
    return this.get("/api/model-stats");
  },
};

function debounce(fn, delay) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), delay); };
}