import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_items(event, context):
    logger.info('event : {event}'.format(event=event))

    return DynamoDB().scan()
