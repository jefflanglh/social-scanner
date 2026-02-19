import requests
import re
import json

def get_twitch_followers(username):
    # 这是一个专门为播放器提供的 JSON 数据接口，通常被认为是“公共资产”，封锁最松
    url = f"https://www.twitch.tv/libs/config/{username.lower()}"
    
    # 另一个极其隐蔽的路径：Twitch 视频流元数据预览
    backup_url = f"https://www.twitch.tv/{username.lower()}/about"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        print(f"--- 尝试 Twitch 隐蔽元数据通道: {username} ---")
        # 步骤 1: 尝试获取配置 JSON
        response = requests.get(url, headers=headers, timeout=15)
        
        # 如果这个路径能通，粉丝数就在 JSON 字符串里
        if response.status_code == 200:
            # 搜索网页源码中的结构化数据
            # Twitch 经常把数据藏在 <script type="application/ld+json"> 里
            res = requests.get(backup_url, headers=headers, timeout=15)
            html = res.text
            
            # 方案 A: 寻找结构化 JSON 数据 (SEO 专用)
            # 这种数据是给 Google 搜索看的，Twitch 不敢轻易封锁或隐藏
            json_pattern = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
            if json_pattern:
                data = json.loads(json_pattern.group(1))
                # 这种 JSON 结构通常包含 interactionStatistic
                for item in data:
                    if 'interactionStatistic' in item:
                        for stat in item['interactionStatistic']:
                            if 'userInteractionCount' in stat:
                                count = stat['userInteractionCount']
                                print(f">>> SEO 通道抓取成功: {count}")
                                return str(count)

            # 方案 B: 寻找网页头部的 Meta 描述 (强制解析)
            # 即使动态加载失败，SEO Meta 通常是服务器端直接生成的
            meta_match = re.search(r'property="og:description" content="[^"]*?([\d\.,MK]+)\s?(followers|位粉丝)', html, re.I)
            if meta_match:
                count = meta_match.group(1).replace(',', '')
                print(f">>> Meta 通道抓取成功: {count}")
                return count

        print(f"状态码: {response.status_code}，未能找到粉丝数标记。")
    except Exception as e:
        print(f"异常: {e}")
    
    return "0"

# 执行逻辑
val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(val)
print(f"写入文件结果: {val}")
