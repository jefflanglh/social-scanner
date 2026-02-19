import requests
import re
import os

print(f"当前脚本运行路径: {os.getcwd()}")
print(f"当前目录下文件列表: {os.listdir('.')}")

def get_fb_followers(page_id):
    url = f"https://mbasic.facebook.com/profile.php?id={page_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Facebook 响应码: {response.status_code}")
        # 匹配数字
        match = re.search(r'(\d+[\d\.,MK]*)\s?(位粉丝|followers|人关注|关注者)', response.text)
        if match:
            val = match.group(1).replace(',', '')
            print(f"抓取成功: {val}")
            return val
        print("诊断：正则未命中")
        return "Wait_No_Match"
    except Exception as e:
        print(f"抓取异常: {e}")
        return "Error"

# 执行
fb_val = get_fb_followers("100090114814925")
with open("fb.txt", "w", encoding="utf-8") as f:
    f.write(fb_val)
print("fb.txt 写入完毕")
