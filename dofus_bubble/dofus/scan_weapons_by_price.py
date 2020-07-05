import boto3

from dofus_bubble.dofus.dofus import Dofus
from utils import success


def scan_weapons_by_price(event, context, **kwargs):
    return success(body=Dofus(**kwargs).scan_weapons_by_price())