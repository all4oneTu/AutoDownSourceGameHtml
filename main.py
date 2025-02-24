import os
import re
import requests
import traceback
from colorama import Fore, Style




try : 
    print("Chương trình đang chạy...")

    def download_file(url, base_host, target_folder):
        if not url.startswith(base_host):
            print(f"Skipping: {url} (Does not match base host)")
            return
        
        relative_path = url[len(base_host):].lstrip("/")
        file_path = os.path.join(target_folder, relative_path)
        folder = os.path.dirname(file_path)
        os.makedirs(folder, exist_ok=True)
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            print(f"Downloaded: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

    def extract_links(file_path):
        links = []
        with open(file_path, "r") as f:
            for line in f:
                match = re.search(r'https?://\S+', line)
                if match:
                    links.append(match.group())
        return links

    def process_links(file_path, base_host, target_folder):
        links = extract_links(file_path)
        
        for link in links:
            download_file(link, base_host, target_folder)

    def change_host(old_host, new_host) :
        file_path = "note.txt"  

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        updated_content = re.sub(re.escape(old_host), new_host, content)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print("Đã thay đổi host thành công!")

    def read_config(filename):
        config = {}
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()  # Loại bỏ khoảng trắng đầu/cuối dòng
                if not line or "=" not in line:  # Bỏ qua dòng trống hoặc dòng sai format
                    continue
                key, value = line.split("=", 1)  # Chia thành key và value
                config[key.strip()] = value.strip()  # Xóa khoảng trắng thừa

        return config

    if __name__ == "__main__":
        config = read_config("config.txt")
        file_path = "note.txt"
        # Lấy giá trị từ file
        host = config.get("host", "")
        local_host = config.get("local_host", "")
        target_folder = config.get("target_folder", "")
        change_host(local_host, host)
        process_links(file_path, host, target_folder)  
        input(Fore.GREEN + "Nhấn Enter để thoát..." +  Style.RESET_ALL)

    
except Exception as e:
    with open("error.log", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())

    print(Fore.RED + "Đã xảy ra lỗi! Xem file error.log để biết chi tiết." + Style.RESET_ALL)
    input("Nhấn Enter để thoát...")  # Giữ terminal không bị đóng ngay