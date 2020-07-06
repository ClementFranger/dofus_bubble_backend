from dynamodb.dynamodb import DynamoDB
from utils import load_payload, check_payload, success


# @load_payload
# @check_payload(id='_id')
# def put_item(event, context, **kwargs):
#     return success(status_code=204, body=DynamoDB(**kwargs).put(Item=kwargs.get('body')))
