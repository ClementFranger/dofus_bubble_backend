import logging

from dynamodb.dynamodb import DynamoDB
from utils import Schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PriceDynamoDB(DynamoDB):
    _TABLE_NAME = 'dofus-bubble'

    class Schema(Schema):
        ID = '_id'
        NAME = 'name'
        PRICE = 'price'
