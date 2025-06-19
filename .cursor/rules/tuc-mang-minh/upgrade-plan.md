# Kế Hoạch Nâng Cấp Công Cụ Túc Mạng Minh (Work Breakdown Structure)

*Tài liệu này phân rã các công việc cần thực hiện để nâng cấp công cụ `Túc Mạng Minh`, giúp nó tương thích với cơ chế lưu trữ Local History tích hợp của VSCode/Cursor.*

---

## 1.0 Phân Tích & Nghiên Cứu

| ID    | Nhiệm vụ                                 | Mô tả                                                                                                                                                                                                 | Kết quả mong đợi                                                                                     |
| :---- | :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| **1.1** | **Xác định các Đường Dẫn Lưu Trữ Khả Thi** | Thay vì tìm kiếm một biến cấu hình, công cụ sẽ kiểm tra một danh sách các đường dẫn có thể được hard-code. Điều này đảm bảo tính ổn định trên các máy khác nhau nơi vị trí cài đặt có thể khác biệt đôi chút. | Một danh sách (array) các đường dẫn tuyệt đối đã được xác minh là nơi Cursor lưu trữ Local History.       |
| 1.1.1 | Liệt kê các đường dẫn tiềm năng         | Dựa trên thực tế, hai đường dẫn khả thi nhất là: `~/.config/Cursor/User/History/` (viết hoa) và `~/.config/cursor/User/History/` (viết thường).                                                          | Một mảng chứa 2 đường dẫn chuỗi.                                                                      |
| 1.1.2 | Kiểm tra sự tồn tại của các đường dẫn   | Thực thi các lệnh terminal để kiểm tra xem đường dẫn nào thực sự tồn tại trên hệ thống hiện tại.                                                                                                         | Xác nhận được đường dẫn chính xác đang được sử dụng trên máy của anh Fong.                                |

## 2.0 Cập Nhật Tài Liệu Kỹ Thuật

| ID    | Nhiệm vụ                                       | Mô tả                                                                                                                                                                                                                                                                    | Kết quả mong đợi                                                                                                            |
| :---- | :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| **2.1** | **Cập nhật file `local-history-storage-analysis.md`** | Chỉnh sửa lại file tài liệu hiện có để phản ánh đúng chiến lược mới: kiểm tra một danh sách các đường dẫn cố định thay vì tìm biến cấu hình.                                                                                                                                | File tài liệu được cập nhật chính xác và đầy đủ.                                                                            |
| 2.1.1 | Sửa đổi phần Kết Luận Chính & Cơ Chế Hoạt Động | Ghi rõ rằng Cursor có thể lưu trữ history ở một trong vài vị trí phổ biến, và `~/.config/Cursor/User/History/` là vị trí thường gặp nhất.                                                                                                                                   | Nội dung được cập nhật để tránh gây hiểu nhầm.                                                                              |
| 2.1.2 | Bổ sung mục về Danh Sách Đường Dẫn             | Thay thế mục về "Biến Cấu Hình" bằng một mục mới, giải thích rằng chiến lược tốt nhất là kiểm tra một danh sách các đường dẫn tiềm năng, bao gồm cả biến thể viết hoa/thường của thư mục `Cursor`.                                                                               | Người đọc hiểu được cách tiếp cận thực tế và linh hoạt hơn để tìm đúng đường dẫn.                                          |
| 2.1.3 | Cập nhật đề xuất cho Túc Mạng Minh             | Nhấn mạnh rằng phiên bản nâng cấp của công cụ nên có một mảng (array) chứa các đường dẫn khả thi. Công cụ nên duyệt qua mảng này và sử dụng đường dẫn đầu tiên mà nó tìm thấy tồn tại trên hệ thống. Điều này đảm bảo công cụ hoạt động đúng trên nhiều môi trường cài đặt khác nhau. | Một yêu cầu kỹ thuật rõ ràng và mạnh mẽ cho việc phát triển công cụ Túc Mạng Minh trong tương lai.                             |

## 3.0 Thiết Kế & Phát Triển (Tương Lai)

| ID    | Nhiệm vụ                       | Mô tả                                                                                                                | Kết quả mong đợi                                                               |
| :---- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **3.1** | **Thiết kế lại Túc Mạng Minh** | Dựa trên các phát hiện, thiết kế lại logic của công cụ để duyệt qua một danh sách các đường dẫn và chọn đường dẫn đúng. | Bản thiết kế kỹ thuật cho phiên bản mới.                                        |
| **3.2** | **Phát triển phiên bản mới**  | Viết code cho phiên bản nâng cấp.                                                                                    | Mã nguồn mới của công cụ.                                                      |
| **3.3** | **Kiểm thử**                  | Kiểm tra công cụ trên các môi trường có các đường dẫn khác nhau (viết hoa/thường) để đảm bảo hoạt động chính xác.      | Báo cáo kiểm thử và công cụ hoạt động ổn định.                                  |

</rewritten_file> 