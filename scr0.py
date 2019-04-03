# encoding:utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup

import sqlite3
import time

from scr0_config.py import DOMAIN_URL
from scr0_config.py import START_URL
from scr0_config.py import TARGET
from scr0_config.py import PATH_TO_DB


def main(start_url=START_URL, domain_url=DOMAIN_URL, path_to_db=PATH_TO_DB):
    try:
        conn = sqlite3.connect(path_to_db)
    except sqlite3.DatabaseError as err:
        print('Error occured!')
        print(err)
    else:
        cur = conn.cursor()
        print('Successfully connected to db!')
    url = START_URL
    existed_article_url = get_existed_article_url(conn, cur)
    while True:
        try:
            next_page_link = parse_search_page(url, domain_url, conn, cur, existed_article_url)
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

def parse_search_page(url, domain_url, conn, cur, existed_article_url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, features="lxml")
    search_target_article(bsObj, conn, cur, existed_article_url, target=TARGET)
    return find_next_page_link(bsObj, domain_url)

def find_next_page_link(bsObj, domain_url):
    if bsObj.find('div', {'class':'pager'}).findAll('a')[-1].get_text() == chr(187):
        return domain_url + bsObj.find('div', {'class':'pager'}).findAll('a')[-1]['href']
    return None

def search_target_article(bsObj, conn, cur, existed_article_url, target=TARGET):
    for link in bsObj.findAll('h2'):
        title = link.get_text()
        print(title)
        if target in title:
            link_to_target = DOMAIN_URL + link.find('a')['href']
            if not check_existence(existed_article_url, link_to_target):
                cur.execute('INSERT INTO urls (url, title) VALUES (?, ?)', (link_to_target, title))
                conn.commit()
    return None

def get_existed_article_url(conn, cur):
    cur.execute('SELECT url FROM urls')
    aux_res = cur.fetchall()
    return [item[0] for item in aux_res]

def check_existence(existed_article_url, article_url):
    # article_url NOT to be added if article_url in existed_article_url
    if article_url in existed_article_url:
        return True
    return False


if __name__ == '__main__':
    print('*' * 125)
    main()
    print('Done!')
