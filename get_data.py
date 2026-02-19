import requests
import re
import time

def get_insta_followers(username):
    # Picuki 镜像站地址
    url = f"https://www.picuki.com/profile/{username}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"DEBUG: 尝试抓取 {username}, HTTP状态码: {response.status_code}")
        
        # 匹配 Picuki 页面上的粉丝数
        # 通常格式为: <span class="info-content">300,000,000</span>
        # 或者是 <div class="followed_by">...</div> 里的数字
        match = re.search(r'followed_by">([\d\.,\sKMB]+)</span>', response.text, re.IGNORECASE)
        
        # 如果上面的没匹配到，换一种通用的 span 匹配
        if not match:
            match = re.search(r'content">([\d\.,\sKMB]+)</span>', response.text, re.IGNORECASE)

        if match:
            # 提取数字，去除逗号、空格
            res = match.group(1).replace(',', '').replace(' ', '').strip()
            print(f"✅ 成功提取 {username}: {res}")
            return res
        
        print(f"❌ 源码中未发现粉丝数关键词: {username}")
        return "Wait"
        
    except Exception as e:
        print(f"💥 {username} 请求异常: {e}")
        return "Wait"

# --- 执行名单 ---
# 建议确保 ID 拼写正确
users = ["justinbieber", "brabitt"] 

final_results = []

for user in users:
    count = get_insta_followers(user)
    # 纯净输出，无硬编码保底
    final_results.append(f"{user}:{count}")
    time.sleep(5)

# --- 写入文本 ---
with open("insta.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_results))

print("\n--- 任务完成，insta.txt 已保存 ---")
