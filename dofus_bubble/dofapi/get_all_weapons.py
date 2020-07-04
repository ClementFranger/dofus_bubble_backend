import logging

from dofus_bubble.dofapi.dofapi import Dofapi

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_weapons(event, context, **kwargs):
    logger.info('event : {event}'.format(event=event))
    return Dofapi().get_all_weapons()

print(get_all_weapons(None, None))