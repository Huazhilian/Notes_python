import requests
import os
from urllib.parse import urlparse

urls = [
    "https://www.runoob.com/python-qt/qt-step1.html",
    "https://www.runoob.com/numpy/numpy-matplotlib.html",
    "https://www.runoob.com/python3/python3-multithreading.html"
]

# 创建保存目录
save_dir = "web_pages"
os.makedirs(save_dir, exist_ok=True)

for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        # 从URL生成安全文件名
        parsed_url = urlparse(url)
        filename = f"{parsed_url.netloc}{parsed_url.path.replace('/', '_')}.html"
        filepath = os.path.join(save_dir, filename)
        
        # 写入文件（UTF-8编码）
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Saved: {filepath}")
    
    except Exception as e:
        print(f"Failed to save {url}: {str(e)}")