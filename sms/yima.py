# coding: utf-8
import json
import re
import time

import requests

import exceptions
import settings
import utils


API = 'http://api.51ym.me/UserInterface.aspx'
ITEMID = 13651

codes = {
    '1008': exceptions.BalanceException,
    '2008': exceptions.MobileOfflineException,
    '3001': exceptions.NoMessageException,
}


def raise_exception(code):
    clazz = codes.get(code, exceptions.SMSException)
    raise clazz(code)


def get(action, **kws):
    params = {
        'action': action,
        'token': settings.YIMA['TOKEN'],
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
        except exceptions.NoMessageException:  # 暂未收到短信
            time.sleep(5)
    # 接收失败的话，自动释放
    release(mobile, itemid)
    raise exceptions.NoMessageException()


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
