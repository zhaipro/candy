# coding: utf-8
import os

from eth_keys import keys
import pyetherscan  # https://github.com/Marto32/pyetherscan

import settings


def gen_account():
    pk = os.urandom(32)
    pk = keys.PrivateKey(pk)
    return pk.public_key.to_address(), pk.to_hex()


def get_token_balance(contract, account):
    key = settings.ETH['ETHERSCAN_API_KEY']
    return pyetherscan.Client(key).get_token_balance_by_address(contract, account).balance
