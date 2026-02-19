import requests
import re
import time

def get_insta_followers(username):
    # 模拟真实浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 构造 Google 搜索链接
    url = f"https://www.google.com/search?q=instagram.com/{username}"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        # 调试输出状态码
        print(f"DEBUG: 正在尝试 {username}, HTTP状态码: {response.status_code}")
        
        # 定义正则匹配模式（匹配数字 + 后缀 + Followers/粉丝）
        # 常见格式如: "511M Followers" 或 "511M 粉丝"
        patterns = [
            r'([\d\.,MK\+]+)\s*Followers', 
            r'([\d\.,MK\+]+)\s*粉丝',
            r'([\d\.,MK\+]+)\s*Abonnés'
        ]
        
        for p in patterns:
            match = re.search(p, response.text, re.IGNORECASE)
            if match:
                res = match.group(1).replace(',', '')
                print(f"✅ 成功从源码抓取到 {username}: {res}")
                return res
        
        # 如果循环结束都没找到匹配
        print(f"❌ 源码匹配失败: {username}")
        return "Wait"
        
    except Exception as e:
        print(f"💥 请求异常: {username}, 错误信息: {e}")
        return "Wait"

# --- 执行多用户抓取 ---
users = ["justin", "brabitt"]
final_results = []

for user in users:
    count = get_followers = get_insta_followers(user)
    # 没有任何保底数字，直接存入真实抓取结果
    final_results.append(f"{user}:{count}")
    
    # 每次请求间隔 5 秒，降低被 Google 拦截的风险
    time.sleep(5)

# --- 写入文件 ---
with open("insta.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_results))

print("\n--- 任务结束，请检查 insta.txt ---")
