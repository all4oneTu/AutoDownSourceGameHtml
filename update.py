import requests
import os
import sys
import time
import shutil

# --- Cấu hình ---
GITHUB_REPO = "all4oneTu/AutoDownSourceGameHtml"  # Thay bằng repo của bạn
EXE_NAME = "main.exe"  # Tên file chạy chính
GITHUB_LATEST_RELEASE = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# --- Lấy link tải mới nhất từ GitHub ---
def get_latest_download_url():
    try:
        response = requests.get(GITHUB_LATEST_RELEASE).json()
        latest_version = response["tag_name"]
        download_url = response["assets"][0]["browser_download_url"]
        return latest_version, download_url
    except Exception as e:
        print(f"⚠ Lỗi kiểm tra cập nhật: {e}")
        sys.exit(1)

# --- Tải phiên bản mới ---
def download_new_version(download_url):
    print(f"🔔 Đang tải bản cập nhật mới từ: {download_url}")

    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(f"new_{EXE_NAME}", "wb") as f:
            shutil.copyfileobj(response.raw, f)
        print("✅ Tải xong bản mới!")
    else:
        print("⚠ Lỗi khi tải bản cập nhật!")
        sys.exit(1)

# --- Cập nhật file exe ---
def update_exe():
    print("🔄 Đang thay thế file cũ...")

    # Đóng chương trình cũ
    os.system(f"taskkill /f /im {EXE_NAME}")

    time.sleep(2)  # Chờ chương trình đóng hẳn

    # Ghi đè file mới
    os.replace(f"new_{EXE_NAME}", EXE_NAME)

    print("✅ Cập nhật thành công! Đang khởi động lại...")
    time.sleep(2)

    # Chạy lại chương trình
    os.system(EXE_NAME)

# --- Chạy cập nhật ---
latest_version, download_url = get_latest_download_url()
download_new_version(download_url)
update_exe()
