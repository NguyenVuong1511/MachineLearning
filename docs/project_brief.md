# Project Brief — Gợi ý sản phẩm mua kèm

## 1. Bài toán của mình là gì?
Khách đang có vài sản phẩm trong giỏ hàng. Mình muốn đoán: khách sẽ mua
thêm sản phẩm nào nữa?

Cách kiểm tra: lấy một hóa đơn cũ, giả vờ **giấu đi 1 sản phẩm** trong đó.
Đưa các sản phẩm còn lại cho hệ thống, xem hệ thống có đoán ra đúng sản
phẩm bị giấu không.

**Câu hỏi cần trả lời:** cách làm bằng cosine của mình có đoán đúng nhiều
hơn cách "cứ gợi ý hàng bán chạy nhất" không?

## 2. Mỗi sản phẩm được biểu diễn thế nào?
Mỗi sản phẩm có một "hồ sơ" là danh sách các hóa đơn từng mua nó.

Ví dụ: sản phẩm A xuất hiện ở hóa đơn 1001 và 1003, không có ở 1002.
Hồ sơ của A viết là `[1, 0, 1]` (1 = có mua, 0 = không mua).

Hai sản phẩm có hồ sơ giống nhau (hay đi cùng hóa đơn) → cosine cao →
gợi ý cho nhau.

## 3. Khi nào hệ thống được "học" thông tin nào?
Nguyên tắc đơn giản: **hệ thống chỉ được nhìn dữ liệu cũ (train), không
được nhìn trước dữ liệu dùng để kiểm tra (test)**.

Ví dụ sai: nếu mình tính "sản phẩm nào phổ biến" bằng **cả** dữ liệu
test lẫn train, tức là hệ thống đã "nhìn trộm" đáp án trước khi thi. Đây
gọi là **rò rỉ dữ liệu (leakage)** — lỗi nặng nhất, đề trừ điểm rất nặng.

## 4. Dùng dữ liệu nào?
Dùng **toàn bộ** file dữ liệu (cả 2 sheet), không cắt bớt. Vì sau khi lọc
bỏ rác thì chỉ còn khoảng 53 nghìn hóa đơn và 5 nghìn sản phẩm — máy chạy
nổi, không cần cắt bớt cho nhẹ.

## 5. Làm sạch dữ liệu — bỏ những dòng nào?
Làm theo đúng thứ tự này, mỗi bước ghi lại **bỏ mất bao nhiêu dòng**:

| Bước | Bỏ dòng nào | Vì sao bỏ |
|---|---|---|
| 1 | Dòng bị lặp y hệt nhau | Do file dữ liệu vô tình chép trùng 1 đoạn |
| 2 | Hóa đơn bắt đầu bằng chữ "C" | Đây là đơn hàng bị **hủy**, không phải mua thật |
| 3 | Hóa đơn bắt đầu bằng chữ "A" | Đây là bút toán sổ sách, không phải khách mua |
| 4 | Số lượng mua ≤ 0 | Số âm hoặc 0 nghĩa là trả hàng, không phải mua |
| 5 | Giá ≤ 0 | Giá 0 hoặc âm là lỗi nhập liệu |
| 6 | Không có tên sản phẩm | Không biết đó là sản phẩm gì |
| 7 | Các mã như "POST", "TEST001", "BANK CHARGES"... | Đây là phí ship, phí ngân hàng, bản ghi thử — không phải sản phẩm thật |

Còn các mã như thẻ quà tặng, túi đóng gói thì **giữ lại**, vì sẽ đem ra
so sánh riêng ở phần thí nghiệm (thử bỏ chúng đi xem kết quả đổi thế nào).

## 6. Chia dữ liệu thành 3 phần
Giống như chia đề thi: một phần để **học** (train), một phần để **thử
và chọn cách làm tốt nhất** (validation), một phần để **thi thật, chỉ
làm một lần** (test).

Cách chia: **theo hóa đơn**, không theo từng dòng. Nghĩa là một hóa đơn
phải nằm trọn trong 1 phần, không được cắt đôi một hóa đơn ra 2 phần.

Tỷ lệ: 70% train, 15% validation, 15% test.

## 7. So sánh với ai? (Baseline)
Trước khi khoe mô hình của mình "thông minh", phải so nó với cách làm
**đơn giản nhất**: cứ gợi ý những sản phẩm bán chạy nhất cho mọi khách.
Nếu mô hình cosine không hơn được cách này, phải giải thích vì sao.

## 8. Cách chấm điểm mô hình (ví dụ cụ thể)
Lấy 1 hóa đơn test có 3 sản phẩm: Cốc, Đĩa, Nến. Giấu đi **Nến**.
Đưa Cốc và Đĩa cho hệ thống, hệ thống trả về Top-5 gợi ý.

- Nếu **Nến** nằm trong Top-5 đó → tính là **đúng (hit)**.
- Nếu không → tính là **sai (miss)**.

Làm vậy với hàng nghìn hóa đơn test, rồi tính:

`Tỷ lệ đúng = số lần đúng / tổng số lần thử`

Đây gọi là **Hit-rate@K** (K = 5 trong ví dụ trên).

**Hai điều cần đo thêm:**
- **Coverage:** hệ thống có đang chỉ gợi ý đi gợi ý lại vài sản phẩm quen
  thuộc không, hay có gợi ý được nhiều sản phẩm khác nhau?
- **Có thiên vị hàng phổ biến không?** Xem trong các gợi ý, bao nhiêu %
  là top 10% sản phẩm bán chạy nhất — nếu quá cao, mô hình đang "lười",
  chỉ gợi ý hàng hot mà không thực sự xét sản phẩm nào hợp giỏ hàng.

## 9. Chọn thông số thế nào?
Có hai thứ cần thử: **K** (gợi ý bao nhiêu sản phẩm) và **ngưỡng tần
suất tối thiểu** (bỏ sản phẩm quá hiếm vì cosine của chúng không đáng
tin).

Thử vài giá trị **trên tập validation** (không đụng vào test):
- K: thử 5, 10, 20
- Ngưỡng tần suất: thử 5, 10, 20, 50 hóa đơn

Chọn ra bộ giá trị cho kết quả tốt nhất trên validation. Sau đó **mới**
chạy trên test — và chỉ chạy **một lần duy nhất**, không được chạy thử
nhiều lần rồi chọn kết quả đẹp nhất.

## 10. Coi như xong khi nào?
- Người khác tải code về máy họ, chạy theo hướng dẫn, ra kết quả giống
  mình.
- Mô hình hơn được baseline (hoặc nếu không hơn, giải thích rõ vì sao).
- Không có dấu hiệu leakage (nhìn thấy tập test trước khi thi).

## 11. Những điều cần nói rõ là mình còn thiếu sót ở đâu
- Cách chia tập là ngẫu nhiên, chưa mô phỏng đúng "dự đoán tương lai"
  (đúng ra phải theo trình tự thời gian).
- Nhiều khách trong dữ liệu này mua với số lượng rất lớn (có giỏ hàng
  tới 1.110 sản phẩm) — có thể là người bán sỉ, không hẳn khách lẻ bình
  thường.
- Gần 23% hóa đơn không có mã khách hàng, nên kiểu gợi ý theo khách hàng
  sẽ có ít dữ liệu hơn kiểu gợi ý theo hóa đơn.
- Không dùng mã khách hàng để hiển thị hay ghi log, để bảo vệ thông tin
  khách.