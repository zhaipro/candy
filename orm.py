# coding: utf-8
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

import settings

db = SqliteExtDatabase(settings.DATABASE['NAME'])


class User(peewee.Model):
    phone = peewee.CharField(16, unique=True)
    balance = peewee.IntegerField(default=0)
    token = peewee.CharField(256)
    expires = peewee.IntegerField(default=0)
    uid = peewee.IntegerField(null=True)

    class Meta:
        database = db


class Account(peewee.Model):
    address = peewee.CharField(20 * 2 + 2)
    key = peewee.CharField(32 * 2 + 2)
    token = peewee.CharField(default='')

    class Meta:
        database = db


class TelegramAccount(peewee.Model):
    phone = peewee.CharField(16, unique=True)
    password = peewee.CharField()

    class Meta:
        database = db


db.connect()
# https://github.com/coleifer/peewee/issues/211
User.create_table(fail_silently=True)
Account.create_table(fail_silently=True)
TelegramAccount.create_table(fail_silently=True)
