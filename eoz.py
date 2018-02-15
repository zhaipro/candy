# coding: utf-8
import random
import re

import requests

import settings
import utils


def _get_captcha(session):
    url = 'http://eoz.one/user/captcha?refresh=1'
    r = utils.get(session, url)
    url = r.json()['url']
    url = 'http://eoz.one' + url
    r = utils.get(session, url)
    return utils.ocr(r.content)


def get_captcha(session):
    while True:
        captcha = _get_captcha(session)
        if len(captcha) == 4 and captcha.isalpha():
            return captcha


def register(invite, phone):
    session = requests.Session()
    url = 'http://eoz.one/i/%s' % invite
    utils.get(session, url, allow_redirects=False)
    while True:
        captcha = get_captcha(session)
        url = 'http://eoz.one/user/register'
        data = {
            'RegisterForm[countrycode]': 'cn',
            'RegisterForm[dialcode]': '86',
            'RegisterForm[password]': settings.PASSWORD,
            'RegisterForm[password2]': settings.PASSWORD,
            'RegisterForm[tel_number]': phone,
            'RegisterForm[verifyCode]': captcha,
        }
        response = utils.post(session, url, data)
        if u'验证码错误' not in response.text:
            response = utils.get(session, 'http://eoz.one/user/invite')
            return re.search('http://eoz.one/i/(\d+)', response.text).group(1)


def main():
    invites = [(settings.EOZ['INVITE'], 0)]
    while True:
        try:
            phone = random.randint(18500000000, 18599999999)
            invite, level = random.choice(invites)
            invite = register(invite, phone)
            level += 1
            if level < 6:
                invites.append((invite, level))
            utils.log('eoz\tfake\t%s\t%s\t%s', phone, invite, level)
        except Exception as e:
            utils.log('Error: %s\t%s', e, phone)

if __name__ == '__main__':
    main()
