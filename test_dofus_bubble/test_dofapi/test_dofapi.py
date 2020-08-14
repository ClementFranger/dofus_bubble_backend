import logging
import unittest

from dofapi.dofapi import Dofapi

logging.basicConfig(level=logging.INFO)


class TestDofapi(unittest.TestCase):
    _DOFAPI = Dofapi()
    __event__ = {'body': None, 'pathParameters': None, 'queryStringParameters': None}
    __context__ = None

    def _test_response(self, result):
        [self.assertIsInstance(i, dict) for i in result]
        self.assertEqual(result, list({v[self._DOFAPI.Schema.ID]: v for v in result}.values()))

    def test_scan(self):
        result = self._DOFAPI.scan(endpoints=[self._DOFAPI.Schema.EQUIPMENTS])
        self._test_response(result)
