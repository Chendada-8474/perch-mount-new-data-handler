#!/bin/bash
# 請複製一個 upload.sh 並把參數改成自己需要的參數。

# ==========================================
# 請將以下路徑替換成你實際的來源與目的地路徑
# ==========================================

SOURCE_DIR="/your/waiting/uploading/data/"
REMOTE_HOST="your remote host"
REMOTE_USER="your_username"
DEST_DIR="~/perch-mount-new-data-handler/new-data/"

echo "==========================================="
echo "開始執行 rsync 同步作業..."
echo "來源: $SOURCE_DIR"
echo "目的: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DEST_DIR}"
echo "==========================================="

rsync -av "$SOURCE_DIR" "$DEST_DIR"

echo "==========================================="
echo "同步作業完成！"
echo "==========================================="