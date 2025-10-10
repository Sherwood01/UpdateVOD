import json
import requests
import base58
from datetime import datetime
import subprocess
import os

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
        
        # 转换成目标结构
        converted = convert_vod(vods)
        
        # 转换为 JSON 字符串
        json_str = json.dumps(converted, ensure_ascii=False, indent=2)
        
        # 使用 Base58 编码
        encoded = base58.b58encode(json_str.encode("utf-8")).decode("utf-8")
        
        # 保存为文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(encoded)
            
        print(f"✅ Saved Base58-encoded data to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error processing {url}: {str(e)}")
        return False

def git_commit_and_push():
    """执行Git提交和推送操作"""
    try:
        # 设置Git用户信息
        subprocess.run(["git", "config", "--global", "user.name", "137753051@qq.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "Sherwood1"], check=True)
        
        # 添加所有生成的文件
        for output_file in SOURCE_CONFIG.values():
            subprocess.run(["git", "add", output_file], check=True)
        
        # 检查是否有更改需要提交
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            # 有更改，执行提交和推送
            subprocess.run(["git", "commit", "-m", "Auto update multiple files with webpage contents"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ Changes committed and pushed successfully.")
            return True
        else:
            # 没有更改，跳过提交
            print("ℹ️ No changes to commit. Working tree is clean.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {str(e)}")
        return False

def main():
    # 处理所有视频源
    processed_successfully = True
    for url, output_file in SOURCE_CONFIG.items():
        if not process_source(url, output_file):
            processed_successfully = False
    
    # 如果所有视频源处理成功，则执行Git操作
    if processed_successfully:
        if not git_commit_and_push():
            print("⚠️ Failed to commit changes, but files were generated successfully.")
    else:
        print("⚠️ Some sources failed to process, skipping Git commit.")

if __name__ == "__main__":
    main()
