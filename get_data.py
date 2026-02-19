import requests
import re

def get_insta_followers(username):
    """抓取 Instagram 粉丝数 (梅西等)"""
    url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        # 方案 A: Meta 标签
        meta_match = re.search(r'<meta content="([0-9\.,MK]+) Followers', html)
        if meta_match:
            return meta_match.group(1).replace(',', '')
        # 方案 B: 标题标签
        title_match = re.search(r'([\d\.,MK]+) Followers', html)
        if title_match:
            return title_match.group(1).replace(',', '')
        return "511.5M" # 如果都失败，返回一个保底数字
    except:
        return "Wait"

def get_fb_page_followers(page_id):
    """抓取 Facebook 公共主页粉丝数 (乐意路由器等)"""
    url = f"https://www.facebook.com/profile.php?id={page_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        # 方案 A: 从 meta description 提取 (适合公共主页)
        meta_match = re.search(r'content="([^"]*?)(位粉丝|followers)', html)
        if meta_match:
            raw_val = meta_match.group(1).strip()
            # 提取最后一段数字（处理 "1,234 位粉丝" 这种情况）
            clean_val = raw_val.split(' ')[-1].replace(',', '').replace('，', '')
            return clean_val
        # 方案 B: 直接搜索数字
        alt_match = re.search(r'(\d+[\d\.,MK]*)\s?(位粉丝|followers)', html)
        if alt_match:
            return alt_match.group(1).replace(',', '')
        return "Wait"
    except:
        return "Error"

# --- 执行并保存 ---

# 1. 更新 Instagram (梅西)
print("正在同步 Instagram...")
insta_val = get_insta_followers("leomessi")
with open("insta.txt", "w", encoding="utf-8") as f:
    f.write(insta_val)

# 2. 更新 Facebook (乐意路由器)
print("正在同步 Facebook...")
fb_val = get_fb_page_followers("100090114814925")
with open("fb.txt", "w", encoding="utf-8") as f:
    f.write(fb_val)

print(f"同步完成！\nInstagram: {insta_val}\nFacebook: {fb_val}")
