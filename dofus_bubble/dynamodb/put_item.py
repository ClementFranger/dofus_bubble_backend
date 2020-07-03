import json
import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import failure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def put_item(event, context):
    logger.info('event : {event}'.format(event=event))

    body, id = event.get('body'), event.get('body').get('id')
    # body = json.loads(body) if isinstance(body, str) else body
    if not body and not id:
        return failure(code=400, body='You should provide a _id key to your body')

    return DynamoDB().put(Item=body)
