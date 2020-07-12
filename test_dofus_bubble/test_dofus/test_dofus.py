import json
import unittest

from dofus_bubble.dofus.lambdas import LambdasDofus


class TestDofus(unittest.TestCase):
    __event__ = {'headers': {'origin': 'http://localhost:3000'}, 'body': None, 'pathParameters': None,
                 'queryStringParameters': None}
    __context__ = None

    def _test_response(self, result):
        body = json.loads(result.get('body'))
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)
        [self.assertIsInstance(i, dict) for i in body]
        self.assertEqual(body, list({v['_id']: v for v in body}.values()))

    def test_scan_items_craft(self):
        result = LambdasDofus().scan_items_craft(self.__event__, self.__context__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)

    def test_scan_consumables_price(self):
        result = LambdasDofus().scan_consumables_price(self.__event__, self.__context__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)

    def test_scan_equipments_price(self):
        result = LambdasDofus().scan_equipments_price(self.__event__, self.__context__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)

    def test_scan_idols_price(self):
        result = LambdasDofus().scan_idols_price(self.__event__, self.__context__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)

    def test_scan_resources_price(self):
        result = LambdasDofus().scan_resources_price(self.__event__, self.__context__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)

    def test_scan_weapons_price(self):
        result = LambdasDofus().scan_weapons_price(self.__event__, self.__context__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)
