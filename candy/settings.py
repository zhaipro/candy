# coding: utf-8
import os

import pytz
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
    'ID': os.getenv('TELEGRAM_ID', 12345),
    'HASH': os.getenv('TELEGRAM_HASH', '0123456789abcdef0123456789abcdef'),
    'PROXY': (socks.SOCKS5, 'localhost', 1080),
}

EOZ = {
    'INVITE': '123456',
}

BEC = {
    'ROBOT': os.getenv('BEC_ROBOT', 'BECTelegram2Bot'),
}

ETH = {
    'ETHERSCAN_API_KEY': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
}

TZ = pytz.FixedOffset(8 * 60)   # 东八区
