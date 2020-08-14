import json
import os
import unittest

from dofus_bubble.familier.lambdas import LambdasFamiliers


class TestFamilier(unittest.TestCase):
    _LAMBDAS_FAMILIERS = LambdasFamiliers()
    __event__ = {'headers': {'origin': 'http://localhost:3000'}, 'body': None, 'pathParameters': None,
                 'queryStringParameters': None}
    __context__ = None
    __mock__ = os.path.dirname(os.getcwd()) + '\mock\\familier\{mock}.json'

    def _test_response(self, result):
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)

    def test_batch_put(self):
        with open(self.__mock__.format(mock='batch_put_small'), "r", encoding="utf8") as mock:
            self.__event__['body'] = json.dumps(json.loads(mock.read()).get('body'))
        result = self._LAMBDAS_FAMILIERS.batch_put(self.__event__, self.__context__)
        self._test_response(result)
        self.assertIsInstance(result.get('body'), str)

