# Túc Mạng Minh (Pubbenivāsānussatiñāṇa 宿命明)

[![Version](https://img.shields.io/badge/version-1.0.0-green)](CHANGELOGS/v1.0.0.md)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](#)
[![Compatibility](https://img.shields.io/badge/Supports-Native_Local_History-blue)](#)

Một công cụ dòng lệnh (CLI tool) bằng Python để tìm kiếm lịch sử thay đổi file được lưu bởi **tính năng Local History tích hợp sẵn (native)** của Visual Studio Code / Cursor AI.

> **Lưu ý:** Công cụ này được thiết kế và chỉ dành cho **mục đích sử dụng nội bộ**. Không phân phối hay cung cấp rộng rãi.

Công cụ này cho phép bạn tìm và kiểm tra các phiên bản cũ của tệp, lọc chúng theo một khoảng thời gian cụ thể và tìm kiếm nội dung bên trong chúng. Nó tự động phát hiện nơi lưu trữ lịch sử của VSCode/Cursor mà không cần cấu hình.

```
███████╗ ██████╗ ███╗   ██╗ ██████╗ 
██╔════╝██╔═══██╗████╗  ██║██╔════╝ 
█████╗  ██║   ██║██╔██╗ ██║██║  ███╗
██╔══╝  ██║   ██║██║╚██╗██║██║   ██║
██║     ╚██████╔╝██║ ╚████║╚██████╔╝
╚═╝     ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
```

## Changelog v1.0.0 - The Native History Upgrade

Đây là một bản cập nhật lớn, viết lại phần lõi của công cụ để tương thích hoàn toàn với tính năng Local History tích hợp sẵn của VSCode/Cursor.

-   **Hỗ trợ Native Local History:** Công cụ không còn phụ thuộc vào extension `xyz.local-history` nữa. Nó có thể đọc trực tiếp từ cơ sở dữ liệu lịch sử của VSCode/Cursor.
-   **Tự động phát hiện đường dẫn:** Tự động quét một danh sách các đường dẫn phổ biến (được định nghĩa trong `src/config.py`) để tìm thư mục Local History.
-   **Cơ chế tìm kiếm mới:** Logic `history_finder` được viết lại hoàn toàn để quét các thư mục được mã hóa (hashed) và đọc file metadata `entries.json`, thay vì dựa vào cấu trúc thư mục nhân bản.
-   **Độ tin cậy cao hơn:** Giờ đây công cụ phản ánh chính xác 100% những gì bạn thấy trong tab "Timeline" của editor.

## Tính năng

-   Tìm tất cả các phiên bản lịch sử của một tệp cụ thể.
-   Lọc các phiên bản theo khoảng ngày và giờ.
-   Tìm kiếm nội dung văn bản cụ thể (`grep`) trong các phiên bản lịch sử.
-   Hiển thị ngữ cảnh (các dòng xung quanh) cho mỗi kết quả khớp.
-   Giới hạn tìm kiếm trong N phiên bản gần đây nhất để cải thiện hiệu suất.
-   Giao diện dòng lệnh dễ dàng tích hợp vào các quy trình làm việc.
-   Tự động lưu kết quả ra file để xem lại sau.
-   **Tương thích cao:** Tự động hoạt động với cả VSCode và Cursor trên Linux.

## Yêu cầu & Tương thích

-   **Hệ điều hành**: Hoạt động hoàn hảo trên môi trường Linux.
-   **Extension**: **Không còn yêu cầu** extension Local History. Hoạt động với tính năng tích hợp sẵn của editor.
-   **Thư viện**: Công cụ này chỉ sử dụng các thư viện chuẩn của Python, không yêu cầu cài đặt thêm bất kỳ gói nào. Một file `requirements.txt` rỗng được cung cấp để tuân thủ quy chuẩn.
-   **Dành cho AI**: Để AI có thể học và sử dụng công cụ này một cách hiệu quả, vui lòng tham khảo file quy tắc tại `.cursor/rules/tuc-mang-minh.mdc`.

## Hướng dẫn sử dụng

```bash
python3 .cursor/rules/tuc-mang-minh/main.py <đường_dẫn_tệp> [tùy_chọn]
```

### Tham số

- `đường_dẫn_tệp`: (Bắt buộc) Đường dẫn đến tệp bạn muốn tra cứu trong lịch sử.
  - **Lưu ý**: Công cụ hỗ trợ cả đường dẫn **tuyệt đối** (ví dụ: `/home/user/project/file.js`) và **tương đối** (ví dụ: `src/file.js`).

### Tùy chọn

- `--text <văn_bản>`: Văn bản cần tìm kiếm trong các phiên bản tệp.
- `--start-date "<YYYY-MM-DD HH:MM:SS>"`: Thời gian bắt đầu cho khoảng thời gian tìm kiếm.
- `--end-date "<YYYY-MM-DD HH:MM:SS>"`: Thời gian kết thúc cho khoảng thời gian tìm kiếm.
- `--context <số_dòng>`: Số dòng ngữ cảnh hiển thị xung quanh một kết quả khớp (mặc định: 5).
- `--limit <số_lượng>`: Giới hạn tìm kiếm trong N phiên bản gần đây nhất (mặc định: 50).
- `--history-path <đường_dẫn>`: (Không bắt buộc) Chỉ định một đường dẫn chính xác đến thư mục lịch sử. Nếu được cung cấp, tùy chọn này sẽ được ưu tiên hàng đầu, bỏ qua cơ chế quét tự động.

## Ví dụ

Tìm kiếm chuỗi "quan_trong" trong lịch sử của `src/app.js`, hiển thị 3 dòng ngữ cảnh:

```bash
python3 .cursor/rules/tuc-mang-minh/main.py src/app.js --text "quan_trong" --context 3
```

## Kết hợp với `git diff`

Để xem chi tiết các thay đổi giữa các phiên bản, bạn có thể kết hợp `Túc Mạng Minh` với `git diff`.

1.  **Tìm đường dẫn phiên bản**: Chạy `Túc Mạng Minh` để lấy danh sách các đường dẫn tệp lịch sử.
2.  **So sánh**: Sử dụng `git diff --no-index` với hai đường dẫn bạn muốn so sánh.

```bash
git diff --no-index <phiên_bản_cũ> <phiên_bản_mới>
```

## Lịch sử & Cảm hứng

Công cụ `Túc Mạng Minh` được sinh ra từ ý tưởng về khả năng "nhìn lại tiền kiếp" của một tệp tin. Tên gọi được lấy cảm hứng từ "Túc Mạng Minh" (Pubbenivāsānussatiñāṇa) trong Phật giáo, có nghĩa là trí tuệ thấy rõ các kiếp sống quá khứ của chúng sinh.

Tương tự, công cụ này giúp các lập trình viên "nhìn lại" các phiên bản đã lưu của một tệp, hiểu rõ quá trình tiến hóa, tìm lại những đoạn mã đã mất, hoặc phân tích nguyên nhân của một lỗi. Ý tưởng ban đầu được anh Fong khởi xướng và được hiện thực hóa từ một kịch bản Bash đơn giản chạy trên Linux, sau đó phát triển thành công cụ Python hoàn chỉnh như hiện tại. **Phiên bản 1.0.0** là một bước nhảy vọt, chuyển từ việc hỗ trợ một extension của bên thứ ba sang tích hợp trực tiếp với lõi của editor.

## Cấu trúc dự án

```
tuc-mang-minh/
├── main.py
├── README.md
└── src/
    ├── __init__.py
    ├── cli.py
    ├── config.py
    ├── content_searcher.py
    ├── file_utils.py
    ├── history_finder.py
    ├── orchestrator.py
    ├── printer.py
    └── validator.py
```
