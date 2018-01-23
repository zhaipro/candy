# coding: utf-8
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def log(fmt, *args):
    msg = fmt % args
    print msg
    fn = os.path.join(BASE_DIR, 'a.log')
    fp = open(fn, 'a')
    print >> fp, msg
    fp.close()
