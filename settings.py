# coding: utf-8
from __future__ import unicode_literals
import argparse


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
