# coding: utf-8
import re

import requests
import socks


def validate(proxy, url='https://telegram.org/'):
    proxies = {'https': proxy}
    try:
        requests.get(url, timeout=7, proxies=proxies)
        return True
    except Exception:   # requests.exceptions.ConnectionError
        return False    # socks模块有问题


def get_socks5():
    url = 'https://tool.ssrshare.com/tool/free_s5'
    r = requests.get(url, timeout=7)
    key = re.search("var subkey = '(.+)';", r.text).group(1)
    url = 'https://tool.ssrshare.com/tool/api/free_s5'
    r = requests.get(url, {'key': key}, timeout=7)
    '''
    [{
        "m_station_cn_status": "true",
        "server": "45.55.27.17",
        "server_port": 1080,
        "status": "true"
    }]
    '''
    proxies = r.json()
    for proxy in proxies:
        # 使用get方法，防御一下
        status = proxy.get('status') == 'true' and proxy.get('m_station_cn_status') == 'true'
        proxy = 'socks5://%s:%s' % (proxy['server'], proxy['server_port'])
        if status and validate(proxy):
            yield proxy


def parser_proxy(proxy):
    addr, port = re.match('socks5://(.+):(.+)', proxy).groups()
    return socks.SOCKS5, addr, port
