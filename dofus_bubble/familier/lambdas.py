import json
from decimal import Decimal
from functools import wraps

from dynamodb.lambdas import LambdasDynamoDB


class LambdasFamilier(LambdasDynamoDB):
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


batch_put = LambdasFamilier().batch_put
