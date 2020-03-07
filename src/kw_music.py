import requests
from bs4 import BeautifulSoup
from lxml import etree


def get_rank_info(url, encoding):
    res = requests.get(url, headers=headers)
    res.encoding = encoding  # 同样读取和写入的编码格式
    soup = BeautifulSoup(res.text, 'lxml')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('a.pc_temp_songname')
    times = soup.select('span.pc_temp_time')
    ids = [song['href'].split('/')[-1].split('.')[0] for song in soup.find_all('a', 'pc_temp_songname')]
    song_list = [(rank.get_text().strip(),
                  title.get_text().strip().split('-')[0].strip(),
                  title.get_text().strip().split('-')[1].strip(),
                  time.get_text().strip(),
                  song_id) for rank, title, time, song_id in zip(ranks, titles, times, ids)]
    return song_list




headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
responce = requests.get("http://www.kuwo.cn/bang/index", headers=headers)

soup = BeautifulSoup(responce.text, 'html.parser')
html = etree.HTML(responce.text)

