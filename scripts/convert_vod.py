import json
import requests
from datetime import datetime

# 多个远程 VOD 地址和对应输出文件
VOD_SOURCES = [
    {"url": "https://d1y.github.io/kitty/vod.json", "output": "vod.json"},
    {"url": "https://d1y.github.io/kitty/xvod.json", "output": "xvod.json"}
]

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

    # 保存为文件（不进行 Base58 编码）
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_str)

    print(f"✅ Saved JSON data to {output_file}\n")

def main():
    for source in VOD_SOURCES:
        fetch_and_convert(source["url"], source["output"])

if __name__ == "__main__":
    main()
