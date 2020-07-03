import json
import logging
import os

import boto3

from utils import success, failure, DecimalEncoder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DynamoDB(object):
    __CLIENT__ = boto3.resource('dynamodb')

    def __init__(self, **kwargs):
        self.__TABLE__ = self.__CLIENT__.Table(kwargs.get('DYNAMODB_TABLE', os.environ['DYNAMODB_TABLE']))

    def scan(self, **kwargs):
        logger.info('Getting all items')

        try:
            result = self.__TABLE__.scan(**kwargs)
            if not result.get('Items'):
                return success(status_code=204, body=json.dumps(result.get('Items'), cls=DecimalEncoder))
        except Exception as e:
            return failure(body=e)

        logger.info('Retrieved all items')
        return success(body=json.dumps(result.get('Items'), cls=DecimalEncoder))

    def create(self):
        return

    def get(self):
        return

