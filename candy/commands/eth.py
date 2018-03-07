# coding: utf-8
import argparse

import eth
import orm
import utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token')
    parser.add_argument('--name')
    args = parser.parse_args()
    if not args.name:
        args.name = args.token
    for account in orm.Account.filter(token=args.name):
        try:
            balance = eth.web3.get_token_balance(args.token, account.address)
            balance /= 10 ** 18
            utils.log('balance\t%s\t%s\t%s', args.token, account.address, balance)
        except Exception as e:
            utils.log('Error: %r', e)
