# encoding:utf-8
# create list of article's url meeting target creteria (contains TARGET in title)

from urllib.request import urlopen
from bs4 import BeautifulSoup

import sqlite3
import time

from scr0_config.py import DOMAIN_URL
from scr0_config.py import START_URL
from scr0_config.py import TARGET
from scr0_config.py import PATH_TO_DB


class TargetUrlHarvester():
    def __init__(self):
        try:
            self.conn = sqlite3.connect(PATH_TO_DB)
        except sqlite3.DatabaseError as err:
            print('Error occured!')
            print(err)
        else:
            self.cur = self.conn.cursor()
            print('Successfully connected to db!')
            self.existed_article_url = self.get_existed_article_url()
        return None


    def get_existed_article_url(self):
        # what if table in database is empty? - todo
        self.cur.execute('SELECT url FROM urls')
        return [item[0] for item in self.cur.fetchall()]

    def check_existence(self, article_url):
        # article_url NOT to be added if article_url in existed_article_url
        if article_url in self.existed_article_url:
            return True
        return False

    def parse_search_page(self, url):
        html = urlopen(url)
        bsObj = BeautifulSoup(html, features="lxml")
        self.search_target_article(bsObj)
        return self.find_next_page_link(bsObj)

    def search_target_article(self, bsObj):
        for link in bsObj.findAll('h2'):
            title = link.get_text()
            print(title)
            if TARGET in title:
                link_to_target = DOMAIN_URL + link.find('a')['href']
                if not self.check_existence(link_to_target):
                    self.cur.execute('INSERT INTO urls (url, title) VALUES (?, ?)', (link_to_target, title))
                    self.conn.commit()
        return None

    def find_next_page_link(self, bsObj):
        if bsObj.find('div', {'class':'pager'}).findAll('a')[-1].get_text() == chr(187):
            return DOMAIN_URL + bsObj.find('div', {'class':'pager'}).findAll('a')[-1]['href']
        return None

    def harvest_target_url(self):
        url = START_URL
        while True:
            try:
                next_page_link = self.parse_search_page(url)
            except Exception as err:
                print('Error occured!')
                print(err)
                cur.close()
                conn.close()
                break
            else:
                print('Page processed: {}'.format(url))
            if next_page_link is None:
                break
            url = next_page_link
            time.sleep(0.5)
        cur.close()
        conn.close()
        return None


if __name__ == '__main__':
    print('*' * 125)

    print('Done!')
