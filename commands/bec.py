# coding: utf-8
import argparse

import bec
import helpers
import settings
import telegram
import utils


def main():
    client = helpers.telegram_sign_up(proxy=args.proxy)
    address = helpers.eth_gen_account('BEC')
    code = bec.invite(settings.BEC['INVITE'], address)
    telegram.join(client, 'beautychian04')
    telegram.send_code(client, 'beautychian04', code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--proxy')
    args = parser.parse_args()
    utils.loop(main)
