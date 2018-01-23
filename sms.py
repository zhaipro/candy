# coding: utf-8
import json
import re
import time

import requests

import settings
import utils


TOKEN = settings.SMS['TOKEN']
API = 'http://api.51ym.me/UserInterface.aspx'
ITEMID = 13651


class Factory(type):
    def __new__(cls, name, bases, attrs):
        base = bases[0]
        clazz = super(Factory, cls).__new__(cls, name, bases, attrs)
        if hasattr(base, '_children'):
            base._children[clazz.code] = clazz
        return clazz


class APIException(Exception):
    '''
    1008: 账户余额不足
    2008: 号码已离线
    3001: 尚未收到短信
    '''
    __metaclass__ = Factory

    _children = {}

    def __init__(self, code=None):
        if code is not None:
            self.code = code

    def __str__(self):
        return 'error code: %s' % self.code


class BalanceException(APIException):
    code = 1008


class MobileOfflineException(APIException):
    code = 2008


class NoMessageException(APIException):
    code = 3001


def raise_exception(code):
    code = int(code)
    clazz = APIException._children.get(code, APIException)
    raise clazz(code)


def get(action, **kws):
    params = {
        'action': action,
        'token': TOKEN,
    }
    params.update(kws)
    utils.log('requests.get(url=%r, params=%r)', API, params)
    response = requests.get(API, params).text
    utils.log('return: %s', response)
    if not response.startswith('success'):
        raise_exception(response)
    if '|' in response:
        _, response = response.split('|', 1)
        return response


def getaccountinfo():
    '''
    {u'UserName': u'yifuda', u'Status': 1, u'MaxHold': 20, u'Frozen': 10.0, u'Discount': 1.0, u'UserLevel': 1, u'Balance': 9.8}
    '''
    response = get('getaccountinfo', format=1)
    return json.loads(response)


def getbalance():
    '''
    Return: float，单位：元
    '''
    return getaccountinfo()['Balance']


def getmobile(mobile=None, itemid=ITEMID):
    '''
    mobile: long or string
    '''
    if mobile:
        return get('getmobile', itemid=itemid, mobile=mobile)
    else:
        return get('getmobile', itemid=itemid)


def getsms(mobile, itemid=ITEMID):
    # 尝试10次，间隔5秒
    for _ in xrange(10):
        try:
            text = get('getsms', itemid=ITEMID, mobile=mobile, release=1)
            return re.search(r'\d+', text).group(0)
        except NoMessageException:  # 暂未收到短信
            time.sleep(5)
    # 接收失败的话，自动释放
    release(mobile, itemid)
    raise NoMessageException()


def release(mobile, itemid=ITEMID):
    return get('release', itemid=ITEMID, mobile=mobile)


def addignore(mobile, itemid=ITEMID):
    return get('addignore', itemid=ITEMID, mobile=mobile)


def releaseall():
    return get('releaseall')


releaseall()


if __name__ == '__main__':
    # print getaccountinfo()
    mobile = getmobile()
    print mobile
    print release(mobile)
