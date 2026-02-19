import requests
import re
import os

def get_insta_followers(username):
    # 使用一个无需登录就能看粉丝数的镜像接口
    url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # 在网页源代码中利用正则寻找粉丝数
        match = re.search(r'"edge_followed_by":\{"count":(\d+)\}', response.text)
        if match:
            count = int(match.group(1))
            if count >= 1000000:
                return f"{count/1000000:.1f}M"
            elif count >= 1000:
                return f"{count/1000:.1f}K"
            return str(count)
        return "Wait"
    except:
        return "Error"

# 抓取梅西的粉丝数
followers = get_insta_followers("leomessi")

# 将结果写入文件
with open("insta.txt", "w") as f:
    f.write(followers)

print(f"Successfully fetched: {followers}")
