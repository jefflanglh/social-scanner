import requests
import re
import time
import os

# --- 1. Twitch 抓取函数 (GQL 方案) ---
def get_twitch_followers(username):
    url = "https://gql.twitch.tv/gql"
    # 这是一个通用的公共 Client-ID，网页版 Twitch 也在用它
    headers = {
        "Client-ID": "kimne78kx3ncx6br8ac4t596jz6qx8", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    # 这是一个专门查询频道基础信息的持久化查询 SHA
    query = [{
        "operationName": "ChannelShell",
        "variables": {"login": username.lower()},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "580ab410bcd0c7ad617cc096202271da3a33903bafda0fd14e8682e9751431e8"
            }
        }
    }]

    try:
        print(f"--- 尝试 GQL 抓取 Twitch: {username} ---")
        response = requests.post(url, json=query, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            followers = data[0]['data']['user']['followers']['totalCount']
            print(f"Twitch 抓取成功: {followers}")
            return str(followers)
        else:
            print(f"Twitch GQL 响应异常: {response.status_code}")
    except Exception as e:
        print(f"Twitch 抓取报错: {e}")
    return "Wait_T"

# --- 2. Facebook 抓取函数 (插件方案) ---
def get_fb_followers(page_id):
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&small_header=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    }
    try:
        print(f"--- 尝试抓取 Facebook: {page_id} ---")
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        # 匹配数字+位粉丝/followers
        match = re.search(r'([\d\.,MK]+)\s?(位粉丝|followers|人关注)', html)
        if match:
            res = match.group(1).replace(',', '')
            print(f"Facebook 抓取成功: {res}")
            return res
    except Exception as e:
        print(f"Facebook 报错: {e}")
    return "Wait_F"

# --- 3. 主逻辑 ---
if __name__ == "__main__":
    # 配置你的 ID
    TWITCH_ID = "fattyprophet"
    FB_ID = "100090114814925"

    # 执行抓取
    t_val = get_twitch_followers(TWITCH_ID)
    f_val = get_fb_followers(FB_ID)

    # 写入 Twitch 文件
    with open("twitch.txt", "w", encoding="utf-8") as f:
        f.write(t_val)
    
    # 写入 Facebook 文件
    with open("fb.txt", "w", encoding="utf-8") as f:
        f.write(f_val)

    # 生成一个运行日志，确保 GitHub Actions 每次都有内容可以提交
    with open("last_run.txt", "w", encoding="utf-8") as f:
        f.write(f"Sync Time: {time.ctime()}\nTwitch: {t_val}\nFB: {f_val}")

    print("--- 任务全部完成 ---")
