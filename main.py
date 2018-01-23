# coding: utf-8
import re
import requests

import sms
import utils
from settings import ENROLL_ID, PASSWORD


def post(session, url, data):
    utils.log('s.post(url=%r, data=%r)', url, data)
    response = session.post(url, data)
    utils.log('return: %s', response)
    return response


def login(phone=None):
    # 准备会话
    s = requests.Session()
    headers = {
        'Referer': 'https://candy.one/i/%s' % ENROLL_ID,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0',
    }
    s.headers.update(headers)

    # 请求登录
    phone = sms.getmobile(mobile=phone)
    data = {
        'phone': phone,
        'dialcode': '86',
        'countrycode': 'cn',
        'status': 'login',
        'enroll_id': ENROLL_ID,
    }
    url = 'https://candy.one/i/%s' % ENROLL_ID
    response = post(s, url, data)
    if len(response.text) <= 80:
        utils.log('return: %s', response.text)
        sms.release(phone)
        raise Exception('注册已达上限')
    code = sms.getsms(phone)

    # 登录
    data = {
        'code': code,
        'status': 'send_msg',
        'phone': '86%s' % phone,
        'countrycode': 'CN',
    }
    url = 'https://candy.one/user'
    post(s, url, data)

    # 设定密码
    data = {
        'usr_pwd': PASSWORD,
        'user_confirm_pwd': PASSWORD,
    }
    url = 'https://candy.one/user/register'
    post(s, url, data)

    # 获取用户id
    url = 'https://candy.one/invite'
    utils.log('s.get(url=%r)', url)
    response = s.get(url)
    uid = re.search(r'candy.one/i/(\d+)', response.text).group(1)
    utils.log('phone: %s, uid: %s', phone, uid)

    sms.addignore(phone)
    return phone


if __name__ == '__main__':
    fp = open('phone.txt', 'a+')
    while True:
        try:
            phone = login()
            print >> fp, phone
        except (KeyboardInterrupt, sms.BalanceException):
            break
        except (sms.NoMessageException, sms.MobileOfflineException):
            pass
        except requests.exceptions.ConnectionError:
            sms.releaseall()
    fp.flush()  # 我并不确定在关闭的时候是否会自动完成刷新工作
    fp.close()
