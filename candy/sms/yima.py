# coding: utf-8
import json
import re
import time

import requests

import settings
import utils
from . import exceptions


API = 'http://api.fxhyd.cn/UserInterface.aspx'
ITEMID = 13651
TELEGRAM = 3988

codes = {
    '1008': exceptions.BalanceException,
    '3001': exceptions.NoMessageException,
    '2007': exceptions.NothingException,    # 号码已被释放
    '2008': exceptions.NothingException,    # 号码已离线
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
    r = utils.get(requests, API, params).text
    if not r.startswith('success'):
        raise_exception(r)
    if '|' in r:
        _, r = r.split('|', 1)
        return r


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
    # 总之50秒是不够用的
    # 尝试20次，间隔6秒
    for _ in range(20):
        try:
            text = get('getsms', itemid=itemid, mobile=mobile, release=1)
            return re.search(r'\d+', text).group(0)
        except (exceptions.NoMessageException, requests.Timeout):   # 暂未收到短信 or 超时
            time.sleep(6)
    # 接收失败的话，自动释放
    release(mobile, itemid)
    raise exceptions.NoMessageException()


def release(mobile, itemid=ITEMID):
    try:
        get('release', itemid=itemid, mobile=mobile)
    except exceptions.NothingException:
        pass


def addignore(mobile, itemid=ITEMID):
    return get('addignore', itemid=itemid, mobile=mobile)


def releaseall():
    return get('releaseall')


if __name__ == '__main__':
    # print getaccountinfo()
    mobile = getmobile()
    print(mobile)
    print(release(mobile))
