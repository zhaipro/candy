# coding: utf-8
import os

# https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-an-erc20-contract
from web3.auto.infura import w3
import eth_keys
import eth_utils

import utils


def gen_account():
    pk = os.urandom(32)
    pk = eth_keys.keys.PrivateKey(pk)
    return pk.public_key.to_checksum_address(), pk.to_hex()


CONTRACT = {
    'BEC': '0x3495Ffcee09012AB7D827abF3E3b3ae428a38443',
}


def get_token_balance(token, account):
    # token: token name or contract address
    token = CONTRACT.get(token, token)
    url = f'https://api.etherscan.io/api?module=contract&action=tokenbalance&contractaddress={token}&address={account}'
    response = requests.get(url)
    return int(response.json()['result'])


@utils.mem.cache
def get_abi(token):
    token = CONTRACT.get(token, token)
    url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&format=raw'
    response = requests.get(url)
    return response.json()


def key_to_address(key):
    return eth_keys.keys.PrivateKey(eth_utils.decode_hex(key)).public_key.to_checksum_address()


def ether_to_wei(number):
    return eth_utils.to_wei(number, 'Ether')


def gwei_to_wei(number):
    return eth_utils.to_wei(number, 'GWei')


def send_transaction(key, to, amount=0, data=b'', gas=60000, nonce=None):
    sender = key_to_address(key)
    if nonce is None:
        local_nonce = w3.eth.getTransactionCount(sender)
        remote_nonce = w3.eth.getTransactionCount(sender, 'pending')
        nonce = max(local_nonce, remote_nonce)
    # https://web3py.readthedocs.io/en/stable/web3.eth.html?#web3.eth.Eth.sendRawTransaction
    tx = {
        'nonce': nonce,
        'gasPrice': gwei_to_wei(1.5),
        'gas': gas,
        'to': to,
        'value': ether_to_wei(amount),
        'data': data,
    }
    tx = w3.eth.account.signTransaction(tx, key)
    tx = w3.eth.sendRawTransaction(tx.rawTransaction)
    tx = eth_utils.encode_hex(tx)
    utils.log('Txhash\t%s', tx)
    return tx, nonce


send_ether = send_transaction


def send_token(token, key, to, amount):
    # token: token name or contract address
    token = CONTRACT.get(token, token)
    abi = get_token_abi(token)
    contract = w3.eth.contract(token, abi=abi)
    data = contract.functions.transfer(to, ether_to_wei(amount))
    data = data._encode_transaction_data()
    data = eth_utils.decode_hex(data)
    return send_transaction(key, token, data=data)
