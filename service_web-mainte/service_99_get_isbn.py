import sys
import os
import csv
import chromedriver_binary
import mojimoji
import requests
import time
from admin_app.service.service_main import ServiceMain
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from django.conf import settings

LOGIN_URL = 'https://www.win-plus.jp/'
SEARCH_TOP_URL = 'https://www.win-plus.jp/sites/gateway/top'
SESSION_NAME = '_session_id'


class GetIsbnService(ServiceMain):

    def getIsbn(self, book_name):
        print('検索対象：' + book_name)
        result = self.get_data(book_name)
        return result

    def get_data(self, ip_name):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(options=options)

        session_id = self.read_session_id()
        browser.get(SEARCH_TOP_URL)
        browser.delete_cookie('_session_id')  # すでにログインしていても、再度ページを開くと別のセッションIDが振られるため、削除して前回のセッションIDに上書きする
        browser.add_cookie({
            'name': SESSION_NAME,
            'value': session_id,
            'domain': 'www.win-plus.jp'})
        browser.get(SEARCH_TOP_URL)
        cookies = browser.get_cookies()
        time.sleep(1)

        try:
            if browser.current_url == LOGIN_URL:
                browser = self.login_on_browser(browser, "BDNWIN0001", "51qW5d3yf2")
            isbn_list = []
            book_title = mojimoji.han_to_zen(ip_name)
            browser = self.search_on_browser(browser, book_title)
            browser, isbn_list = self.get_isbn_on_browser(browser, isbn_list)
            if isbn_list == [] : raise BaseException('結果0件')
        except:
            print('取得なし')
        finally:
            return isbn_list
            browser.quit()

    def login_on_browser(self, browser, ID, PASSWORD):
        username = browser.find_element_by_name('username')
        username.send_keys("BDNWIN0001")
        password = browser.find_element_by_name('password')
        password.send_keys("51qW5d3yf2")
        browser.find_element_by_xpath('/html/body/div/div/form/div[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td[2]/input').click()  # ログインボタン押下

        cookies = browser.get_cookies()
        for tmp in cookies:
            if tmp['name'] == SESSION_NAME :
                session_id = tmp['value']

        self.write_session_id(session_id)
        return browser

    def search_on_browser(self, browser, book_title):
        time.sleep(1)
        title_input = browser.find_element_by_xpath('//*[@id="searchmeigara_meigara_mei"]')  # 銘柄名(全角)
        title_input.send_keys(book_title)
        browser.find_element_by_xpath('/html/body/div/div/div/table/tbody/tr/td[1]/div/form/ol[4]/li/input').click()  # 検索ボタン
        return browser

    def get_isbn_on_browser(self, browser, isbn_list):
        next_button = True
        while next_button:
            soup = Bs(browser.page_source, 'lxml')
            table_tag = soup.find(id='searchResultTarget')
            if table_tag is None:
                browser.get(SEARCH_TOP_URL)
                return browser, isbn_list
            else:
                tr_tags = table_tag.select('#searchResultTarget > div > div:nth-child(4) > table > tbody > tr')

            for tr_tag in tr_tags[1:]:
                td_tags = tr_tag.find_all('td')
                isbn = td_tags[2].find('a').text
                title = td_tags[3].text
                release_date = td_tags[7].text
#                 print('ISBN:{}/書籍名:{}/発行年月日:{}'.format(isbn, title, release_date))
                isbn_list.append([str(isbn), title, release_date])

            browser, next_button = self.check_next_page_on_browser(browser, soup)

        browser.get(SEARCH_TOP_URL)
        return browser, isbn_list

    def check_next_page_on_browser(self, browser, soup):
        a_tag = soup.select_one('#searchResultTarget > div > div:nth-child(4) > ul > li:nth-child(2) > div > a.next_page')
        if a_tag is not None:
            class_name = a_tag.get('class')[0]
        else:
            class_name = 'not next page'

        if class_name == 'next_page':
            next_button = True
            browser.find_element_by_class_name('next_page').click()
            time.sleep(3)
        else:
            next_button = False

        return browser, next_button

    def read_session_id(self):
        path = settings.MEDIA_ROOT + '/win_plus/session_id.txt'
        with open(path, 'r') as f:
            session_id = f.readline()
            return session_id

    def write_session_id(self, session_id):
        path = settings.MEDIA_ROOT + '/win_plus/session_id.txt'
        with open(path, 'w') as f:
            f.write(session_id)
