# coding: utf-8
from __future__ import absolute_import
import orm
import proxy


def main():
    for url in proxy.get_socks5():
        orm.Proxy.insert(url=url).on_conflict_ignore().execute()


if __name__ == '__main__':
    main()
