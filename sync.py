# coding: utf-8
import sys

import candy
import orm
import utils


for phone in sys.stdin:
    try:
        phone = phone.strip()
        session = candy.password_login(phone)
        token = session.headers.get('x-access-token')
        balance = candy.get_balance(session)
        orm.User.create(phone=phone, token=token, balance=balance)
    except KeyboardInterrupt:
        break
    except Exception, e:
        utils.log('Error: %s', e)
