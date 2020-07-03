import requests

from utils import handle_request, output_request


class Dofapi(object):
    __DOFAPI_API_ = 'https://fr.dofus.dofapi.fr/'
    __WEAPONS__ = 'weapons'

    @handle_request
    @output_request
    def get_all_weapons(self, *args, **kwargs):
        return requests.get(self.__DOFAPI_API_ + self.__WEAPONS__, *args, **kwargs)
