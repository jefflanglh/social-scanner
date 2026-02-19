import os

# 强制创建两个文件
with open("insta.txt", "w") as f:
    f.write("511.5M")

with open("fb.txt", "w") as f:
    f.write("120M")

print("Files created successfully!")
