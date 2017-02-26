import time
from multiprocessing import Pool
from jiandan import get_image_url, download_image
from pymongo import MongoClient



seed_url = 'http://jandan.net/ooxx/page-'

def get_all_links(url):
    get_image_url(url)
    time.sleep(2)


if __name__ == '__main__':
    pool = Pool(processes=6)
    links = [seed_url + str(i) for i in range(1, 1888)]
    pool.map(get_all_links, links)
    client = MongoClient('localhost', 27017, connect=False)
    jiandan = client['jiandan']
    url_list = jiandan['url_list']
    URLS = list(map(lambda x: x['url'], url_list.find()))
    pool.map(download_image, URLS)
    pool.close()
