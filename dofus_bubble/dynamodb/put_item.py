import json
import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import failure, load_body

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@load_body
def put_item(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))

    # try:
    #     body = json.loads(event.get('body'))
    # except TypeError as e:
    #     return failure(body='Error when parsing body : {e}'.format(e=e))
    if not kwargs.get('body').get('_id'):
        return failure(code=400, body='You should provide a _id key to your body')

    return DynamoDB().put(Item=event.get('body'))
