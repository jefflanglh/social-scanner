import requests
import json
import time

def get_twitch_followers(username):
    # 这是目前最稳定的第三方公益接口，它专门把 Twitch 数据转成 JSON 给开发者用
    # 相比 API，它更像是一个公开的计数器镜像
    url = f"https://api.socialcounts.org/twitch-live-follower-count/search/{username.lower()}"
    
    try:
        print(f"--- 正在连接 Twitch 数据节点: {username} ---")
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            # 根据该接口的 JSON 结构提取数字
            if "items" in data and len(data["items"]) > 0:
                count = data["items"][0].get("followerCount")
                if count is not None:
                    print(f">>> 抓取成功！粉丝数: {count}")
                    return str(count)
            print(f"接口返回格式不符: {data}")
        else:
            print(f"服务器返回错误码: {response.status_code}")
            
    except Exception as e:
        print(f"抓取异常: {e}")
    
    return "0"

# --- 执行并写入文件 ---
twitch_user = "fattyprophet"
result = get_twitch_followers(twitch_user)

with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(result)

print(f"--- 脚本执行结束，结果已写入 twitch.txt: {result} ---")
