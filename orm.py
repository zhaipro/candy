# coding: utf-8
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

import settings

db = SqliteExtDatabase(settings.DATABASE['NAME'])


class User(peewee.Model):
    phone = peewee.CharField(16, unique=True)
    balance = peewee.IntegerField()
    token = peewee.CharField(256)
    expires = peewee.IntegerField()
    uid = peewee.IntegerField()

    class Meta:
        database = db


db.connect()
# https://github.com/coleifer/peewee/issues/211
User.create_table(fail_silently=True)
