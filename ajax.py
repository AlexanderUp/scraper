# encoding:utf-8

# today selenium deprecated PhantomJS support. Use insteed it headless FireFox.
from selenium import webdriver
import time


if __name__ == '__main__':
    driver = webdriver.PhantomJS(executable_path='')
    driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
    time.sleep(3)
    print(driver.find_element_by_id('content').text)
    driver.close()
