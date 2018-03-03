# coding: utf-8
import argparse

import telethon

import orm
import telegram
import helpers


def ping():
    for account in orm.TelegramAccount.select():
        client = helpers.telegram_create_client(account.phone)
        telegram.ping(client)


def fetch(phone):
    client = helpers.telegram_create_client(phone)
    for dialog in client.get_dialogs(limit=10):
        print(telethon.utils.get_display_name(dialog.entity), dialog.message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['debug', 'ping', 'fetch'])
    parser.add_argument('--phone')
    args = parser.parse_args()
    if args.cmd == 'ping':
        ping()
    elif args.cmd == 'fetch':
        fetch(args.phone)
    else:
        print(args)
