# coding: utf-8
import threading
import time

import jwt
import six

import candy
import orm
import settings
import telegram
import utils
from sms import exceptions
from sms import yima as sms


def create_user(phone, token):
    payload = jwt.decode(token, verify=False)
    orm.User.create(phone=phone, token=token, expires=payload['exp'], uid=payload['id'])


def _register(phone):
    s = candy.register(phone)
    code = sms.getsms(phone)
    candy.verify_code_login(s, phone, code)
    create_user(phone, s.headers['x-access-token'])
    candy.set_password(s, phone)
    code = candy.get_redeem_code(s)
    telegram.send_code(code)


run_event = None


def register():
    while run_event.is_set():
        try:
            phone = sms.getmobile()
            if not candy.is_register(phone):
                _register(phone)
            sms.addignore(phone)
        except exceptions.BalanceException:
            run_event.clear()
        except (exceptions.NoMessageException, exceptions.NothingException):
            pass
        except Exception as e:
            utils.log('Error: %s', e)
            sms.release(phone)


def main():
    global run_event
    run_event = threading.Event()
    run_event.set()
    threads = [threading.Thread(target=register) for _ in six.moves.range(settings.NTHREAD)]
    for thread in threads:
        thread.start()
    try:
        while run_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        run_event.clear()
    for thread in threads:
        thread.join()


def _relogin(user):
    session = candy.password_login(user.phone)
    user.token = session.headers.get('x-access-token')
    user.balance = candy.get_balance(session)
    payload = jwt.decode(user.token, verify=False)
    user.expires = payload['exp']
    user.save()


def relogin():
    now = time.time()
    for user in orm.User.filter(expires__lt=now):
        try:
            _relogin(user)
        except Exception as e:
            utils.log('Error: %s', e)


if __name__ == '__main__':
    relogin()
