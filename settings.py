# coding: utf-8
from __future__ import unicode_literals
import os

import socks


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ENROLL_ID = 'your enroll id'
PASSWORD = 'your password'
ADDRESS = 'your address'

YIMA = {
    'TOKEN': 'your token',
}

XINGKONG = {
    'TOKEN': 'your token'
}

PROXIES = None
# {
#     'http': 'socks5://127.0.0.1:1080',
#     'https': 'socks5://127.0.0.1:1080',
# }

DATABASE = {
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

TELEGRAM = {
    'ID': 12345,
    'HASH': '0123456789abcdef0123456789abcdef',
    'PROXY': (socks.SOCKS5, 'localhost', 1080),
}

EOZ = {
    'INVITE': '123456',
}

BEC = {
    'INVITE': 'ABCDEFGH',
}
