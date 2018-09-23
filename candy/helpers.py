# coding: utf-8
# 胶水模块
import os
import random
import time

import telethon

from proxy import parser_proxy
from sms import yima as sms
from sms.exceptions import BalanceException
import eth
import orm
import settings
import telegram
import utils


def eth_gen_account(token):
    address, key = eth.utils.gen_account()
    orm.Account.create(address=address, key=key, token=token)
    return address


def eth_send_transaction(key, to, amount=0, gas_price=6, gas=60000, data=b'', nonce=None):
    tx, nonce = eth.web3.send_transaction(key, to, gas_price, gas, amount, data, nonce)
    utils.log('Txhash\t%s', tx)
    return tx, nonce


@utils.mem.cache
def eth_get_abi(token):
    return eth.etherscan.get_abi(token)


CONTRACT = {
    'BEC': '0x3495Ffcee09012AB7D827abF3E3b3ae428a38443',
}


def eth_get_token_balance(token, address):
    token = CONTRACT.get(token, token)
    return eth.web3.get_token_balance(token, address)


def eth_send_token(token, key, to, amount, nonce=None):
    # token: token name or contract address
    token = CONTRACT.get(token, token)
    data = eth.web3.encode_token_transfer_data(token, to, amount)
    return eth_send_transaction(key, token, data=data, nonce=nonce)


def proxy_sslocal():
    import telnetlib
    tn = telnetlib.Telnet('localhost', port=9051, timeout=10)
    tn.write(b'AUTHENTICATE "password"\r\nSIGNAL NEWNYM\r\nQUIT')
    time.sleep(5)


class TelegramClient(telethon.TelegramClient):

    def __call__(self, request):
        try:
            utils.log('telegram.invoke: %s', request)
            r = super(TelegramClient, self).__call__(request)
            utils.log('return: %s', r)
            return r
        except (telethon.errors.rpc_error_list.FloodWaitError, RuntimeError):
            proxy_sslocal()
            raise


def telegram_create_client(phone, proxy=None):
    proxy = parser_proxy(proxy) if proxy else settings.TELEGRAM['PROXY']
    phone = '+86' + phone
    session = os.path.join(settings.DATA_DIR, 'sessions', phone)
    client = TelegramClient(session,
                            settings.TELEGRAM['ID'],
                            settings.TELEGRAM['HASH'],
                            proxy=proxy)
    client.connect()
    return client


def telegram_sign_up(proxy=None):
    phone = sms.getmobile(itemid=sms.TELEGRAM)
    try:
        def code_callback():
            return sms.getsms(phone, itemid=sms.TELEGRAM)
        client = telegram_create_client(phone, proxy)
        fn = os.path.join(settings.DATA_DIR, 'names.txt')
        name = random.choice(open(fn).readlines())
        name = name.strip()
        telegram.sign_up(client, phone, code_callback, name)
        orm.TelegramAccount.create(phone=phone, password=settings.PASSWORD)
    finally:
        sms.addignore(phone, itemid=sms.TELEGRAM)
    return client


def loop(func):
    errors = (BalanceException, telethon.errors.ApiIdInvalidError)
    utils.loop(func, errors)
