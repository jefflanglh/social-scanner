import requests
import re
import os

def get_fb_followers(page_id):
    # 尝试两个可能的链接，增加成功率
    urls = [
        f"https://www.facebook.com/profile.php?id={page_id}",
        f"https://www.facebook.com/{page_id}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }

    for url in urls:
        try:
            print(f"正在尝试抓取: {url}")
            # 使用 session 保持一些 cookie 状态，降低被拦截概率
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=15)
            print(f"响应码: {response.status_code}")
            
            if response.status_code == 200:
                html = response.text
                # 方案 A: 寻找 "follower_count":1234
                json_match = re.search(r'"follower_count":(\d+)', html)
                if json_match:
                    val = json_match.group(1)
                    print(f"方案 A 成功: {val}")
                    return val

                # 方案 B: 寻找 Meta 描述里的粉丝数 (针对公共主页最稳)
                # 例如: "1,234 位粉丝"
                meta_match = re.search(r'content="([^"]*?)(位粉丝|followers|粉丝)', html)
                if meta_match:
                    raw_text = meta_match.group(1).strip()
                    # 提取文本中最后出现的数字
                    numbers = re.findall(r'[\d\.,MK]+', raw_text)
                    if numbers:
                        val = numbers[-1].replace(',', '')
                        print(f"方案 B 成功: {val}")
                        return val
            
            print(f"链接 {url} 未找到有效数据")
        except Exception as e:
            print(f"链接 {url} 访问异常: {e}")
            
    return "Wait_Retry"

# --- 执行部分 ---
fb_val = get_fb_followers("100090114814925")

# 如果抓取不到真实数字，为了不让 ESP32 显示 Wait，我们可以先保留上一次的值
if fb_val == "Wait_Retry":
    try:
        with open("fb.txt", "r") as f:
            fb_val = f.read()
            print("抓取失败，保留旧值")
    except:
        fb_val = "1.2K" # 最终保底

with open("fb.txt", "w", encoding="utf-8") as f:
    f.write(fb_val)

# 强制更新时间戳调试文件
import time
with open("last_run.txt", "w") as f:
    f.write(f"Sync: {time.ctime()}, FB: {fb_val}")

print(f"任务完成，最终写入: {fb_val}")
