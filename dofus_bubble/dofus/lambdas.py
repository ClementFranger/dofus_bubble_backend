import logging
import json
from functools import wraps, reduce

from dofapi.dofapi import Dofapi
from dofus_bubble.dofus.professions import Professions
from dofus_bubble.familier.dynamodb import Familiers
from dofus_bubble.price.dynamodb import Prices
from lambdas.lambdas import Lambdas
from utils import DecimalEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LambdasDofus(Lambdas):
    _DOFAPI = Dofapi()
    _PRICES = Prices()
    _FAMILIERS = Familiers()
    _PROFESSIONS = Professions()

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
        def price(cls, remove=False, recipe=False, profit=False):
            def decorator(f):
                @wraps(f)
                def wrapper(self, *args, **kwargs):
                    result = f(self, *args, **kwargs)
                    result = self._set_items_price(*result, recipe=recipe, **kwargs)
                    if remove:
                        result = self._filter_items_price(result, **kwargs)
                    if profit:
                        result = self._set_items_profit(result, **kwargs)
                    return result

                return wrapper

            return decorator

    def _set_items_price(self, items, prices, id, **kwargs):
        recipe = kwargs.get('recipe', False)
        d_prices, d_prices_recipe = {d[id]: d for d in prices}, {d[self._DOFAPI.IDSchema.ID]: d for d in prices}
        if recipe:
            for i in items:
                for r in i.get(self._DOFAPI.Schema.RECIPE, []):
                    """ set price to the recipe items """
                    r[self._PRICES.Schema.PRICE] = d_prices_recipe.get(r[self._DOFAPI.IDSchema.ANKAMA_ID], {}).get(
                        self._PRICES.Schema.PRICE, None)
                """ set price to the item itself """
                i[self._PRICES.Schema.PRICE] = d_prices.get(i[id], {}).get(self._PRICES.Schema.PRICE, None)
        else:
            for i in items:
                """ set price to the item itself """
                i[self._PRICES.Schema.PRICE] = d_prices.get(i[id], {}).get(self._PRICES.Schema.PRICE, None)
        logger.info('Set price for {count} items'.format(count=len(items)))
        return items

    def _filter_items_price(self, items, **kwargs):
        items = list(filter(lambda i: i.get(self._PRICES.Schema.PRICE), items))
        logger.info('Filtered {count} non empty price items'.format(count=len(items)))
        return items

    def _set_items_profit(self, items, **kwargs):
        for i in items:
            if i.get(self._PRICES.Schema.PRICE) and all(
                    [r.get(self._PRICES.Schema.PRICE) for r in i.get(self._DOFAPI.Schema.RECIPE)]):
                i['profit'] = i.get(self._PRICES.Schema.PRICE) - reduce(lambda a, b: a + b, [
                    r.get(self._PRICES.Schema.PRICE) * r.get(self._DOFAPI.Schema.QUANTITY) for r in
                    i.get(self._DOFAPI.Schema.RECIPE)])
        return items

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Lambdas.Decorators.payload(id='items')
    @Decorators.output
    @Decorators.price()
    def scan_items_price(self, *args, **kwargs):
        items = kwargs.get('path').get('items')
        result = self._DOFAPI.scan(endpoints=items, *args, **kwargs)
        prices = self._PRICES.scan(**kwargs).get('Items')
        return result, prices, self._DOFAPI.Schema.ID

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Decorators.output
    @Decorators.price(remove=True)
    def scan_familiers_price(self, *args, **kwargs):
        familiers = self._FAMILIERS.scan(**kwargs).get('Items')
        prices = self._PRICES.scan(**kwargs).get('Items')
        return familiers, prices, self._FAMILIERS.Schema.NAME

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Lambdas.Decorators.payload(id='profession')
    @Decorators.output
    @Decorators.price(recipe=True, profit=True)
    def scan_profession_price(self, *args, **kwargs):
        profession = kwargs.get('path').get('profession')
        result = [r for r in self._DOFAPI.scan(endpoints=self._PROFESSIONS.get(profession).ENDPOINTS, *args, **kwargs)
                  if r.get(self._DOFAPI.Schema.RECIPE) and r.get(self._DOFAPI.Schema.TYPE) in self._PROFESSIONS.get(
                profession).CRAFT]
        prices = self._PRICES.scan(**kwargs).get('Items')
        logger.info(
            'Filtered {count} craft for {profession} profession'.format(count=len(result), profession=profession))
        return result, prices, self._DOFAPI.Schema.NAME


scan_items_price = LambdasDofus().scan_items_price
scan_familiers_price = LambdasDofus().scan_familiers_price
scan_profession_price = LambdasDofus().scan_profession_price
