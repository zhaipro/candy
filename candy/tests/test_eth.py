# coding: utf-8
import unittest

import eth_utils

import eth


class Test(unittest.TestCase):

    def test_gen_account(self):
        # 随机生成的地址必须带有校验和
        address, password = eth.utils.gen_account()
        self.assertTrue(eth_utils.is_checksum_address(address))

    def test_key_to_address(self):
        # 必须返回带有校验和的地址
        key = '0xa676a1eb74b7958b6be2c02e72d2616b2b6885684f71baf25f349b557215402b'
        address = eth.utils.key_to_address(key)
        self.assertTrue(eth_utils.is_checksum_address(address))

    def test_to_wei(self):
        self.assertEqual(eth.utils.ether_to_wei(1), 1e18)
        self.assertEqual(eth.utils.gwei_to_wei(1), 1e9)
        self.assertIsInstance(eth.utils.ether_to_wei(0.00009), int)
        self.assertIsInstance(eth.utils.gwei_to_wei(1.5), int)

    # 下面的测试需要联网
    def test_web3_is_connected(self):
        self.assertTrue(eth.web3.w3.isConnected())

    def test_get_balance(self):
        balance = eth.web3.get_balance('0x7C2Ac866F763ABC1200e2d0E7Bf475b71cc47663')
        self.assertEqual(balance, eth.utils.ether_to_wei(0.00005649))

    def test_get_token_balance(self):
        token = '0xC5d105E63711398aF9bbff092d4B6769C82F793D'
        address = '0x2d427eb47EbBf2Bb7c3BBFD30222D072634Ea6a2'
        balance = eth.web3.get_token_balance(token, address)
        self.assertEqual(balance, eth.utils.ether_to_wei(5))
