# coding: utf-8
import argparse

import orm
import telegram


def ping():
    for account in orm.TelegramAccount.select():
        client = telegram.create_client(account.phone)
        telegram.ping(client)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['ping'])
    args = parser.parse_args()
    if args.cmd == 'ping':
        ping()
