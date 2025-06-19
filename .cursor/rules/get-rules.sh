#!/bin/bash
# Mod by Asi on 2024-06-12--12:12-AM
# Mod by Fong on 2024-06-12--10-53-PM

# === Đồng bộ quy tắc từ Obsidian về Project ===
# Script này đồng bộ các file quy tắc (.mdc) và các công cụ mini (ví dụ: tuc-mang-minh)
# từ một vault Obsidian cụ thể về thư mục .cursor/rules/ của dự án hiện tại.
# Cảnh báo: Lệnh này sẽ ghi đè lên các file trong thư mục đích nếu file
# ở thư mục nguồn mới hơn.

# Định nghĩa các biến
SOURCE_DIR="/home/fong/onedrive/Apps/remotely-save/FongObsidian/AI-notes/project-boilerplate-cursor/"
DEST_DIR="./.cursor/rules/"

# Kiểm tra xem thư mục nguồn có tồn tại không
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Loi: Thu muc nguon Obsidian khong ton tai: $SOURCE_DIR"
  exit 1
fi

# Thông báo bắt đầu
echo "Bat dau dong bo tat ca rules va tools tu Obsidian: $SOURCE_DIR"
echo "Den thu muc du an: $DEST_DIR"

# Thực hiện rsync
# -a (archive): Tương đương -rlptgoD. Quan trọng nhất là:
#   -r: Đệ quy vào các thư mục, đảm bảo đồng bộ cả thư mục con như 'tuc-mang-minh'.
#   -l: Sao chép symlinks dưới dạng symlinks.
#   -p: Giữ nguyên quyền (permissions).
#   -t: Giữ nguyên thời gian sửa đổi (modification times).
# -v (verbose): Hiển thị chi tiết quá trình đồng bộ.
# -h (human-readable): Hiển thị kích thước file một cách dễ đọc.
rsync -avh "$SOURCE_DIR" "$DEST_DIR"

# Thông báo hoàn tất
echo "Dong bo toan bo rules va tools tu Obsidian ve du an hoan tat." 