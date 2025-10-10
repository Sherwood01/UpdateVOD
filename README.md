# vod-converter

自动抓取 [https://d1y.github.io/kitty/vod.json](https://d1y.github.io/kitty/vod.json)  
并转换为自定义格式的 `20.json`，自动托管到 GitHub Pages。

---

## 🚀 功能
- 定时（每 6 小时）自动抓取最新 VOD 源。
- 将原始数组格式转换为 `20.json` 对象格式。
- 自动提交并部署到 GitHub Pages。

---

## 🧩 输出示例
生成的 `20.json` 文件结构如下：
```json
{
  "cache_time": 7200,
  "api_site": {
    "dyttzy": {
      "api": "http://caiji.dyttzyapi.com/api.php/provide/vod",
      "name": "电影天堂资源",
      "detail": "http://caiji.dyttzyapi.com"
    },
    "bfzy": {
      "api": "https://bfzyapi.com/api.php/provide/vod",
      "name": "暴风资源"
    }
  }
}
