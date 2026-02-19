import requests

def get_twitch_followers(username):
    url = "https://gql.twitch.tv/gql"
    # 这是一个通用的公共客户端 ID
    headers = {
        "Client-ID": "kimne78kx3ncx6br8ac4t596jz6qx8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    # 这里的查询体采用了 Twitch 内部最基础的 user 查询逻辑
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
        print(f"--- 尝试 Twitch 官方 GQL 通道: {username} ---")
        response = requests.post(url, headers=headers, json=query, timeout=15)
        
        # 即使 400/403，我们也打印出来看看到底为什么
        if response.status_code == 200:
            data = response.json()
            # 路径: data[0] -> data -> user -> followers -> totalCount
            user_data = data[0].get('data', {}).get('user')
            if user_data:
                followers = user_data.get('followers', {}).get('totalCount')
                if followers is not None:
                    print(f">>> 最终抓取成功: {followers}")
                    return str(followers)
            print(f"解析异常，结构已变: {data}")
        else:
            print(f"服务器返回错误码: {response.status_code}, 内容: {response.text[:100]}")
    except Exception as e:
        print(f"运行异常: {e}")
    
    # 【最后保底：不要给 22，给 0，这样你看到 0 就知道还没通】
    return "0"

# --- 写入文件 ---
twitch_val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w", encoding="utf-8") as f:
    f.write(twitch_val)
print(f"写入文件结果: {twitch_val}")
