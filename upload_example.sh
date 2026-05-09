#!/bin/bash
# 請複製一個 upload.sh 並把參數改成自己需要的參數。

# ==========================================
# 請將以下路徑替換成你實際的來源與目的地路徑
# ==========================================

SOURCE_DIR="/your/waiting/uploading/data/"
REMOTE_DEST="<username>@<host>:<where ever you put repo>/perch-mount-new-data-handler/new-data/"

echo "==========================================="
echo "開始執行 rsync 同步作業..."
echo "來源: $SOURCE_DIR"
echo "目的: $REMOTE_DEST"
echo "==========================================="

rsync -av "$SOURCE_DIR" "$REMOTE_DEST"

if [ $? -eq 0 ]; then
    echo "✅ rsync 同步成功！準備清空來源資料夾..."
    
    # 刪除 SOURCE_DIR 裡面的所有檔案與資料夾，但保留 SOURCE_DIR 本身
    rm -rf "${SOURCE_DIR:?}"/*
    
    echo "==========================================="
    echo "🎉 同步與清理作業全部完成！"
    echo "==========================================="
else
    echo "==========================================="
    echo "❌ 同步過程發生錯誤，已保留來源檔案以供檢查。"
    echo "==========================================="
fi
