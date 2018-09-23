# coding: utf-8
import unittest

import eth
import utils


class TestUtils(unittest.TestCase):

    def test_now(self):
        utils.now()


class TestEth(unittest.TestCase):

    def test_key_to_address(self):
        # 必须返回带有校验和的地址
        key = '0xa676a1eb74b7958b6be2c02e72d2616b2b6885684f71baf25f349b557215402b'
        address = '0x68B6853a780EFe36275219fe7298c23192AEcD01'
        self.assertEqual(eth.key_to_address(key), address)

    def test_to_wei(self):
        self.assertEqual(eth.ether_to_wei(1), 1e18)
        self.assertEqual(eth.gwei_to_wei(1), 1e9)
        self.assertIsInstance(eth.ether_to_wei(0.00009), int)
        self.assertIsInstance(eth.gwei_to_wei(1.5), int)
