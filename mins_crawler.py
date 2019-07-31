from weibo import WeiboCrawler


def crawl_weibo_mins():
    wc = WeiboCrawler()
    wc.extract_hcy_num_fans_to_csv()
    wc.extract_super_topic_data_to_csv()
    wc.quit_driver()
    return 1


if __name__ == '__main__':
    crawl_weibo_mins()