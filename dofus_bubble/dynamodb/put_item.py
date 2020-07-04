import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import load_payload, check_payload, success

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@load_payload
@check_payload(id='_id')
def put_item(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    return success(body=DynamoDB(**kwargs).put(Item=kwargs.get('body')))
