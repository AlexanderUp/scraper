# encoding:utf-8

import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth


if __name__ == '__main__':
    # params = {'firstname':'R', 'lastname':'M'}
    # r = requests.post('http://pythonscraping.com/files/processing.php', data=params)
    # print(r.text)
    # ##########################################################################
    params = {'username':'Ryan', 'password':'password'}
    # r = requests.post('http://pythonscraping.com/pages/cookies/welcome.php', params)
    # print('Cookies is set to:')
    # print(r.cookies.get_dict())
    # print('-------------------')
    # print('Going to profile page...')
    # r = requests.get('http://pythonscraping.com/pages/cookies/profile.php', cookies=r.cookies)
    # print(r.text)
    # ##########################################################################
    # session = requests.Session()
    # s = session.post('http://pythonscraping.com/pages/cookies/welcome.php', params)
    # print('Cookie is set to:')
    # print(s.cookies.get_dict())
    # print('-------------------')
    # print('Going to profile page...')
    # s =  session.get('http://pythonscraping.com/pages/cookies/profile.php')
    # print(s.text)
    # ##########################################################################
    auth = HTTPBasicAuth('ryan', 'password')
    r = requests.post(url='http://pythonscraping.com/pages/auth/login.php', auth=auth)
    print(r.text)
