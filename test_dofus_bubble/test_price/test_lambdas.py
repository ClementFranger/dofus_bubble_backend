import json
import os
import unittest

from dofus_bubble.price.lambdas import LambdasPrices


class TestPrice(unittest.TestCase):
    _LAMBDAS_PRICES = LambdasPrices()
    __event__ = {'headers': {'origin': 'http://localhost:3000'}, 'body': None, 'pathParameters': None,
                 'queryStringParameters': None}
    __context__ = None
    __mock__ = os.path.dirname(os.getcwd()) + '\mock\price\{mock}.json'

    def _test_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)

    def test_put(self):
        with open(self.__mock__.format(mock='put'), "r") as mock:
            self.__event__['body'] = json.dumps(json.loads(mock.read()).get('body'))
        result = self._LAMBDAS_PRICES.put(self.__event__, self.__context__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

    def test_get(self):
        with open(self.__mock__.format(mock='get'), "r") as mock:
            self.__event__['pathParameters'] = json.loads(mock.read()).get('pathParameters')
        result = self._LAMBDAS_PRICES.get(self.__event__, self.__context__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

    def test_scan(self):
        result = self._LAMBDAS_PRICES.scan(self.__event__, self.__context__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

