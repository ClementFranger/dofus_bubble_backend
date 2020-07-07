import unittest

from dofus_bubble.dofus.lambdas import scan_weapons_by_price


class TestDofus(unittest.TestCase):
    __DYNAMODB_TABLE__ = 'dofus-bubble'
    __event__ = {'body': None, 'pathParameters': None, 'queryStringParameters': None}
    __context__ = None

    def test_scan_weapons_by_price(self):
        result = scan_weapons_by_price(self.__event__, self.__context__,DYNAMODB_TABLE=self.__DYNAMODB_TABLE__)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)
