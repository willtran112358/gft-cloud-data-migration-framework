#!/bin/bash

# Thư mục chứa JSON
JSON_DIR="stepfunctions"
# File lưu hash MD5 lần trước
MD5_FILE=".stepfunctions.md5"

# Tính tổng MD5 của tất cả file .json
CURRENT_MD5=$(find "$JSON_DIR" -type f -name "*.json" -exec md5sum {} \; | sort | md5sum | awk '{print $1}')

# Kiểm tra nếu đã có hash cũ
if [ -f "$MD5_FILE" ]; then
  PREVIOUS_MD5=$(cat "$MD5_FILE")

  if [ "$CURRENT_MD5" == "$PREVIOUS_MD5" ]; then
    echo "Không có thay đổi trong thư mục $JSON_DIR."
    exit 0
  else
    echo "Đã phát hiện thay đổi trong $JSON_DIR."
    echo "Hãy chạy thủ công: terraform plan và terraform apply nếu cần."
  fi
else
  echo "Chưa có file hash. Có thể đây là lần đầu hoặc file bị xoá."
  echo "Hãy chạy terraform plan và terraform apply nếu bạn mới cập nhật JSON."
fi

# Cập nhật hash mới vào file .stepfunctions.md5
echo "$CURRENT_MD5" > "$MD5_FILE"
