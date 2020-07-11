import json
from functools import wraps, reduce
from itertools import chain

from dofus_bubble.dofapi.lambdas import Dofapi, LambdasDofapi
from dofus_bubble.dynamodb.lambdas import LambdasDynamoDB
from lambdas.lambdas import Lambdas
from utils import DecimalEncoder


class LambdasDofus(LambdasDofapi):

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                return {'statusCode': 200, 'headers': kwargs.get('headers'), 'body': json.dumps(result, cls=DecimalEncoder)}
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

        @classmethod
        def price(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                result = LambdasDofus._merge_items_price(*result, remove=False)
                return result
            return wrapper

    @staticmethod
    def _find_item(**kwargs):
        items, id = kwargs.get('items'), kwargs.get('id')
        return next((item for item in items if item.get(Dofapi.__ID__) == id), dict())

    @staticmethod
    def _reduce_craft(**kwargs):
        def compute_craft(r):
            return int(r.get('quantity')) * int(LambdasDofus._find_item(items=items, id=r.get(Dofapi.__ANKAMA_ID__)).get('price'))

        items, recipe = kwargs.get('items'), kwargs.get('recipe')
        return reduce(lambda a, b: compute_craft(a) + compute_craft(b), recipe)

    @staticmethod
    def _merge_items_price(dofapi, dynamodb, **kwargs):
        if kwargs.get('remove', True):
            return [{**w, **i} for i in dynamodb for w in dofapi if w.get(Dofapi.__ID__) == i.get(Dofapi.__ID__)]
        [LambdasDofus._find_item(items=dofapi, id=i.get('_id')).update(i) for i in dynamodb if LambdasDofus._find_item(items=dofapi, id=i.get('_id'))]
        return dofapi

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
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Lambdas.Decorators.limit()
    @Decorators.craft
    def scan_items_craft(*args, **kwargs):
        items = list({v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus._scan_items(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return items, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_consumables_price(*args, **kwargs):
        consumables = list({v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_consumables(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return consumables, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_equipments_price(*args, **kwargs):
        equipments = list({v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_equipments(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return equipments, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_idols_price(*args, **kwargs):
        idols = list({v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_idols(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return idols, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_resources_price(*args, **kwargs):
        resources = list({v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_resources(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return resources, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_weapons_price(*args, **kwargs):
        weapons = list({v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_weapons(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return weapons, items_db


scan_items_craft = LambdasDofus().scan_items_craft
scan_consumables_price = LambdasDofus().scan_consumables_price
scan_equipments_price = LambdasDofus().scan_equipments_price
scan_idols_price = LambdasDofus().scan_idols_price
scan_resources_price = LambdasDofus().scan_resources_price
scan_weapons_price = LambdasDofus().scan_weapons_price
