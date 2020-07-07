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
    def scan_weapons(*args, **kwargs):
        return Dofapi().scan_weapons()


scan_weapons = LambdasDofapi().scan_weapons
