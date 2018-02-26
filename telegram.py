# coding: utf-8
from telethon import TelegramClient

import utils
from settings import TELEGRAM


client = TelegramClient('telegram', TELEGRAM['ID'], TELEGRAM['HASH'], proxy=TELEGRAM['PROXY'])
client.start()


def send_code(enity, code):
    client.send_message(enity, code)
    utils.log('telegram.send_message(enity=%r, code=%r)', enity, code)
