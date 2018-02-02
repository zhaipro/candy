# coding: utf-8
import sys
import time

import requests
from splinter import Browser
from selenium.webdriver import ActionChains

import utils
from settings import PASSWORD, ADDRESS


def _login(phone, password):
    '''
    登录指定账号，并返回cookies
    '''
    utils.log('login: %s', phone)
    with Browser(headless=True) as browser:
        browser.cookies.delete()
        url = 'https://candy.one/user/login'
        browser.visit(url)
        browser.fill('phone', phone)
        browser.find_by_css('.candy-btn').click()

        time.sleep(1)
        driver = browser.driver
        fuck = driver.find_element_by_id('nc_1_n1z')
        action = ActionChains(driver)
        action.click_and_hold(fuck)
        action.move_by_offset(550, 0)
        action.release().perform()

        time.sleep(1)
        utils.log(browser.url)
        browser.fill('password', password)
        browser.find_by_css('.candy-btn').click()

        time.sleep(1)
        utils.log(browser.url)
        return browser.cookies.all()


def login(phone, password=PASSWORD):
    '''
    登录指定账号，并返回requests.Session对象
    '''
    cookies = _login(phone, password)
    s = requests.Session()
    headers = {
        'Referer': 'https://candy.one/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0',
        'x-access-token': cookies['_candy_token'],
    }
    s.headers.update(headers)
    s.cookies.update(cookies)
    return s


def get_balance(session):
    response = session.get('https://candy.one/api/user/balance')
    utils.log(response.text)
    return response.json()['data']['balance']


def withdraw(session, address=ADDRESS):
    '''
    提取全部余额到指定BigOne账户
    '''
    balance = get_balance(session)
    if balance <= 0:
        return
    url = 'https://candy.one/api/transaction/withdraw'
    data = {
        'amount': balance,
        'recipient_id': address,
    }
    utils.post(session, url, data)


if __name__ == '__main__':
    for phone in sys.stdin:
        try:
            phone = phone.strip()
            session = login(phone)
            withdraw(session)
        except Exception, e:
            utils.log('Error: %s', e)
