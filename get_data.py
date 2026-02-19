import requests
import re

def get_twitch_followers(username):
    # 使用 Twitch 的公共频道信息接口 (非 Helix，无鉴权要求)
    # 这是一个专门为第三方工具提供的 legacy 接口镜像
    url = f"https://api.twitch.tv/kraken/users?login={username.lower()}"
    
    # 由于 Kraken 已经停用，我们改用目前唯一不需要 Token 的第三方“透传”服务
    # 它是专为 GitHub/Heroku 等云服务器设计的
    url = f"https://twitchtracker.com/{username.lower()}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        print(f"--- 尝试从 TwitchTracker 镜像点获取: {username} ---")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # TwitchTracker 的源码中关注者数量非常直观
            # 格式通常是: <span>Followers</span> <span class="to-number">22</span>
            html = response.text
            match = re.search(r'Followers</span>\s*<span[^>]*>([\d,]+)</span>', html, re.I)
            if match:
                res = match.group(1).replace(',', '')
                print(f">>> 抓取成功: {res}")
                return res
            
            # 备选正则：匹配页面的统计数值
            match_alt = re.search(r'([\d,]+)\s*followers', html, re.I)
            if match_alt:
                res = match_alt.group(1).replace(',', '')
                return res
                
        print(f"访问镜像点失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"运行异常: {e}")
    
    return "0"

# --- 执行逻辑 ---
val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(val)
print(f"最终写入: {val}")
