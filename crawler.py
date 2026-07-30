import json
import re
import datetime
import requests
from bs4 import BeautifulSoup

def get_daily_passwords():
    codes = []
    print("🔄 Đang quét dữ liệu Daily Code...")
    
    # Cào từ trang deltaforcetools.gg qua Proxy
    try:
        url = "https://deltaforcetools.gg/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for el in soup.find_all(['button', 'code', 'span', 'div']):
                text = el.get_text().strip()
                if text and re.match(r'^[A-Z0-9]{6,15}$', text) and text not in codes:
                    codes.append(text)
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")

    # Danh sách dự phòng nếu chưa cào được
    if not codes:
        codes = ["DELTAFORCE2026", "HAWKOPS2026", "GARENAVNNOW"]

    # Lưu dữ liệu vào file data.json
    data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "codes": codes
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Đã ghi {len(codes)} mã vào file data.json")

if __name__ == "__main__":
    get_daily_passwords()
