# encoding:utf-8
# loading articles from url list

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
import sys


from scr0_add_config import PATH_TO_DB


class ArticleLoader():
    def __init__():
        try:
            conn = sqlite3.connect(PATH_TO_DB)
        except sqlite3.DatabaseError as err:
            print('The following error occured during connection to database:')
            print(err)
            sys.exit()
        else:
            cur = conn.cursor()
            print('Successfully connected to database!')
        cur.execute('SELECT url FROM urls ORDER BY title ASC')
        self.existed_article_url = [item[0] for item in cur.fetchall()]
        return None

    def load_article(url):
        html = urlopen(url)
        bsObj = BeautifulSoup(html, features='lxml')



if __name__ == '__main__':
    print('8'*125)
