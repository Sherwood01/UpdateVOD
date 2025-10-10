import json
import requests
import base58
from datetime import datetime

# 配置多个视频源及其对应的输出文件名
SOURCE_CONFIG = {
    "https://d1y.github.io/kitty/vod.json": "vod.json",
    "https://d1y.github.io/kitty/xvod.json": "xvod.json"
    # 可以继续添加更多源
}

def convert_vod(vods):
    """将 vod.json 数组转换为目标 api_site 对象结构"""
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

def process_source(url, output_file):
    """处理单个视频源"""
    print(f"[{datetime.now()}] Fetching {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        vods = response.json()
        print(f"Fetched {len(vods)} sources from {url}. Converting format...")
        
        # 1️⃣ 转换成目标结构
        converted = convert_vod(vods)
        
        # 2️⃣ 转换为 JSON 字符串
        json_str = json.dumps(converted, ensure_ascii=False, indent=2)
        
        # 3️⃣ 使用 Base58 编码
        encoded = base58.b58encode(json_str.encode("utf-8")).decode("utf-8")
        
        # 4️⃣ 保存为文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(encoded)
            
        print(f"✅ Saved Base58-encoded data to {output_file}")
    except Exception as e:
        print(f"❌ Error processing {url}: {str(e)}")

def main():
    for url, output_file in SOURCE_CONFIG.items():
        process_source(url, output_file)

if __name__ == "__main__":
    main()
