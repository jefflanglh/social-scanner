import requests
import re

def get_twitch_followers(username):
    # 这个接口是 Twitch 专门给搜索框联想词用的，校验极松，目前 GitHub IP 可用
    url = f"https://www.twitch.tv/search?term={username.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        print(f"--- 尝试 Twitch 搜索联想通道: {username} ---")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            html = response.text
            # 搜索结果页的源码中会包含 "followersCount": 数字
            # 或者是针对该用户的描述摘要
            match = re.search(r'"followersCount":(\d+)', html)
            if match:
                res = match.group(1)
                print(f">>> 联想通道抓取成功: {res}")
                return str(res)
            
            # 备选：匹配类似 "22 followers" 的纯文本
            match_alt = re.search(r'([\d\.,MK]+)\s?followers', html, re.I)
            if match_alt:
                res = match_alt.group(1).replace(',', '')
                print(f">>> 文本解析抓取成功: {res}")
                return res

        print(f"状态码: {response.status_code}, 该通道也已被拦截。")
    except Exception as e:
        print(f"异常: {e}")
    
    return "0"

# --- 执行逻辑 ---
val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(val)
print(f"最终写入: {val}")
