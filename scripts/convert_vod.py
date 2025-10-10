import json
import requests
import base58
from datetime import datetime

# 远程 vod.json 地址
VOD_URL = "https://d1y.github.io/kitty/vod.json"
OUTPUT_FILE = "20.json"

def convert_vod(vods):
    """
    将 vod.json 数组转换为 20.json 的 api_site 对象结构
    """
    api_site = {}
    for v in vods:
        site = {
            "api": v.get("api", ""),
            "name": v.get("name", "")
        }
        if v.get("logo"):
            site["detail"] = v["logo"]
        api_site[v["id"]] = site
    return {
        "cache_time": 7200,
        "api_site": api_site
    }

def main():
    print(f"[{datetime.now()}] Fetching remote vod.json...")
    response = requests.get(VOD_URL)
    response.raise_for_status()
    vods = response.json()
    print(f"Fetched {len(vods)} sources. Converting format...")

    # 1️⃣ 转换成目标结构
    converted = convert_vod(vods)

    # 2️⃣ 转换为 JSON 字符串
    json_str = json.dumps(converted, ensure_ascii=False, indent=2)

    # 3️⃣ 使用 Base58 编码
    encoded = base58.b58encode(json_str.encode("utf-8")).decode("utf-8")

    # 4️⃣ 保存为文件（文件中是 Base58 文本）
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"✅ Saved Base58-encoded data to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
