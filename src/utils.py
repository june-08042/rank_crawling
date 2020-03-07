import re
import requests
import time
from selenium import webdriver
import os
import pandas as pd


def get_website_encoding(url, headers):  # 一般每个网站自己的网页编码都是一致的,所以只需要搜索一次主页确定
    res = requests.get(url, headers=headers)
    charset = re.search("charset=(.*?)>", res.text)
    if charset is not None:
        blocked = ['\'', ' ', '\"', '/']
        filter = [c for c in charset.group(1) if c not in blocked]
        return ''.join(filter)  # 修改res编码格式为源网页的格式,防止出现乱码
    else:
        return res.encoding  # 没有找到编码格式,返回res的默认编码


def launch_driver_in_headless_mode():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(executable_path='driver/chromedriver', options=options)
    return driver


def scroll_page(driver):
    try:
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "")
    except:
        pass
    return "Scrolled successfully."


def scroll_to_page_end(driver, element_name, timeToSleep=100):
    before = 0
    after = 0
    n = 0
    while True:
        before = after
        scroll_page(driver)
        time.sleep(3)
        elems = driver.find_elements_by_css_selector(element_name)
        after = len(elems)
        if after > before:
            n = 0
        if after == before:
            n = n + 1
        if n == 5:
            break
        if after > timeToSleep:
            timeToSleep += timeToSleep
            time.sleep(30)


def append_new_results_to_csv(df, filepath, check_duplicates_subset=None):
    if os.path.exists(filepath):
        past_df = pd.read_csv(filepath)
        df = past_df.append(df)
        df = df.drop_duplicates(subset=check_duplicates_subset)
    df.to_csv(filepath, index=False)
    return "Successfully saved."
