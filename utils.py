# coding: utf-8
import binascii
import os
import re

import requests
import six
import tesserocr

from settings import PROXIES


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def random_hex(n):
    return binascii.b2a_hex(os.urandom((n + 1) // 2)).decode('ascii')[:n]


pid = random_hex(7)     # 4 * 7 bits


def text_digest(text, length):
    text = text.replace('\n', r'\n')
    if len(text) > length:
        text = text[:length - 3] + '...'
    return text


def log(fmt, *args):
    msg = fmt % args
    six.print_(msg)
    fn = os.path.join(BASE_DIR, 'a.log')
    fp = open(fn, 'a')
    six.print_(pid, msg, file=fp)
    fp.close()


def post(session, url, data):
    log('s.post(url=%r, data=%r)', url, data)
    r = session.post(url, data, proxies=PROXIES, timeout=5)
    log('return: %s %s, %s', r.status_code, r.reason, r.text)
    return r


def get(session, url, params=None, **kws):
    log('s.get(url=%r, params=%r)', url, params)
    r = session.get(url, params=params, proxies=PROXIES, timeout=5, **kws)
    if re.search('text|json', r.headers['content-type'], re.I):
        text = text_digest(r.text, 100)
    else:
        text = '<binary>'
    log('return: %s %s, %s', r.status_code, r.reason, text)
    return r


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


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'   # NOQA


def gen_session(token=None):
    s = requests.Session()
    headers = {
        'Referer': 'https://candy.one/',
        'User-Agent': UA,
    }
    s.headers.update(headers)
    if token is not None:
        s.headers['x-access-token'] = token
    return s


def ocr(img):
    img = tesserocr.Image.open(tesserocr.BytesIO(img))
    return tesserocr.image_to_text(img).strip()
