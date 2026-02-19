def get_twitch_followers(username):
    # 使用 Twitch 的移动端页面，数据更易提取
    url = f"https://m.twitch.tv/{username}/home"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # Twitch 移动版源码中通常包含 "followerCount":123
        match = re.search(r'"followerCount":(\d+)', response.text)
        if match:
            return match.group(1)
        # 备选正则
        match_alt = re.search(r'([\d\.,MK]+)\s?followers', response.text, re.I)
        if match_alt:
            return match_alt.group(1).replace(',', '')
    except:
        pass
    return "Wait"

# 在主循环里加入
twitch_val = get_twitch_followers("fattyprophet")
with open("twitch.txt", "w") as f:
    f.write(twitch_val)
