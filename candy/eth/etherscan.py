# coding: utf-8
# https://etherscan.io/apis#tokens
import requests


def get_abi(address):
    url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&format=raw'
    response = requests.get(url)
    return response.json()


def get_token_balance(token, account, apikey=''):
    url = f'https://api.etherscan.io/api?module=aa&action=tokenbalance&contractaddress={token}&address={account}&apikey={apikey}'
    response = requests.get(url)
    return int(response.json()['result'])
