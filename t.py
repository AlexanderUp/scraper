# encoding:utf-8

import sqlite3

if __name__ == '__main__':
    try:
        conn = sqlite3.connect('p.sqlite3')
        cur = conn.cursor()
    except sqlite3.DatabaseError as err:
        print('Error occured!')
        print(err)
    else:
        print('Connected to db!')
    cur.execute('SELECT content FROM pages')
    pages = cur.fetchall()
    print('Pages:')
    print(pages)
    with open('tales.txt', 'w') as file:
        for page in pages:
            file.write(page[0])
    print('Completed!')
    cur.close()
    conn.close()
    print('DB closed!')
