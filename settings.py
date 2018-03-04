# coding: utf-8
import os

import socks


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.getenv('DATA_DIR', os.path.join(BASE_DIR, 'data'))


ENROLL_ID = 'your enroll id'
PASSWORD = 'your password'
ADDRESS = 'your address'

YIMA = {
    'TOKEN': 'your token',
}

XINGKONG = {
    'TOKEN': 'your token'
}

PROXIES = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080',
}

DATABASE = {
    'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
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
    'INVITE': '',
}
