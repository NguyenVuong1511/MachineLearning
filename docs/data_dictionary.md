\# Từ điển dữ liệu — Online Retail II



| Cột | Kiểu (pandas) | Ý nghĩa | Vai trò trong bài | Thời điểm có sẵn |

|---|---|---|---|---|

| Invoice | str | Mã hóa đơn; bắt đầu bằng "C" = hủy, bắt đầu bằng "A" = điều chỉnh nợ xấu | Khóa chia train/val/test; khóa nhóm giỏ hàng | Lúc lập hóa đơn |

| StockCode | str | Mã sản phẩm. Một số mã không phải sản phẩm thật (POST, DOT, M, C2, D, S, BANK CHARGES, ADJUST, AMAZONFEE, CRUK, TEST001, PADS, gift\_0001\_\*, DCGSSGIRL, DCGSSBOY) | Định danh sản phẩm = một hàng của ma trận; các mã không phải sản phẩm dùng cho Thí nghiệm 4 | Lúc lập hóa đơn |

| Description | object (str, có thể thiếu) | Tên sản phẩm, 4.382 dòng thiếu | Chỉ hiển thị trên web, không đưa vào vector | Lúc lập hóa đơn |

| Quantity | int64 | Số lượng mua; âm là trả/hủy hàng | Dùng để lọc (Quantity ≤ 0 bị loại); nhị phân hóa bỏ qua giá trị số | Lúc lập hóa đơn |

| InvoiceDate | datetime64\[us] | Thời điểm lập hóa đơn, dữ liệu trải 01/12/2009–09/12/2011 | Kiểm tra phạm vi; cơ sở nếu chọn chia theo thời gian | Lúc lập hóa đơn |

| Price | float64 | Đơn giá (đơn vị bảng Anh, £); 6.207 dòng ≤ 0 | Dùng để lọc, không đưa vào vector | Lúc lập hóa đơn |

| Customer ID | float64, có thể thiếu (thiếu 243.007 dòng, 22,8%) | Mã khách hàng | Cột của vector item–customer; \*\*ẩn trên giao diện và log\*\* | Lúc lập hóa đơn |

| Country | str | Quốc gia của khách, 43 quốc gia | Baseline theo quốc gia; phân tích nhóm | Lúc lập hóa đơn |

| source\_sheet | str | "Year 2009-2010" / "Year 2010-2011" — cột do nhóm tự thêm khi gộp 2 sheet, không có trong dữ liệu gốc | Chỉ dùng để dò và loại phần \*\*chồng ngày 01–09/12/2010\*\* giữa hai sheet | Do nhóm tạo |



\*\*Ghi chú kiểm tra đã làm:\*\* 1.067.371 dòng, 9 cột gốc; không có `Invoice`/`StockCode`/`Quantity`/`InvoiceDate`/`Price`/`Country` nào bị thiếu; chỉ `Description` và `Customer ID` có giá trị thiếu.

