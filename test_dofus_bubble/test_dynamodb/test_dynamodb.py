import json
import os
import unittest

from dofus_bubble.dynamodb.lambdas import get_item, put_item, scan_items


class TestDynamoDB(unittest.TestCase):
    __DYNAMODB_TABLE__ = 'dofus-bubble'
    __event__ = {'headers': {'origin': 'http://localhost:3000'}, 'body': None, 'pathParameters': None,
                 'queryStringParameters': None}
    __context__ = None
    __mock__ = os.path.dirname(os.getcwd()) + '\mock\dynamodb\{mock}.json'

    def _test_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)

    def test_put_item(self):
        with open(self.__mock__.format(mock='put_item'), "r") as mock:
            self.__event__['body'] = json.dumps(json.loads(mock.read()).get('body'))
        result = put_item(self.__event__, self.__context__, DYNAMODB_TABLE=self.__DYNAMODB_TABLE__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

    def test_get_item(self):
        with open(self.__mock__.format(mock='get_item'), "r") as mock:
            self.__event__['pathParameters'] = json.loads(mock.read()).get('pathParameters')
        result = get_item(self.__event__, self.__context__, DYNAMODB_TABLE=self.__DYNAMODB_TABLE__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

    def test_scan_items(self):
        result = scan_items(self.__event__, self.__context__, DYNAMODB_TABLE=self.__DYNAMODB_TABLE__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

