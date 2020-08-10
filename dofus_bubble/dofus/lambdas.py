import logging
import json
import os
from functools import wraps
from itertools import chain
from enum import Enum

from dofapi.dofapi import Dofapi
from dofus_bubble.dofus.professions import Profession, Professions
# from dofus_bubble.familier.lambdas import LambdasFamilier
# from dofus_bubble.price.lambdas import LambdasPrice
from dofus_bubble.price.dynamodb import PriceDynamoDB
from lambdas.lambdas import Lambdas
from utils import DecimalEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LambdasDofus(Lambdas):
    _DOFAPI = Dofapi()
    _PRICES = PriceDynamoDB()
    # __FAMILIER__ = LambdasFamilier()
    _PROFESSIONS = Professions()

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
        def price(cls, remove=False):
            def decorator(f):
                @wraps(f)
                def wrapper(self, *args, **kwargs):
                    result = f(self, *args, **kwargs)
                    result = self._set_items_price(*result, id=id, **kwargs)
                    if remove:
                        result = self._filter_items_price(result, **kwargs)
                    return result

                return wrapper

            return decorator

    def _find_item(self, **kwargs):
        items, item, on = kwargs.get('items'), kwargs.get('item'), kwargs.get('on', self._DOFAPI.Schema.ID)
        on = on if isinstance(on, list) else [(on, on)]
        return next((i for i in items if all([i.get(id1) == item.get(id2) for id1, id2 in on])), dict())

    def _set_items_price(self, items, prices, **kwargs):
        logger.info('Setting price for all items')
        return [{**item,
                 **self._find_item(items=prices, item=item, **kwargs),
                 **{self._DOFAPI.Schema.RECIPE: [
                     {**v, **self._find_item(items=prices, item=v, on=[(self._DOFAPI.Schema.ID,
                                                                        self._DOFAPI.Schema.ANKAMA_ID)])}
                     for v in list(chain(*[r.values() for r in item.get(self._DOFAPI.Schema.RECIPE)]))]}} for item in
                items]

    def _filter_items_price(self, items, **kwargs):
        # remove, type = kwargs.get('remove'), kwargs.get('type')
        # if remove:
        #     if type == 'craft':
        #         return list(filter(
        #             lambda i: i.get('price') and i.get('recipe') and all([r.get('price') for r in i.get('recipe')]),
        #             items))
        #     if type == 'familiers':
        #         return list(filter(lambda i: i.get('price'), items))
        logger.info('Filtering empty price for all items')
        items = list(filter(lambda i: i.get(self._PRICES.Schema.PRICE), items))
        logger.info('Filtered {count} non empty price items'.format(count=len(items)))
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
            {v[self._DOFAPI.__ID__]: v for v in json.loads(self._scan_items(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return items, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_consumables_price(self, *args, **kwargs):
        consumables = list({v[self._DOFAPI.__ID__]: v for v in
                            json.loads(self.scan_consumables(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return consumables, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_equipments_price(self, *args, **kwargs):
        equipments = list({v[self._DOFAPI.__ID__]: v for v in
                           json.loads(self.scan_equipments(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return equipments, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_idols_price(self, *args, **kwargs):
        idols = list(
            {v[self._DOFAPI.__ID__]: v for v in json.loads(self.scan_idols(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return idols, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_resources_price(self, *args, **kwargs):
        resources = list({v[self._DOFAPI.__ID__]: v for v in
                          json.loads(self.scan_resources(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return resources, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price()
    def scan_weapons_price(self, *args, **kwargs):
        weapons = list(
            {v[self._DOFAPI.__ID__]: v for v in json.loads(self.scan_weapons(*args, **kwargs).get('body'))}.values())
        items_db = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return weapons, items_db

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price(remove=True)
    def scan_familiers_price(self, *args, **kwargs):
        familiers = json.loads(self.__FAMILIER__.scan(*args, **kwargs).get('body')).get('Items')
        prices = json.loads(self._PRICES.scan(*args, **kwargs).get('body')).get('Items')
        return familiers, prices

    @Lambdas.Decorators.payload(id='profession')
    @Decorators.output
    @Decorators.price()
    def _scan_profession_craft(self, *args, **kwargs):
        profession = kwargs.get('path').get('profession')
        result = [r for r in self._DOFAPI.scan(endpoints=self._PROFESSIONS.get(profession).ENDPOINTS, *args, **kwargs)
                  if r.get('recipe') and r.get('type') in self._PROFESSIONS.get(profession).CRAFT]
        prices = self._PRICES.scan(**kwargs).get('Items')
        logger.info('Filtered {count} craft for {profession} profession'.format(count=len(result), profession=profession))
        return result, prices


scan_items_craft = LambdasDofus().scan_items_craft
scan_consumables_price = LambdasDofus().scan_consumables_price
scan_equipments_price = LambdasDofus().scan_equipments_price
scan_idols_price = LambdasDofus().scan_idols_price
scan_resources_price = LambdasDofus().scan_resources_price
scan_weapons_price = LambdasDofus().scan_weapons_price
scan_familiers_price = LambdasDofus().scan_familiers_price
