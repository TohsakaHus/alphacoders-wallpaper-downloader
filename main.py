import os
import json
import requests
from pyquery import PyQuery as pq

with open('config.json', 'r') as file_obj:
    config = file_obj.read()
    config = json.loads(config)
    tag_id = str(config['tag_id'])
    max_page = int(config['max_page'])
    api_key = str(config['api_key'])
    min_width = int(config['min_width'])

url = 'https://wall.alphacoders.com/tags.php?tid=' + str(tag_id)
html = pq(url=url)
dir_name = html('span.breadcrumb-element').text()
dir_name = "".join(i for i in dir_name if i.isalnum())
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)

for i in range(1, max_page + 1):
    info = requests.get('https://wall.alphacoders.com/api2.0/get.php?auth=%s&method=tag&id=%s&page=%d&sort=views' % 
                        (api_key, tag_id, i))
    info = json.loads(info.text)

    if info['success']:
        if len(info['wallpapers']) == 0:
            print('已无更多图片')
            break

        for j in range(len(info['wallpapers'])):
            pic_info = info['wallpapers'][j]

            # 若当前图片小于设定的min_width，则直接下一张
            if int(pic_info['width']) < min_width:
                continue

            file_name = pic_info['id'] + '.' + pic_info['file_type']
            if os.path.exists(file_name):
                continue

            pic = requests.get(pic_info['url_image'])
            with open(file_name, 'wb') as file_obj:
                file_obj.write(pic.content)

        print('第 %d 页下载完成' % i)

