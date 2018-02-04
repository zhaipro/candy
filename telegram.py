# coding: utf-8
import sys
import time

from telethon import TelegramClient

from settings import TELEGRAM


client = TelegramClient('session_name', TELEGRAM['ID'], TELEGRAM['HASH'], proxy=TELEGRAM['PROXY'])
client.start()
for code in sys.stdin:
    cmd = '/redeem ' + code
    client.send_message('CandyOfficialBot', cmd)
    time.sleep(2)
