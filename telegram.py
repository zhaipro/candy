# coding: utf-8
import os

import telethon
from telethon import helpers
from telethon.tl.functions import account
from telethon.tl.functions import channels
from telethon.tl.functions import PingRequest
from telethon.tl.types.account import PasswordInputSettings

from settings import PASSWORD


def send_code(client, enity, code):
    client.send_message(enity, code)


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


def sign_up(client, phone, code_callback, nickname='me', pw=PASSWORD):
    phone = '+86' + phone
    r = client.send_code_request(phone)
    if r.phone_registered:
        raise PhoneRegisteredException()
    code = code_callback()
    client.sign_up(code, nickname)
    set_password(client, pw)


def ping(client):
    return client(PingRequest(0))


def join(client, channel):
    request = channels.JoinChannelRequest(channel)
    request.resolve(client, telethon.utils)
    client(request)


def update_username(client, username):
    return client(account.UpdateUsernameRequest(username))
