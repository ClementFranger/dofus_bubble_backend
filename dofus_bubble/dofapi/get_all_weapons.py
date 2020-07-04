from dofus_bubble.dofapi.dofapi import Dofapi
from utils import success


def get_all_weapons(event, context, **kwargs):
    return success(body=Dofapi().get_all_weapons())
