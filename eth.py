# coding: utf-8
import os

from eth_keys import keys


def gen_account():
    pk = os.urandom(32)
    pk = keys.PrivateKey(pk)
    return pk.public_key.to_address(), pk.to_hex()
