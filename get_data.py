import requests
import re
import time
import os

# --- 1. Twitch 抓取函数 (GQL 方案) ---
def get_twitch_followers(username):
    # 使用 Twitch 的全量页面，但伪装成一个普通的爬虫
    url = f"https://www.twitch.tv/{username.lower()}/about"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }
    try:
        print(f"--- 尝试元数据抓取 Twitch: {username} ---")
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        
        # 匹配 "123 followers" 或 "123 位粉丝"
        # Twitch 的 Meta Data 格式非常固定
        match = re.search(r'([\d\.,MK]+)\s?(followers|关注者|位粉丝)', html, re.I)
        if match:
            res = match.group(1).replace(',', '')
            print(f"Twitch 元数据抓取成功: {res}")
            return res
            
        print("Twitch 正则未匹配到内容")
    except Exception as e:
        print(f"Twitch 请求异常: {e}")
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
