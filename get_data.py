import requests
import re

def get_fb_page_followers(page_id):
    url = f"https://www.facebook.com/profile.php?id={page_id}"
    headers = {
        # 伪装成更像真实的浏览器，增加一些 FB 喜欢的参数
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Sec-Fetch-Mode': 'navigate',
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text

        # 方案 A: 深度扫描源码中的数字指纹 (针对新版公共主页)
        # 寻找类似 "follower_count":1234
        json_match = re.search(r'"follower_count":(\d+)', html)
        if json_match:
            count = int(json_match.group(1))
            if count > 0: return format_num(count)

        # 方案 B: 扫描搜索快照格式
        # 寻找 "1.2万位粉丝" 或 "511 followers"
        meta_match = re.search(r'content="([^"]*?)(位粉丝|followers|粉丝)', html)
        if meta_match:
            raw_text = meta_match.group(1).strip()
            # 提取文本中的数字部分
            numbers = re.findall(r'[\d\.,MK]+', raw_text)
            if numbers: return numbers[-1].replace(',', '')

        # 方案 C: 暴力搜索文本块
        # 寻找类似 "1.2K 粉丝"
        text_match = re.search(r'([\d\.,MK]+)\s?(位粉丝|followers|粉丝)', html)
        if text_match:
            return text_match.group(1).replace(',', '')

        return "Wait"
    except:
        return "Error"

def format_num(num):
    if num >= 1000000: return f"{num/1000000:.1f}M"
    if num >= 1000: return f"{num/1000:.1f}K"
    return str(num)

# --- 下面保持你的主逻辑不变 ---
