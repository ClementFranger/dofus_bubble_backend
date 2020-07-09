import unittest

from dofus_bubble.dofapi.lambdas import LambdasDofapi


class TestDofapi(unittest.TestCase):
    __event__ = {'body': None, 'pathParameters': None, 'queryStringParameters': None}
    __context__ = None

    def _test_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)
        [self.assertIsInstance(i, dict) for i in result.get('body')]
        self.assertEqual(result.get('body'), list({v['_id']: v for v in result.get('body')}.values()))

    def test_scan_consumables(self):
        result = LambdasDofapi.scan_consumables(self.__event__, self.__context__)
        self._test_response(result)

    def test_scan_equipments(self):
        result = LambdasDofapi.scan_equipments(self.__event__, self.__context__)
        self._test_response(result)

    def test_scan_idols(self):
        result = LambdasDofapi.scan_idols(self.__event__, self.__context__)
        self._test_response(result)

    def test_scan_resources(self):
        result = LambdasDofapi.scan_resources(self.__event__, self.__context__)
        self._test_response(result)

    def test_scan_weapons(self):
        result = LambdasDofapi.scan_weapons(self.__event__, self.__context__)
        self._test_response(result)

    def test_scan_items(self):
        result = LambdasDofapi.scan_items(self.__event__, self.__context__)
        self._test_response(result)
