from dofus_bubble.dynamodb.dynamodb import DynamoDB
from utils import success


def get_all_items(event, context, **kwargs):
    return success(body=DynamoDB(**kwargs).scan().get('Items'))
