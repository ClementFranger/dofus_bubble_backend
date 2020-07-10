from functools import wraps, reduce
from itertools import chain

from dofus_bubble.dofapi.lambdas import Dofapi, LambdasDofapi
from dofus_bubble.dynamodb.lambdas import LambdasDynamoDB
from lambdas.lambdas import Lambdas


class LambdasDofus(LambdasDofapi):

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                return {'statusCode': 200, 'headers': kwargs.get('headers'), 'body': result}
            return wrapper

        @classmethod
        def craft(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                result = LambdasDofus._merge_items_price(*result)
                result = LambdasDofus.filter_items_recipe(result)
                result = LambdasDofus.compute_items_craft(result)
                return sorted(result, key=lambda i: i.get('price') - i.get('craft'), reverse=True)
            return wrapper

    @staticmethod
    def _find_item(**kwargs):
        items, id = kwargs.get('items'), kwargs.get('id')
        return next((item for item in items if item.get(Dofapi.__ID__) == id), dict())

    @staticmethod
    def _reduce_craft(**kwargs):
        def compute_craft(r):
            return r.get('quantity') * LambdasDofus._find_item(items=items, id=r.get(Dofapi.__ANKAMA_ID__)).get('price')

        items, recipe = kwargs.get('items'), kwargs.get('recipe')
        return reduce(lambda a, b: compute_craft(a) + compute_craft(b), recipe)

    @staticmethod
    def _merge_items_price(dofapi, dynamodb):
        return [{**w, **i} for i in dynamodb for w in dofapi if w.get(Dofapi.__ID__) == i.get(Dofapi.__ID__)]

    @staticmethod
    def filter_items_recipe(items):
        return [i for i in items if all(
            v.get(Dofapi.__ANKAMA_ID__) in set([item.get(Dofapi.__ANKAMA_ID__) for item in items]) for v in
            list(chain(*[r.values() for r in i.get('recipe')])))]

    @staticmethod
    def compute_items_craft(items):
        return [{**i, **{
            'craft': LambdasDofus._reduce_craft(items=items, recipe=list(chain(*[r.values() for r in i.get('recipe')])))}} for i
                in items if i.get('recipe')]

    @staticmethod
    @Decorators.output
    @Decorators.craft
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    def scan_items_craft(*args, **kwargs):
        items = list({v['_id']: v for v in LambdasDofus._scan_items(*args, **kwargs).get('body')}.values())
        items_db = LambdasDynamoDB.scan_items(*args, **kwargs).get('body').get('Items')
        return items, items_db


scan_items_craft = LambdasDofus().scan_items_craft
