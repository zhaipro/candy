# coding: utf-8
import binascii
import os
import time

from settings import PROXIES


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def random_hex(n):
    return binascii.b2a_hex(os.urandom((n + 1) / 2))[:n]


pid = random_hex(7)     # 4 * 7 bits


def log(fmt, *args):
    msg = fmt % args
    if isinstance(msg, unicode):
        msg = msg.encode('utf-8')
    print msg
    fn = os.path.join(BASE_DIR, 'a.log')
    fp = open(fn, 'a')
    print >> fp, pid, msg
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
    print >> fp, '%d\t%s\t%s' % (time.time(), name, value)
    fp.close()
