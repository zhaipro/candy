# coding: utf-8
import re
import time

import requests

import utils
import exceptions
from settings import XINGKONG

API = 'http://www.xk-yzm.com:9180/service.asmx/'
ITEMID = 5994


def check_response(response, codes=None):
    if re.match('^-?\d{1,2}$', response):
        if codes:
            clazz = codes.get(response, exceptions.SMSException)
        else:
            clazz = exceptions.SMSException
        raise clazz(response)


def get(action, **kws):
    api = API + action
    params = {
        'token': XINGKONG['TOKEN'],
    }
    params.update(kws)
    utils.log('requests.get(url=%r, params=%r)', api, params)
    response = requests.get(api, params).text
    utils.log('return: %s', response)
    return response


def login():
    return get('UserLoginStr', name='yifuda', psw='xk3051346')


def getmobile(mobile=None):
    mobile = get('GetHMStr', xmid=ITEMID, sl=1, lx=0, a1='', a2='', pk='')
    check_response(mobile, {'-8': exceptions.BalanceException})
    return mobile[3:]


def release(mobile):
    return get('sfHmStr', hm=mobile)


def releaseall():
    return get('sfAllStr')


def getsms(mobile):
    for _ in xrange(10):
        try:
            sms = get('GetYzmStr', hm=mobile, xmid=ITEMID)
            check_response(sms, {'1': exceptions.NoMessageException})
            release(mobile)
            code = re.search('\d{6}', sms).group(0)
            return code
        except exceptions.NoMessageException:
            time.sleep(5)
    release(mobile)
    raise exceptions.NoMessageException()


def addignore(mobile):
    return get('HmdStr', hm=mobile, xmid=ITEMID)


releaseall()


if __name__ == '__main__':
    mobile = getmobile()
    getsms(mobile)
