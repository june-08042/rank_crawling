from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
import utils


class KgMusicCrawler(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.encoding = utils.get_website_encoding('http://www.kugou.com', self.headers)

    def get_rank_info(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = self.encoding  # 同样读取和写入的编码格式
        a = res.text
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

    def get_singer_list(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = self.encoding
        soup = BeautifulSoup(res.text, 'lxml')

        singer_list1 = [(sg['title'],
                         sg['href'].split('/')[-1].split('.')[0],
                         sg['href']) for sg in soup.find_all('a', 'pic', onclick="sdnClick(12070)")]
        singer_list2 = [(sg.text,
                         sg['href'].split('/')[-1].split('.')[0],
                         sg['href']) for sg in soup.find_all('a', onclick="sdnClick(12071)")]

        return singer_list1 + singer_list2

    def get_rank_500(self):
        urls = ['http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(i)) for i in range(1, 23)]
        rank_500_list = []
        for url in urls:
            rank_500_list += self.get_rank_info(url)
            time.sleep(1) #缓冲一秒,防止请求频率过快
        rank_500_df = pd.DataFrame(data=rank_500_list, columns=['rank', 'singer', 'title', 'time', 'id'])
        return rank_500_df

    def get_rank_ics(self):
        urls = ['http://www.kugou.com/yy/rank/home/{}-6666.html?from=rank'.format(str(i)) for i in range(1, 6)]
        rank_ics_list = []
        for url in urls:
            rank_ics_list += self.get_rank_info(url)
            time.sleep(1)
        rank_ics_df = pd.DataFrame(data=rank_ics_list, columns=['rank', 'singer', 'title', 'time', 'id'])
        return rank_ics_df

    def get_rank_singers(self):
        urls = ['https://www.kugou.com/yy/singer/index/{}-all-1.html'.format(str(i)) for i in range(1, 6)]
        single_list = []
        for url in urls:
            single_list += self.get_singer_list(url)
            time.sleep(1)
        singer_df = pd.DataFrame(data=single_list, columns=['name', 'href', 'id'])
        return singer_df

    def get_singer_info(self):
        # TODO: Singer info is not available in web version.
        #  Have to use app to find the api for getting the number of followers.
        #  Cannot login to the app using overseas IP.
        #  Will need to get others' help on that.
        pass

    def get_song_info(self):
        # TODO: Same as singer info.
        pass


if __name__ == '__main__':
    kmc = KgMusicCrawler()
    kmc.get_rank_500()
    kmc.get_rank_ics()
    kmc.get_rank_singers()
