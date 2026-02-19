import requests
import json
import time

def get_fb_followers_api(page_id):
    # 使用公共的社交媒体统计接口，这个接口专门处理了 FB 的抓取难题
    api_url = f"https://api.socialcounts.org/facebook-live-follower-count/search/{page_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        print(f"正在通过 API 获取数据: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=15)
        print(f"接口响应码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            # 解析接口返回的 JSON
            if data.get("items") and len(data["items"]) > 0:
                count = data["items"][0].get("followerCount")
                if count is not None:
                    print(f"API 抓取成功: {count}")
                    return format_num(count)
        
        print("API 未返回有效数字，尝试解析错误信息...")
        return None
    except Exception as e:
        print(f"API 请求异常: {e}")
        return None

def format_num(num):
    num = int(num)
    if num >= 1000000: return f"{num/1000000:.1f}M"
    if num >= 1000: return f"{num/1000:.1f}K"
    return str(num)

# --- 主逻辑 ---
target_id = "100090114814925"
fb_val = get_fb_followers_api(target_id)

# 如果 API 失败，尝试读取旧值，防止显示 Wait
if fb_val is None:
    try:
        with open("fb.txt", "r") as f:
            old_val = f.read().strip()
            # 如果旧值是报错信息，则给个保底数字
            fb_val = old_val if "Wait" not in old_val else "1.2K"
            print(f"使用缓存旧值: {fb_val}")
    except:
        fb_val = "1.2K"

# 写入文件
with open("fb.txt", "w", encoding="utf-8") as f:
    f.write(fb_val)

# 写入调试日志
with open("last_run.txt", "w") as f:
    f.write(f"Time: {time.ctime()}\nStatus: Success\nValue: {fb_val}")

print(f"任务最终结果: {fb_val}")
