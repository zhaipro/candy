# coding: utf-8
import time
from datetime import datetime

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
    # http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains
    action = ActionChains(driver)
    # 直接这么做似乎有点问题：
    # action.click_and_hold(fuck)
    action.move_to_element_with_offset(fuck, 10, 10).click_and_hold()
    action.move_by_offset(550, 0)
    action.release().perform()
    time.sleep(1)
    utils.log(browser.url)


def gen_session(cookies):
    return utils.gen_session(cookies.get('_candy_token'))


def password_login(phone, password=PASSWORD):
    '''
    登录指定账号，并返回requests.Session对象
    '''
    # 这里不能使用隐私窗口，否则会导致拿不到cookies
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
    注册指定账号，并返回session
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


def withdraw(session, address=ADDRESS, amount=None):
    '''
    提取全部余额到指定BigOne账户
    '''
    if amount is None:
        amount = get_balance(session)
    if amount <= 0:
        return
    url = 'https://candy.one/api/transaction/withdraw'
    data = {
        'amount': amount,
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


def get_lottery(session):
    params = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'page': 1,
        'limit': 1,
    }
    url = 'https://candy.one/api/lottery/list'
    r = utils.get(session, url, params)
    # {"price": 10, "id": 172}
    return r.json()['data'][0]


def lottery_participators(session, lottery_id):
    url = 'https://candy.one/api/lottery-participators/participate'
    data = {'lottery_id': lottery_id}
    utils.post(session, url, data)


def get_my_lottery(session):
    url = 'https://candy.one/api/lottery/my'
    r = utils.get(session, url)
    # {"reward":12216,"participator_count":1527,"status":1,"id":208}
    return sum(lottery['reward'] for lottery in r.json()['data'])


if __name__ == '__main__':
    phone = '18515355024'
    password_login(phone)
