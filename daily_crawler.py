from qq_music import QQMusicCrawler
from weibo import WeiboCrawler
import pandas as pd


def crawl_qq_music():
    date = pd.to_datetime('today').strftime('%Y-%m-%d')
    qmc = QQMusicCrawler(date)
    qmc.extract_ranks_to_csv()
    qmc.extract_singer_list_to_csv()
    return 1


def crawl_weibo_st_details():
    wc = WeiboCrawler()
    # wc.login_weibo()
    # df = wc.get_rank_super_topic_id()
    # df.to_csv('rank_st_id.csv', index=False)
    wc.extract_rank_super_topic_details_to_csv()
    wc.quit_driver()


if __name__ == '__main__':
    crawl_qq_music()
    crawl_weibo_st_details()

