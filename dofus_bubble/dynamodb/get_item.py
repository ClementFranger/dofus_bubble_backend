import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import success, load_payload, check_payload

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@load_payload
@check_payload(id='_id')
def get_item(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    return success(body=DynamoDB(**kwargs).get(Key=kwargs.get('path')).get('Item'))
