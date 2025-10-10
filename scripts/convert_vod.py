import json
import requests
import base58
from datetime import datetime
import os

# 多个远程 VOD 地址和对应输出文件名
VOD_SOURCES = [
    {"url": "https://d1y.github.io/kitty/vod.json", "output": "vod.json"},
    {"url": "https://d1y.github.io/kitty/xvod.json", "output": "xvod.json"}
]

# 输出目录
OUTPUT_DIR = "output"

def convert_vod(vods):
    """
    将 vod.json 数组转换为目标 api_site 对象结构
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

def fetch_and_convert(url, output_file):
    print(f"[{datetime.now()}] Fetching {url} ...")
    response = requests.get(url)
    response.raise_for_status()
    vods = response.json()
    print(f"Fetched {len(vods)} sources. Converting format...")

    # 转换成目标结构
    converted = convert_vod(vods)

    # 转换为 JSON 字符串
    json_str = json.dumps(converted, ensure_ascii=False, indent=2)

    # 使用 Base58 编码
    encoded = base58.b58encode(json_str.encode("utf-8")).decode("utf-8")

    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_file)

    # 保存为文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"✅ Saved Base58-encoded data to {output_path}\n")

def main():
    for source in VOD_SOURCES:
        try:
            fetch_and_convert(source["url"], source["output"])
        except requests.RequestException as e:
            print(f"❌ Failed to fetch {source['url']}: {e}")
        except Exception as e:
            print(f"❌ Error processing {source['url']}: {e}")

if __name__ == "__main__":
    main()
