import logging
import os

from dynamodb.dynamodb import DynamoDB
from utils import Schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Prices(DynamoDB):
    _TABLE_NAME = os.environ.get('PRICES_TABLE')

    class Schema(Schema):
        ID = '_id'
        NAME = 'name'
        PRICE = 'price'
