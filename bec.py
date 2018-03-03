# coding: utf-8
import re

import requests

import utils


def invite(invite_id, address):
    url = 'https://referral.beauty.io/' + invite_id
    data = {
        'address': address,
    }
    r = utils.post(requests, url, data)
    # $('#j-code')[0].value
    regex = '<input readonly id="j-code" type="text" value="(/[0-9a-zA-Z]+)">'
    return re.search(regex, r.text).group(1)
