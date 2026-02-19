import requests
import json

def get_twitch_followers(username):
    url = "https://gql.twitch.tv/gql"
    # 这个 Client-ID 是 Twitch 官网公开通用的，不需要申请
    headers = {
        "Client-ID": "kimne78kx3ncx6br8ac4t596jz6qx8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    # 构造查询指令，直接问 Twitch 的数据库要这个 ID 的粉丝数
    query = [{
        "operationName": "ChannelShell",
        "variables": {"login": username.lower()},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "580ab410bcd0c7ad617cc096202271da3a33903bafda0fd14e8682e9751431e8"
            }
        }
    }]

    try:
        print(f"--- 尝试通过官方 GQL 接口抓取: {username} ---")
        response = requests.post(url, headers=headers, json=query, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # 这里的路径非常深，我们需要小心提取
            # data[0] -> data -> user -> followers -> totalCount
            user_data = data[0].get('data', {}).get('user')
            if user_data:
                followers = user_data.get('followers', {}).get('totalCount')
                if followers is not None:
                    print(f">>> 抓取成功！当前粉丝数: {followers}")
                    return str(followers)
            
            print(f"解析失败，返回内容: {data}")
        else:
            print(f"GQL 接口响应错误: {response.status_code}")
            
    except Exception as e:
        print(f"GQL 运行异常: {e}")
    
    return "0"

# --- 执行并写入 ---
twitch_val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(twitch_val)

# 同时也把 Facebook 带上，确保它不丢失
# (这里建议保留你之前的 FB 抓取代码，或者先测试 Twitch)
print(f"最终写入文件: {twitch_val}")
