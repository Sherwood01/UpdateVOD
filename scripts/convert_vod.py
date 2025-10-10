import json
import requests

# 远程 vod.json 源
VOD_URL = "https://d1y.github.io/kitty/vod.json"
OUTPUT_FILE = "20.json"

def convert_vod(vods):
    """
    将 vod.json 数组结构转换为 20.json 的 api_site 对象结构
    """
    api_site = {}
    for v in vods:
        api_site[v["id"]] = {
            "api": v["api"],
            "name": v["name"]
        }
        # 如果存在 logo 或其他字段，也可以加入
        if "logo" in v:
            api_site[v["id"]]["detail"] = v["logo"]
    return {
        "cache_time": 7200,
        "api_site": api_site
    }

def main():
    print("Fetching remote vod.json...")
    response = requests.get(VOD_URL)
    response.raise_for_status()
    vods = response.json()

    print(f"Fetched {len(vods)} sources. Converting...")
    converted = convert_vod(vods)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False, indent=2)
    print(f"Saved converted data to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
