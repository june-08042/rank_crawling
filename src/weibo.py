import time
import pandas as pd
import utils
import random
import os
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver.common.keys import Keys

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)
username = os.environ.get("WB_USERNAME")
password = os.environ.get("WB_PASSWORD")


class WeiboCrawler(object):

    def __init__(self):
        self.driver = utils.launch_driver_in_headless_mode()
        self.dt = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M')

    def get_user_num_fans(self, id):
        url = 'https://m.weibo.cn/p/{}'.format(id)
        self.driver.get(url)
        time.sleep(3 + random.random())
        nk_name = self.driver.find_element_by_css_selector('span.txt-shadow').text
        elems = self.driver.find_elements_by_css_selector('div.txt-shadow')
        num_fans = int(elems[1].text[2:])
        return nk_name, num_fans

    def extract_hcy_num_fans_to_csv(self):
        nk_name, num_fans = self.get_user_num_fans('1005051624923463')
        hcy_fans = pd.DataFrame({'nickname': [nk_name], 'num_fans': [num_fans], 'datetime': self.dt})
        hcy_fans_cvs_filepath = 'weibo_results/hcy_fans.csv'
        utils.append_new_results_to_csv(hcy_fans, hcy_fans_cvs_filepath)
        return 'Number of fans of {}: {} has been saved to csv files. '.format(nk_name, num_fans)

    def login_weibo(self):
        self.driver.get("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F")
        time.sleep(3)
        # 登陆
        elem = self.driver.find_element_by_xpath("//*[@id='loginName']");
        elem.send_keys(username)
        elem = self.driver.find_element_by_xpath("//*[@id='loginPassword']");
        elem.send_keys(password)
        elem = self.driver.find_element_by_xpath("//*[@id='loginAction']");
        elem.send_keys(Keys.ENTER)
        time.sleep(7 + random.random() * 3)
        return 1

    def get_rank_super_topic_id(self):
        rank_url = 'https://huati.weibo.cn/discovery/super?extparam=ctg1_2%7Cscorll_1&luicode=10000011&lfid=100803_-_super#'
        rank_st_id_list = []

        for i in range(100)[81:]:
            rank = i + 1
            self.driver.get(rank_url)
            time.sleep(5 + random.random() * 3)

            names = self.driver.find_elements_by_css_selector('em.super_name')

            while len(names) < rank:
                self.driver.execute_script("arguments[0].scrollIntoView();", names[-1])
                time.sleep(5 + random.random() * 3)
                names = self.driver.find_elements_by_css_selector('em.super_name')

            name = names[i]
            name_text = name.text
            self.driver.execute_script("arguments[0].click();", name)
            time.sleep(4 + random.random() * 4)
            url = self.driver.current_url
            id = url.split('/')[-2]
            print(name_text, rank, id)
            rank_st_id_list.append([name_text, rank, id])
        rank_st_id_df = pd.DataFrame(rank_st_id_list)
        return rank_st_id_df

    def get_super_topic_detail(self, st_id):
        st_url = 'https://m.weibo.cn/p/index?containerid={}&luicode=10000011&lfid=100103type%3D1%26q%3D'.format(st_id)
        self.driver.get(st_url)
        time.sleep(5 + random.random() * 3)
        detail_str = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div[4]/div/div/div/a/div[2]/h4[1]').text
        return detail_str

    def get_rank_super_topic_details(self):
        st_id_df = pd.read_csv('st_id.csv')
        st_details_list = []
        for name, id in zip(st_id_df['name'], st_id_df['id']):
            detail_str = self.get_super_topic_detail(id)
            st_details_list.append([name, id, detail_str])
        st_details_df = pd.DataFrame(st_details_list, columns=['name', 'id', 'details'])
        st_details_df['reads'] = st_details_df['details'].apply(lambda x: float(x.split()[0][2:-1]) * 10000)
        st_details_df['posts'] = st_details_df['details'].apply(lambda x: float(x.split()[1][2:-1]) * 10000)
        st_details_df['fans'] = st_details_df['details'].apply(lambda x: float(x.split()[2][2:-1]) * 10000)
        st_details_df['date'] = self.dt
        return st_details_df

    def extract_rank_super_topic_details_to_csv(self):
        cur_st = self.get_rank_super_topic_details()
        super_topic_details_cvs_file = 'weibo_results/super_topic_details.csv'
        utils.append_new_results_to_csv(cur_st, super_topic_details_cvs_file)
        return 1

    def get_rank_super_topic(self):
        url = 'https://huati.weibo.cn/discovery/super?extparam=ctg1_2%7Cscorll_1&luicode=10000011&lfid=100803_-_super#'
        self.driver.get(url)
        num_elems = 0
        while num_elems < 101:
            print('Number of super topic presented: {}, scroll down.'.format(num_elems))
            elems = self.driver.find_elements_by_css_selector('div.card-list')
            self.driver.execute_script("arguments[0].scrollIntoView();", elems[-1])
            num_elems = len(elems)
            time.sleep(5)
        rank_st_list = []

        for elem in elems[:100]:
            text = ''
            for a in elem.text:
                text += a
            text_list = text.split('\n')
            topic_info = dict(
                rank = text_list[0][3:],
                name = text_list[1],
                infn = text_list[2].split()[0][:-3],
                fans = text_list[2].split()[1][:-2],
                time = self.dt)
            rank_st_list.append(topic_info)
        rank_st_df = pd.DataFrame(rank_st_list)
        return rank_st_df

    def extract_super_topic_data_to_csv(self):
        cur_st = self.get_rank_super_topic()
        super_topic_cvs_file = 'weibo_results/super_topic.csv'
        utils.append_new_results_to_csv(cur_st, super_topic_cvs_file)
        return 1

    def quit_driver(self):
        self.driver.quit()
        return 1


if __name__ == '__main__':
    wc = WeiboCrawler()
    # wc.login_weibo()
    # df = wc.get_rank_super_topic_id()
    # df.to_csv('rank_st_id.csv', index=False)
    wc.extract_rank_super_topic_details_to_csv()
    wc.quit_driver()
