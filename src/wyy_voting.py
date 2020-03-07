from selenium import webdriver
from datetime import datetime
import time
import urllib.request, urllib.error, urllib.parse
import requests
import json

cur_time_str = datetime.now().strftime("%m%d%Y_%H%M%S")
rank_class_list = ['male_artist', 'super_idol', 'popular_single']

screenshot_url = 'https://music.163.com/m/at/Yearendvoting2019'
brower = webdriver.Chrome('/home/yajing/PycharmProjects/rank_crawling_dev/driver/chromedriver')
brower.get(screenshot_url)

brower.maximize_window()

elem_path_list = ['/html/body/div[1]/div/div[3]/div[6]/img', '/html/body/div[1]/div/div[21]/div/img', '/html/body/div[1]/div/div[45]/div/img']
for rank_class, elem_path in zip(rank_class_list, elem_path_list):
    element = brower.find_element_by_xpath(elem_path)
    brower.execute_script("arguments[0].scrollIntoView();", element)
    brower.save_screenshot(f'/home/yajing/PycharmProjects/rank_crawling_dev/wyy_voting/{rank_class}_{cur_time_str}.png')

brower.close()

detail_url_list = [
    'https://interface.music.163.com/api/act/modules/work/page?status=0&pageSize=10&name=Yearendvoting2019&moduleName=ChineseMaleArtist&pageNo=1',
    'https://interface.music.163.com/api/act/modules/work/page?status=0&pageSize=20&name=Yearendvoting2019&moduleName=SuperIdol&pageNo=1',
    'https://interface.music.163.com/api/act/modules/work/page?status=0&pageSize=15&name=Yearendvoting2019&moduleName=HitSong&pageNo=1'
]
for rank_class, detail_url in zip(rank_class_list, detail_url_list):
    res = requests.get(detail_url)

    res.encoding = 'utf-8'
    data = json.loads(res.text, encoding=res.encoding)

    f = open(f'/home/yajing/PycharmProjects/rank_crawling_dev/wyy_voting/{rank_class}_{cur_time_str}.json', 'w')
    json.dump(data, f)
    f.close()
    time.sleep(2)


