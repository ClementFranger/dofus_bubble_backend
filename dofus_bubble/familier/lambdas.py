import json
from decimal import Decimal
from functools import wraps

from dofus_bubble.price.lambdas import LambdasPrice
from dynamodb.lambdas import LambdasDynamoDB
from lambdas.lambdas import Lambdas


class LambdasFamilier(LambdasDynamoDB):
    __PRICE__ = LambdasPrice()
    __DYNAMODB_TABLE__ = 'dofus-bubble-familier'

    class Decorators(object):
        @classmethod
        def output(cls, f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                result = f(*args, **kwargs)
                return {'statusCode': 200, 'headers': kwargs.get('headers'), 'body': json.dumps(result)}
            return wrapper

    @Decorators.output
    def batch_put(self, event, *args, **kwargs):
        event['body'] = list({v['name']: v for v in [{**f, **{'xp': Decimal(str(f.get('xp')))}} for f in json.loads(event.get('body'))]}.values())
        return super().batch_put(event, *args, **kwargs)

    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    # @Decorators.output
    # @Decorators.price
    def scan_familiers_price(self, *args, **kwargs):
        familiers = json.loads(self.scan(*args, **kwargs).get('body')).get('Items')
        prices = json.loads(self.__PRICE__.scan(*args, **kwargs).get('body')).get('Items')
        print(familiers, prices)
        return familiers, prices


batch_put = LambdasFamilier().batch_put
scan_familiers_price = LambdasFamilier().scan_familiers_price
