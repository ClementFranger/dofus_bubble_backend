import json
from functools import wraps
from itertools import chain
from enum import Enum

from dofapi.dofapi import Dofapi
from dofus_bubble.familier.lambdas import LambdasFamilier
from dofus_bubble.price.lambdas import LambdasPrice
from lambdas.lambdas import Lambdas
from utils import DecimalEncoder


class LambdasDofus(Lambdas):
    __DOFAPI__ = Dofapi()
    __PRICE__ = LambdasPrice()
    __FAMILIER__ = LambdasFamilier()

    class Professions(Enum):
        ALCHIMIE = 'Alchimie'
        FORGERON = 'Forgeron'
        SCULPTEUR = 'Sculpteur'

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
        def craft(cls, id='_id', type='craft', remove=True):
            def decorator(f):
                @wraps(f)
                def wrapper(self, *args, **kwargs):
                    result = f(self, *args, **kwargs)
                    result = self._set_items_price(*result, id=id, type=type, **kwargs)
                    result = LambdasDofus._filter_items_price(result, remove=remove, type=type, **kwargs)
                    result = LambdasDofus._compute_items_craft(result, **kwargs)
                    return sorted(result, key=lambda i: i.get('price') - i.get('craft'), reverse=True)
                return wrapper
            return decorator

        @classmethod
        def price(cls, id='_id', type='items', remove=False):
            def decorator(f):
                @wraps(f)
                def wrapper(self, *args, **kwargs):
                    result = f(self, *args, **kwargs)
                    result = self._set_items_price(*result, id=id, type=type, **kwargs)
                    result = LambdasDofus._filter_items_price(result, remove=remove, type=type, **kwargs)
                    return result
                return wrapper
            return decorator

    def _find_item(self, **kwargs):
        items, item, id = kwargs.get('items'), kwargs.get('item'), kwargs.get('id')
        id1, id2 = (id.get('id1'), id.get('id2')) if isinstance(id, dict) else (id, id)
        return next((i for i in items if i.get(id1) == item.get(id2)), dict())

    def _set_items_price(self, items, dynamodb, **kwargs):
        id, type = kwargs.get('id', self.__DOFAPI__.__ID__), kwargs.get('type')
        if type == 'craft':
            return [{**item,
                     **self._find_item(items=dynamodb, item=item, id=id),
                     **{'recipe': [{**v, **self._find_item(items=dynamodb, item=v, id={'id1': self.__DOFAPI__.__ID__,
                                                                                       'id2': self.__DOFAPI__.__ANKAMA_ID__})}
                                   for v in list(chain(*[r.values() for r in item.get('recipe')]))]}} for item in items]
        return [{**item, **self._find_item(items=dynamodb, item=item, id=id)} for item in items]

    @staticmethod
    def _filter_items_price(items, **kwargs):
        remove, type = kwargs.get('remove'), kwargs.get('type')
        if remove:
            if type == 'craft':
                return list(filter(lambda i: i.get('price') and i.get('recipe') and all([r.get('price') for r in i.get('recipe')]), items))
            if type == 'familiers':
                return list(filter(lambda i: i.get('price'), items))
        return items

    @staticmethod
    def _compute_items_craft(items, **kwargs):
        return [{**item,
                 **{'craft': sum([r.get('price') * r.get('quantity') for r in item.get('recipe')])}} for item in items]

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Lambdas.Decorators.limit(length=100)
    @Decorators.craft()
    def scan_items_craft(self, *args, **kwargs):
        items = list(
            {v[self.__DOFAPI__.__ID__]: v for v in json.loads(self._scan_items(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return items, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_consumables_price(self, *args, **kwargs):
        consumables = list({v[self.__DOFAPI__.__ID__]: v for v in
                            json.loads(self.scan_consumables(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return consumables, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_equipments_price(self, *args, **kwargs):
        equipments = list({v[self.__DOFAPI__.__ID__]: v for v in
                           json.loads(self.scan_equipments(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return equipments, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_idols_price(self, *args, **kwargs):
        idols = list(
            {v[self.__DOFAPI__.__ID__]: v for v in json.loads(self.scan_idols(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return idols, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_resources_price(self, *args, **kwargs):
        resources = list({v[self.__DOFAPI__.__ID__]: v for v in
                          json.loads(self.scan_resources(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return resources, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_weapons_price(self, *args, **kwargs):
        weapons = list(
            {v[self.__DOFAPI__.__ID__]: v for v in json.loads(self.scan_weapons(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return weapons, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price(id='name', type='familiers', remove=True)
    def scan_familiers_price(self, *args, **kwargs):
        familiers = json.loads(self.__FAMILIER__.scan(*args, **kwargs).get('body')).get('Items')
        prices = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        return familiers, prices

    @Lambdas.Decorators.payload(id='profession')
    def scan_profession_craft(self, **kwargs):
        print(kwargs)
        return


scan_items_craft = LambdasDofus().scan_items_craft
scan_consumables_price = LambdasDofus().scan_consumables_price
scan_equipments_price = LambdasDofus().scan_equipments_price
scan_idols_price = LambdasDofus().scan_idols_price
scan_resources_price = LambdasDofus().scan_resources_price
scan_weapons_price = LambdasDofus().scan_weapons_price
scan_familiers_price = LambdasDofus().scan_familiers_price
