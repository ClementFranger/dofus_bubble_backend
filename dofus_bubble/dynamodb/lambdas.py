from lambdas.lambdas import Lambdas
from dynamodb.dynamodb import DynamoDB
from utils import success, load_payload, check_payload


class LambdasDynamoDB(Lambdas):

    def scan_items(self, *args, **kwargs):
        return success(body=DynamoDB(**kwargs).scan())

    @load_payload
    @check_payload(id='_id')
    def get_item(self, event, context, **kwargs):
        return success(body=DynamoDB(**kwargs).get(Key=kwargs.get('path')))

    @load_payload
    @check_payload(id='_id')
    def put_item(self, *args, **kwargs):
        return success(status_code=204, body=DynamoDB(**kwargs).put(Item=kwargs.get('body')))


scan_items = LambdasDynamoDB().scan_items
get_item = LambdasDynamoDB().get_item
put_item = LambdasDynamoDB().put_item
