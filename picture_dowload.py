import requests
from bs4 import BeautifulSoup
import os

def download_images_from_webpage(url, save_directory):
    try:
        # 添加请求头部信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        # 发送 HTTP 请求获取网页内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查是否有请求错误

        # 使用 BeautifulSoup 解析网页内容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到所有图片标签
        img_tags = soup.find_all('img')

        # 下载每个图片
        for index, img_tag in enumerate(img_tags):
            img_url = img_tag.get('src')  # 获取图片链接
            if img_url:
                # 发送 HTTP 请求下载图片
                img_response = requests.get(img_url, headers=headers)
                img_response.raise_for_status()  # 检查是否有请求错误

                # 将图片保存到文件
                with open(f"{save_directory}/image_{index}.jpg", "wb") as f:
                    f.write(img_response.content)

                print(f"图片{index}已成功下载")
            else:
                print(f"图片{index}没有找到有效的链接")

    except Exception as e:
        print(f"下载图片时出错：{e}")

# 示例URL和保存目录
url = "https://zhuanlan.zhihu.com/p/392297136"
save_directory = "./images_from_webpage"

# 确保保存目录存在
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 下载图片
download_images_from_webpage(url, save_directory)

