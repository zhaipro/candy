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


def register(phone):
    s = candy.register(phone)
    code = sms.getsms(phone)
    candy.verify_code_login(s, phone, code)
    create_user(phone, s.headers['x-access-token'])
    candy.set_password(s, phone)
    code = candy.get_redeem_code(s)
    telegram.send_code(code)


def main():
    while run_event.is_set():
        try:
            phone = sms.getmobile()
            if not candy.is_register(phone):
                register(phone)
                utils.record('phone', phone)
            sms.addignore(phone)
        except exceptions.BalanceException:
            run_event.clear()
        except (exceptions.NoMessageException, exceptions.NothingException):
            pass
        except Exception as e:
            utils.log('Error: %s', e)
            sms.release(phone)


if __name__ == '__main__':
    run_event = threading.Event()
    run_event.set()
    threads = [threading.Thread(target=main) for _ in six.moves.range(settings.NTHREAD)]
    for thread in threads:
        thread.start()
    try:
        while run_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        run_event.clear()
    for thread in threads:
        thread.join()
