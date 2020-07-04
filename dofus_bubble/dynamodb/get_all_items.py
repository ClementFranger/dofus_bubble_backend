import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import success

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_items(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    return success(body=DynamoDB(**kwargs).scan().get('Items'))
