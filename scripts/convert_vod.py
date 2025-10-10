import json
import requests
import base58
from datetime import datetime
import subprocess
import os
import hashlib

# 配置多个视频源及其对应的输出文件名
SOURCE_CONFIG = {
    "https://d1y.github.io/kitty/vod.json": "vod.json",
    "https://d1y.github.io/kitty/xvod.json": "xvod.json"
}

def get_file_hash(filename):
    """计算文件的哈希值"""
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

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
        # 获取原始文件哈希（如果存在）
        old_hash = get_file_hash(output_file)
        
        response = requests.get(url)
        response.raise_for_status()
        vods = response.json()
        
        # 转换成目标结构
        converted = convert_vod(vods)
        
        # 转换为 JSON 字符串
        json_str = json.dumps(converted, ensure_ascii=False, indent=2)
        
        # 使用 Base58 编码
        encoded = base58.b58encode(json_str.encode("utf-8")).decode("utf-8")
        
        # 计算新内容的哈希
        new_hash = hashlib.md5(encoded.encode('utf-8')).hexdigest()
        
        # 只有当内容发生变化时才写入文件
        if old_hash != new_hash:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(encoded)
            print(f"✅ Updated {output_file} (content changed)")
            return True, True  # (处理成功, 有变化)
        else:
            print(f"ℹ️ No changes detected in {output_file}, skipping update")
            return True, False  # (处理成功, 无变化)
            
    except Exception as e:
        print(f"❌ Error processing {url}: {str(e)}")
        return False, False  # (处理失败, 无变化)

def git_commit_and_push():
    """执行Git提交和推送操作"""
    try:
        # 检查是否有更改需要提交
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            # 设置Git用户信息
            subprocess.run(["git", "config", "--global", "user.name", "137753051@qq.com"], check=True)
            subprocess.run(["git", "config", "--global", "user.email", "Sherwood1"], check=True)
            
            # 添加所有生成的文件
            for output_file in SOURCE_CONFIG.values():
                subprocess.run(["git", "add", output_file], check=True)
            
            # 执行提交和推送
            subprocess.run(["git", "commit", "-m", "Auto update multiple files with webpage contents"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("✅ Changes committed and pushed successfully.")
            return True
        else:
            print("ℹ️ No changes to commit. Working tree is clean.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {str(e)}")
        return False

def main():
    # 处理所有视频源
    any_changes = False
    all_success = True
    
    for url, output_file in SOURCE_CONFIG.items():
        success, changed = process_source(url, output_file)
        all_success = all_success and success
        any_changes = any_changes or changed
    
    # 如果有任何变化且所有处理都成功，则执行Git操作
    if any_changes and all_success:
        if not git_commit_and_push():
            print("⚠️ Failed to commit changes, but files were updated successfully.")
    elif not any_changes:
        print("ℹ️ No changes detected in any files, skipping Git commit.")
    else:
        print("⚠️ Some sources failed to process, skipping Git commit.")

if __name__ == "__main__":
    main()
