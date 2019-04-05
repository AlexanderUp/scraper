# encoding:utf-8
# scraper for p_tales


from urllib.request import urlopen
from bs4 import BeautifulSoup

import sqlite3
import re
import urllib

from scr_p_config import DB_PATH
from scr_p_config import START_URL
from scr_p_config import MASK


def connect_to_db(path_to_db=DB_PATH):
    try:
        conn = sqlite3.connect(path_to_db)
        cur = conn.cursor()
    except sqlite3.DatabaseError as err:
        print('During connection to database the following error ocurred:')
        print(err)
    else:
        print('Successfully connected to database!')
    return (conn, cur)

def get_title(bsObj):
    return bsObj.find('meta', {'name':'description'})['content']

def get_title2(bsObj, mask=MASK):
    title2 = bsObj.find('head').find('title').get_text()
    title2 = title2[:title2.index(mask)]
    return title2

def get_host_name(start_url=START_URL):
    start_url = start_url.split('//')[1]
    return start_url.split('/')[0]

def get_next_page_url(base_url, bsObj):
    try:
        link_found = bsObj.find('link', {'rel':'next'})['href']
    except Exception as err:
        print('Error in get_next_page_url')
        print(err)
    else:
        if isinstance(link_found, str):
            return 'http://' + base_url + link_found
    return None

def get_content(bsObj):
    return bsObj.find('li', {'class':'zero'}).get_text()

def get_date_written(bsObj):
    pass

def parse_page(url, conn, cur):
    html = urlopen(url)
    bsObj = BeautifulSoup(html, features="lxml")
    host_name = get_host_name()
    title = get_title(bsObj)
    title2 = get_title2(bsObj)
    next_page_link = get_next_page_url(host_name, bsObj)
    content = get_content(bsObj)
    print('****** Next page: {}'.format(next_page_link))
    store(conn, cur, url, title2, content)
    if next_page_link is not None:
        parse_page(next_page_link, conn, cur)
    return None

def store(conn, cur, url, title2, content):
    try:
        cur.execute('INSERT INTO pages (url, name, content, time_written) VALUES (?, ?, ?, ?)',
        (url, title2, content, 'unknown'))
    except sqlite3.DatabaseError as err:
        print('Database Error')
        print(err)
    else:
        print('URL written!')
        print(url)
    return None

def main(url):
    conn, cur = connect_to_db()
    try:
        parse_page(url, conn, cur)
    except Exception as err:
        print('General error')
        print(err)
    else:
        print('Successful!')
    finally:
        conn.commit()
        cur.close()
        conn.close()
    return None


if __name__ == '__main__':
    print('*'*125)
    main(START_URL)
