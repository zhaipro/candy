# coding: utf-8
import argparse

from projects import bec
import helpers
import settings
import telegram


def main():
    client = helpers.telegram_sign_up(proxy=args.proxy)
    address = helpers.eth_gen_account('BEC2')
    bec.create_wallet(address)
    telegram.send_code(client, settings.BEC['ROBOT'], address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy')
    args = parser.parse_args()
    helpers.loop(main)
