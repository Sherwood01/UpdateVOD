import json
import requests
import base58
from datetime import datetime

# 多个远程 VOD 地址和对应输出文件
VOD_SOURCES = [
    {"url": "https://d1y.github.io/kitty/vod.json", "output": "vod.json", "convert": True},
    {"url": "https://d1y.github.io/kitty/xvod.json", "output": "xvod.json", "convert": True},
    {"url": "http://vod.xwqin.com/20.json", "output": "20.json", "convert": False},
    {"url": "http://vod.xwqin.com/98.json", "output": "98.json", "convert": False},
    {"url": "http://vod.xwqin.com/118.json", "output": "118.json", "convert": False}
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

def fetch_and_convert(url, output_file, convert):
    print(f"[{datetime.now()}] Fetching {url} ...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(f"Fetched {len(data)} sources. Processing...")

    if convert:
        # 如果需要转换格式，执行格式转换
        data = convert_vod(data)

    # 转换为 JSON 字符串
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    # 使用 Base58 编码
    encoded = base58.b58encode(json_str.encode("utf-8")).decode("utf-8")

    # 保存为文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"✅ Saved Base58-encoded data to {output_file}\n")

def main():
    for source in VOD_SOURCES:
        try:
            fetch_and_convert(source["url"], source["output"], source["convert"])
        except requests.RequestException as e:
            print(f"❌ Failed to fetch {source['url']}: {e}")
        except Exception as e:
            print(f"❌ Error processing {source['url']}: {e}")

if __name__ == "__main__":
    main()
