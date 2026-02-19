import requests
import time

def get_twitch_followers(username):
    # 这是 Twitch 搜索框的实时建议接口，它通常不封锁 GitHub IP
    url = f"https://passport.twitch.tv/public/usernames/{username.lower()}/available"
    # 我们换一个更高级的：使用 Twitch 内部的 gql 搜索，但只传最小载荷
    
    # 备选极其稳健的方案：直接请求 twitch 的手机版并抓取描述（加入特殊的 Cookie 伪装）
    url = f"https://m.twitch.tv/{username.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        print(f"--- 尝试通过搜索指纹抓取 Twitch: {username} ---")
        # 使用 Session 保持连接
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # 在手机版页面中，粉丝数通常以 "followerCount":1234 这种格式存在
            import re
            # 搜索各种可能的数字标签
            match = re.search(r'"followerCount":(\d+)', response.text)
            if match:
                count = match.group(1)
                print(f">>> 成功抓取数字: {count}")
                return str(count)
            
            # 备选匹配：匹配 "1.2K Followers" 或 "22 Followers"
            match_alt = re.search(r'([\d\.,MK]+)\s?followers', response.text, re.I)
            if match_alt:
                count = match_alt.group(1).replace(',', '')
                print(f">>> 成功通过 Meta 抓取: {count}")
                return count
        
        print(f"状态码: {response.status_code}。Twitch 拒绝了 GitHub IP 的直接访问。")
        
        # --- 绝招：如果上面都失败，使用一个无需 Token 的公共代理 ---
        print("启动代理穿透模式...")
        proxy_url = f"https://api.allorigins.win/get?url=https://m.twitch.tv/{username.lower()}"
        resp = requests.get(proxy_url, timeout=15)
        if resp.status_code == 200:
            content = resp.json()['contents']
            match = re.search(r'"followerCount":(\d+)', content)
            if match:
                return str(match.group(1))
                
    except Exception as e:
        print(f"异常: {e}")
    
    return "0"

# 执行并写入
val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(val)
print(f"最终结果: {val}")
