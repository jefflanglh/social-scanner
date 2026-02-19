import requests
import re
import time

def get_twitch_followers(username):
    # 使用公益中转接口，这个接口在海外访问非常稳定，且返回的就是纯数字
    url = f"https://decapi.me/twitch/follow_count/{username.lower()}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (ESP32; SocialCounter)'
    }
    try:
        print(f"--- 尝试通过 DecAPI 获取 Twitch: {username} ---")
        response = requests.get(url, headers=headers, timeout=15)
        
        # 这个接口如果成功，直接返回类似 "22" 的纯文本
        if response.status_code == 200:
            res = response.text.strip()
            # 简单校验一下是不是数字
            if res.isdigit() or ("K" in res.upper()) or ("M" in res.upper()):
                print(f"Twitch 抓取成功: {res}")
                return res
        
        print(f"Twitch 接口返回异常: {response.text}")
    except Exception as e:
        print(f"Twitch 接口连接失败: {e}")
    return "Wait_T"

def get_fb_followers(page_id):
    # 你已经成功的 Facebook 逻辑保持不变
    url = f"https://www.facebook.com/plugins/page.php?href=https://www.facebook.com/{page_id}&tabs&small_header=true"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        match = re.search(r'([\d\.,MK]+)\s?(位粉丝|followers|人关注)', response.text)
        if match:
            return match.group(1).replace(',', '')
    except:
        pass
    return "Wait_F"

# --- 主逻辑 ---
if __name__ == "__main__":
    TWITCH_ID = "fattyprophet"
    FB_ID = "100090114814925"

    t_val = get_twitch_followers(TWITCH_ID)
    f_val = get_fb_followers(FB_ID)

    with open("twitch.txt", "w", encoding="utf-8") as f: f.write(t_val)
    with open("fb.txt", "w", encoding="utf-8") as f: f.write(f_val)
    
    print(f"任务结束: Twitch={t_val}, FB={f_val}")
