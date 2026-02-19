import requests
import re
import time

def test_social_searcher(username):
    # 模拟一个真实的浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    # 你的目标链接
    url = f"https://www.social-searcher.com/user-search/?q={username}"
    
    print(f"--- 正在测试用户: {username} ---")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"HTTP 状态码: {response.status_code}")
        
        # 打印部分网页源码，看看里面有没有关键词
        content_sample = response.text[:1000] 
        print("网页内容预览 (前1000字):")
        print(content_sample)
        
        # 尝试匹配粉丝数逻辑 (假设它以 Followers 结尾)
        # 这里的正则根据该站点的实际输出可能需要微调
        match = re.search(r'([\d\.,MK]+)\s+Followers', response.text, re.IGNORECASE)
        
        if match:
            count = match.group(1)
            print(f"🎉 成功匹配到粉丝数: {count}")
            return count
        else:
            print("❌ 未在源码中直接发现 'Followers' 关键字")
            return "Wait"
            
    except Exception as e:
        print(f"💥 请求发生错误: {e}")
        return "Error"

# --- 执行测试 ---
# 我们测试两个大号，看看结果
test_users = ["leomessi", "arianagrande"]
results = []

for user in test_users:
    count = test_social_searcher(user)
    results.append(f"{user}:{count}")
    time.sleep(3) # 停顿一下

# 写入文件供观察
with open("insta.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("\n--- 测试结束，文件已生成 ---")
