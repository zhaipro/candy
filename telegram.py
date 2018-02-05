# coding: utf-8
from telethon import TelegramClient

from settings import TELEGRAM


client = TelegramClient('session_name', TELEGRAM['ID'], TELEGRAM['HASH'], proxy=TELEGRAM['PROXY'])
client.start()


def send_code(code):
    cmd = '/redeem ' + code
    client.send_message('CandyOfficialBot', cmd)
