# coding: utf-8
import argparse

import eth
import helpers
import orm
import utils
import settings


def step1(account, nonce):
    _, nonce = helpers.eth_send_transaction(settings.ETH['KEY'],
                                            account.address,
                                            0.00036,
                                            nonce=nonce)
    return nonce + 1


def step2(account, nonce=None):
    to = eth.utils.key_to_address(settings.ETH['KEY'])
    helpers.eth_send_token(args.token, account.key, to, balance)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token')
    parser.add_argument('--name')
    parser.add_argument('--step', type=int)
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args()
    if not args.name:
        args.name = args.token

    if args.step == 1:
        step = step1
    elif args.step == 2:
        step = step2
    else:
        assert 'There is no such step!'

    nonce = None
    accounts = orm.Account.filter(token=args.name)
    if args.limit > 0:
        accounts = accounts.limit(args.limit)
    for account in accounts:
        try:
            balance = helpers.eth_get_token_balance(args.token, account.address)
            balance /= 10 ** 18
            utils.log('balance\t%s\t%s\t%s', args.token, account.address, balance)
            if balance > 0:
                nonce = step(account, nonce)
        except Exception as e:
            utils.log('Error: %r', e)
