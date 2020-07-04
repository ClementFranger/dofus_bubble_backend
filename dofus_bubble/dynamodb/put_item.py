import json
import logging

from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import failure, load_body, check_body_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@load_body
@check_body_id('_id')
def put_item(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    return DynamoDB(**kwargs).put(Item=kwargs.get('body'))


event_mock=dict(body=json.dumps(dict(id='test_local', name='test_name')))
print(put_item(event_mock, None, DYNAMODB_TABLE='dofus-bubble'))