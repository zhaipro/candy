# coding: utf-8
import candy
import utils
from sms import exceptions
from sms import yima as sms


def register(phone):
    s = candy.register(phone)
    code = sms.getsms(phone)
    candy.verify_code_login(s, phone, code)
    candy.set_password(s, phone)
    code = candy.get_redeem_code(s)
    utils.record('exchange_code', code)


if __name__ == '__main__':
    while True:
        try:
            phone = sms.getmobile()
            if not candy.is_register(phone):
                register(phone)
                utils.record('phone', phone)
            sms.addignore(phone)
        except (KeyboardInterrupt, exceptions.BalanceException):
            break
        except (exceptions.NoMessageException, exceptions.NothingException):
            pass
        except Exception, e:
            utils.log('Error: %s', e)
            sms.release(phone)
