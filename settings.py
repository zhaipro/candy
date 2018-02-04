# coding: utf-8
from __future__ import unicode_literals
import argparse
import os

import socks


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='主程序')
parser.add_argument('-p', '--process', default='process1',
                    help='进程名')
parser.add_argument('-t', '--nthread', default=2, type=int,
                    help='线程数')
args = parser.parse_args()


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

PROCESS = args.process
NTHREAD = args.nthread

DATABASE = {
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

TELEGRAM = {
    'ID': 12345,
    'HASH': '0123456789abcdef0123456789abcdef',
    'PROXY': (socks.SOCKS5, 'localhost', 1080),
}
