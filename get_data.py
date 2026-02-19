import requests
import re
import os

def get_twitch_followers(username):
    # 尝试移动版网页，它通常更轻量，对爬虫更友好
    url = f"https://m.twitch.tv/{username}/home"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    try:
        print(f"--- 正在请求 Twitch 用户: {username} ---")
        response = requests.get(url, headers=headers, timeout=15)
        html = response.text
        
        # 【排查关键】打印网页源码前 2000 个字符
        print("--- 网页源码片段 (前2000字) ---")
        print(html[:2000])
        print("-------------------------------")

        # 匹配方式 1: 寻找 JSON 里的 count
        # 例如: "followerCount":22
        match_json = re.search(r'followerCount":(\d+)', html)
        if match_json:
            val = match_json.group(1)
            print(f"命中方案 A (JSON): {val}")
            return val

        # 匹配方式 2: 寻找 Meta 标签描述
        # 例如: <meta name="description" content="... 22 followers ...">
        match_meta = re.search(r'([\d\.,MK]+)\s?(位粉丝|followers|人关注)', html, re.I)
        if match_meta:
            val = match_meta.group(1).replace(',', '')
            print(f"命中方案 B (Meta): {val}")
            return val
            
        # 匹配方式 3: 寻找标题
        match_title = re.search(r'(\d+)\s?位粉丝', html)
        if match_title:
            val = match_title.group(1)
            print(f"命中方案 C (Title): {val}")
            return val

        print("错误: 所有正则均未匹配到数字")
        return "Wait_Match_Fail"

    except Exception as e:
        print(f"请求发生异常: {e}")
        return "Wait_Error"

# --- 主逻辑 ---
target_user = "fattyprophet"
twitch_val = get_twitch_followers(target_user)

# 写入文件
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(str(twitch_val))

# 顺便保留一个时间戳，方便观察文件是否更新
import time
with open("last_run_twitch.txt", "w", encoding="utf-8") as f:
    f.write(f"Updated at: {time.ctime()}")

print(f"脚本执行完毕，最终写入 twitch.txt 的值: {twitch_val}")
