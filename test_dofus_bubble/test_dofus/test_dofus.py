import unittest

from dofus_bubble.dofus.scan_weapons_by_price import scan_weapons_by_price


class TestDofapi(unittest.TestCase):
    __event__ = {'body': None, 'pathParameters': None, 'queryStringParameters': None}
    __context__ = None

    def test_scan_weapons_by_price(self):
        result = scan_weapons_by_price(self.__event__, self.__context__)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)