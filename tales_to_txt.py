# encoding:utf-8
# extract content from sqlite3 database and write to txt file

import sqlite3

from tales_to_txt_config import PATH_TO_DB

class ContentExtractor():
    def __init__(self):
        try:
            self.conn = sqlite3.connect(PATH_TO_DB)
        except sqlite3.DatabaseError as err:
            print('The following error occured:')
            print(err)
        else:
            self.cur = self.conn.cursor()
            print('Successfully connected to database!')
        return None

    def get_url_ids(self):
        self.cur.execute('SELECT id FROM urls')
        self.url_ids = [item[0] for item in self.cur.fetchall()]
        return None

    def extract_content(self):
        for id in self.url_ids:
            self.cur.execute('SELECT title FROM urls WHERE id=?', (str(id),))
            title = self.cur.fetchone()[0]
            print('Now processing: {}'.format(title))
            self.cur.execute('SELECT page_content FROM content WHERE url_id=? ORDER BY id ASC', (str(id),))
            with open('{}.txt'.format(title[31:]), 'w') as file:
                for page in self.cur.fetchall():
                    file.write(page[0])
        print('Task completed!')
        self.cur.close()
        self.conn.close()
        print('Database closed!')
        return None


if __name__ == '__main__':
    print('*'*125)
    extractor = ContentExtractor()
    extractor.get_url_ids()
    extractor.extract_content()
