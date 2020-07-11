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
                return {'statusCode': 200, 'headers': kwargs.get('headers'),
                        'body': json.dumps(result, cls=DecimalEncoder)}

            return wrapper

        @classmethod
        def craft(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                result = LambdasDofus._set_items_price(*result, **kwargs)
                result = LambdasDofus._filter_items_price(result, **kwargs)
                result = LambdasDofus.compute_items_craft(result, **kwargs)
                return result

            return wrapper

        @classmethod
        def price(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                result = LambdasDofus._set_items_price(*result, **kwargs)
                result = LambdasDofus._filter_items_price(result, remove=False, **kwargs)
                return result

            return wrapper

    @staticmethod
    def _find_item(**kwargs):
        items, id = kwargs.get('items'), kwargs.get('id')
        return next((item for item in items if item.get(Dofapi.__ID__) == id), dict())

    @staticmethod
    def _set_items_price(dofapi, dynamodb, **kwargs):
        return [{**item,
                 **LambdasDofus._find_item(items=dynamodb, id=item.get('_id')),
                 **{'recipe': [{**v, **LambdasDofus._find_item(items=dynamodb, id=v.get('ankamaId'))}
                               for v in list(chain(*[r.values() for r in item.get('recipe')]))]}} for item in dofapi]

    @staticmethod
    def _filter_items_price(items, **kwargs):
        if kwargs.get('remove', True):
            return list(filter(lambda i: i.get('price') and i.get('recipe') and all([r.get('price') for r in i.get('recipe')]), items))
        return items

    @staticmethod
    def compute_items_craft(items, **kwargs):
        return [{**item,
                 **{'craft': sum([r.get('price') * r.get('quantity') for r in item.get('recipe')])}} for item in items]

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Lambdas.Decorators.limit()
    @Decorators.craft
    def scan_items_craft(*args, **kwargs):
        items = list(
            {v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus._scan_items(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return items, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_consumables_price(*args, **kwargs):
        consumables = list({v[Dofapi.__ID__]: v for v in
                            json.loads(LambdasDofus.scan_consumables(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return consumables, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_equipments_price(*args, **kwargs):
        equipments = list({v[Dofapi.__ID__]: v for v in
                           json.loads(LambdasDofus.scan_equipments(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return equipments, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_idols_price(*args, **kwargs):
        idols = list(
            {v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_idols(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return idols, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_resources_price(*args, **kwargs):
        resources = list({v[Dofapi.__ID__]: v for v in
                          json.loads(LambdasDofus.scan_resources(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return resources, items_db

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_weapons_price(*args, **kwargs):
        weapons = list(
            {v[Dofapi.__ID__]: v for v in json.loads(LambdasDofus.scan_weapons(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(LambdasDynamoDB.scan_items(*args, **kwargs).get('body')).get('Items')
        return weapons, items_db


scan_items_craft = LambdasDofus().scan_items_craft
scan_consumables_price = LambdasDofus().scan_consumables_price
scan_equipments_price = LambdasDofus().scan_equipments_price
scan_idols_price = LambdasDofus().scan_idols_price
scan_resources_price = LambdasDofus().scan_resources_price
scan_weapons_price = LambdasDofus().scan_weapons_price
