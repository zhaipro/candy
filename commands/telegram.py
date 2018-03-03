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


def update(phone, username):
    client = helpers.telegram_create_client(phone)
    telegram.update_username(client, username)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['debug', 'ping', 'fetch', 'update'])
    parser.add_argument('-p', '--phone')
    parser.add_argument('-u', '--username')
    args = parser.parse_args()
    if args.cmd == 'ping':
        ping()
    elif args.cmd == 'fetch':
        fetch(args.phone)
    elif args.cmd == 'update':
        update(args.phone, args.username)
    else:
        print(args)
