# coding: utf-8
import requests


def get_abi(address):
    url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&format=raw'
    response = requests.get(url)
    return response.json()


def get_token_balance(token, account):
    url = f'https://api.etherscan.io/api?module=contract&action=tokenbalance&contractaddress={token}&address={account}'
    response = requests.get(url)
    return int(response.json()['result'])
