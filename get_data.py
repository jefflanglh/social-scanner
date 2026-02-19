import requests
import os

def save_data(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(content))
        print(f"Successfully saved {filename}")
    except Exception as e:
        print(f"Failed to save {filename}: {e}")

def fetch_all():
    # --- Instagram 部分 ---
    insta_val = "511.5M" # 默认值
    # 这里可以放你之前的抓取逻辑...
    save_data("insta.txt", insta_val)

    # --- Facebook 暴力测试部分 ---
    # 我们先不抓取真实网页，先强行生成文件测试链路
    fb_val = "120M" 
    save_data("fb.txt", fb_val)

    print(f"All tasks done. Insta: {insta_val}, FB: {fb_val}")

if __name__ == "__main__":
    fetch_all()
