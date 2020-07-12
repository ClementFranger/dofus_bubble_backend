import json
from functools import wraps

from lambdas.lambdas import Lambdas
from dofapi.dofapi import Dofapi


class LambdasDofapi(Lambdas):

    def __init__(self):
        self.__DOFAPI__ = Dofapi()

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                if isinstance(result, dict) and result.get('error'):
                    return result.get('error')
                return {'statusCode': 200, 'headers': kwargs.get('headers'), 'body': json.dumps(result)}
            return wrapper

    @Decorators.output
    def scan_consumables(self, *args, **kwargs):
        return self.__DOFAPI__.scan_consumables()

    @Decorators.output
    def scan_equipments(self, *args, **kwargs):
        return self.__DOFAPI__.scan_equipments()

    @Decorators.output
    def scan_idols(self, *args, **kwargs):
        return self.__DOFAPI__.scan_idols()

    @Decorators.output
    def scan_resources(self, *args, **kwargs):
        return self.__DOFAPI__.scan_resources()

    @Decorators.output
    def scan_weapons(self, *args, **kwargs):
        return self.__DOFAPI__.scan_weapons()

    @Decorators.output
    def _scan_items(self, *args, **kwargs):
        return self.__DOFAPI__._scan_items()


scan_consumables = LambdasDofapi().scan_consumables
scan_equipments = LambdasDofapi().scan_equipments
scan_idols = LambdasDofapi().scan_idols
scan_resources = LambdasDofapi().scan_resources
scan_weapons = LambdasDofapi().scan_weapons
_scan_items = LambdasDofapi()._scan_items
