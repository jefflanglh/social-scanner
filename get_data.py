import requests
import re
import time

def fetch_real_fb_count(page_id):
    """
    尝试从多个公开的社交媒体镜像接口获取实时数据
    """
    # 方案 1: 使用特定的 FB 开放数据端点（伪装成移动端查询）
    url1 = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&width=340&height=70&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    print(f"尝试从插件接口抓取实时粉丝数...")
    try:
        response = requests.get(url1, headers=headers, timeout=15)
        if response.status_code == 200:
            # 这种插件页通常会包含类似 "22 followers" 或 "22 位粉丝"
            html = response.text
            # 正则搜索数字
            match = re.search(r'([\d\.,MK]+)\s?(位粉丝|followers|likes|人喜欢)', html)
            if match:
                res = match.group(1).replace(',', '')
                print(f"成功抓取到实时数据: {res}")
                return res
    except Exception as e:
        print(f"插件接口访问失败: {e}")

    # 方案 2: 如果方案 1 失败，尝试搜索引擎深度指纹
    print("切换至搜索引擎备选方案...")
    url2 = f"https://www.google.com/search?q=site:facebook.com/{page_id}+followers"
    try:
        response = requests.get(url2, headers=headers, timeout=15)
        # 匹配搜索结果中的数字
        match = re.search(r'(\d+)\s?(位粉丝|followers)', response.text)
        if match:
            return match.group(1)
    except:
        pass

    return None

# --- 执行逻辑 ---
page_id = "100090114814925"
real_count = fetch_real_fb_count(page_id)

# 核心判断：只有抓取到新数字才更新，否则保留旧数字不破坏数据
if real_count:
    with open("fb.txt", "w", encoding="utf-8") as f:
        f.write(real_count)
    print(f"数据已更新为最新抓取值: {real_count}")
else:
    print("本次未能抓取到实时数据，保持文件内容不变以防报错。")

# 强制触发 GitHub Action 提交 (更新时间戳)
with open("last_run.txt", "w", encoding="utf-8") as f:
    f.write(str(time.time()))
