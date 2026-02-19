import requests
import re

def get_insta_followers(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        html = response.text

        # 方案 A: 寻找特定的 Meta 标签 (这是目前最稳的)
        # 格式通常是: <meta content="511M Followers, 304 Following, 3,747 Posts..."
        meta_match = re.search(r'<meta content="([0-9\.,MK]+) Followers', html)
        if meta_match:
            return meta_match.group(1).replace(',', '')

        # 方案 B: 寻找 JSON 里的数据
        json_match = re.search(r'"edge_followed_by":\s*\{\s*"count":\s*(\d+)\}', html)
        if json_match:
            count = int(json_match.group(1))
            if count >= 1000000: return f"{count/1000000:.1f}M"
            if count >= 1000: return f"{count/1000:.1f}K"
            return str(count)

        # 方案 C: 寻找标题标签 (例如 "Leo Messi (@leomessi) • 511M Followers")
        title_match = re.search(r'([\d\.,MK]+) Followers', html)
        if title_match:
            return title_match.group(1).replace(',', '')

        return "Wait"
    except Exception as e:
        print(f"Error: {e}")
        return "Error"

# 执行抓取
followers = get_insta_followers("leomessi")

# 强制检查：如果是 1 或空，就标记为 Wait 避免误导
if followers == "1" or not followers:
    followers = "Wait"

with open("insta.txt", "w") as f:
    f.write(followers)
    
print(f"Captured: {followers}")
