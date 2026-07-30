import json
import re
import datetime
import requests
from bs4 import BeautifulSoup

def get_map_passwords():
    print("🔄 Đang quét mật khẩu Operations Daily...")
    map_names = ["Zero Dam", "Layali Grove", "Brakkesh", "Space City", "Tide Prison", "AZ3"]
    passwords = []
    
    try:
        url = "https://deltaforcetools.gg/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Xóa bớt khoảng trắng dư thừa để cấu trúc chuỗi gọn gàng hơn
            full_text = re.sub(r'\s+', ' ', soup.get_text(separator=' '))
            
            for map_name in map_names:
                # THUẬT TOÁN MỚI: 
                # Bắt buộc 4 chữ số (\d{4}) phải nằm cực gần tên Map (trong vòng tối đa 80 ký tự đổ lại).
                # Ngăn chặn hoàn toàn việc trượt xuống cuối trang lấy nhầm số 7810.
                pattern = re.compile(rf'{re.escape(map_name)}.{{0,80}}?(\b\d{{4}}\b)', re.IGNORECASE)
                match = pattern.search(full_text)
                
                if match:
                    passwords.append({"map": map_name, "code": match.group(1)})
                    
    except Exception as e:
        print(f"❌ Lỗi khi cào dữ liệu: {e}")

    # Nếu không tìm thấy đủ số lượng map trên web (có thể do cấu trúc web bị đổi),
    # tự động dùng khung dữ liệu dự phòng chuẩn để không bị lỗi giao diện.
    if len(passwords) == 0:
        print("⚠️ Không tìm thấy mã trên web, đang sử dụng dữ liệu dự phòng...")
        passwords = [
            {"map": "Zero Dam", "code": "0129"},
            {"map": "Layali Grove", "code": "0469"},
            {"map": "Brakkesh", "code": "0789"},
            {"map": "Space City", "code": "0183"},
            {"map": "Tide Prison", "code": "0035"},
            {"map": "AZ3", "code": "0854"}
        ]

    # Đóng gói dữ liệu ra file JSON
    data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "passwords": passwords
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Đã cập nhật xong {len(passwords)} mật khẩu map!")

if __name__ == "__main__":
    get_map_passwords()
