# coding: utf-8
# https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-an-erc20-contract
# https://web3py.readthedocs.io/en/stable/quickstart.html#provider-infura
from web3.auto.infura import w3
import eth_utils

from . import abi
from . import utils


def get_balance(address):
    return w3.eth.getBalance(address)


def get_token_balance(token, address):
    contract = w3.eth.contract(token, abi=abi.ERC20)
    return contract.functions.balanceOf(address).call()


def send_transaction(key, to, gas_price, gas_limit, amount=0, data=b'', nonce=None):
    sender = utils.key_to_address(key)
    if nonce is None:
        local_nonce = w3.eth.getTransactionCount(sender)
        remote_nonce = w3.eth.getTransactionCount(sender, 'pending')
        nonce = max(local_nonce, remote_nonce)
    # https://web3py.readthedocs.io/en/stable/web3.eth.html?#web3.eth.Eth.sendRawTransaction
    tx = {
        'nonce': nonce,
        'gasPrice': utils.gwei_to_wei(gas_price),
        'gas': gas_limit,
        'to': to,
        'value': utils.ether_to_wei(amount),
        'data': data,
    }
    tx = w3.eth.account.signTransaction(tx, key)
    tx = w3.eth.sendRawTransaction(tx.rawTransaction)
    tx = eth_utils.encode_hex(tx)
    return tx, nonce


def encode_token_transfer_data(token, to, amount):
    contract = w3.eth.contract(token, abi=abi.ERC20)
    data = contract.functions.transfer(to, utils.ether_to_wei(amount))
    return data._encode_transaction_data()
