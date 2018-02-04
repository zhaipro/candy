# coding: utf-8
import sys
import time

import requests
from splinter import Browser
from selenium.webdriver import ActionChains

import utils
from settings import PASSWORD, ADDRESS, ENROLL_ID, PROCESS


def _login(browser, phone):
    '''
    登录指定账号
    '''
    utils.log('login: %s', phone)
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


def gen_session(cookies):
    s = requests.Session()
    headers = {
        'Referer': 'https://candy.one/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0',
    }
    s.headers.update(headers)
    s.cookies.update(cookies)
    if '_candy_token' in cookies:
        s.headers['x-access-token'] = cookies['_candy_token']
    return s


def password_login(phone, password=PASSWORD):
    '''
    登录指定账号，并返回requests.Session对象
    '''
    with Browser(headless=True) as browser:
        _login(browser, phone)
        browser.fill('password', password)
        browser.find_by_css('.candy-btn').click()

        time.sleep(1)
        utils.log(browser.url)
        cookies = browser.cookies.all()
        return gen_session(cookies)


def register(phone):
    '''
    注册指定账号，并返回cookies
    '''
    with utils.Lock(PROCESS):
        with Browser(headless=True) as browser:
            _login(browser, phone)
            cookies = browser.cookies.all()
            return gen_session(cookies)


def get_balance(session):
    url = 'https://candy.one/api/user/balance'
    r = utils.get(session, url)
    return r.json()['data']['balance']


def is_register(phone):
    url = 'https://candy.one/api/user/is_register'
    data = {
        'country_code': 'cn',
        'phone': '+86' + phone,
    }
    r = utils.post(requests, url, data)
    data = r.json()['data']
    return data['registed']     # data['hasPas']


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


def set_password(session, phone):
    url = 'https://candy.one/api/passport/set-password'
    data = {
        'country_code': 'cn',
        'password': PASSWORD,
        'password2': PASSWORD,
        'phone': '+86' + phone,
    }
    utils.post(session, url, data)


def get_redeem_code(session):
    url = 'https://candy.one/api/exchange-code/redeem-code?page=1&limit=30'
    r = utils.get(session, url)
    return r.json()['data']['redcords'][0]['exchange_code']


def verify_code_login(session, phone, code):
    url = 'https://candy.one/api/passport/verify-code-login'
    data = {
        'phone': '+86' + phone,
        'country_code': 'cn',
        'code': code,
        'inviter_id': ENROLL_ID,
    }
    r = utils.post(session, url, data)
    at = r.json()['data']['access_token']
    session.headers['x-access-token'] = at


def main():
    for phone in sys.stdin:
        try:
            phone = phone.strip()
            session = password_login(phone)
            withdraw(session)
        except Exception, e:
            utils.log('Error: %s', e)


if __name__ == '__main__':
    phone = '18515355023'
    session = register(phone)
    verify_code_login(session, phone, '123456')
