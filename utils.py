# coding: utf-8
import binascii
import os


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
