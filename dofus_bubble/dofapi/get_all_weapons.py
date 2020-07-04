import logging

from dofus_bubble.dofapi.dofapi import Dofapi
from utils import success

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_weapons(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    return success(body=Dofapi().get_all_weapons())
