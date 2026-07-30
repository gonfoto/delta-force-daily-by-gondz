import json
import re
import datetime
import requests
import time
from bs4 import BeautifulSoup

def scrape_website(url):
    """Hàm cào dữ liệu chung áp dụng cho mọi URL"""
    map_names = ["Zero Dam", "Layali Grove", "Brakkesh", "Space City", "Tide Prison", "AZ3"]
    codes = {}
    
    # BỘ LỌC RÁC: Khai báo các số ảo, số placeholder bị cấm
    invalid_codes = ["9999", "0000", "1234", "2024", "2025", "2026"]
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            full_text = re.sub(r'\s+', ' ', soup.get_text(separator=' '))
            
            for map_name in map_names:
                pattern = re.compile(rf'{re.escape(map_name)}.{{0,150}}?(\b\d{{4}}\b)', re.IGNORECASE)
                match = pattern.search(full_text)
                if match:
                    code = match.group(1)
                    # Nếu số quét được KHÔNG nằm trong bộ lọc rác thì mới chấp nhận
                    if code not in invalid_codes:
                        codes[map_name] = code
    except Exception as e:
        print(f"❌ Lỗi kết nối khi cào {url}: {e}")
        
    return codes

def get_map_passwords():
    print("🔄 BẮT ĐẦU TIẾN TRÌNH QUÉT KÉP VÀ ĐỐI CHIẾU MẬT KHẨU...")
    
    map_names = ["Zero Dam", "Layali Grove", "Brakkesh", "Space City", "Tide Prison", "AZ3"]
    default_passwords = {
        "Zero Dam": "0129", "Layali Grove": "0469", "Brakkesh": "0789", 
        "Space City": "0183", "Tide Prison": "0035", "AZ3": "0854"
    }
    
    max_retries = 3
    final_passwords = []
    
    for attempt in range(max_retries):
        print(f"\n--- ⏳ LẦN QUÉT THỨ {attempt + 1}/{max_retries} ---")
        
        codes_tools = scrape_website("https://deltaforcetools.gg/")
        codes_hq = scrape_website("https://www.playdeltaforce.com/events/hq/vi/")
        
        print(f"Dữ liệu Tool (Bên thứ 3) : {codes_tools}")
        print(f"Dữ liệu HQ (Chính thức)  : {codes_hq}")
        
        is_match_all = True
        temp_passwords = []
        
        for m in map_names:
            c_tool = codes_tools.get(m)
            c_hq = codes_hq.get(m)
            
            if c_tool and c_hq and c_tool == c_hq:
                temp_passwords.append({"map": m, "code": c_tool})
            else:
                is_match_all = False
                print(f"⚠️ PHÁT HIỆN LỆCH tại {m} -> Tool: {c_tool} | HQ: {c_hq}")
        
        if is_match_all and len(temp_passwords) == len(map_names):
            print("✅ TẤT CẢ MẬT KHẨU KHỚP NHAU 100%! Tiến hành xuất file.")
            final_passwords = temp_passwords
            break 
        else:
            if attempt < max_retries - 1:
                print("🔄 Dữ liệu chưa đồng nhất hoặc cào thiếu. Chờ 15 giây để quét lại...")
                time.sleep(15)
            else:
                print("❌ Đã hết 3 lần quét lại nhưng vẫn lệch. Kích hoạt cơ chế chốt dữ liệu an toàn...")
                for m in map_names:
                    c_hq = codes_hq.get(m)
                    c_tool = codes_tools.get(m)
                    
                    if c_hq:
                        final_passwords.append({"map": m, "code": c_hq})
                        print(f"🔹 {m}: Quyết định dùng mã Web Chính Thức ({c_hq})")
                    elif c_tool:
                        final_passwords.append({"map": m, "code": c_tool})
                        print(f"🔹 {m}: Quyết định dùng mã Tool ({c_tool})")
                    else:
                        final_passwords.append({"map": m, "code": default_passwords[m]})
                        print(f"🔹 {m}: Quyết định dùng mã Dự Phòng ({default_passwords[m]})")

    final_passwords = sorted(final_passwords, key=lambda x: map_names.index(x["map"]))

    data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "passwords": final_passwords
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"\n✅ Hoàn tất! Đã ghi thành công {len(final_passwords)} mã xác thực vào file data.json.")

if __name__ == "__main__":
    get_map_passwords()
