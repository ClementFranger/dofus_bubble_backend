import json
import logging
import boto3

from dofapi.dofapi import Dofapi
from utils import request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dofus(object):
    __CLIENT__ = boto3.client('lambda')
    __SERVICE__ = 'dofus-bubble'
    __STAGE__ = 'dev'

    def __init__(self, **kwargs):
        self.__SERVICE__ = kwargs.get('__SERVICE__', self.__SERVICE__)
        self.__STAGE__ = kwargs.get('__STAGE__', self.__STAGE__)

    @request
    def _invoke(self, **kwargs):
        return json.loads(self.__CLIENT__.invoke(
            FunctionName='{service}-{stage}-{function}'.format(service=self.__SERVICE__,
                                                               stage=self.__STAGE__,
                                                               function=kwargs.get('function'))).get('Payload').read())

    # def scan_weapons_by_price(self, **kwargs):
    #     weapons = self._invoke(function='scan_weapons')
    #     # items = self.__CLIENT__.invoke(FunctionName='{service}-{stage}-scan_items'.format(service=self.__SERVICE__,
    #     #                                                                                   stage=self.__STAGE__)).get('Payload').read()
    #     print(weapons)
    #     print(type(weapons))
    #     print(weapons.keys())
    #     # print(items)
    #
    #     return weapons

    @request
    def scan_weapons_by_price(self, **kwargs):
        weapons = Dofapi().scan_weapons()
        # items =
        return weapons