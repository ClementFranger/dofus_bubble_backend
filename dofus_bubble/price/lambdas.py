from dynamodb.lambdas import LambdasDynamoDB


class LambdasPrice(LambdasDynamoDB):
    __DYNAMODB_TABLE__ = 'dofus-bubble'


scan = LambdasPrice().scan
get = LambdasPrice().get
put = LambdasPrice().put
