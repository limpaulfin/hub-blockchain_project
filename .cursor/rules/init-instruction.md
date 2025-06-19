Pre-prompt

2025-06-18


Mệnh lệnh bất khả kháng:
1.  **Bước 1: Khởi tạo Ngữ cảnh (BẮT BUỘC & ƯU TIÊN TỐC ĐỘ)**
    *   Ngay lập tức, em PHẢI dùng lệnh `cat .cursor/rules/__init.mdc | xarg` để đọc nhanh file quy tắc cốt lõi. Tuyệt đối không dùng công cụ `read_file` cho bước này.
    *   Dựa vào quy trình "Init" trong file đó, em phải **LÊN KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT TRONG IM LẶNG** (sử dụng thẻ `<thinking>`). Kế hoạch này là để em tự định hướng và không cần trình bày ra cho anh.

2.  **Bước 2: Thực thi Kế hoạch**
    *   Sau khi đã có kế hoạch nội bộ, em bắt đầu thực thi để giải quyết yêu cầu của anh.
    *   Em phải tuân thủ nghiêm ngặt kế hoạch đã lập và TOÀN BỘ các quy tắc khác trong `.cursor/rules/`.

3.  **Bước 3: Tự điều chỉnh & Khám phá (Self-Correction & Exploration)**
    *   Nếu trong quá trình thực thi, em cảm thấy chưa hiểu rõ về cấu trúc dự án hoặc các lệnh thao tác file bắt đầu thất bại, em PHẢI chủ động tạm dừng và áp dụng quy trình "Progressive Deepening" được mô tả trong file `rule-project-onboarding-and-memory-alignment.mdc` để tái lập bản đồ dự án trước khi tiếp tục.

**Yêu cầu của anh:**



 (2025-06-04):




2025-06-14 

Mệnh lệnh bất khả kháng:

1.  **Bước 1: Khởi tạo Ngữ cảnh (BẮT BUỘC & ƯU TIÊN TỐC ĐỘ)**
    *   Ngay lập tức, em PHẢI dùng lệnh `cat .cursor/rules/__init.mdc` để đọc nhanh file quy tắc cốt lõi. Tuyệt đối không dùng công cụ `read_file` cho bước này.
    *   Dựa vào quy trình "Init" trong file đó, em phải **LÊN KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT TRONG IM LẶNG** (sử dụng thẻ `<thinking>`). Kế hoạch này là để em tự định hướng và không cần trình bày ra cho anh.

2.  **Bước 2: Thực thi Kế hoạch**
    *   Sau khi đã có kế hoạch nội bộ, em bắt đầu thực thi để giải quyết yêu cầu của anh.
    *   Em phải tuân thủ nghiêm ngặt kế hoạch đã lập và TOÀN BỘ các quy tắc khác trong `.cursor/rules/`.

3.  **Bước 3: Tự điều chỉnh & Khám phá (Self-Correction & Exploration)**
    *   Nếu trong quá trình thực thi, em cảm thấy chưa hiểu rõ về cấu trúc dự án hoặc các lệnh thao tác file bắt đầu thất bại, em PHẢI chủ động tạm dừng và áp dụng quy trình "Progressive Deepening" được mô tả trong file `rule-project-onboarding-and-memory-alignment.mdc` để tái lập bản đồ dự án trước khi tiếp tục.

**Yêu cầu của anh:**


=== (cũ rồi)

🤖💡🧠 PHẢI ĐỌC TOÀN BỘ file quy tắc '.cursor/rules/__init.mdc' trước khi đưa ra bất kỳ phản hồi nào + <thinking> <reasoning> + PHẢI TUÂN THỦ NGHIÊM NGẶT rule trong đó + , **TRONG IM LẶNG** + LUÔN TRẢ LỜI TIẾNG VIỆT + kết hợp với context+conversation hiện tại. Nếu không thấy file này được cung cấp trong context, dùng công cụ file_search để tìm và đọc file này.



## Hướng dẫn kiểm tra và cập nhật cấu hình Espanso

### Kiểm tra cài đặt Espanso

1. Kiểm tra xem Espanso đã được cài đặt chưa:
   ```bash
   which espanso
   ```
   - Nếu kết quả hiển thị đường dẫn (ví dụ: `/usr/bin/espanso`), Espanso đã được cài đặt
   - Nếu không có kết quả, Espanso chưa được cài đặt

### Tìm file cấu hình base.yml

2. Tìm vị trí file cấu hình `base.yml`:
   ```bash
   find /home/fong/.config -name "base.yml" | grep -i espanso
   ```
   - Vị trí tiêu chuẩn trên Linux: `/home/fong/.config/espanso/match/base.yml`
   - Nếu không tìm thấy, thử mở rộng tìm kiếm:
     ```bash
     find /home -name "base.yml" 2>/dev/null | grep -i espanso
     ```

### Kiểm tra cấu hình hiện tại

3. Xem nội dung của cấu hình hiện tại:
   ```bash
   cat /home/fong/.config/espanso/match/base.yml
   ```
   Hoặc xem phần cấu hình cụ thể:
   ```bash
   grep -A 5 "mmm" /home/fong/.config/espanso/match/base.yml
   ```

### Cập nhật cấu hình

4. Cập nhật cấu hình để thay đổi trigger `mmm` thành `pre-prompt`:

   ```bash
   # Tạo backup trước khi sửa đổi
   cp /home/fong/.config/espanso/match/base.yml /home/fong/.config/espanso/match/base.yml.backup

   # Chỉnh sửa file bằng trình soạn thảo (ví dụ: nano, vim, gedit)
   nano /home/fong/.config/espanso/match/base.yml
   ```

5. Trong file cấu hình, tìm phần:

   ```yaml
   - trigger: "mmm"
     replace: "PHẢI ĐỌC TOÀN BỘ file quy tắc '.cursor/rules/__init.mdc'..."
   ```

6. Sửa thành:
   ```yaml
   - trigger: "pre-prompt"
     replace: "PHẢI ĐỌC TOÀN BỘ file quy tắc '.cursor/rules/__init.mdc'..."
   ```

### Áp dụng thay đổi

7. Khởi động lại Espanso để áp dụng thay đổi:
   ```bash
   espanso restart
   ```

### Kiểm tra thay đổi

8. Kiểm tra xem thay đổi đã được áp dụng chưa:
   ```bash
   grep -A 5 "pre-prompt" /home/fong/.config/espanso/match/base.yml
   ```

### Khôi phục cấu hình (nếu cần)

9. Nếu có vấn đề, khôi phục từ backup:
   ```bash
   cp /home/fong/.config/espanso/match/base.yml.backup /home/fong/.config/espanso/match/base.yml
   espanso restart
   ```
