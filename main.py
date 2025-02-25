import os
import json
import requests
from pyquery import PyQuery as pq

def fetch(api_key, tag_id, min_width, i):
    info = requests.get('https://wall.alphacoders.com/api2.0/get.php?auth=%s&method=tag&id=%s&page=%d&sort=views' % 
                        (api_key, tag_id, i))
    info = json.loads(info.text)

    if info['success']:
        if len(info['wallpapers']) == 0:
            print('已无更多图片')
            return False

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
        return True

# Read Config
with open('config.json', 'r') as file_obj:
    config = file_obj.read()
    config = json.loads(config)
    tag_id = str(config['tag_id'])
    api_key = str(config['api_key'])
    try:
        max_page = int(config['max_page'])
    except:
        max_page = 0
    try:
        min_width = int(config['min_width'])
    except:
        min_width = 0
# Main
url = 'https://wall.alphacoders.com/tags.php?tid=' + str(tag_id)
html = pq(url=url)
dir_name = html('span.breadcrumb-element').text()
dir_name = "".join(i for i in dir_name if i.isalnum())
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)

if max_page != 0:
    for i in range(1, max_page + 1):
        status = fetch(api_key, tag_id, min_width, i)
        if status == False:
            break
else:
    i = 1
    while True:
        status = fetch(api_key, tag_id, min_width, i)
        if status == False:
            break
        i += 1
        
    

