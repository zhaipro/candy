# coding: utf-8
# 胶水模块
import os
import random
import time

import telethon

from proxy import parser_proxy
from sms import yima as sms
import eth
import orm
import settings
import telegram
import utils


def eth_gen_account(token):
    address, key = eth.gen_account()
    orm.Account.create(address=address, key=key, token=token)
    return address


def proxy_sslocal():
    os.system('echo -e \'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\' | nc 127.0.0.1 9051')
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
    client = TelegramClient('sessions/+86' + phone,
                            settings.TELEGRAM['ID'],
                            settings.TELEGRAM['HASH'],
                            proxy=proxy)
    client.connect()
    return client


def telegram_sign_up(proxy=None):
    try:
        phone = sms.getmobile(itemid=sms.TELEGRAM)

        def code_callback():
            return sms.getsms(phone, itemid=sms.TELEGRAM)
        client = telegram_create_client(phone, proxy)
        name = random.choice(open('data/names.txt').readlines())
        name = name.strip()
        telegram.sign_up(client, phone, code_callback, name)
        orm.TelegramAccount.create(phone=phone, password=settings.PASSWORD)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        utils.log('Error: %r', e)
        raise e
    finally:
        sms.addignore(phone, itemid=sms.TELEGRAM)
    return client
