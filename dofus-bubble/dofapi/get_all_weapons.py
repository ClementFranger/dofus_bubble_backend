import logging

from dofapi.dofapi import Dofapi

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_all_weapons(event, context):
    logger.info('event : {event}'.format(event=event))

    logger.info('Getting all weapons')

    result = Dofapi().get_all_weapons()

    logger.info('Retrieved all weapons')
    return result
