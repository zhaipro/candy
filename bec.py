# coding: utf-8
import re

import requests

import utils


def invite(invite_id, address):
    url = 'https://referral.beauty.io/' + invite_id
    data = {
        'address': address,
    }
    r = utils.post(requests, url, data)
    # $('#j-code')[0].value
    regex = '<input readonly id="j-code" type="text" value="(/[0-9a-zA-Z]+)">'
    return re.search(regex, r.text).group(1)


def main():
    import eth
    import orm
    import settings
    import telegram

    address, pk = eth.gen_account()
    orm.Account.create(address=address, key=pk, token='BEC')
    code = invite(settings.BEC['INVITE'], address)
    telegram.send_code('beautychain', code)


if __name__ == '__main__':
    utils.loop(main)
