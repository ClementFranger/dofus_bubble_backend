import json
import logging
import os
import boto3

from utils import success, failure, DecimalEncoder, request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DynamoDB(object):
    __CLIENT__ = boto3.resource('dynamodb')

    def __init__(self, **kwargs):
        if not kwargs.get('DYNAMODB_TABLE'):
            kwargs.update({'DYNAMODB_TABLE': os.environ['DYNAMODB_TABLE']})
        self.__TABLE__ = self.__CLIENT__.Table(kwargs.get('DYNAMODB_TABLE'))

    @request
    def scan(self, **kwargs):
        logger.info('Getting all items')

        result = self.__TABLE__.scan(**kwargs)

        logger.info('Retrieved all items')
        return result

    @request
    def put(self, **kwargs):
        logger.info('Creating item {item}'.format(item=kwargs.get('item')))

        result = self.__TABLE__.put_item(**kwargs)

        logger.info('Created item {item}'.format(item=kwargs.get('item')))
        return result

    @request
    def get(self, **kwargs):
        logger.info('Getting item {key}'.format(key=kwargs.get('key')))

        result = self.__TABLE__.get_item(**kwargs)

        logger.info('Retrieved item {key}'.format(key=kwargs.get('key')))
        return result
