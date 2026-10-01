\# Dữ liệu: Online Retail II



\- Nguồn: UCI Machine Learning Repository —

&#x20; https://archive.ics.uci.edu/dataset/502/online%2Bretail

\- DOI: https://doi.org/10.24432/C5CG6D

\- Giấy phép: CC BY 4.0 (được dùng và chỉnh sửa, phải ghi nguồn)

\- Ngày tải: 29/09/2026

\- Tệp sử dụng: online\_retail\_II.xlsx, gồm 2 sheet

&#x20; "Year 2009-2010" và "Year 2010-2011"

\- SHA-256: bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980

\- Số dòng thô: 1.067.371 | Số cột thô: 9

\- Khoảng thời gian: 01/12/2009 – 09/12/2011

&#x20; (2 sheet chồng nhau 9 ngày, từ 01/12/2010 đến 09/12/2010)

\- Sau bước loại dòng trùng lặp hoàn toàn: -34.335 dòng

\- Sau làm sạch (loại hóa đơn hủy "C", hóa đơn điều chỉnh "A",

&#x20; Quantity ≤ 0, Price ≤ 0, thiếu Description, các mã dịch vụ

&#x20; POST/DOT/M/C2/D/S/BANK CHARGES/ADJUST/AMAZONFEE/CRUK/TEST001):

&#x20; còn lại 39.520 hóa đơn, 4.906 mã sản phẩm, 5.942 khách hàng,

&#x20; 43 quốc gia

\- Tỷ lệ thiếu Customer ID trên dữ liệu thô: 22,8%

\- Cách tái tạo:

&#x20; 1. Tải tệp từ link trên, đặt vào `data/raw/`

&#x20; 2. Chạy `python src/inspect_raw.py` để kiểm tra và cache thành CSV

&#x20; 3. (Thứ Ba) chạy `python src/data.py` để làm sạch theo đúng thứ tự

&#x20;    trong `docs/project_brief.md` mục 6

\- Lưu ý: dữ liệu thô không đưa vào Git (đã liệt kê trong .gitignore)

