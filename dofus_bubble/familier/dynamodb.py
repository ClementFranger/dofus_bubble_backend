import logging
import os

from dynamodb.dynamodb import DynamoDB
from utils import Schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Familiers(DynamoDB):
    _TABLE_NAME = os.environ.get('FAMILIER_TABLE')

    class Schema(Schema):
        NAME = 'name'
        XP = 'xp'
