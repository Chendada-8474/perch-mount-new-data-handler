import os
import tarfile
import shutil
import model
import glob
import json
from datetime import datetime

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}


def clear_tmp_directory(target_dir="./tmp"):

    if not os.path.exists(target_dir):
        print(f"⚠️ 目錄 {target_dir} 不存在，無需清理。")
        return False

    print(f"開始清理目錄: {target_dir}")

    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:
            print(f"❌ 刪除 {file_path} 失敗，原因: {e}")
            return False

    print("✅ 目錄清理完成！")
    return True


def extract_tar_simple(tar_path, dest_dir="./tmp"):
    """
    單純將 tar 檔解壓縮到指定的目錄中 (會保留原有的資料夾結構)
    """
    # 檢查 tar 檔是否存在
    if not os.path.exists(tar_path):
        print(f"❌ 錯誤：找不到指定的檔案 {tar_path}")
        return False

    # 確保目的地資料夾存在
    os.makedirs(dest_dir, exist_ok=True)

    try:
        # 使用 'r:*' 自動支援 .tar, .tar.gz, .tgz 等格式
        with tarfile.open(tar_path, "r:*") as tar:
            print(f"📦 正在解壓縮 {tar_path} 到 {dest_dir} ...")

            # Python 3.12+ 引入了 filter 參數來防止「路徑穿越攻擊」(Directory Traversal)
            # 這裡做一個簡單的相容性判斷，確保舊版 Python 也能跑
            if hasattr(tarfile, "data_filter"):
                tar.extractall(path=dest_dir, filter="data")
            else:
                tar.extractall(path=dest_dir)

            print("✅ 解壓縮完成！")
            return True

    except tarfile.TarError as e:
        print(f"❌ 解壓縮失敗，可能不是有效的 tar 檔案: {e}")
        return False
    except Exception as e:
        print(f"❌ 發生未知的錯誤: {e}")
        return False


def read_json_from_tmp(tmp_dir: str = "./tmp") -> dict | None:
    search_pattern = os.path.join(tmp_dir, "**", "*.json")

    json_files = glob.glob(search_pattern, recursive=True)

    if not json_files:
        print(f"❌ 在 {tmp_dir} 及其子目錄中找不到任何 JSON 檔案。")
        return None

    if len(json_files) > 1:
        print(
            f"⚠️ 警告：在 {tmp_dir} 及其子目錄中找到 {len(json_files)} 個 JSON 檔案。"
        )
        print(f"👉 將預設讀取第一個：{json_files[0]}")

    target_file = json_files[0]

    try:
        with open(target_file, "r", encoding="utf-8") as f:
            section = json.load(f)
        return section
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")
        return None
    except Exception as e:
        print(f"❌ 讀取檔案時發生錯誤: {e}")
        return None


def get_media_from_tmp(
    perch_mount_name: str, tmp_dir: str = "./tmp"
) -> list[model.Medium]:
    """
    遞迴讀取 ./tmp 及其所有子資料夾下的影像/影片檔案，回傳 list[Medium]
    """
    media = []

    if not os.path.exists(tmp_dir):
        print(f"❌ 找不到目錄: {tmp_dir}")
        return media

    # 使用 os.walk 進行深度遍歷 (會走訪所有子資料夾)
    # root: 目前所在的資料夾路徑
    # dirs: 該資料夾底下的子資料夾清單
    # files: 該資料夾底下的檔案清單
    for root, dirs, files in os.walk(tmp_dir):
        for filename in files:
            # 將目前的資料夾路徑與檔名組合，得到完整的檔案路徑
            filepath = os.path.join(root, filename)

            _, ext = os.path.splitext(filename)
            ext_lower = ext.lower()

            # 先過濾掉 json 或其他無關的檔案，避免建立不必要的 Medium 物件
            if ext_lower in IMAGE_EXTS or ext_lower in VIDEO_EXTS:
                try:
                    # 建立 Medium 物件
                    medium_obj = model.Medium(
                        path=filepath, perch_mount_name=perch_mount_name
                    )
                    media.append(medium_obj)
                    # 💡 小建議：如果檔案很多層，印出 filepath 會比 filename 更清楚
                    # print(f"✅ 成功載入: {filepath}")
                except Exception as e:
                    # 錯誤訊息也改成印出 filepath，方便除錯找檔案
                    print(f"❌ 處理檔案 {filepath} 時發生錯誤: {e}")

    return media
