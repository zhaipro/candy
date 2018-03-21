# coding: utf-8
import eth_utils
import requests

import utils


def create_wallet(address, idfa='00000000-0000-0000-0000-000000000000'):
    address = eth_utils.to_checksum_address(address)
    url = 'https://api.bec.com/wallet/create.json'
    data = {
        'address': address,     # 0x87909eEA49982A966A168Ee2B7A51AE524FAaDb5
        'app_version': '1.2.1',
        'chain_addr': address,
        'chain_type': 2,
        'gid': 447635452,
        'gid_status': 1,
        'idfa': idfa,
        'idfv': 'EABEF850-5741-467C-A41A-2D2DF8097772',
        'language': 'zh-Hans',
        'model': 'iPhone8,1',
        'os_type': 'iOS',
        'os_version': '11.1.1',
        'type': 2,
    }
    ua = 'BECWallet/1.2.1 (bec.meitu.wallet; build:1.2.17; iOS 11.1.1) Alamofire/4.6.0'
    headers = {'User-Agent': ua}
    return utils.post(requests, url, data, headers=headers)
