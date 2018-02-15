# coding: utf-8
import eth_utils
import requests

import settings
import utils


def create_wallet(address):
    # 接口里使用了校验和地址，这里如此处理，用于反防作弊
    address = eth_utils.to_checksum_address(address)
    url = 'https://api.bec.com/wallet/create.json'
    data = {
        'address': address,
        'app_version': '1.2.1',
        'chain_addr': address,
        'chain_type': 2,
        'gid': 447635452,
        'gid_status': 1,
        'idfa': utils.gen_uuid(),
        'idfv': utils.gen_uuid(),     # 0042B207-FE18-4FE9-A66A-A4BF318B78A5
        'language': 'zh-Hans',
        'model': 'iPhone8,1',
        'os_type': 'iOS',
        'os_version': '11.1.1',
        'type': 2,
    }
    ua = 'BECWallet/1.2.1 (bec.meitu.wallet; build:1.2.17; iOS 11.1.1) Alamofire/4.6.0'
    headers = {'User-Agent': ua}
    # 戴Tor访问，用于反防作弊
    return utils.post(requests, url, data, headers=headers, proxies=settings.TOR)
