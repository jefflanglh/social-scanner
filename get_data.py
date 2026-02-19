import requests
import os

def save_data(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(content))

# --- 尝试抓取数据 ---
def fetch_all():
    # 1. Instagram 保底逻辑
    insta_val = "511.5M" 
    try:
        # 你之前的抓取代码... (这里简化，确保先成功)
        pass 
    except:
        pass
    save_data("insta.txt", insta_val)

    # 2. Facebook 暴力保底逻辑
    fb_val = "120M" # 先给个假数字测试链路
    try:
        # 尝试访问一个不需要复杂验证的镜像或直接模拟
        # 暂时先用保底数字，确保 fb.txt 能出现在仓库里
        pass
    except:
        pass
    save_data("fb.txt", fb_val)

    print(f"Done! Insta: {insta_val}, FB: {fb_val}")

if __name__ == "__main__":
    fetch_all()
