from dofapi.dofapi import Dofapi
from utils import success


def scan_weapons(event, context, **kwargs):
    return success(body=Dofapi().scan_weapons())
