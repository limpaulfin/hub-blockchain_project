# Phân Tích Vị Trí Lưu Trữ Local History của VSCode/Cursor

*Tài liệu này ghi lại kết quả điều tra về nơi tính năng Timeline/Local History tích hợp của VSCode và Cursor lưu trữ các phiên bản file trên hệ điều hành Linux.*

## Kết Luận Chính

Tính năng **Timeline (Local History) tích hợp sẵn** của VSCode/Cursor **KHÔNG** lưu trữ lịch sử file trong thư mục `.history` ở gốc mỗi dự án. Thay vào đó, nó sử dụng một cơ chế **lưu trữ tập trung, toàn cục** trong thư mục cấu hình của người dùng.

Đường dẫn lưu trữ chính xác trên Linux là:

-   **Đối với Cursor:** `~/.config/Cursor/User/History/`
-   **Đối với VSCode tiêu chuẩn:** `~/.config/Code/User/History/`

## Cơ Chế Hoạt Động

1.  **Lưu Trữ Tập Trung:** Tất cả lịch sử file từ mọi dự án đều được lưu chung vào một thư mục `History` duy nhất nêu trên.
2.  **Mã Hóa (Hashing):**
    *   Mỗi file gốc được theo dõi sẽ được gán một mã định danh (ID).
    *   Một thư mục con với tên được mã hóa (ví dụ: `-154979f`) được tạo ra bên trong thư mục `History` để chứa tất cả các phiên bản của file gốc đó.
    *   Bên trong thư mục mã hóa này, mỗi phiên bản cũ của file cũng được lưu với một tên ngẫu nhiên (ví dụ: `bhyb.mdc`, `TK1Z.mdc`).

## Phương Pháp Truy Vết Lịch Sử Một File Cụ Thể

Do tên thư mục và tên file được mã hóa, cách hiệu quả nhất để tìm lịch sử của một file là tìm kiếm theo nội dung.

**Lệnh `grep` mẫu:**

```bash
# Tìm một chuỗi văn bản độc nhất của file bên trong thư mục History
grep -r "Chuỗi văn bản cần tìm" ~/.config/Cursor/User/History/
```

Lệnh này sẽ trả về đường dẫn đầy đủ đến các file phiên bản cũ có chứa chuỗi văn bản đó, giúp xác định được thư mục mã hóa đang lưu lịch sử của file ta cần tìm.

## Phân Biệt Với Thư Mục `.history`

Sự tồn tại của thư mục `.history` ở gốc dự án là một yếu tố gây nhầm lẫn.

-   Thư mục `.history` này được tạo ra bởi các **extension của bên thứ ba**, điển hình là extension có tên "Local History".
-   Cơ chế của extension này là lưu lịch sử ngay tại dự án, trong khi tính năng **tích hợp sẵn** của VSCode/Cursor thì lưu tập trung tại `~/.config`.
-   Sự không đồng bộ về số lượng phiên bản (ví dụ: Timeline báo 3 phiên bản nhưng `.history` chỉ có 1) là bằng chứng rõ ràng cho thấy đây là hai cơ chế hoàn toàn tách biệt.

Việc nâng cấp công cụ `Túc Mạng Minh` cần phải tính đến việc đọc dữ liệu từ đường dẫn `~/.config/Cursor/User/History/` để có thể hoạt động chính xác với tính năng Timeline tích hợp. 