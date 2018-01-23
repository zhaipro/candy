# coding: utf-8


class SMSException(Exception):
    def __init__(self, code=None):
        self.code = code

    def __str__(self):
        return 'Error code: %s' % self.code


class BalanceException(SMSException):
    pass


class MobileOfflineException(SMSException):
    pass


class NoMessageException(SMSException):
    pass
