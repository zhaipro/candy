# coding: utf-8
import json
import os

from eth_keys import keys
from ethereum.transactions import Transaction
from web3 import HTTPProvider
from web3 import Web3
from web3.utils.encoding import to_bytes
import pyetherscan  # https://github.com/Marto32/pyetherscan
import rlp

import settings
import utils


def gen_account():
    pk = os.urandom(32)
    pk = keys.PrivateKey(pk)
    return pk.public_key.to_address(), pk.to_hex()


CONTRACT = {
    'BEC': '0xc5d105e63711398af9bbff092d4b6769c82f793d',
}


def get_token_balance(token, account):
    # token: token name or contract address
    token = CONTRACT.get(token, token)
    key = settings.ETH['ETHERSCAN_API_KEY']
    return pyetherscan.Client(key).get_token_balance_by_address(token, account).balance


@utils.mem.cache
def get_token_abi(token):
    token = CONTRACT.get(token, token)
    key = settings.ETH['ETHERSCAN_API_KEY']
    r = pyetherscan.Client(key).get_contract_abi(token)
    return json.loads(r.contract_abi)


w3 = None


def get_w3():
    global w3
    if w3 is None:
        w3 = Web3(HTTPProvider('https://api.myetherapi.com/eth', {'proxies': settings.PROXIES}))
        w3.isConnected()
    return w3


def key_to_address(key):
    return keys.PrivateKey(to_bytes(hexstr=key)).public_key.to_address()


def send_transaction(key, to, amount=0, data=b'', gas_limit=60000, nonce=None):
    w3 = get_w3()
    sender = key_to_address(key)
    if nonce is None:
        local_nonce = w3.eth.getTransactionCount(sender)
        remote_nonce = w3.eth.getTransactionCount(sender, 'pending')
        nonce = max(local_nonce, remote_nonce)
    tx = Transaction(
        nonce=nonce,
        gasprice=int(1.5e9),
        startgas=gas_limit,
        to=to,
        value=w3.toWei(amount, 'ether'),
        data=data,
    )
    tx.sign(key)
    tx = rlp.encode(tx)
    tx = w3.toHex(tx)
    tx = w3.eth.sendRawTransaction(tx)
    utils.log('Txhash\t%s', tx)
    return tx, nonce


send_ether = send_transaction


def send_token(token, key, to, amount):
    w3 = get_w3()
    # token: token name or contract address
    token = CONTRACT.get(token, token)
    abi = get_token_abi(token)
    contract = w3.eth.contract(token, abi=abi)
    data = contract._encode_transaction_data('transfer', args=(to, w3.toWei(amount, 'ether')))
    data = to_bytes(hexstr=data)
    return send_transaction(key, token, data=data)
