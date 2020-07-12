import json
from functools import wraps
from itertools import chain

from dofus_bubble.dofapi.lambdas import LambdasDofapi
from dofus_bubble.price.lambdas import LambdasPrice
from lambdas.lambdas import Lambdas
from utils import DecimalEncoder


class LambdasDofus(LambdasDofapi):
    __PRICE__ = LambdasPrice()

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
            def wrapper(self, *args, **kwargs):
                result = f(self, *args, **kwargs)
                result = self._set_items_price(*result, **kwargs)
                result = LambdasDofus._filter_items_price(result, **kwargs)
                result = LambdasDofus._compute_items_craft(result, **kwargs)
                return sorted(result, key=lambda i: i.get('price') - i.get('craft'), reverse=True)
            return wrapper

        @classmethod
        def price(cls, f):
            @wraps(f)
            def wrapper(self, *args, **kwargs):
                result = f(self, *args, **kwargs)
                result = self._set_items_price(*result, **kwargs)
                result = LambdasDofus._filter_items_price(result, remove=False, **kwargs)
                return result
            return wrapper

    def _find_item(self, **kwargs):
        items, id = kwargs.get('items'), kwargs.get('id')
        return next((item for item in items if item.get(self.__DOFAPI__.__ID__) == id), dict())

    def _set_items_price(self, dofapi, dynamodb, **kwargs):
        return [{**item,
                 **self._find_item(items=dynamodb, id=item.get('_id')),
                 **{'recipe': [{**v, **self._find_item(items=dynamodb, id=v.get('ankamaId'))}
                               for v in list(chain(*[r.values() for r in item.get('recipe')]))]}} for item in dofapi]

    @staticmethod
    def _filter_items_price(items, **kwargs):
        if kwargs.get('remove', True):
            return list(filter(lambda i: i.get('price') and i.get('recipe') and all([r.get('price') for r in i.get('recipe')]), items))
        return items

    @staticmethod
    def _compute_items_craft(items, **kwargs):
        return [{**item,
                 **{'craft': sum([r.get('price') * r.get('quantity') for r in item.get('recipe')])}} for item in items]

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Lambdas.Decorators.limit()
    @Decorators.craft
    def scan_items_craft(self, *args, **kwargs):
        items = list(
            {v[self.__DOFAPI__.__ID__]: v for v in json.loads(self._scan_items(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return items, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_consumables_price(self, *args, **kwargs):
        consumables = list({v[self.__DOFAPI__.__ID__]: v for v in
                            json.loads(self.scan_consumables(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return consumables, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_equipments_price(self, *args, **kwargs):
        equipments = list({v[self.__DOFAPI__.__ID__]: v for v in
                           json.loads(self.scan_equipments(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return equipments, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_idols_price(self, *args, **kwargs):
        idols = list(
            {v[self.__DOFAPI__.__ID__]: v for v in json.loads(self.scan_idols(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return idols, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_resources_price(self, *args, **kwargs):
        resources = list({v[self.__DOFAPI__.__ID__]: v for v in
                          json.loads(self.scan_resources(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return resources, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price
    def scan_weapons_price(self, *args, **kwargs):
        weapons = list(
            {v[self.__DOFAPI__.__ID__]: v for v in json.loads(self.scan_weapons(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return weapons, items_db


scan_items_craft = LambdasDofus().scan_items_craft
scan_consumables_price = LambdasDofus().scan_consumables_price
scan_equipments_price = LambdasDofus().scan_equipments_price
scan_idols_price = LambdasDofus().scan_idols_price
scan_resources_price = LambdasDofus().scan_resources_price
scan_weapons_price = LambdasDofus().scan_weapons_price
