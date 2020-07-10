from functools import wraps

from lambdas.lambdas import Lambdas
from dofapi.dofapi import Dofapi


class LambdasDofapi(Lambdas):

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                if isinstance(result, dict) and result.get('error'):
                    return result.get('error')
                return {'statusCode': 200, 'body': result}
            return wrapper

    @staticmethod
    @Decorators.output
    def scan_consumables(*args, **kwargs):
        return Dofapi().scan_consumables()

    @staticmethod
    @Decorators.output
    def scan_equipments(*args, **kwargs):
        return Dofapi().scan_equipments()

    @staticmethod
    @Decorators.output
    def scan_idols(*args, **kwargs):
        return Dofapi().scan_idols()

    @staticmethod
    @Decorators.output
    def scan_resources(*args, **kwargs):
        return Dofapi().scan_resources()

    @staticmethod
    @Decorators.output
    def scan_weapons(*args, **kwargs):
        return Dofapi().scan_weapons()

    @staticmethod
    @Decorators.output
    def _scan_items(*args, **kwargs):
        return Dofapi()._scan_items()


scan_consumables = LambdasDofapi().scan_consumables
scan_equipments = LambdasDofapi().scan_equipments
scan_idols = LambdasDofapi().scan_idols
scan_resources = LambdasDofapi().scan_resources
scan_weapons = LambdasDofapi().scan_weapons
_scan_items = LambdasDofapi()._scan_items
