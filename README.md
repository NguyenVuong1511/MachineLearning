## 1. Chuẩn bị môi trường

```bash
python -m venv .venv  &&  source .venv/bin/activate  &&  pip install -r requirements.txt
```

## 2. Tải và xử lý dữ liệu

Tải tệp `online_retail_II.xlsx` từ trang dữ liệu UCI (xem Tài liệu tham khảo [2]) vào thư mục `data/raw/`, sau đó chạy lần lượt các lệnh sau:

```bash
python -m src.data          # Làm sạch dữ liệu, tạo data/processed/clean.csv
python -m src.split         # Chia train/validation/test, tạo data/processed/split.csv
python -m src.build_lookup  # Tạo bảng tra cứu tên sản phẩm
```

## 3. Huấn luyện và đánh giá mô hình

```bash
python -m src.train           # Xây ma trận cosine, lưu models/cosine_model.joblib
python -m src.final_test      # Đánh giá trên tập test (chỉ chạy một lần), tạo reports/final_test_result.json
python -m src.error_analysis  # Phân tích lỗi, tạo reports/figures/error_analysis.png
```

## 4. Chạy ứng dụng web

```bash
uvicorn app.main:app --reload
```

Mở trình duyệt tại địa chỉ [http://127.0.0.1:8000/](http://127.0.0.1:8000/) để sử dụng giao diện, hoặc [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) để xem tài liệu API tự sinh.

## 5. Chạy kiểm thử tự động

```bash
pytest tests/ -v
```

## 6. Cấu hình đã đóng băng

- **Cách biểu diễn:** `item-invoice`
- **min_freq:** 60
- **K:** 20
- **Mã quà tặng/đóng gói:** Đã loại khỏi pipeline chính.
- **random_state:** 42 _(áp dụng cho việc chia tập và việc giấu sản phẩm trong đánh giá leave-one-out)_.

> **Lưu ý:** Toàn bộ mã nguồn, dữ liệu đã xử lý (không bao gồm dữ liệu thô do giới hạn dung lượng) và nhật ký làm việc hằng tuần được lưu trữ tại kho mã nguồn của nhóm trên GitHub, kèm theo lịch sử commit thể hiện đóng góp của cả hai thành viên.
