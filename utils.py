# coding: utf-8
import binascii
import os
import re

import requests
import six
import tesserocr

import settings


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
    fn = os.path.join(settings.DATA_DIR, 'a.log')
    fp = open(fn, 'a')
    six.print_(pid, msg, file=fp)
    fp.close()


def log_response(r):
    if re.search('text|json', r.headers['content-type'], re.I):
        text = text_digest(r.text, 100)
    else:
        text = '<binary>'
    log('return: %s %s, %s', r.status_code, r.reason, text)


# 总之5秒是不够用的
TIMEOUT = 13


def post(session, url, data):
    log('s.post(url=%r, data=%r)', url, data)
    r = session.post(url, data, proxies=settings.PROXIES, timeout=TIMEOUT)
    log_response(r)
    return r


def get(session, url, params=None, **kws):
    log('s.get(url=%r, params=%r)', url, params)
    r = session.get(url, params=params, proxies=settings.PROXIES, timeout=TIMEOUT, **kws)
    log_response(r)
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


def loop(func, errors=None):
    # errors: 致命错误列表
    if errors:
        errors = (KeyboardInterrupt, *errors)
    else:
        errors = KeyboardInterrupt
    while True:
        try:
            func()
        except errors:
            # 触发致命异常，一定要退出啊，而且要正常退出，不然supervisor会重启程序
            exit(0)
        # TODO: 这里使用这么强力的异常捕获，要千万小心
        # 请始终确保这里是唯一捕获顶级异常的地方，不要在增加维护成本了
        except Exception as e:
            log('Error: %r', e)
