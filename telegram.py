# coding: utf-8
import os

import telethon
from telethon import helpers
from telethon.tl.functions import account
from telethon.tl.types.account import PasswordInputSettings

import utils
from settings import TELEGRAM, PASSWORD


def send_code(enity, code):
    g = globals()
    if 'client' not in g:
        g['client'] = TelegramClient('telegram',
                                     TELEGRAM['ID'],
                                     TELEGRAM['HASH'],
                                     proxy=TELEGRAM['PROXY'])
        g['client'].start()

    client = g['client']
    client.send_message(enity, code)


class TelegramClient(telethon.TelegramClient):

    def __call__(self, request):
        utils.log('telegram.invoke: %s', request)
        r = super(TelegramClient, self).__call__(request)
        utils.log('return: %s', r)
        return r


def set_password(client, pw):
    new_salt = client(account.GetPasswordRequest()).new_salt
    salt = new_salt + os.urandom(8)
    pw_hash = helpers.get_password_hash(pw, salt)
    client(account.UpdatePasswordSettingsRequest(
        current_password_hash=salt,
        new_settings=PasswordInputSettings(
            new_salt=salt,
            new_password_hash=pw_hash,
            hint='No hint',
        )
    ))


class PhoneRegisteredException(Exception):
    def __init__(self):
        super(PhoneRegisteredException, self).__init__('The phone number is already in use')


def sign_up(phone, code_callback, pw=PASSWORD):
    phone = '+86' + phone
    client = TelegramClient('sessions/' + phone,
                            TELEGRAM['ID'],
                            TELEGRAM['HASH'],
                            proxy=TELEGRAM['PROXY'])
    client.connect()
    r = client.send_code_request(phone)
    if r.phone_registered:
        raise PhoneRegisteredException()
    code = code_callback()
    client.sign_up(code, 'me')
    set_password(client, pw)


if __name__ == '__main__':
    import orm
    from sms import yima as sms

    while True:
        try:
            phone = sms.getmobile(itemid=sms.TELEGRAM)

            def code_callback():
                return sms.getsms(phone, itemid=sms.TELEGRAM)
            sign_up(phone, code_callback)
            orm.TelegramAccount.create(phone=phone, password=PASSWORD)
        except Exception as e:
            utils.log('Error: %r', e)
        try:
            sms.addignore(phone, itemid=sms.TELEGRAM)
        except Exception as e:
            utils.log('Error: %r', e)
