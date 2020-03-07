from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
import utils
import json


class XmMusicCrawler(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        self.encoding = utils.get_website_encoding('http://www.xiami.com', self.headers)

    def get_rank_info(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = self.encoding  # 同样读取和写入的编码格式
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

    def get_singer_list(self):
        with open('xm_artist_list.txt') as f:
            hot_singers_data = json.load(f)
        singer_list = hot_singers_data['result']['data']['hotArtists']
        singer_list_df = pd.DataFrame(singer_list)
        return singer_list_df

    def get_rank_new(self):
        url = 'https://www.xiami.com/billboard/102'

    def get_rank_hot(self):
        url = 'https://www.xiami.com/billboard/103'

    def get_rank_org(self):
        url = 'https://www.xiami.com/billboard/104'


    def get_song_list(self):

        url = 'https://www.xiami.com/api/song/getArtistSongs?_q=%7B%22pagingVO%22:%7B%22page%22:1,%22pageSize%22:60%7D,%22artistId%22:%223110%22%7D&_s=5fd21c611b8c8f750b1fc9d4d25278fb'

    def get_singer_info(self):
        # TODO: Song info is not available in web version.
        #  Have to use app to find the api for getting the number of followers.
        #  Cannot login to the app using overseas IP.
        #  Will need to get others' help on that.
        pass

    def get_song_info(self):
        # TODO: Same as singer info.
        pass


if __name__ == '__main__':
    xmc = XmMusicCrawler()
    singer_df = xmc.get_hot_singers()
    # kmc.get_rank_ics()
    # kmc.get_rank_singers()
