import unittest

from dofus_bubble.dofapi.lambdas import scan_weapons


class TestDofapi(unittest.TestCase):
    __event__ = {'body': None, 'pathParameters': None, 'queryStringParameters': None}
    __context__ = None

    def test_scan_weapons(self):
        result = scan_weapons(self.__event__, self.__context__)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('statusCode'), 200)
