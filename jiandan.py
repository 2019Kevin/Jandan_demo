#爬取jiandan妹子部分图片,并保存到本地文件中

import requests
import os
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017, connect=False)
jiandan = client['jiandan']
url_list = jiandan['url_list']

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

# 此网站会有针对 ip 的反爬取，可以采用代理的方式
#proxies = {"http": "http://121.69.29.162:8118"}

def get_image_url(url):
    #获取每个页面的图片链接
    wb_data = requests.get(url, headers = headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    images = soup.select('div.text > p > img')
    image_urls = set()
    for image in images:
        im_url = image.get('src')
        if not im_url.startswith('https:') and not im_url.startswith('http:'):
            im_url = 'https:' + im_url
        image_urls.add(im_url)
        url_list.insert_one({'url': im_url})
        print(im_url)


def download_image(url):
    # 下载图片并保存到本地文件目录中
    os.makedirs('jiandan', exist_ok=True)
    try:
        wb_data = requests.get(url, headers=headers)
    except Exception:
        print('此地址的图片链接已经失效！')
    else:
        imageFile = open(os.path.join('jiandan', os.path.basename(url)), 'wb')
        for chunk in wb_data.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

