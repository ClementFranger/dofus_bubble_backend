from lambdas.lambdas import Lambdas
from dynamodb.dynamodb import DynamoDB


class LambdasDynamoDB(Lambdas):

    @Lambdas.Decorators.output
    def scan_items(*args, **kwargs):
        return DynamoDB(**kwargs).scan()

    @staticmethod
    @Lambdas.Decorators.output
    @Lambdas.Decorators.payload(id='_id')
    def get_item(*args, **kwargs):
        return DynamoDB(**kwargs).get(Key=kwargs.get('path'))

    @staticmethod
    @Lambdas.Decorators.cors(ips=[r"^https://master\..+\.amplifyapp\.com$", r"^http://localhost:3000$"])
    @Lambdas.Decorators.output
    @Lambdas.Decorators.payload(id='_id')
    def put_item(*args, **kwargs):
        return DynamoDB(**kwargs).put(Item=kwargs.get('body'))


scan_items = LambdasDynamoDB().scan_items
get_item = LambdasDynamoDB().get_item
put_item = LambdasDynamoDB().put_item
