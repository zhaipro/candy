# coding: utf-8
import os

import eth_keys
import eth_utils


def gen_account():
    pk = os.urandom(32)
    pk = eth_keys.keys.PrivateKey(pk)
    return pk.public_key.to_checksum_address(), pk.to_hex()


def to_checksum_address(address):
    return eth_utils.to_checksum_address(address)


def key_to_address(key):
    return eth_keys.keys.PrivateKey(eth_utils.decode_hex(key)).public_key.to_checksum_address()


def ether_to_wei(number):
    return eth_utils.to_wei(number, 'Ether')


def gwei_to_wei(number):
    return eth_utils.to_wei(number, 'GWei')
