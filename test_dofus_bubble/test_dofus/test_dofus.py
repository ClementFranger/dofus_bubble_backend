import json
import unittest

from dofus_bubble.dofus.lambdas import LambdasDofus


class TestDofus(unittest.TestCase):
    __DYNAMODB_TABLE__ = 'dofus-bubble'
    __event__ = {'headers': {'origin': 'http://localhost:3000'}, 'body': None, 'pathParameters': None, 'queryStringParameters': None}
    __context__ = None

    def _test_response(self, result):
        body = json.loads(result.get('body'))
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)
        [self.assertIsInstance(i, dict) for i in body]
        self.assertEqual(body, list({v['_id']: v for v in body}.values()))

    def test_scan_items_craft(self):
        result = LambdasDofus().scan_items_craft(self.__event__, self.__context__, DYNAMODB_TABLE=self.__DYNAMODB_TABLE__)
        self.assertIsInstance(result.get('body'), str)
        self._test_response(result)
