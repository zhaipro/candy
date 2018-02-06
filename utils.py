# coding: utf-8
import binascii
import os
import time

import requests
import six

from settings import PROXIES


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def random_hex(n):
    return binascii.b2a_hex(os.urandom((n + 1) // 2))[:n]


pid = random_hex(7)     # 4 * 7 bits


def log(fmt, *args):
    msg = fmt % args
    if hasattr(msg, 'encode'):
        msg = msg.encode('utf-8')
    six.print_(msg)
    fn = os.path.join(BASE_DIR, 'a.log')
    fp = open(fn, 'a')
    six.print_(pid, msg, file=fp)
    fp.close()


def post(session, url, data):
    log('s.post(url=%r, data=%r)', url, data)
    r = session.post(url, data, proxies=PROXIES)
    log('return: %s %s, %s', r.status_code, r.reason, r.text)
    return r


def get(session, url, params=None):
    log('s.get(url=%r, params=%r)', url, params)
    r = session.get(url, params=params, proxies=PROXIES)
    log('return: %s %s, %s', r.status_code, r.reason, r.text)
    return r


def record(name, value):
    fn = os.path.join(BASE_DIR, 'record.txt')
    fp = open(fn, 'a')
    msg = '%d\t%s\t%s' % (time.time(), name, value)
    six.print_(msg, file=fp)
    fp.close()


class Lock(object):
    def __init__(self, fn):
        self.fn = fn

    def __enter__(self):
        import fcntl
        self.fp = open(self.fn, 'w')
        fcntl.flock(self.fp, fcntl.LOCK_EX)

    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        import fcntl
        fcntl.flock(self.fp, fcntl.LOCK_UN)
        self.fp.close()


def gen_session(token=None):
    s = requests.Session()
    headers = {
        'Referer': 'https://candy.one/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    }
    s.headers.update(headers)
    if token is not None:
        s.headers['x-access-token'] = token
    return s
