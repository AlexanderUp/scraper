# encoding:utf-8
# loading articles from url list

from urllib.request import urlopen
from bs4 import BeautifulSoup

import sqlite3
import re
import urllib
import sys


from scr0_add_config import PATH_TO_DB
from scr0_add_config import MASK
from scr0_add_config import DOMAIN_URL


class ArticleHarvester():
    def __init__(self):
        try:
            self.conn = sqlite3.connect(PATH_TO_DB)
        except sqlite3.DatabaseError as err:
            print('The following error occured during connection to database:')
            print(err)
            sys.exit()
        else:
            self.cur = self.conn.cursor()
            print('Successfully connected to database!')
        # checks to be added - e.g. (for example) db is empty
        try:
            self.cur.execute('SELECT url, id FROM urls ORDER BY title ASC')
        except sqlite3.DatabaseError as err:
            print('During initial request to db the following error occured:')
            print(err)
        else:
            self.existed_article_url = {item[0]:item[1] for item in self.cur.fetchall()}
            for article_url in self.existed_article_url.keys():
                print('url: {1:>8}; id: {0}'.format(article_url, self.existed_article_url[article_url]))
        return None

    # can be used as static method - TODO
    # @staticmethod
    def harvest_article(self, start_url):
        url_id = self.existed_article_url[start_url]
        url = start_url
        while True:
            try:
                print('Proceccing: {}'.format(url))
                html = urlopen(url)
            # error handling to be accureted
            except Exception as err:
                print('Error occured diring page openning.')
                print(err)
            else:
                bsObj = BeautifulSoup(html, features='lxml')
                content = bsObj.find('li', {'class':'zero'}).get_text()
                self.cur.execute('INSERT INTO content (url_id, page_url, page_content) VALUES (?, ?, ?)', (url_id, url, content))
                try:
                    next_page_link_candidate = bsObj.find('div', {'class':'pager'}).findAll('a')[-1]
                except Exception as err:
                    print('Error occured during looking for next article page.')
                    print(err)
                else:
                    if next_page_link_candidate.get_text() == chr(187):
                        url = DOMAIN_URL + next_page_link_candidate['href']
                    else:
                        break
        self.conn.commit()
        return None

    def get_articles(self):
        print('Commence harvesting!')
        target_urls = [item for item in self.existed_article_url.keys()]
        print('Target urls: {}'.format(target_urls))
        for url in target_urls:
            self.harvest_article(url)
            print('Processed url: {}'.format(url))
        print('Task completed!')
        self.cur.close()
        self.conn.close()
        print('DB closed!')
        return None


if __name__ == '__main__':
    print('*'*125)
    harvester = ArticleHarvester()
    harvester.get_articles()
    print('Task completed!')
